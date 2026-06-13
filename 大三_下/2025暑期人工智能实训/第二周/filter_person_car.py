import os
import random
import glob


def reduce_dataset_size(dataset_dir, reduction_ratio=0.5):
    """
    随机删除数据集中指定比例的文件（图片、标签、XML）

    Args:
        dataset_dir (str): 数据集根目录（包含images, labels, xml目录）
        reduction_ratio (float): 要删除的比例（0-1之间）
    """
    # 检查必需的目录结构
    required_dirs = ['images', 'labels', 'xml']
    for dir_name in required_dirs:
        dir_path = os.path.join(dataset_dir, dir_name)
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            print(f"错误: 缺少必需的目录 '{dir_name}'")
            return

    # 获取所有图片文件（支持多种格式）
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(dataset_dir, 'images', f'*{ext}')))

    if not image_files:
        print(f"错误: 在 {os.path.join(dataset_dir, 'images')} 中未找到任何图片文件")
        return

    # 获取所有文件的基名（不带扩展名）
    base_names = set()
    for img_path in image_files:
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        base_names.add(base_name)

    total_files = len(base_names)
    num_to_delete = int(total_files * reduction_ratio)

    if num_to_delete <= 0:
        print(f"警告: 删除数量为0 (总文件数={total_files}, 删除比例={reduction_ratio})")
        return

    print(f"数据集原始大小: {total_files} 个样本")
    print(f"计划删除 {num_to_delete} 个样本 ({reduction_ratio * 100:.1f}%)")

    # 随机选择要删除的文件
    base_names_list = list(base_names)
    random.shuffle(base_names_list)
    delete_set = set(base_names_list[:num_to_delete])

    # 创建备份目录
    backup_dir = os.path.join(dataset_dir, "backup")
    backup_dirs = {
        'images': os.path.join(backup_dir, 'images'),
        'labels': os.path.join(backup_dir, 'labels'),
        'xml': os.path.join(backup_dir, 'xml')
    }
    for dir_path in backup_dirs.values():
        os.makedirs(dir_path, exist_ok=True)

    # 删除文件（实际是移动到备份目录）
    deleted_count = 0
    for base_name in delete_set:
        # 处理图片文件
        img_found = False
        for ext in image_extensions:
            img_path = os.path.join(dataset_dir, 'images', f'{base_name}{ext}')
            if os.path.exists(img_path):
                # 移动图片到备份
                dst_img = os.path.join(backup_dirs['images'], f'{base_name}{ext}')
                os.rename(img_path, dst_img)
                img_found = True
                break

        if not img_found:
            print(f"警告: 未找到 {base_name} 的图片文件")
            continue

        # 处理标签文件
        label_path = os.path.join(dataset_dir, 'labels', f'{base_name}.txt')
        if os.path.exists(label_path):
            dst_label = os.path.join(backup_dirs['labels'], f'{base_name}.txt')
            os.rename(label_path, dst_label)
        else:
            print(f"警告: 未找到 {base_name} 的标签文件")

        # 处理XML文件
        xml_path = os.path.join(dataset_dir, 'xml', f'{base_name}.xml')
        if os.path.exists(xml_path):
            dst_xml = os.path.join(backup_dirs['xml'], f'{base_name}.xml')
            os.rename(xml_path, dst_xml)
        else:
            print(f"警告: 未找到 {base_name} 的XML文件")

        deleted_count += 1

    # 检查剩余文件数量
    remaining_images = len(glob.glob(os.path.join(dataset_dir, 'images', '*')))
    remaining_labels = len(glob.glob(os.path.join(dataset_dir, 'labels', '*.txt')))
    remaining_xml = len(glob.glob(os.path.join(dataset_dir, 'xml', '*.xml')))

    print("\n操作完成!")
    print(f"成功删除: {deleted_count} 个样本")
    print(f"剩余样本: {total_files - deleted_count}")
    print(f"备份文件保存在: {backup_dir}")
    print(f"剩余文件统计: images={remaining_images}, labels={remaining_labels}, xml={remaining_xml}")

    # 提示用户确认后删除备份
    print("\n请检查备份目录内容，确认无误后可以手动删除整个备份目录以释放空间")
    print(f"删除命令: rmdir /s /q \"{backup_dir}\"")


if __name__ == '__main__':
    # 配置参数
    dataset_path = r"G:\大三\大三_下\2025暑期人工智能实训\第二周\yolov5_dataset"
    delete_ratio = 0.5  # 删除一半文件

    # 执行删除操作
    reduce_dataset_size(dataset_path, delete_ratio)