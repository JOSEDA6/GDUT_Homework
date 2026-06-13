class TargetModule:
    """推荐目标模块 - 修正参数占位符"""

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_recommendations(self, user_id, limit=10):
        """为用户推荐商品 - 使用 ? 作为参数占位符[6,7](@ref)"""
        recommendations = []

        # 基于用户浏览历史的推荐
        user_categories = self._get_user_preferred_categories(user_id)

        for category in user_categories:
            # 使用 ? 作为参数占位符
            query = """
            SELECT * FROM products 
            WHERE category = ? AND status = 'active' 
            ORDER BY created_at DESC 
            LIMIT ?
            """
            products = self.db_manager.execute_query(query, (category, limit))
            recommendations.extend(products)

        # 如果推荐数量不足，添加热门商品
        if len(recommendations) < limit:
            hot_products = self._get_hot_products(limit - len(recommendations))
            recommendations.extend(hot_products)

        return recommendations[:limit]

    def _get_user_preferred_categories(self, user_id):
        """获取用户偏好的商品分类 - 使用 ? 作为参数占位符"""
        # 使用 ? 作为参数占位符
        query = """
        SELECT category FROM products 
        WHERE seller_id = ? OR product_id IN (
            SELECT product_id FROM orders WHERE buyer_id = ?
        )
        GROUP BY category ORDER BY COUNT(*) DESC LIMIT 3
        """
        result = self.db_manager.execute_query(query, (user_id, user_id))
        categories = [row['category'] for row in result] if result else []

        # 如果没有历史数据，返回默认分类
        if not categories:
            return ['电子产品', '学习资料', '生活用品']

        return categories

    def _get_hot_products(self, limit):
        """获取热门商品 - 使用 ? 作为参数占位符"""
        # 使用 ? 作为参数占位符
        query = """
        SELECT p.*, COUNT(o.order_id) as order_count 
        FROM products p 
        LEFT JOIN orders o ON p.product_id = o.product_id 
        WHERE p.status = 'active' 
        GROUP BY p.product_id 
        ORDER BY order_count DESC, p.created_at DESC 
        LIMIT ?
        """
        return self.db_manager.execute_query(query, (limit,))