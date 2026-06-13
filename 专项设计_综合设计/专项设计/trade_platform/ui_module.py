import threading
import webbrowser
from flask import Flask, render_template_string, jsonify, request
from database import DatabaseManager

app = Flask(__name__)
db_instance = None  # 全局数据库实例


# --- 1. 后端 API 接口 ---

@app.route('/api/products')
def get_products():
    """获取商品列表 API"""
    category = request.args.get('category', '全部')
    if category == '全部':
        query = "SELECT * FROM products WHERE status = 'active' ORDER BY created_at DESC"
        data = db_instance.execute_query(query)
    else:
        query = "SELECT * FROM products WHERE category = ? AND status = 'active'"
        data = db_instance.execute_query(query, (category,))
    return jsonify(data)


@app.route('/api/buy', methods=['POST'])
def buy_product():
    """执行购买逻辑 API"""
    product_id = request.json.get('product_id')
    # 真实修改数据库状态
    update_sql = "UPDATE products SET status = 'sold' WHERE product_id = ?"
    affected_rows = db_instance.execute_update(update_sql, (product_id,))

    if affected_rows > 0:
        return jsonify({"status": "success", "message": f"商品 {product_id} 购买成功！"})
    return jsonify({"status": "error", "message": "商品可能已被买走"})


# --- 2. 前端 HTML/JavaScript 模板 ---
# 这里我们将 JavaScript 直接嵌入，方便你直接运行测试

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Campus Trade | 校园交易系统</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .apple-card { transition: all 0.3s ease; border-radius: 18px; }
        .apple-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
    </style>
</head>
<body class="bg-[#f5f5f7] text-[#1d1d1f]">
    <nav class="sticky top-0 bg-white/80 backdrop-blur-md border-b border-gray-200 z-50 p-4">
        <div class="max-w-5xl mx-auto flex justify-between items-center">
            <h1 class="text-xl font-semibold">Campus Trade</h1>
            <div id="user-info" class="text-sm text-blue-600">数据库已连接 (SQL Server)</div>
        </div>
    </nav>

    <main class="max-w-5xl mx-auto p-8">
        <header class="mb-10 text-center">
            <h2 class="text-4xl font-bold mb-4">寻找你需要的校园好物</h2>
            <div class="flex justify-center space-x-4" id="category-filters">
                <button onclick="loadProducts('全部')" class="px-4 py-2 rounded-full bg-black text-white text-sm">全部</button>
                <button onclick="loadProducts('电子产品')" class="px-4 py-2 rounded-full bg-white border text-sm">电子产品</button>
                <button onclick="loadProducts('学习资料')" class="px-4 py-2 rounded-full bg-white border text-sm">学习资料</button>
            </div>
        </header>

        <div id="product-grid" class="grid grid-cols-1 md:grid-cols-3 gap-6">
            </div>
    </main>

    <script>
        // --- JavaScript 核心逻辑：连接 Python ---

        // 1. 调用 Python 获取商品
        async function loadProducts(cat) {
            const grid = document.getElementById('product-grid');
            grid.innerHTML = '<div class="col-span-3 text-center py-20 text-gray-400">正在查询数据库...</div>';

            try {
                const response = await fetch(`/api/products?category=${cat}`);
                const data = await response.json();

                grid.innerHTML = data.map(p => `
                    <div class="apple-card bg-white p-6 border border-gray-100">
                        <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">${p.category}</span>
                        <h3 class="text-lg font-bold mt-1">${p.title}</h3>
                        <p class="text-gray-500 text-sm mt-2 h-10 overflow-hidden">${p.description}</p>
                        <div class="flex justify-between items-center mt-6">
                            <span class="text-xl font-semibold">¥${p.price}</span>
                            <button onclick="handleBuy(${p.product_id})" 
                                    class="bg-blue-600 text-white px-4 py-2 rounded-full text-sm hover:bg-blue-700 active:scale-95 transition">
                                购买
                            </button>
                        </div>
                    </div>
                `).join('');

                if(data.length === 0) grid.innerHTML = '<div class="col-span-3 text-center py-20">该类目下暂无商品</div>';
            } catch (err) {
                grid.innerHTML = '<div class="col-span-3 text-red-500 text-center">无法连接 Python 服务，请检查后端是否运行</div>';
            }
        }

        // 2. 调用 Python 执行购买
        async function handleBuy(productId) {
            if(!confirm('确认从 SQL Server 扣减该库存并生成订单吗？')) return;

            const res = await fetch('/api/buy', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ product_id: productId })
            });
            const result = await res.json();

            if(result.status === 'success') {
                alert('交易成功！已同步更新数据库。');
                loadProducts('全部'); // 刷新列表
            }
        }

        // 初始化加载
        window.onload = () => loadProducts('全部');
    </script>
</body>
</html>
"""


# --- 3. UI 启动包装类 ---

class UIModule:
    def __init__(self, db_manager):
        global db_instance
        db_instance = db_manager

        # 在子线程启动 Flask 避免阻塞
        server_thread = threading.Thread(target=self._run_server, daemon=True)
        server_thread.start()

        print(f"\\n[系统信息] Python 3.12 Web 服务器已就绪")
        print(f"[访问地址] http://127.0.0.1:5000")

        # 自动打开浏览器
        webbrowser.open("http://127.0.0.1:5000")

    def _run_server(self):
        # 运行 Flask
        app.run(port=5000, debug=False, use_reloader=False)

    @app.route('/')
    def serve_index(self):
        return render_template_string(HTML_UI)