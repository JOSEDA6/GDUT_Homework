from database import encrypt_password


class CustomerModule:
    """用户管理模块"""

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def register_user(self, username, password, email, phone):
        """用户注册"""
        # 检查用户名是否已存在
        check_query = "SELECT username FROM users WHERE username = ?"
        if self.db_manager.execute_query(check_query, (username,)):
            return False, "用户名已存在"

        # 检查邮箱是否已存在
        check_email_query = "SELECT email FROM users WHERE email = ?"
        if self.db_manager.execute_query(check_email_query, (email,)):
            return False, "邮箱已存在"

        encrypted_pwd = encrypt_password(password)

        insert_query = """
        INSERT INTO users (username, password, email, phone) 
        VALUES (?, ?, ?, ?)
        """
        result = self.db_manager.execute_update(insert_query,
                                                (username, encrypted_pwd, email, phone))

        if result > 0:
            return True, "注册成功"
        else:
            return False, "注册失败"

    def login_user(self, username, password):
        """用户登录"""
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        encrypted_pwd = encrypt_password(password)
        users = self.db_manager.execute_query(query, (username, encrypted_pwd))

        if users:
            return True, users[0]
        else:
            return False, "用户名或密码错误"

    def update_user_profile(self, user_id, email=None, phone=None):
        """更新用户资料"""
        update_fields = []
        params = []

        if email:
            update_fields.append("email = ?")
            params.append(email)
        if phone:
            update_fields.append("phone = ?")
            params.append(phone)

        if update_fields:
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = ?"
            result = self.db_manager.execute_update(query, params)
            return result > 0
        return False