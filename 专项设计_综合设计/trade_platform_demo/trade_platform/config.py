# SQL Server 数据库配置 - 根据图片中的实际密码修正
DB_CONFIG = {
    'server': 'JOS-LAPTOP\\SQL',  # 服务器名称（从图片中确认）
    'database': 'campus_trade',
    'user': 'sa',
    'password': '@SQsql2004',  # 从图片中确认的实际密码
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': 'no',
    'autocommit': True
}

# 系统配置
SYSTEM_CONFIG = {
    'max_products_per_user': 50,
    'session_timeout': 3600,
    'max_login_attempts': 5
}

# 分类配置
CATEGORIES = [
    '电子产品', '学习资料', '生活用品', '服装鞋帽',
    '运动器材', '图书杂志', '其他'
]

# 默认用户凭证
DEFAULT_USERS = {
    'admin': {'password': '123456', 'email': 'admin@campus.com'},
    'student1': {'password': '123456', 'email': 'student1@campus.com'}
}