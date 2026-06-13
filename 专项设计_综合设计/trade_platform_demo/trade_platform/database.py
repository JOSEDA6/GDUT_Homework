import pyodbc
import config
import hashlib


class DatabaseManager:
    """SQL Server 数据库管理类 - 修正连接状态检查"""

    def __init__(self, auto_init=True):
        self.connection = None
        if auto_init:
            self.connect()

    def get_connection_string(self):
        """获取连接字符串"""
        return f"""
            DRIVER={{{config.DB_CONFIG['driver']}}};
            SERVER={config.DB_CONFIG['server']};
            DATABASE={config.DB_CONFIG['database']};
            UID={config.DB_CONFIG['user']};
            PWD={config.DB_CONFIG['password']};
            Trusted_Connection={config.DB_CONFIG['trusted_connection']};
        """

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pyodbc.connect(self.get_connection_string())
            print("SQL Server 数据库连接成功")
            return True
        except pyodbc.Error as e:
            print(f"数据库连接失败: {e}")
            return False

    def is_connected(self):
        """检查连接是否有效 - 修正方法"""
        try:
            if self.connection:
                # 尝试执行简单查询来测试连接
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                return True
            return False
        except pyodbc.Error:
            return False

    def execute_query(self, query, params=None):
        """执行查询语句 - 修正连接检查"""
        try:
            # 修正：使用正确的方法检查连接状态
            if not self.is_connected():
                print("连接已断开，尝试重新连接...")
                self.connect()
                if not self.is_connected():
                    print("重新连接失败")
                    return []

            # 将 %s 替换为 ? 以兼容 pyodbc
            query = query.replace('%s', '?')

            cursor = self.connection.cursor()
            cursor.execute(query, params or ())

            # 获取列名
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor:
                    results.append(dict(zip(columns, row)))
                cursor.close()
                return results
            else:
                cursor.close()
                return []

        except pyodbc.Error as e:
            print(f"查询执行失败: {e}")
            print(f"SQL: {query}")
            print(f"参数: {params}")
            # 尝试重新连接
            self.connect()
            return []

    def execute_update(self, query, params=None):
        """执行更新语句 - 修正连接检查"""
        try:
            # 修正：使用正确的方法检查连接状态
            if not self.is_connected():
                print("连接已断开，尝试重新连接...")
                self.connect()
                if not self.is_connected():
                    print("重新连接失败")
                    return 0

            query = query.replace('%s', '?')

            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            rowcount = cursor.rowcount
            cursor.close()
            return rowcount

        except pyodbc.Error as e:
            print(f"更新执行失败: {e}")
            print(f"SQL: {query}")
            print(f"参数: {params}")
            if self.connection:
                try:
                    self.connection.rollback()
                except:
                    pass
            # 尝试重新连接
            self.connect()
            return 0

    def test_connection(self):
        """测试数据库连接"""
        return self.is_connected()


def encrypt_password(password):
    """MD5密码加密"""
    return hashlib.md5(password.encode()).hexdigest()