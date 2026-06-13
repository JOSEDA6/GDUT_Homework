import os
import xml.etree.ElementTree as ET
import shutil


def convert_voc_to_yolo(voc_root, output_dir):
    """
    将VOC格式数据集转换为YOLOv5格式（包含单独的xml目录）
    Args:
        voc_root (str): VOC数据集根目录路径 (包含Annotations/JPEGImages等文件夹)
        output_dir (str): 输出目录路径
    """
    # 使用原始字符串处理Windows路径（在路径前添加r）
    voc_root = os.path.normpath(voc_root)  # 规范化路径
    output_dir = os.path.normpath(output_dir)  # 规范化路径

    # 创建所需的输出目录
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'xml'), exist_ok=True)

    # VOC数据集路径 - 添加路径存在性检查
    anno_dir = os.path.join(voc_root, 'Annotations')
    img_dir = os.path.join(voc_root, 'JPEGImages')

    # 检查路径是否存在
    if not os.path.exists(anno_dir):
        print(f"错误: Annotations目录不存在 - {anno_dir}")
        print("请确保VOC数据集包含Annotations目录")
        return

    if not os.path.exists(img_dir):
        print(f"错误: JPEGImages目录不存在 - {img_dir}")
        print("请确保VOC数据集包含JPEGImages目录")
        return

    # 获取所有XML文件（完整路径）
    xml_files = []
    for f in os.listdir(anno_dir):
        if f.endswith('.xml'):
            # 获取文件名（不含扩展名）
            file_id = os.path.splitext(f)[0]
            xml_files.append(file_id)

    if not xml_files:
        print(f"错误: 在{anno_dir}中未找到任何XML文件")
        return

    # 定义VOC类别（按字母顺序）
    voc_classes = [
        'aeroplane', 'bicycle', 'bird', 'boat', 'bottle',
        'bus', 'car', 'cat', 'chair', 'cow',
        'diningtable', 'dog', 'horse', 'motorbike', 'person',
        'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'
    ]

    # 创建classes.txt
    with open(os.path.join(output_dir, 'classes.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(voc_classes))

    print(f"开始转换: 发现 {len(xml_files)} 个XML文件")

    # 处理每个文件
    for i, file_id in enumerate(xml_files):
        src_xml = os.path.join(anno_dir, f'{file_id}.xml')
        dst_xml = os.path.join(output_dir, 'xml', f'{file_id}.xml')

        # 复制XML文件到xml目录
        shutil.copy2(src_xml, dst_xml)

        # 解析XML
        try:
            tree = ET.parse(src_xml)
            root = tree.getroot()
        except Exception as e:
            print(f"警告: 无法解析 {src_xml} - {e}")
            continue

        # 获取图片尺寸
        size = root.find('size')
        if size is None:
            print(f"警告: {file_id}.xml 缺少size信息")
            continue

        w_element = size.find('width')
        h_element = size.find('height')
        if w_element is None or h_element is None:
            print(f"警告: {file_id}.xml 缺少宽高信息")
            continue

        try:
            w = int(w_element.text)
            h = int(h_element.text)
        except (ValueError, TypeError):
            print(f"警告: {file_id}.xml 有无效的宽高值")
            continue

        # 检查对象数量
        objects = root.findall('object')
        if not objects:
            print(f"警告: {file_id}.xml 不包含任何object标签")

        # 创建YOLO标注文件
        label_file = os.path.join(output_dir, 'labels', f'{file_id}.txt')
        with open(label_file, 'w', encoding='utf-8') as lf:
            for obj in objects:
                name_element = obj.find('name')
                if name_element is None or name_element.text is None:
                    print(f"警告: {file_id}.xml 中有object缺少name")
                    continue

                cls_name = name_element.text.strip()
                # 忽略未定义类别
                if cls_name not in voc_classes:
                    # 自动添加新类别（可选）
                    # if cls_name not in voc_classes:
                    #     voc_classes.append(cls_name)
                    #     print(f"添加新类别: {cls_name}")
                    continue

                # 获取类别ID
                cls_id = voc_classes.index(cls_name)

                # 获取边界框
                bbox = obj.find('bndbox')
                if bbox is None:
                    print(f"警告: {file_id}.xml 中的对象缺少bndbox")
                    continue

                # 检查所有必需的坐标元素
                coords = {}
                required_coords = ['xmin', 'ymin', 'xmax', 'ymax']
                for coord in required_coords:
                    coord_element = bbox.find(coord)
                    if coord_element is None or coord_element.text is None:
                        print(f"警告: {file_id}.xml 缺少 {coord}")
                        break
                    try:
                        coords[coord] = float(coord_element.text)
                    except ValueError:
                        print(f"警告: {file_id}.xml 有无效的 {coord} 值")
                        break
                else:  # 仅当所有坐标都存在且有效时执行
                    # 转换坐标为整数
                    xmin = int(coords['xmin'])
                    ymin = int(coords['ymin'])
                    xmax = int(coords['xmax'])
                    ymax = int(coords['ymax'])

                    # 转换为YOLO格式 (归一化的中心点坐标和宽高)
                    x_center = max(0, min(1, ((xmin + xmax) / 2) / w))
                    y_center = max(0, min(1, ((ymin + ymax) / 2) / h))
                    bbox_w = max(0, min(1, (xmax - xmin) / w))
                    bbox_h = max(0, min(1, (ymax - ymin) / h))

                    # 写入标签文件
                    lf.write(f'{cls_id} {x_center:.6f} {y_center:.6f} {bbox_w:.6f} {bbox_h:.6f}\n')

        # 复制图像文件（尝试多种扩展名）
        img_extensions = ['.jpg', '.jpeg', '.png']
        img_found = False
        for ext in img_extensions:
            src_img = os.path.join(img_dir, f'{file_id}{ext}')
            if os.path.exists(src_img):
                dst_img = os.path.join(output_dir, 'images', f'{file_id}{ext}')
                shutil.copy2(src_img, dst_img)
                img_found = True
                break

        if not img_found:
            print(f"警告: 未找到 {file_id} 的图片文件")

        # 显示进度
        if (i + 1) % 100 == 0 or (i + 1) == len(xml_files):
            print(f"已处理: {i + 1}/{len(xml_files)}")

    print(f'\n转换完成! 输出目录: {output_dir}')
    print(f'数据集结构:')
    print(f'yolov5_dataset/')
    print(f'├── images/       # 训练图片')
    print(f'├── labels/       # YOLO格式标签文件')
    print(f'├── xml/          # XML文件')
    print(f'└── classes.txt   # 类别名称文件')
    print(f'\n总XML文件数量: {len(xml_files)}')
    print(f'总类别数量: {len(voc_classes)}')


if __name__ == '__main__':
    # 配置路径（使用原始字符串路径）
    # 在路径前添加 r 或在路径字符串前添加引号
    voc_root = r'G:\大三\大三_下\2025暑期人工智能实训\第二周\VOC2012'
    output_dir = r'G:\大三\大三_下\2025暑期人工智能实训\第二周\yolov5_dataset'

    convert_voc_to_yolo(voc_root, output_dir)