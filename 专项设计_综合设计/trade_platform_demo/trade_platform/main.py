from database import DatabaseManager, encrypt_password
from ui_module import UIModule
from customer_module import CustomerModule
from classification_module import ClassificationModule
from member_module import MemberModule
from target_module import TargetModule
import config


class CampusTradePlatform:
    """校园交易平台主类"""

    def __init__(self):
        self.db_manager = DatabaseManager()
        if not self.db_manager.test_connection():
            self.handle_database_error()
            return

        self.ui_module = UIModule(self.db_manager)
        self.customer_module = CustomerModule(self.db_manager)
        self.classification_module = ClassificationModule(self.db_manager)
        self.member_module = MemberModule(self.db_manager)
        self.target_module = TargetModule(self.db_manager)
        self.current_user = None

    def handle_database_error(self):
        """处理数据库连接错误"""
        print("\n" + "=" * 60)
        print("数据库连接失败！")
        print("=" * 60)
        print("请按照以下步骤解决问题：")
        print("1. 确保SQL Server服务已启动")
        print("2. 运行 'python init_database.py' 初始化数据库")
        print("3. 检查 config.py 中的数据库配置")
        print("\n现在将进入离线模式（功能受限）...")

    def run(self):
        """运行主程序"""
        if not self.db_manager.test_connection():
            self.run_offline_mode()
            return

        print("欢迎使用校园交易平台!")

        while True:
            if not self.current_user:
                self.show_login_menu()
            else:
                self.show_main_menu()

    def show_main_menu(self):
        """显示主菜单"""
        # 获取推荐商品
        recommendations = []
        if self.current_user:
            recommendations = self.target_module.get_recommendations(self.current_user['user_id'], 5)

        homepage = self.ui_module.render_homepage(recommendations)
        print(homepage)

        choice = input("请选择操作: ")

        if choice == '1':
            self.browse_products()
        elif choice == '2':
            self.search_products()
        elif choice == '3':
            self.publish_product()
        elif choice == '4':
            self.view_orders()
        elif choice == '5':
            self.user_profile()
        elif choice == '6':
            self.current_user = None
            self.ui_module.current_user = None
            print("已退出登录")
        else:
            print("无效选择，请重新输入")

    def run_offline_mode(self):
        """离线模式运行"""
        print("\n离线模式 - 仅提供有限功能")
        print("请先解决数据库连接问题以获得完整功能")

        while True:
            print("\n1. 查看系统信息")
            print("2. 退出系统")
            choice = input("请选择: ")

            if choice == '1':
                print("\n系统信息：")
                print("- 校园交易平台 v1.0")
                print("- 当前状态: 数据库未连接")
                print("- 请运行 init_database.py 初始化数据库")
            elif choice == '2':
                exit()
            else:
                print("无效选择")

    def show_login_menu(self):
        """显示登录菜单"""
        print("\n" + "=" * 50)
        print("校园交易平台 - 登录/注册")
        print("=" * 50)
        print("1. 用户登录")
        print("2. 用户注册")
        print("3. 退出系统")

        choice = input("请选择操作: ")

        if choice == '1':
            self.user_login()
        elif choice == '2':
            self.user_register()
        elif choice == '3':
            print("感谢使用，再见!")
            exit()
        else:
            print("无效选择，请重新输入")

    def user_login(self):
        """用户登录"""
        username = input("请输入用户名: ")
        password = input("请输入密码: ")

        success, result = self.customer_module.login_user(username, password)
        if success:
            self.current_user = result
            self.ui_module.current_user = result
            print(f"登录成功! 欢迎 {username}")
        else:
            print(f"登录失败: {result}")

    def user_register(self):
        """用户注册"""
        print("\n用户注册")
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        email = input("请输入邮箱: ")
        phone = input("请输入手机号: ")

        success, message = self.customer_module.register_user(username, password, email, phone)
        print(message)

    def browse_products(self):
        """浏览商品"""
        categories = self.classification_module.get_all_categories()
        print("\n商品分类:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        try:
            choice = int(input("请选择分类编号: "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                products = self.classification_module.get_products_by_category(selected_category)

                print(f"\n{selected_category}分类商品:")
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product['title']} - ¥{product['price']}")

                if products:
                    product_choice = input("\n输入商品编号查看详情(0返回主菜单): ")
                    if product_choice.isdigit() and 1 <= int(product_choice) <= len(products):
                        self.view_product_detail(products[int(product_choice) - 1])
            else:
                print("无效选择")
        except ValueError:
            print("请输入有效数字")

    def view_product_detail(self, product):
        """查看商品详情"""
        detail = self.ui_module.render_product_detail(product)
        print(detail)

        if self.current_user and self.current_user['user_id'] != product['seller_id']:
            choice = input("请选择操作(1购买 2返回): ")
            if choice == '1':
                self.buy_product(product)

    def buy_product(self, product):
        """购买商品"""
        print(f"\n确认购买: {product['title']} - ¥{product['price']}")
        confirm = input("确认购买? (y/n): ")

        if confirm.lower() == 'y':
            query = """
            INSERT INTO orders (product_id, buyer_id, seller_id, amount) 
            VALUES (?, ?, ?, ?)
            """
            result = self.db_manager.execute_update(query,
                                                    (product['product_id'], self.current_user['user_id'],
                                                     product['seller_id'], product['price']))

            if result > 0:
                self.db_manager.execute_update(
                    "UPDATE products SET status = 'sold' WHERE product_id = ?",
                    (product['product_id'],))

                print("购买成功! 请联系卖家完成交易")

                self.member_module.add_points(self.current_user['user_id'], 5, "购买商品")
                self.member_module.add_points(product['seller_id'], 10, "售出商品")
            else:
                print("购买失败")

    def search_products(self):
        """搜索商品"""
        keyword = input("请输入搜索关键词: ")
        query = "SELECT * FROM products WHERE (title LIKE ? OR description LIKE ?) AND status = 'active'"
        products = self.db_manager.execute_query(query, (f"%{keyword}%", f"%{keyword}%"))

        print(f"\n搜索 '{keyword}' 结果({len(products)}个商品):")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product['title']} - ¥{product['price']}")

        if products:
            product_choice = input("\n输入商品编号查看详情(0返回): ")
            if product_choice.isdigit() and 1 <= int(product_choice) <= len(products):
                self.view_product_detail(products[int(product_choice) - 1])

    def publish_product(self):
        """发布商品"""
        if not self.current_user:
            print("请先登录")
            return

        print("\n发布新商品")
        title = input("商品标题: ")
        description = input("商品描述: ")

        try:
            price = float(input("价格: "))
        except ValueError:
            print("价格格式错误")
            return

        categories = self.classification_module.get_all_categories()
        print("可选分类:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        try:
            category_choice = int(input("选择分类编号: "))
            category = categories[category_choice - 1] if 1 <= category_choice <= len(categories) else "其他"
        except (ValueError, IndexError):
            category = "其他"

        insert_query = """
        INSERT INTO products (title, description, price, category, seller_id) 
        VALUES (?, ?, ?, ?, ?)
        """
        result = self.db_manager.execute_update(insert_query,
                                                (title, description, price, category, self.current_user['user_id']))

        if result > 0:
            print("商品发布成功!")
            self.member_module.add_points(self.current_user['user_id'], 10, "发布商品")
        else:
            print("商品发布失败")

    def view_orders(self):
        """查看我的订单"""
        if not self.current_user:
            print("请先登录")
            return

        print("\n我的订单")
        print("1. 我购买的")
        print("2. 我出售的")
        choice = input("请选择: ")

        if choice == '1':
            query = """
            SELECT o.*, p.title, p.description 
            FROM orders o 
            JOIN products p ON o.product_id = p.product_id 
            WHERE o.buyer_id = ? 
            ORDER BY o.created_at DESC
            """
            orders = self.db_manager.execute_query(query, (self.current_user['user_id'],))

            print("\n我购买的订单:")
            for i, order in enumerate(orders, 1):
                print(f"{i}. {order['title']} - ¥{order['amount']} - 状态: {order['status']}")

        elif choice == '2':
            query = """
            SELECT o.*, p.title, p.description, u.username as buyer_name
            FROM orders o 
            JOIN products p ON o.product_id = p.product_id 
            JOIN users u ON o.buyer_id = u.user_id
            WHERE o.seller_id = ? 
            ORDER BY o.created_at DESC
            """
            orders = self.db_manager.execute_query(query, (self.current_user['user_id'],))

            print("\n我出售的订单:")
            for i, order in enumerate(orders, 1):
                print(
                    f"{i}. {order['title']} - ¥{order['amount']} - 买家: {order['buyer_name']} - 状态: {order['status']}")
        else:
            print("无效选择")

    def user_profile(self):
        """用户个人中心"""
        if not self.current_user:
            print("请先登录")
            return

        print(f"\n个人中心 - {self.current_user['username']}")
        print("=" * 30)
        print(f"用户名: {self.current_user['username']}")
        print(f"邮箱: {self.current_user['email']}")
        print(f"电话: {self.current_user['phone']}")
        print(f"信用评分: {self.current_user['credit_score']}")
        print(f"积分: {self.current_user['points']}")
        print(f"用户类型: {self.current_user['user_type']}")
        print(f"注册时间: {self.current_user['created_at']}")
        print("=" * 30)

        print("\n1. 修改资料")
        print("2. 返回主菜单")
        choice = input("请选择: ")

        if choice == '1':
            self.update_profile()

    def update_profile(self):
        """修改用户资料"""
        print("\n修改资料")
        new_email = input(f"新邮箱(当前: {self.current_user['email']}): ").strip()
        new_phone = input(f"新电话(当前: {self.current_user['phone']}): ").strip()

        if new_email or new_phone:
            success = self.customer_module.update_user_profile(
                self.current_user['user_id'],
                new_email if new_email else None,
                new_phone if new_phone else None
            )

            if success:
                print("资料更新成功")
                query = "SELECT * FROM users WHERE user_id = ?"
                updated_user = self.db_manager.execute_query(query, (self.current_user['user_id'],))
                if updated_user:
                    self.current_user = updated_user[0]
            else:
                print("资料更新失败")
        else:
            print("未作任何修改")


if __name__ == "__main__":
    platform = CampusTradePlatform()
    platform.run()