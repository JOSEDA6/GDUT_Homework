# sources/__init__.py
print("Initializing sources package")

# 导入子模块
from .data_utils import get_CIFAR10_data
from .gradient_check import eval_numerical_gradient

# 定义公共接口
__all__ = ['get_CIFAR10_data', 'eval_numerical_gradient']

# 包级元数据
__version__ = "1.0.0"