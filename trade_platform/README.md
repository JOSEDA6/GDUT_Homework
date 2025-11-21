
# 校园交易平台

> 一个面向大学生社群的简单交易平台，使用 Python 和 SQL Server 构建

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-2022-green.svg)](https://www.microsoft.com/sql-server)

## 项目简介

校园交易平台是一个为大学生设计的二手商品交易系统，支持商品发布、浏览、搜索、购买等功能。采用控制台界面，简洁易用，适合课程设计或学习Python数据库编程 。

**主要功能：**
- 用户注册与登录系统
- 商品分类管理（电子产品、学习资料、生活用品等）
- 商品发布与搜索
- 在线交易与订单管理
- 用户信用评分与积分系统
- 个性化商品推荐

## 功能特点

- 🏪 **商品管理**：支持商品发布、编辑、下架
- 🔍 **智能搜索**：按关键词搜索商品
- 📊 **分类浏览**：按分类查看商品列表
- 👤 **用户系统**：完整的用户注册、登录、资料管理
- 💳 **交易系统**：完整的购买流程和订单管理
- ⭐ **信用体系**：用户信用评分和积分奖励机制
- 🎯 **智能推荐**：基于用户行为的商品推荐

## 快速开始

### 环境要求

- Python 3.8+
- SQL Server 2012+
- Windows/Linux/macOS

### 安装步骤

1. **克隆项目**
   bash
   git clone https://github.com/yourusername/campus-trade-platform.git
   cd campus-trade-platform


2. **创建虚拟环境（推荐）**
   bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate


3. **安装依赖**
   bash
   pip install -r requirements.txt


4. **数据库配置**
   - 确保 SQL Server 服务正在运行
   - 修改 `config.py` 中的数据库连接信息：
   python
   DB_CONFIG = {
       'server': '你的服务器名称\\SQL实例名',
       'database': 'campus_trade',
       'user': 'sa',
       'password': '你的密码',
       'driver': 'ODBC Driver 17 for SQL Server'
   }


5. **初始化数据库**
   bash
   python init_database.py


6. **运行程序**
   bash
   python main.py


## 使用说明

### 首次运行

1. 程序启动后，将显示登录/注册菜单
2. 选择注册新账户或使用测试账户：
   - 用户名: `admin`，密码: `123456`（管理员账户）
   - 用户名: `student1`，密码: `123456`（普通用户）
   - 用户名: `施乔`，密码: `123456`（测试账户）

### 主要功能操作

**浏览商品**
- 在主菜单中选择"浏览商品"
- 按分类查看商品列表
- 选择商品查看详情并购买

**发布商品**
- 登录后选择"发布商品"
- 填写商品信息（标题、描述、价格、分类）
- 发布成功后获得积分奖励

**搜索商品**
- 使用关键词搜索商品
- 支持标题和描述模糊搜索

**订单管理**
- 查看"我的订单"
- 区分"我购买的"和"我出售的"订单

## 项目结构


trade_platform/
├── main.py                 # 主程序入口
├── database.py             # 数据库连接管理
├── customer_module.py      # 用户管理模块
├── classification_module.py # 商品分类管理
├── member_module.py        # 会员积分管理
├── target_module.py        # 推荐系统模块
├── ui_module.py           # 用户界面模块
├── config.py              # 配置文件
├── init_database.py       # 数据库初始化脚本
├── requirements.txt       # 项目依赖
└── README.md              # 项目说明文档


## 数据库设计

项目使用 SQL Server 数据库，包含以下主要表结构：

- **users**：用户信息表（用户ID、用户名、密码、邮箱、信用分等）
- **products**：商品信息表（商品ID、标题、描述、价格、分类等）
- **orders**：订单表（订单ID、商品ID、买家ID、卖家ID、金额等）
- **credit_logs**：信用日志表
- **points_logs**：积分日志表

## 依赖管理

项目使用 `requirements.txt` 管理依赖，当前版本依赖：
- `pyodbc==4.0.39`：SQL Server 数据库连接驱动

生成依赖文件的方法：
bash
生成精确的项目依赖（推荐）

pip install pipreqs
pipreqs ./ --encoding=utf8 --force

或生成当前环境所有包

pip freeze > requirements.txt
 

## 常见问题

### Q: 数据库连接失败怎么办？
A: 检查 SQL Server 服务是否启动，确认 config.py 中的连接信息正确。

### Q: 初始化数据库时出现权限错误？
A: 确保使用有足够权限的数据库账户，或使用 Windows 身份验证。

### Q: 运行时报错找不到模块？
A: 确保已安装所有依赖：`pip install -r requirements.txt`

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建功能分支：`git checkout -b feature/新功能`
3. 提交更改：`git commit -am '添加新功能'`
4. 推送分支：`git push origin feature/新功能`
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

- 项目维护者：施乔
- 学号：3122009224
- 邮箱：3122009224.@gdut.edu.cn

---

**提示**：本项目为课程设计作品，主要用于学习 Python 数据库编程和软件开发流程 。

