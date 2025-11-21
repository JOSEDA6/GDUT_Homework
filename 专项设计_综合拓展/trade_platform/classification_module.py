class ClassificationModule:
    """商品分类管理模块 - 修正参数占位符"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.categories = ['电子产品', '学习资料', '生活用品', '服装鞋帽', '运动器材', '图书杂志', '其他']

    def get_all_categories(self):
        """获取所有分类"""
        return self.categories

    def get_products_by_category(self, category, page=1, page_size=20):
        """根据分类获取商品 - 使用 ? 作为参数占位符[6](@ref)"""
        offset = (page - 1) * page_size
        # 使用 ? 作为参数占位符
        query = """
        SELECT * FROM products 
        WHERE category = ? AND status = 'active' 
        ORDER BY created_at DESC 
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
        """
        return self.db_manager.execute_query(query, (category, offset, page_size))

    def add_category(self, category_name):
        """添加新分类（管理员功能）"""
        if category_name not in self.categories:
            self.categories.append(category_name)
            return True
        return False

    def get_category_stats(self):
        """获取分类统计信息 - 使用 ? 作为参数占位符"""
        stats = {}
        for category in self.categories:
            # 使用 ? 作为参数占位符
            query = "SELECT COUNT(*) as count FROM products WHERE category = ? AND status = 'active'"
            result = self.db_manager.execute_query(query, (category,))
            stats[category] = result[0]['count'] if result else 0
        return stats