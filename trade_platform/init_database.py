import pyodbc
import config
import hashlib


class DatabaseInitializer:
    """SQL Server 数据库初始化类 - 完全修正版本"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def create_connection(self, database='master'):
        """创建数据库连接"""
        try:
            # 构建连接字符串
            connection_string = f"""
                DRIVER={{{config.DB_CONFIG['driver']}}};
                SERVER={config.DB_CONFIG['server']};
                DATABASE={database};
                UID={config.DB_CONFIG['user']};
                PWD={config.DB_CONFIG['password']};
                Trusted_Connection={config.DB_CONFIG['trusted_connection']};
            """

            self.connection = pyodbc.connect(connection_string, autocommit=True)
            self.cursor = self.connection.cursor()
            print(f"成功连接到 SQL Server 数据库: {database}")
            return True

        except pyodbc.Error as e:
            print(f"数据库连接失败: {e}")
            print(f"连接字符串: SERVER={config.DB_CONFIG['server']}, USER={config.DB_CONFIG['user']}")
            return False

    def check_database_exists(self):
        """检查数据库是否存在"""
        try:
            self.cursor.execute("SELECT name FROM sys.databases WHERE name = 'campus_trade'")
            return self.cursor.fetchone() is not None
        except pyodbc.Error as e:
            print(f"检查数据库存在性时出错: {e}")
            return False

    def create_database(self):
        """创建数据库"""
        try:
            if self.check_database_exists():
                print("数据库 campus_trade 已存在")
                return True

            # 创建数据库
            self.cursor.execute("CREATE DATABASE campus_trade")
            print("数据库 campus_trade 创建成功")
            return True

        except pyodbc.Error as e:
            print(f"创建数据库时出错: {e}")
            return False

    def create_tables(self):
        """创建所有数据表"""
        try:
            # 切换到目标数据库
            self.cursor.execute("USE campus_trade")

            # 用户表
            if not self.check_table_exists('users'):
                self.cursor.execute("""
                    CREATE TABLE users (
                        user_id INT IDENTITY(1,1) PRIMARY KEY,
                        username NVARCHAR(50) UNIQUE NOT NULL,
                        password NVARCHAR(255) NOT NULL,
                        email NVARCHAR(100) UNIQUE NOT NULL,
                        phone NVARCHAR(20),
                        credit_score INT DEFAULT 100,
                        points INT DEFAULT 0,
                        user_type NVARCHAR(10) DEFAULT 'student',
                        created_at DATETIME DEFAULT GETDATE()
                    )
                """)
                print("用户表创建成功")

            # 商品表
            if not self.check_table_exists('products'):
                self.cursor.execute("""
                    CREATE TABLE products (
                        product_id INT IDENTITY(1,1) PRIMARY KEY,
                        title NVARCHAR(200) NOT NULL,
                        description NTEXT,
                        price DECIMAL(10,2) NOT NULL,
                        category NVARCHAR(50) NOT NULL,
                        seller_id INT,
                        status NVARCHAR(10) DEFAULT 'active',
                        images NVARCHAR(MAX),
                        created_at DATETIME DEFAULT GETDATE()
                    )
                """)
                print("商品表创建成功")

            # 订单表
            if not self.check_table_exists('orders'):
                self.cursor.execute("""
                    CREATE TABLE orders (
                        order_id INT IDENTITY(1,1) PRIMARY KEY,
                        product_id INT,
                        buyer_id INT,
                        seller_id INT,
                        amount DECIMAL(10,2) NOT NULL,
                        status NVARCHAR(10) DEFAULT 'pending',
                        created_at DATETIME DEFAULT GETDATE()
                    )
                """)
                print("订单表创建成功")

            # 信用日志表
            if not self.check_table_exists('credit_logs'):
                self.cursor.execute("""
                    CREATE TABLE credit_logs (
                        log_id INT IDENTITY(1,1) PRIMARY KEY,
                        user_id INT,
                        change_amount INT NOT NULL,
                        reason NVARCHAR(255),
                        new_score INT NOT NULL,
                        created_at DATETIME DEFAULT GETDATE()
                    )
                """)
                print("信用日志表创建成功")

            # 积分日志表
            if not self.check_table_exists('points_logs'):
                self.cursor.execute("""
                    CREATE TABLE points_logs (
                        log_id INT IDENTITY(1,1) PRIMARY KEY,
                        user_id INT,
                        change_amount INT NOT NULL,
                        reason NVARCHAR(255),
                        new_points INT NOT NULL,
                        created_at DATETIME DEFAULT GETDATE()
                    )
                """)
                print("积分日志表创建成功")

            return True

        except pyodbc.Error as e:
            print(f"创建表时出错: {e}")
            return False

    def check_table_exists(self, table_name):
        """检查表是否存在"""
        try:
            self.cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = ?
            """, table_name)
            return self.cursor.fetchone()[0] > 0
        except pyodbc.Error:
            return False

    def insert_sample_data(self):
        """插入示例数据"""
        try:
            # 检查是否已有用户数据
            self.cursor.execute("SELECT COUNT(*) as count FROM users")
            if self.cursor.fetchone()[0] > 0:
                print("数据库中已有数据，跳过示例数据插入")
                return True

            # 插入示例用户（密码都是123456的MD5加密）
            encrypted_password = hashlib.md5('123456'.encode()).hexdigest()

            sample_users = [
                ("admin", encrypted_password, "admin@campus.com", "13800138000", "admin"),
                ("student1", encrypted_password, "student1@campus.com", "13900139000", "student"),
                ("student2", encrypted_password, "student2@campus.com", "13700137000", "student"),
                ("施乔", encrypted_password, "3122009224@campus.com", "13800138001", "student")
            ]

            for username, password, email, phone, user_type in sample_users:
                self.cursor.execute("""
                    INSERT INTO users (username, password, email, phone, user_type) 
                    VALUES (?, ?, ?, ?, ?)
                """, (username, password, email, phone, user_type))

            print("示例用户数据插入成功")

            # 插入示例商品
            sample_products = [
                ("二手笔记本电脑", "性能良好的二手笔记本电脑，i5处理器，8GB内存", 2000.00, "电子产品", 2),
                ("高等数学教材", "几乎全新的高等数学教材，包含详细笔记", 30.00, "学习资料", 2),
                ("篮球", "标准7号篮球，使用次数少，质量良好", 50.00, "运动器材", 3),
                ("Java编程思想", "经典编程教材，适合计算机专业学生", 45.00, "图书杂志", 3),
                ("冬季棉服", "保暖棉服，九成新，L码", 80.00, "服装鞋帽", 2),
                ("计算器", "科学计算器，考试必备", 25.00, "电子产品", 4),
                ("英语四级词汇", "英语四级考试词汇书，带记忆方法", 20.00, "学习资料", 4)
            ]

            for title, description, price, category, seller_id in sample_products:
                self.cursor.execute("""
                    INSERT INTO products (title, description, price, category, seller_id) 
                    VALUES (?, ?, ?, ?, ?)
                """, (title, description, price, category, seller_id))

            print("示例商品数据插入成功")
            return True

        except pyodbc.Error as e:
            print(f"插入示例数据时出错: {e}")
            return False

    def test_connection(self):
        """测试数据库连接"""
        try:
            connection_string = f"""
                DRIVER={{{config.DB_CONFIG['driver']}}};
                SERVER={config.DB_CONFIG['server']};
                DATABASE=campus_trade;
                UID={config.DB_CONFIG['user']};
                PWD={config.DB_CONFIG['password']};
                Trusted_Connection={config.DB_CONFIG['trusted_connection']};
            """

            test_conn = pyodbc.connect(connection_string)
            test_cursor = test_conn.cursor()
            test_cursor.execute("SELECT @@VERSION as version")
            result = test_cursor.fetchone()
            test_conn.close()

            print(f"数据库连接测试成功! SQL Server 版本: {result[0][:50]}...")
            return True

        except pyodbc.Error as e:
            print(f"数据库连接测试失败: {e}")
            return False


def initialize_database():
    """初始化数据库的主函数"""
    print("开始初始化校园交易平台数据库...")
    print("=" * 50)

    initializer = DatabaseInitializer()

    # 第一步：连接到 master 数据库
    print("1. 连接到 SQL Server master 数据库...")
    if not initializer.create_connection('master'):
        print("\n无法连接到 SQL Server，请检查：")
        print("1. SQL Server 服务是否正在运行")
        print("2. 服务器名称是否正确: JOS-LAPTOP\\SQL")
        print("3. 用户名和密码是否正确")
        print("4. SQL Server 身份验证是否已启用")
        return False

    # 第二步：创建数据库
    print("2. 创建数据库...")
    if not initializer.create_database():
        print("数据库创建失败")
        return False

    # 第三步：创建表
    print("3. 创建数据表...")
    if not initializer.create_tables():
        print("数据表创建失败")
        return False

    # 第四步：插入示例数据
    print("4. 插入示例数据...")
    if not initializer.insert_sample_data():
        print("示例数据插入失败")
        return False

    # 关闭当前连接
    if initializer.connection:
        initializer.connection.close()

    # 第五步：测试最终连接
    print("5. 测试最终连接...")
    if not initializer.test_connection():
        print("最终连接测试失败")
        return False

    print("\n" + "=" * 50)
    print("校园交易平台数据库初始化完成！")
    print("默认测试账户:")
    print("用户名: admin, 密码: 123456")
    print("用户名: student1, 密码: 123456")
    print("用户名: 施乔, 密码: 123456")
    print("=" * 50)
    return True


if __name__ == "__main__":
    if initialize_database():
        print("\n现在可以运行: python main.py 启动交易平台")
    else:
        print("\n数据库初始化失败，请检查上述错误信息")
        print("\n故障排除建议:")
        print("1. 确保 SQL Server 服务正在运行")
        print("2. 在 SQL Server Management Studio 中测试连接")
        print("3. 检查 config.py 中的服务器名称和密码")
        print("4. 确保已启用 SQL Server 身份验证")