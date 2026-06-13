# 设置环境变量，限制线程数为1，python的并行并不是真正的并行，因为GIL锁
import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
import copy
import sys

sys.path.insert(0, './yolov5')

import argparse
import os
import platform
import shutil
import time
from pathlib import Path
import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn

from yolov5.models.experimental import attempt_load
from yolov5.utils.downloads import attempt_download
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.datasets import LoadImages, LoadStreams, VID_FORMATS
from yolov5.utils.general import (LOGGER, check_img_size, non_max_suppression, scale_coords,
                                  check_imshow, xyxy2xywh, increment_path, strip_optimizer, colorstr)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors, save_one_box
from tracker.utils.parser import get_config
from tracker.deep_sort import DeepSort

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # yolov5 deepsort root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
count = 0
count2 = 0
data = []


def detect(opt, grstatus=False):  # gradio可视化时需要加一个参数
    out, source, yolo_model, deep_sort_model, show_vid, save_vid, save_txt, imgsz, evaluate, half, \
        project, exist_ok, update, save_crop = \
        opt.output, opt.source, opt.yolo_model, opt.deep_sort_model, opt.show_vid, opt.save_vid, \
            opt.save_txt, opt.imgsz, opt.evaluate, opt.half, opt.project, opt.exist_ok, opt.update, opt.save_crop
    webcam = source == '0' or source.startswith(
        'rtsp') or source.startswith('http') or source.endswith('.txt')

    # Initialize
    device = select_device(opt.device)  # 设备选择 cpu还是gpu
    half &= device.type != 'cpu'  # 半精度

    # The MOT16 evaluation runs multiple inference streams in parallel, each one writing to
    # its own .txt file. Hence, in that case, the output folder is not restored
    if not evaluate:  # 是否需要评估，在测试整个pipeline时可以使用
        if os.path.exists(out):  # 判断是否存在输出文件夹，有就删掉
            pass
            shutil.rmtree(out)  # 删掉输出文件夹
        os.makedirs(out)  # # 新建输出文件夹

    # Directories
    if type(yolo_model) is str:  # 单个yolo模型
        exp_name = yolo_model.split(".")[0]  # 导出目录yolo名称，下同
    elif type(yolo_model) is list and len(yolo_model) == 1:  # 单个yolo模型，以list方式送入
        exp_name = yolo_model[0].split(".")[0]
    else:  # 多个yolo模型，在写论文时可以快速出对比结果
        exp_name = "ensemble"
    exp_name = exp_name + "_" + deep_sort_model.split('/')[-1].split('.')[0]  # 导出目录yolo+deepsort名称，
    save_dir = increment_path(Path(project) / exp_name, exist_ok=exist_ok)  # 组装路径
    (save_dir / 'tracks' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # 根据组装的路径创建文件夹

    # 加载yolo模型
    model = DetectMultiBackend(yolo_model, device=device, dnn=opt.dnn)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # 检查图片的输入尺寸

    # 半精度
    half &= pt and device.type != 'cpu'  # 半精度只支持cuda，也就是GPU运行时
    if pt:
        model.model.half() if half else model.model.float()

    # 配置数据加载器
    vid_path, vid_writer = None, None
    # 检查环境是否支持结果实时显示，也就是Matplotlib和opencv
    if show_vid:
        show_vid = check_imshow()

    # 数据加载器
    if webcam:  # 如果输入是摄像头，也就是source 为0
        show_vid = check_imshow()
        cudnn.benchmark = True  # 使用cudnn去批量加速图片推理
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)  # 因为是摄像头，所以走加载视频流的方式
        nr_sources = len(dataset)  # 获取数据集的长度
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)  # 如果不是摄像头，就走加载图片
        nr_sources = 1
    vid_path, vid_writer, txt_path = [None] * nr_sources, [None] * nr_sources, [None] * nr_sources  # 结果列表的创建初始化

    # 根据配置文件初始化deepsort
    cfg = get_config()
    cfg.merge_from_file(opt.config_deepsort)

    # 根据输入的数量来创建deepsort的数量，达到并行处理的目的
    deepsort_list = []
    for i in range(nr_sources):
        deepsort_list.append(
            DeepSort(
                deep_sort_model,
                device,
                max_dist=cfg.DEEPSORT.MAX_DIST,
                max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
            )  # deepsort模型加载
        )
    outputs = [None] * nr_sources  # 输出的数量要和输入相对应

    # 获取类别的名称，并分配相应的颜色
    names = model.module.names if hasattr(model, 'module') else model.names

    # 运行追踪器，model表示Yolo模型，deepsort_list里装的是deepsort模型
    model.warmup(imgsz=(1 if pt else nr_sources, 3, *imgsz))  # 预热阶段，模型加载起来都要先预热，相当于快速推理，将模型加载到内存里，以便后续使用
    dt, seen = [0.0, 0.0, 0.0, 0.0], 0
    for frame_idx, (path, im, im0s, vid_cap, s) in enumerate(dataset):  # 开始循环遍历数据集中的数据
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)  # 将数据加载到GPU或者CPU上
        im = im.half() if half else im.float()  # uint8 to fp16/32  半精度的数据类型转换
        im /= 255.0  # 0 - 255 to 0.0 - 1.0  #归一化，加快计算
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # 预测
        visualize = increment_path(save_dir / Path(path[0]).stem, mkdir=True) if opt.visualize else False
        pred = model(im, augment=opt.augment, visualize=visualize)  # yolo预测，获取类别，置信度，边框
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS非极大值抑制
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, opt.classes, opt.agnostic_nms,
                                   max_det=opt.max_det)
        dt[2] += time_sync() - t3

        # 检测结果后处理
        for i, det in enumerate(pred):  # 循环遍历检测结果
            seen += 1
            if webcam:  # 摄像头，if else过程是用来获取保存路径名称
                p, im0, _ = path[i], im0s[i].copy(), dataset.count
                p = Path(p)  # to Path
                s += f'{i}: '
                txt_file_name = p.name
                save_path = str(save_dir / p.name)  # im.jpg, vid.mp4, ...
            else:
                p, im0, _ = path, im0s.copy(), getattr(dataset, 'frame', 0)
                p = Path(p)  # to Path
                # video file
                if source.endswith(VID_FORMATS):
                    txt_file_name = p.stem
                    save_path = str(save_dir / p.name)  # im.jpg, vid.mp4, ...
                # folder with imgs
                else:
                    txt_file_name = p.parent.name  # get folder name containing current img
                    save_path = str(save_dir / p.parent.name)  # im.jpg, vid.mp4, ...

            txt_path = str(save_dir / 'tracks' / txt_file_name)  # 数据结果txt文件名称及位置。
            s += '%gx%g ' % im.shape[2:]
            imc = im0.copy() if save_crop else im0  # save_crop，保存目标裁切结果
            imo = copy.deepcopy(im0)
            annotator = Annotator(im0, line_width=2, pil=not ascii)  # 标签处理

            w, h = im0.shape[1], im0.shape[0]

            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                xywhs = xyxy2xywh(det[:, 0:4])
                confs = det[:, 4]
                clss = det[:, 5]

                # 将检测结果送到deepsort里面
                t4 = time_sync()
                outputs[i] = deepsort_list[i].update(xywhs.cpu(), confs.cpu(), clss.cpu(), im0)
                t5 = time_sync()
                dt[3] += t5 - t4

                # 保存结果
                if len(outputs[i]) > 0:
                    for j, (output, conf) in enumerate(zip(outputs[i], confs)):

                        bboxes = output[0:4]
                        id = output[4]
                        cls = output[5]
                        count_obj(bboxes, w, h, id)

                        if save_txt:
                            # to MOT format
                            bbox_left = output[0]
                            bbox_top = output[1]
                            bbox_w = output[2] - output[0]
                            bbox_h = output[3] - output[1]
                            # Write MOT compliant results to file
                            with open(txt_path + '.txt', 'a') as f:
                                f.write(('%g ' * 10 + '\n') % (frame_idx + 1, id, bbox_left,  # MOT format
                                                               bbox_top, bbox_w, bbox_h, -1, -1, -1, i))

                        if save_vid or save_crop or show_vid:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = f'{id} {names[c]} {conf:.2f}'
                            annotator.box_label(bboxes, label, color=colors(c, True))
                            if save_crop:
                                txt_file_name = txt_file_name if (isinstance(path, list) and len(path) > 1) else ''
                                save_one_box(bboxes, imc, file=save_dir / 'crops' / txt_file_name / names[
                                    c] / f'{id}' / f'{p.stem}.jpg', BGR=True)

                LOGGER.info(f'{s}Done. YOLO:({t3 - t2:.3f}s), DeepSort:({t5 - t4:.3f}s)')

            else:
                deepsort_list[i].increment_ages()
                LOGGER.info('No detections')

            # 可视化
            im0 = annotator.result()
            if show_vid:
                color = (0, 255, 0)
                start_point = (0, h - 350)  # 横线起始点
                end_point = (int(w / 2) - 50, h - 350)  # 横线终结点
                cv2.line(im0, start_point, end_point, color, thickness=2)  # 画线
                org = (150, 150)
                font = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 3
                thickness = 3
                cv2.putText(im0, str(count), org, font, fontScale, color, thickness, cv2.LINE_AA)  # 在图片上加字

                color = (255, 0, 0)
                start_point = (int(w / 2) + 50, h - 350)
                end_point = (w, h - 350)
                cv2.line(im0, start_point, end_point, color, thickness=2)
                org = (w - 150, 150)
                font = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 3
                thickness = 3
                print('========')
                cv2.putText(im0, str(count2), org, font, fontScale, color, thickness, cv2.LINE_AA)
                if grstatus:  # 需要加的
                    yield cv2.cvtColor(imo, cv2.COLOR_BGR2RGB), cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # 保存结果，每张图像带着检测框
            if save_vid:
                color = (0, 255, 0)
                start_point = (0, h - 350)
                end_point = (int(w / 2) - 50, h - 350)
                cv2.line(im0, start_point, end_point, color, thickness=2)
                org = (150, 150)
                font = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 3
                thickness = 3
                cv2.putText(im0, str(count), org, font, fontScale, color, thickness, cv2.LINE_AA)

                color = (255, 0, 0)
                start_point = (int(w / 2) + 50, h - 350)
                end_point = (w, h - 350)
                cv2.line(im0, start_point, end_point, color, thickness=2)
                org = (w - 150, 150)
                font = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 3
                thickness = 3
                cv2.putText(im0, str(count2), org, font, fontScale, color, thickness, cv2.LINE_AA)
                # yield imres,im
                if vid_path[i] != save_path:  # new video
                    vid_path[i] = save_path
                    if isinstance(vid_writer[i], cv2.VideoWriter):
                        vid_writer[i].release()  # release previous video writer
                    if vid_cap:  # video
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    else:  # stream
                        fps, w, h = 30, im0.shape[1], im0.shape[0]
                    save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                    vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                vid_writer[i].write(im0)

    # Print results
    t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS, %.1fms deep sort update \
        per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_vid:
        s = f"\n{len(list(save_dir.glob('tracks/*.txt')))} tracks saved to {save_dir / 'tracks'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(yolo_model)  # update model (to fix SourceChangeWarning)


def count_obj(box, w, h, id):
    global count, count2, data
    center_coor = (int(box[0] + (box[2] - box[0]) / 2), int(box[1] + (box[3] - box[1]) / 2))
    if int(box[1] + (box[3] - box[1]) / 2) > h - 350 and id not in data:
        if int(box[0] + (box[2] - box[0]) / 2) > int(w / 2):
            count2 += 1
        else:
            count += 1
        data.append(id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--yolo_model', nargs='+', type=str, default='yolov5m.pt', help='model.pt path(s)')
    parser.add_argument('--deep_sort_model', type=str, default='osnet_ibn_x1_0_MSMT17')
    parser.add_argument('--source', type=str, default='example.mp4', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.5, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--show-vid', action='store_true', help='display tracking video results', default=True)
    parser.add_argument('--save-vid', action='store_true', help='save video tracking results')
    parser.add_argument('--save-txt', action='store_true', help='save MOT compliant results to *.txt')
    # class 0 is person, 1 is bycicle, 2 is car... 79 is oven
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 16 17')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--evaluate', action='store_true', help='augmented inference')
    parser.add_argument("--config_deepsort", type=str, default="tracker/configs/deep_sort.yaml")
    parser.add_argument("--half", action="store_true", help="use FP16 half-precision inference")
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detection per image')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--project', default=ROOT / 'runs/track', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand

    origin = False
    if origin:
        with torch.no_grad():
            detect(opt)

    else:
        import gradio as gr
        def mydetect(videoname):
            opt.source = videoname
            # vn = cv2.VideoCapture(videoname)
            # fps = int(vn.get(cv2.CAP_PROP_FPS))
            # print(fps)
            with torch.no_grad():
                for x in detect(opt, grstatus=True):
                    yield x[0],x[1]

        demo = gr.Interface(
            fn=mydetect,
            inputs=gr.Video(sources="upload"),
            outputs=[gr.Image(), gr.Image()]
        )
        demo.queue().launch()