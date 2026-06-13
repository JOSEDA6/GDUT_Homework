import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from datetime import datetime


class DatasetCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv5 数据集检查工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(self.main_frame, text="YOLOv5 数据集完整性检查工具",
                  font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

        # 数据集路径选择
        ttk.Label(self.main_frame, text="数据集路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.path_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.path_var, width=50).grid(row=1, column=1, sticky=tk.W + tk.E)
        ttk.Button(self.main_frame, text="浏览...", command=self.browse_dataset).grid(row=1, column=2, padx=5)

        # 操作选项
        self.clean_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.main_frame, text="自动清理无效文件", variable=self.clean_var).grid(row=2, column=0,
                                                                                                columnspan=3, pady=10)

        # 执行按钮
        ttk.Button(self.main_frame, text="开始检查", command=self.run_check).grid(row=3, column=0, columnspan=3,
                                                                                  pady=15)

        # 结果文本框
        ttk.Label(self.main_frame, text="检查结果:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.result_text = tk.Text(self.main_frame, height=20, width=80)
        self.result_text.grid(row=5, column=0, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S)

        # 滚动条
        scrollbar = ttk.Scrollbar(self.main_frame, command=self.result_text.yview)
        scrollbar.grid(row=5, column=3, sticky=tk.N + tk.S)
        self.result_text.config(yscrollcommand=scrollbar.set)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

        # 配置网格权重
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(5, weight=1)

    def browse_dataset(self):
        """打开文件夹选择对话框"""
        path = filedialog.askdirectory(title="选择数据集目录")
        if path:
            self.path_var.set(path)

    def run_check(self):
        """执行数据集检查"""
        dataset_path = self.path_var.get()
        if not dataset_path:
            messagebox.showerror("错误", "请先选择数据集目录")
            return

        if not os.path.exists(dataset_path):
            messagebox.showerror("错误", f"目录不存在: {dataset_path}")
            return

        self.status_var.set("正在检查数据集...")
        self.root.update()

        # 清空结果文本框
        self.result_text.delete(1.0, tk.END)

        try:
            # 执行检查
            results = self.check_dataset(dataset_path)

            # 显示结果
            self.display_results(results)

            # 如果需要清理
            if self.clean_var.get():
                self.cleanup_dataset(results, dataset_path)
                self.status_var.set("清理完成!")
            else:
                self.status_var.set("检查完成!")

        except Exception as e:
            self.result_text.insert(tk.END, f"发生错误: {str(e)}\n")
            self.status_var.set("检查失败")

    def check_dataset(self, dataset_path):
        """执行数据集检查"""
        results = {
            'empty_files': {'txt': [], 'xml': []},
            'invalid_xml': [],
            'missing_matches': {
                'image_no_label': [],
                'label_no_image': [],
                'image_no_xml': [],
                'xml_no_image': []
            }
        }

        # 定义路径
        paths = {
            'images': os.path.join(dataset_path, "images"),
            'labels': os.path.join(dataset_path, "labels"),
            'xml': os.path.join(dataset_path, "xml"),
            'split_files': [
                os.path.join(dataset_path, "train.txt"),
                os.path.join(dataset_path, "val.txt"),
                os.path.join(dataset_path, "test.txt")
            ]
        }

        # 检查空文件
        if os.path.exists(paths['labels']):
            results['empty_files']['txt'] = self.check_empty_files(paths['labels'], '.txt')

        if os.path.exists(paths['xml']):
            results['empty_files']['xml'] = self.check_empty_files(paths['xml'], '.xml')
            results['invalid_xml'] = self.check_xml_validity(paths['xml'])

        # 检查文件对应关系
        if os.path.exists(paths['images']) and os.path.exists(paths['labels']):
            image_files = self.get_base_names(paths['images'], ['.jpg', '.jpeg', '.png'])
            label_files = self.get_base_names(paths['labels'], ['.txt'])

            results['missing_matches']['image_no_label'] = list(image_files - label_files)
            results['missing_matches']['label_no_image'] = list(label_files - image_files)

        if os.path.exists(paths['images']) and os.path.exists(paths['xml']):
            image_files = self.get_base_names(paths['images'], ['.jpg', '.jpeg', '.png'])
            xml_files = self.get_base_names(paths['xml'], ['.xml'])

            results['missing_matches']['image_no_xml'] = list(image_files - xml_files)
            results['missing_matches']['xml_no_image'] = list(xml_files - image_files)

        return results

    def check_empty_files(self, directory, extension):
        """检查指定目录中指定扩展名的空文件"""
        empty_files = []
        for filename in os.listdir(directory):
            if filename.endswith(extension):
                filepath = os.path.join(directory, filename)
                if os.path.getsize(filepath) == 0:
                    empty_files.append(filepath)
        return empty_files

    def check_xml_validity(self, xml_dir):
        """检查XML文件的格式有效性"""
        invalid_files = []
        for xml_file in os.listdir(xml_dir):
            if xml_file.endswith('.xml'):
                filepath = os.path.join(xml_dir, xml_file)
                try:
                    tree = ET.parse(filepath)
                    root = tree.getroot()

                    # 基础XML结构检查
                    if root.tag != 'annotation':
                        raise ValueError("根标签不是'annotation'")

                    # 检查必需字段
                    required_fields = ['filename', 'size', 'object']
                    for field in required_fields:
                        if root.find(field) is None:
                            raise ValueError(f"缺少必需字段: {field}")

                    # 检查是否有实际标注
                    objects = root.findall('object')
                    if len(objects) == 0:
                        raise ValueError("没有有效的object标签")

                    # 检查对象字段完整性
                    for obj in objects:
                        obj_fields = ['name', 'bndbox']
                        for field in obj_fields:
                            if obj.find(field) is None:
                                raise ValueError(f"对象缺少必需字段: {field}")

                except Exception as e:
                    invalid_files.append({
                        'file': filepath,
                        'error': str(e)
                    })
        return invalid_files

    def get_base_names(self, directory, extensions):
        """获取目录中指定扩展名文件的基本名称（不含扩展名）"""
        base_names = set()
        for filename in os.listdir(directory):
            for ext in extensions:
                if filename.lower().endswith(ext):
                    base_names.add(os.path.splitext(filename)[0])
                    break
        return base_names

    def display_results(self, results):
        """在文本框中显示检查结果"""
        self.result_text.insert(tk.END, "=" * 70 + "\n")
        self.result_text.insert(tk.END, "数据集检查结果\n")
        self.result_text.insert(tk.END, "=" * 70 + "\n\n")

        # 显示空文件结果
        txt_empty = len(results['empty_files']['txt'])
        xml_empty = len(results['empty_files']['xml'])

        if txt_empty or xml_empty:
            self.result_text.insert(tk.END, f"⚠️ 发现 {txt_empty} 个空TXT标签文件和 {xml_empty} 个空XML标签文件\n\n")
        else:
            self.result_text.insert(tk.END, "✅ 未发现空标签文件\n\n")

        # 显示无效XML结果
        if results['invalid_xml']:
            self.result_text.insert(tk.END, f"⚠️ 发现 {len(results['invalid_xml'])} 个无效的XML文件:\n")
            for item in results['invalid_xml']:
                self.result_text.insert(tk.END, f"  - {os.path.basename(item['file'])}: {item['error']}\n")
            self.result_text.insert(tk.END, "\n")
        else:
            self.result_text.insert(tk.END, "✅ 所有XML文件格式有效\n\n")

        # 显示文件对应关系结果
        mm = results['missing_matches']
        issues_found = False

        if mm['image_no_label']:
            issues_found = True
            self.result_text.insert(tk.END, f"⚠️ 发现 {len(mm['image_no_label'])} 个图片没有对应的标签文件\n")

        if mm['label_no_image']:
            issues_found = True
            self.result_text.insert(tk.END, f"⚠️ 发现 {len(mm['label_no_image'])} 个标签没有对应的图片文件\n")

        if mm['image_no_xml']:
            issues_found = True
            self.result_text.insert(tk.END, f"⚠️ 发现 {len(mm['image_no_xml'])} 个图片没有对应的XML文件\n")

        if mm['xml_no_image']:
            issues_found = True
            self.result_text.insert(tk.END, f"⚠️ 发现 {len(mm['xml_no_image'])} 个XML没有对应的图片文件\n")

        if not issues_found:
            self.result_text.insert(tk.END, "✅ 所有文件匹配完整\n\n")

        # 添加清理建议
        if any([txt_empty, xml_empty, results['invalid_xml'], mm['image_no_label'],
                mm['label_no_image'], mm['image_no_xml'], mm['xml_no_image']]):
            self.result_text.insert(tk.END, "\n" + "=" * 70 + "\n")
            self.result_text.insert(tk.END, "建议: 勾选'自动清理无效文件'选项并重新运行检查，自动修复问题\n")
            self.result_text.insert(tk.END, "=" * 70 + "\n")

    def cleanup_dataset(self, results, dataset_path):
        """清理无效文件"""
        self.result_text.insert(tk.END, "\n" + "=" * 70 + "\n")
        self.result_text.insert(tk.END, "开始清理无效文件...\n")
        self.result_text.insert(tk.END, "=" * 70 + "\n\n")

        # 定义路径
        paths = {
            'images': os.path.join(dataset_path, "images"),
            'labels': os.path.join(dataset_path, "labels"),
            'xml': os.path.join(dataset_path, "xml")
        }

        # 删除空文件
        for file_type in ['txt', 'xml']:
            for file_path in results['empty_files'][file_type]:
                try:
                    os.remove(file_path)
                    self.result_text.insert(tk.END, f"已删除空文件: {os.path.basename(file_path)}\n")
                except Exception as e:
                    self.result_text.insert(tk.END, f"删除失败 {os.path.basename(file_path)}: {str(e)}\n")

        # 删除无效XML
        for item in results['invalid_xml']:
            try:
                os.remove(item['file'])
                self.result_text.insert(tk.END, f"已删除无效XML: {os.path.basename(item['file'])}\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"删除失败 {os.path.basename(item['file'])}: {str(e)}\n")

        # 删除不匹配的文件
        mm = results['missing_matches']

        # 删除没有标签的图片
        for base_name in mm['image_no_label']:
            try:
                image_path = self.find_image_path(paths['images'], base_name)
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
                    self.result_text.insert(tk.END, f"已删除无标签图片: {os.path.basename(image_path)}\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"删除失败 {base_name}: {str(e)}\n")

        # 删除没有图片的标签
        for base_name in mm['label_no_image']:
            try:
                label_path = os.path.join(paths['labels'], base_name + '.txt')
                if os.path.exists(label_path):
                    os.remove(label_path)
                    self.result_text.insert(tk.END, f"已删除无图片标签: {base_name}.txt\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"删除失败 {base_name}.txt: {str(e)}\n")

        # 删除没有XML的图片
        for base_name in mm['image_no_xml']:
            try:
                image_path = self.find_image_path(paths['images'], base_name)
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
                    self.result_text.insert(tk.END, f"已删除无XML图片: {os.path.basename(image_path)}\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"删除失败 {base_name}: {str(e)}\n")

        # 删除没有图片的XML
        for base_name in mm['xml_no_image']:
            try:
                xml_path = os.path.join(paths['xml'], base_name + '.xml')
                if os.path.exists(xml_path):
                    os.remove(xml_path)
                    self.result_text.insert(tk.END, f"已删除无图片XML: {base_name}.xml\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"删除失败 {base_name}.xml: {str(e)}\n")

        self.result_text.insert(tk.END, "\n✅ 清理完成!\n")

    def find_image_path(self, images_dir, base_name):
        """在图片目录中查找匹配的文件名（支持多种图片格式）"""
        if not os.path.exists(images_dir):
            return None

        for ext in ['.jpg', '.jpeg', '.png']:
            path = os.path.join(images_dir, base_name + ext)
            if os.path.exists(path):
                return path

        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = DatasetCheckerApp(root)
    root.mainloop()