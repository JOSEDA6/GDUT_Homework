from flask import Flask, render_template, request, redirect, url_for
from database import init_db, db_session
# 导入你的模型，请确保 models.py 里有这些类
# 如果类名不同，请修改这里
from models import Customer, Member, Target, Classification

app = Flask(__name__)

# 在应用关闭时移除数据库会话
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# --- 路由 ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def list_customers():
    # 查询所有客户
    customers = db_session.query(Customer).all()
    return render_template('customers.html', customers=customers)

@app.route('/members')
def list_members():
    members = db_session.query(Member).all()
    # 你需要创建 templates/members.html，结构参考 customers.html
    return render_template('members.html', members=members)

@app.route('/targets')
def list_targets():
    targets = db_session.query(Target).all()
    # 你需要创建 templates/targets.html
    return render_template('targets.html', targets=targets)

@app.route('/classifications')
def list_classifications():
    classes = db_session.query(Classification).all()
    # 你需要创建 templates/classifications.html
    return render_template('classifications.html', classes=classes)

# 启动
if __name__ == '__main__':
    # 初始化数据库（如果还没初始化）
    init_db()
    print("系统启动中... http://127.0.0.1:5000")
    app.run(debug=True)