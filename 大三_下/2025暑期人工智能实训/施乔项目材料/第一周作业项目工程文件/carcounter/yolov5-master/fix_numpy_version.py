import sys
import subprocess
import re


def resolve_conflicts():
    python_exec = sys.executable
    print(f"当前 Python 路径: {python_exec}")

    try:
        # 1. 卸载有冲突的现有包
        uninstall_cmds = [
            [python_exec, "-m", "pip", "uninstall", "-y", "opencv-python", "numpy", "scipy"]
        ]

        # 2. 安装兼容版本
        install_cmds = [
            [python_exec, "-m", "pip", "install", "numpy==1.26.4"],
            [python_exec, "-m", "pip", "install", "opencv-python==4.5.4.62"],
            [python_exec, "-m", "pip", "install", "scipy==1.8.1"]
        ]

        # 执行所有命令
        for cmd in uninstall_cmds + install_cmds:
            print(f"执行: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)

        # 验证安装结果
        result = subprocess.run([python_exec, "-m", "pip", "show", "numpy", "scipy", "opencv-python"],
                                capture_output=True, text=True)
        print("安装验证结果:")
        print(result.stdout)

        print("\n>>> 依赖问题已解决! <<<")
        print(">>> 请重新运行 YOLOv5 训练脚本 <<<")

    except subprocess.CalledProcessError as e:
        print(f"操作失败: {e}")
        print(f"错误详情: {e.stderr}")
        print("请手动执行以下命令:")
        print("pip uninstall -y opencv-python numpy scipy")
        print("pip install numpy==1.26.4 opencv-python==4.5.4.62 scipy==1.8.1")


if __name__ == "__main__":
    print("=" * 60)
    print("YOLOv5 依赖冲突解决工具")
    print("=" * 60)
    resolve_conflicts()
