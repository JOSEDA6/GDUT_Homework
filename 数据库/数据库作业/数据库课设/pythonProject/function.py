import pymysql
from contextlib import contextmanager
import tkinter as tk
from tkinter import messagebox, ttk


# 数据库连接
@contextmanager
def get_db_connection():
    conn = pymysql.connect(
        user='root',
        password='@SQmysql2004',
        host='127.0.0.1',
        database='物资管理',
        port=3306
    )
    try:
        yield conn
    finally:
        conn.close()


def query_db(sql, params=None):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
    return result


def execute_db(sql, params=None):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()


# 用户登录和注册
def login_user(username, password):
    if username == 'Q' and password == '123456':
        return 'admin'
    user = query_db("SELECT * FROM 客户 WHERE 客户名称 = %s AND 密码 = %s", (username, password))
    if user:
        return 'customer'
    supplier = query_db("SELECT * FROM 供应商 WHERE 供应商名称 = %s AND 密码 = %s", (username, password))
    if supplier:
        return 'supplier'
    return None


def register_customer(username, password, contact, phone, address):
    execute_db("INSERT INTO 客户 (客户名称, 密码, 联系人, 联系电话, 客户地址) VALUES (%s, %s, %s, %s, %s)",
               (username, password, contact, phone, address))


# 管理员功能 - 物资管理
def add_material(name, quantity, unit):
    execute_db("INSERT INTO 物资 (物资名称, 库存数量, 单位) VALUES (%s, %s, %s)", (name, quantity, unit))


def delete_material(material_id):
    execute_db("DELETE FROM 物资 WHERE 物资编号 = %s", (material_id,))


def update_material(material_id, name, quantity, unit):
    execute_db("UPDATE 物资 SET 物资名称 = %s, 库存数量 = %s, 单位 = %s WHERE 物资编号 = %s",
               (name, quantity, unit, material_id))


def view_materials():
    return query_db("SELECT * FROM 物资")


# 管理员功能 - 供应商管理
def add_supplier(name, contact, phone, address, password):
    execute_db("INSERT INTO 供应商 (供应商名称, 联系人, 联系电话, 供应商地址, 密码) VALUES (%s, %s, %s, %s, %s)",
               (name, contact, phone, address, password))


def delete_supplier(supplier_id):
    execute_db("DELETE FROM 供应商 WHERE 供应商编号 = %s", (supplier_id,))


def update_supplier(supplier_id, name, contact, phone, address, password):
    execute_db(
        "UPDATE 供应商 SET 供应商名称 = %s, 联系人 = %s, 联系电话 = %s, 供应商地址 = %s, 密码 = %s WHERE 供应商编号 = %s",
        (name, contact, phone, address, password, supplier_id))


def view_suppliers():
    return query_db("SELECT * FROM 供应商")


# 管理员功能 - 客户管理
def add_customer(name, contact, phone, address, password):
    execute_db("INSERT INTO 客户 (客户名称, 联系人, 联系电话, 客户地址, 密码) VALUES (%s, %s, %s, %s, %s)",
               (name, contact, phone, address, password))


def delete_customer(customer_id):
    execute_db("DELETE FROM 客户 WHERE 客户编号 = %s", (customer_id,))


def update_customer(customer_id, name, contact, phone, address, password):
    execute_db(
        "UPDATE 客户 SET 客户名称 = %s, 联系人 = %s, 联系电话 = %s, 客户地址 = %s, 密码 = %s WHERE 客户编号 = %s",
        (name, contact, phone, address, password, customer_id))


def view_customers():
    return query_db("SELECT * FROM 客户")


# 管理员功能 - 采购订单管理
def add_purchase_order(supplier_id, date, delivery_date, quantity, material_id):
    execute_db("INSERT INTO 采购订单 (供应商编号, 采购日期, 交货日期, 数量, 物资编号) VALUES (%s, %s, %s, %s, %s)",
               (supplier_id, date, delivery_date, quantity, material_id))


def delete_purchase_order(order_id):
    execute_db("DELETE FROM 采购订单 WHERE 采购订单编号 = %s", (order_id,))


def update_purchase_order(order_id, supplier_id, date, delivery_date, quantity, material_id):
    execute_db(
        "UPDATE 采购订单 SET 供应商编号 = %s, 采购日期 = %s, 交货日期 = %s, 数量 = %s, 物资编号 = %s WHERE 采购订单编号 = %s",
        (supplier_id, date, delivery_date, quantity, material_id, order_id))


def view_purchase_orders():
    return query_db("SELECT * FROM 采购订单")


# 管理员功能 - 出库单管理
def add_outbound_order(customer_id, date, quantity, material_id):
    execute_db("INSERT INTO 出库单 (客户编号, 出库日期, 数量, 物资编号) VALUES (%s, %s, %s, %s)",
               (customer_id, date, quantity, material_id))


def delete_outbound_order(order_id):
    execute_db("DELETE FROM 出库单 WHERE 出库单编号 = %s", (order_id,))


def update_outbound_order(order_id, customer_id, date, quantity, material_id):
    execute_db("UPDATE 出库单 SET 客户编号 = %s, 出库日期 = %s, 数量 = %s, 物资编号 = %s WHERE 出库单编号 = %s",
               (customer_id, date, quantity, material_id, order_id))


def view_outbound_orders():
    return query_db("SELECT * FROM 出库单")


# 管理员功能 - 入库单管理
def add_inbound_order(purchase_order_id, date, quantity, material_id):
    execute_db("INSERT INTO 入库单 (采购订单编号, 入库日期, 数量, 物资编号) VALUES (%s, %s, %s, %s)",
               (purchase_order_id, date, quantity, material_id))


def delete_inbound_order(order_id):
    execute_db("DELETE FROM 入库单 WHERE 入库单编号 = %s", (order_id,))


def update_inbound_order(order_id, purchase_order_id, date, quantity, material_id):
    execute_db("UPDATE 入库单 SET 采购订单编号 = %s, 入库日期 = %s, 数量 = %s, 物资编号 = %s WHERE 入库单编号 = %s",
               (purchase_order_id, date, quantity, material_id, order_id))


def view_inbound_orders():
    return query_db("SELECT * FROM 入库单")


# 密码修改
def change_password(user_type, username, new_password):
    if user_type == 'customer':
        execute_db("UPDATE 客户 SET 密码 = %s WHERE 客户名称 = %s", (new_password, username))
    elif user_type == 'supplier':
        execute_db("UPDATE 供应商 SET 密码 = %s WHERE 供应商名称 = %s", (new_password, username))


# UI 界面
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("物资管理系统")

        self.frame_login = tk.Frame(root)
        self.frame_login.pack(pady=20)

        tk.Label(self.frame_login, text="用户名:").grid(row=0, column=0)
        self.entry_username = tk.Entry(self.frame_login)
        self.entry_username.grid(row=0, column=1)

        tk.Label(self.frame_login, text="密码:").grid(row=1, column=0)
        self.entry_password = tk.Entry(self.frame_login, show="*")
        self.entry_password.grid(row=1, column=1)

        tk.Button(self.frame_login, text="登录", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.frame_login, text="注册新用户", command=self.register).grid(row=3, column=0, columnspan=2,
                                                                                   pady=10)
        tk.Button(self.frame_login, text="忘记密码", command=self.reset_password).grid(row=4, column=0, columnspan=2,
                                                                                       pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user_type = login_user(username, password)
        if user_type == 'admin':
            self.show_admin_panel()
        elif user_type == 'customer':
            self.show_customer_panel()
        elif user_type == 'supplier':
            self.show_supplier_panel()
        else:
            messagebox.showerror("错误", "用户名或密码错误")

    def register(self):
        # 注册界面代码
        pass

    def reset_password(self):
        # 忘记密码界面代码
        pass

    def show_admin_panel(self):
        self.clear_frame()
        tk.Label(self.root, text="管理员界面", font=("Arial", 16)).pack(pady=10)
        # 添加管理员功能按钮
        buttons = [
            ("物资管理", self.manage_materials),
            ("采购订单管理", self.manage_purchase_orders),
            ("出库单管理", self.manage_outbound_orders),
            ("入库单管理", self.manage_inbound_orders),
            ("客户管理", self.manage_customers),
            ("供应商管理", self.manage_suppliers)
        ]
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command).pack(pady=5)

    def show_customer_panel(self):
        self.clear_frame()
        tk.Label(self.root, text="客户界面", font=("Arial", 16)).pack(pady=10)
        # 添加客户功能按钮
        buttons = [
            ("查看物资", self.view_materials),
            ("创建采购订单", self.create_purchase_order)
        ]
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command).pack(pady=5)

    def show_supplier_panel(self):
        self.clear_frame()
        tk.Label(self.root, text="供应商界面", font=("Arial", 16)).pack(pady=10)
        # 添加供应商功能按钮
        buttons = [
            ("查看物资", self.view_materials),
            ("查看采购订单", self.view_supplier_purchase_orders),
            ("创建出库单", self.create_outbound_order),
            ("创建入库单", self.create_inbound_order)
        ]
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command).pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def manage_materials(self):
        # 管理物资的界面代码
        pass

    def manage_purchase_orders(self):
        # 管理采购订单的界面代码
        pass

    def manage_outbound_orders(self):
        # 管理出库单的界面代码
        pass

    def manage_inbound_orders(self):
        # 管理入库单的界面代码
        pass

    def manage_customers(self):
        # 管理客户的界面代码
        pass

    def manage_suppliers(self):
        # 管理供应商的界面代码
        pass

    def create_purchase_order(self):
        # 创建采购订单的界面代码
        pass

    def view_supplier_purchase_orders(self):
        # 查看供应商采购订单的界面代码
        pass

    def create_outbound_order(self):
        # 创建出库单的界面代码
        pass

    def create_inbound_order(self):
        # 创建入库单的界面代码
        pass

    def view_materials(self):
        # 查看物资的界面代码
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()