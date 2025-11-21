class UIModule:
    """UI模块 - 基于控制台的界面"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.current_user = None

    def render_homepage(self, products=None):
        """渲染首页"""
        if products is None:
            query = "SELECT * FROM products WHERE status = 'active' ORDER BY created_at DESC LIMIT 10"
            products = self.db_manager.execute_query(query)

        user_info = self.current_user['username'] if self.current_user else '未登录'
        credit_info = f"(信用: {self.current_user['credit_score']})" if self.current_user and 'credit_score' in self.current_user else ""

        homepage_template = f"""
        =========================================
             校园交易平台 - 首页
        =========================================
        当前用户: {user_info} {credit_info}

        {'为您推荐:' if products and self.current_user else '最新商品:'}
        {self._format_products_list(products)}

        功能菜单:
        1. 浏览商品    2. 搜索商品    3. 发布商品
        4. 我的订单    5. 个人中心    6. 退出登录
        =========================================
        """
        return homepage_template

    def render_product_detail(self, product):
        """渲染商品详情页"""
        # 获取卖家信息
        seller_query = "SELECT username FROM users WHERE user_id = ?"
        seller_result = self.db_manager.execute_query(seller_query, (product['seller_id'],))
        seller_name = seller_result[0]['username'] if seller_result else "未知用户"

        detail_template = f"""
        =========================================
                 商品详情 - {product['title']}
        =========================================
        商品标题: {product['title']}
        价格: ¥{product['price']}
        分类: {product['category']}
        卖家: {seller_name}
        发布时间: {product['created_at']}

        商品描述:
        {product['description']}

        操作选项:
        1. 立即购买    2. 返回
        =========================================
        """
        return detail_template

    def _format_products_list(self, products):
        """格式化商品列表显示"""
        if not products:
            return "暂无商品"

        product_list = ""
        for i, product in enumerate(products, 1):
            # 限制标题长度
            title = product['title'][:20] + "..." if len(product['title']) > 20 else product['title']
            product_list += f"{i}. {title} - ¥{product['price']}\n"
        return product_list