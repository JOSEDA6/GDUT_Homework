class MemberModule:
    """会员管理模块 - 修正参数占位符"""

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def update_credit_score(self, user_id, score_change, reason):
        """更新用户信用评分 - 使用 ? 作为参数占位符[7](@ref)"""
        # 获取当前信用分
        query = "SELECT credit_score FROM users WHERE user_id = ?"
        result = self.db_manager.execute_query(query, (user_id,))

        if result:
            current_score = result[0]['credit_score']
            new_score = max(0, min(100, current_score + score_change))

            # 使用 ? 作为参数占位符
            update_query = "UPDATE users SET credit_score = ? WHERE user_id = ?"
            self.db_manager.execute_update(update_query, (new_score, user_id))

            # 记录信用变更日志
            self._log_credit_change(user_id, score_change, reason, new_score)
            return new_score
        return None

    def add_points(self, user_id, points, reason):
        """增加用户积分"""
        query = "SELECT points FROM users WHERE user_id = ?"
        result = self.db_manager.execute_query(query, (user_id,))

        if result:
            current_points = result[0]['points']
            new_points = current_points + points

            # 使用 ? 作为参数占位符
            update_query = "UPDATE users SET points = ? WHERE user_id = ?"
            self.db_manager.execute_update(update_query, (new_points, user_id))

            # 记录积分变更日志
            self._log_points_change(user_id, points, reason, new_points)
            return new_points
        return None

    def _log_credit_change(self, user_id, change, reason, new_score):
        """记录信用分变更日志"""
        # 使用 ? 作为参数占位符
        log_query = """
        INSERT INTO credit_logs (user_id, change_amount, reason, new_score, created_at) 
        VALUES (?, ?, ?, ?, GETDATE())
        """
        self.db_manager.execute_update(log_query, (user_id, change, reason, new_score))

    def _log_points_change(self, user_id, change, reason, new_points):
        """记录积分变更日志 - 使用 ? 作为参数占位符"""
        # 使用 ? 作为参数占位符
        log_query = """
        INSERT INTO points_logs (user_id, change_amount, reason, new_points, created_at) 
        VALUES (?, ?, ?, ?, GETDATE())
        """
        self.db_manager.execute_update(log_query, (user_id, change, reason, new_points))