import numpy as np
import matplotlib.pyplot as plt
import os  # 新增导入

def run():
    N = 100
    nodes, flag = node_factory(N)
    iter_classes = classify(nodes, flag, k=10)

    # 创建保存图片的文件夹
    save_dir = "images"
    os.makedirs(save_dir, exist_ok=True)

    # 遍历迭代并保存图片
    for idx, classes in enumerate(iter_classes):
        save_path = os.path.join(save_dir, f"cluster_iteration_{idx}.png")
        show_plt(classes, save_path)

# ...（其他函数保持不变，确保函数名已修正）...

def show_plt(classes, save_path=None):
    fig = plt.figure()
    ax1 = plt.gca()
    ax1.set_title('WSN1')
    plt.xlabel('X')
    plt.ylabel('Y')
    icon = ['o', '*', 'x', '+', 's']
    color = ['r', 'b', 'g', 'c', 'y', 'm']

    for i in range(len(classes)):
        if not classes[i]:
            continue
        centor = classes[i][0]
        for point in classes[i]:
            ax1.plot([centor[0], point[0]], [centor[1], point[1]],
                     c=color[i % 6], marker=icon[i % 5], alpha=0.4)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":
    run()