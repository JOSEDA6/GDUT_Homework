import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    """用户数据模型"""
    user_id: int
    username: str
    password: str
    email: str
    phone: str
    credit_score: int = 100  # 信用评分
    points: int = 0  # 积分
    user_type: str = 'student'  # 用户类型
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class Product:
    """商品数据模型"""
    product_id: int
    title: str
    description: str
    price: float
    category: str
    seller_id: int
    status: str = 'active'  # active, sold, removed
    images: List[str] = None
    created_at: str = None

    def __post_init__(self):
        if self.images is None:
            self.images = []
        if self.created_at is None:
            self.created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class Order:
    """订单数据模型"""
    order_id: int
    product_id: int
    buyer_id: int
    seller_id: int
    amount: float
    status: str = 'pending'  # pending, paid, shipped, completed
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')