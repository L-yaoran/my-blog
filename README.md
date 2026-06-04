# AI幻世录·GeoLib — 个人博客与交互练习平台

> 用代码构建 · 用文字记录 · 用实践验证  
> 一个与 AI 共进化的开发者，记录技术探索与项目实践的个人网站。

**线上地址：** [https://829007.xyz](https://829007.xyz) | [https://geolib.top](https://geolib.top)

---

## 目录

- [项目概述](#项目概述)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
  - [本地运行](#本地运行)
  - [部署到服务器](#部署到服务器)
- [功能详解](#功能详解)
  - [首页（Hub）](#首页hub)
  - [博客文章](#博客文章)
  - [交互式练习](#交互式练习)
  - [做题记录与进度暂存](#做题记录与进度暂存)
  - [关于·联系](#关于联系)
- [内容管理](#内容管理)
  - [添加博客文章](#添加博客文章)
  - [添加练习页面](#添加练习页面)
- [部署架构](#部署架构)
  - [阿里云 ECS 部署](#阿里云-ecs-部署)
  - [Nginx 配置](#nginx-配置)
  - [SSL 证书](#ssl-证书)
- [技术设计](#技术设计)
  - [前端架构](#前端架构)
  - [练习引擎架构](#练习引擎架构)
  - [Bauhaus 设计风格](#bauhaus-设计风格)
- [API 参考](#api-参考)
- [常见问题](#常见问题)
- [许可证](#许可证)

---

## 项目概述

AI幻世录·GeoLib 是一个轻量级个人技术博客，兼具交互式编程练习功能。它使用 **Flask** + **Flask-FlatPages** 驱动，内容以 Markdown 存储，无需数据库。前端采用 **Bauhaus（包豪斯）** 设计风格，浅色主题，注重排版与几何构成感。

项目亮点：

- 📝 **Markdown 写作** — 博文用 Markdown 撰写，支持表格、代码高亮
- 🎯 **交互式 Python 练习** — 6 套练习页面，含选择题/填空题/简答题/代码实操
- 📊 **自动评分与做题记录** — 提交后自动打分，历史记录可回溯加载
- 💾 **进度暂存与恢复** — 手动存档 + 提交自动存档，支持恢复
- 🎨 **Bauhaus 风格 UI** — 几何装饰、无衬线字体、蓝紫金配色
- 🌐 **HTTPS 公网部署** — 阿里云 ECS + Nginx + Let's Encrypt SSL

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端框架** | Flask 3.1.0 | Python Web 框架 |
| **内容管理** | Flask-FlatPages 0.7.3 | Markdown 驱动的无数据库 CMS |
| **模板引擎** | Jinja2 | 服务器端模板渲染 |
| **Markdown** | Python-Markdown 3.7 | 支持 tables、fenced_code、codehilite 扩展 |
| **前端样式** | 自定义 CSS（Bauhaus 主题） | 浅色配色 + 几何装饰 + 响应式布局 |
| **前端交互** | 原生 JavaScript | 练习引擎、题目评分、暂存/加载、代码高亮 |
| **生产服务器** | Gunicorn 23.0.0 | WSGI HTTP 服务器 |
| **反向代理** | Nginx | 静态文件服务 + SSL 终端 |
| **SSL 证书** | Let's Encrypt (Certbot) | 自动续签 |
| **云服务器** | 阿里云 ECS | Ubuntu / CentOS |
| **域名** | 829007.xyz / geolib.top | Cloudflare DNS，Spaceship 注册 |

---

## 项目结构

```
my_blog/
├── app.py                          # Flask 应用入口（路由 + FlatPages 配置）
├── requirements.txt                # Python 依赖
├── Procfile                        # Render 部署进程声明
├── render.yaml                     # Render 部署配置（备用）
├── runtime.txt                     # Python 版本声明（3.13.0）
├── .gitignore                      # Git 忽略规则
├── README.md                       # 本文件
│
├── content/                        # Markdown 博客文章
│   ├── learning-python.md          #   Python OOP 面向对象编程完全解析
│   ├── my-first-flask-app.md       #   用 Flask 搭建这个博客
│   └── ollama-guide.md             #   Ollama 完全指南：大模型私有化部署
│
├── templates/                      # Jinja2 模板
│   ├── base.html                   #   博客公共模板（导航栏 + 页脚）
│   ├── hub.html                    #   首页门户（博客卡片 + 练习卡片 + 关于）
│   ├── post.html                   #   文章详情页
│   ├── about.html                  #   关于页面
│   └── 404.html                    #   404 错误页
│
├── static/
│   ├── css/
│   │   ├── style.css               #   博客公共样式（Bauhaus 浅色主题）
│   │   └── quiz.css                #   练习页面公共样式
│   │
│   ├── js/
│   │   ├── main.js                 #   博客导航交互（汉堡菜单）
│   │   └── quiz-engine.js          #   练习引擎（评分/暂存/历史/高亮，共用）
│   │
│   ├── images/ollama/              #   Ollama 文章配图（36 张）
│   │
│   └── python_basic_test_001.html  #   练习 001 — 类与对象（38 题）
│       python_basic_test_002.html  #   练习 002 — 继承/多态（38 题）
│       python_basic_test_003.html  #   练习 003 — 闭包/装饰器（34 题）
│       python_basic_test_004.html  #   练习 004 — 网络编程/多进程（33 题）
│       python_basic_test_005.html  #   练习 005 — 线程/生成器/协程（34 题）
│       python_basic_test_006.html  #   练习 006 — 线程/锁/GIL 补充（32 题）
│       python_basic_test_007.html  #   练习 007 — 正则表达式/MySQL（38 题）
│       python_basic_test_008.html  #   练习 008 — 正则/MySQL 补充（32 题）
│       python_basic_test_009.html  #   练习 009 — 正则/MySQL 综合（30 题）
│
└── 回收站/                         # 废弃文件暂存，不参与运行
```

---

## 快速开始

### 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/L-yaoran/my-blog.git
cd my-blog

# 2. 安装依赖
pip install -r requirements.txt
# 或手动安装：
pip install flask==3.1.0 flask-flatpages==0.7.3 markdown==3.7 gunicorn==23.0.0

# 3. 启动开发服务器
python app.py

# 4. 在浏览器打开
# http://127.0.0.1:5000
```

开发模式默认开启 `debug=True`，支持热重载。

### 部署到服务器

#### 简单部署（Gunicorn + 后台运行）

```bash
# 生产环境启动
cd /path/to/my_blog
gunicorn -w 4 -b 127.0.0.1:8000 app:app --daemon

# 查看进程
ps aux | grep gunicorn

# 重新启动
pkill -f gunicorn
sleep 1
gunicorn -w 4 -b 127.0.0.1:8000 app:app --daemon
```

#### Nginx 反向代理配置

```nginx
server {
    server_name 829007.xyz www.829007.xyz;

    location /static {
        alias /var/www/my_blog/static;
        expires 1h;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 10m;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/829007.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/829007.xyz/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    listen 80;
    server_name 829007.xyz www.829007.xyz;
    return 301 https://$host$request_uri;
}
```

#### Certbot SSL 自动续签

```bash
certbot --nginx -d 829007.xyz -d www.829007.xyz
# 证书自动续期，无需手动干预
```

---

## 功能详解

### 首页（Hub）

主页是一个**单页式门户**，包含五大板块：

1. **个人 Hero** — 自我介绍、标语、技术标签
2. **最新·博客** — 动态从 `content/` 目录读取 Markdown 文章，按日期排序展示
3. **学习·练习** — 交互式 Python 练习卡片网格，最新练习排列在前
4. **实践·项目** — 项目作品展示
5. **关于·联系** — 个人简介、技术架构说明、联系方式（邮箱/QQ/微信）

首页不继承 `base.html`，拥有独立的导航栏和页脚布局。

### 博客文章

博客内容使用 **Flask-FlatPages** 管理，每篇文章是一个带 YAML 头的 Markdown 文件。

**文章元数据格式：**

```yaml
title: 文章标题
date: 2026-05-28
badge: 私有化部署    # 可选，首页卡片标签
summary: 文章摘要，显示在首页卡片上

文章正文使用 Markdown 编写...
```

支持 Markdown 扩展：
- **tables** — 表格渲染
- **fenced_code** — 围栏代码块
- **codehilite** — 代码语法高亮（需安装 Pygments）

路由规则：
- `/` — 首页
- `/<slug>/` — 文章详情（slug 对应 content/ 中的文件名，不含扩展名）
- `/about` — 关于页面

### 交互式练习

6 套 Python 练习页面，每套包含四种题型：

| 题型 | 标签色 | 评分方式 | 说明 |
|------|--------|---------|------|
| 单选题 | 蓝色 | 自动评分 | 四选一，点击选择 |
| 填空题 | 金色 | 自动评分 | 输入答案，支持模糊匹配 |
| 简答题 | 绿色 | 主观题（自行核对） | 文本框输入，点击查看参考答案 |
| 代码实操 | 紫色 | 主观题（自行核对） | 代码编辑器，Tab 缩进，查看参考代码 |

所有练习页共用 `static/js/quiz-engine.js` 引擎，功能包括：

- **自动评分** — 客观题自动批改，标记对错并显示解析
- **得分统计** — 顶部实时显示客观题/主观题完成数
- **做题记录** — 每次提交自动保存到 localStorage，可查看详细答题情况
- **进度暂存** — 手动命名存档，可恢复继续做题
- **代码高亮** — Python 关键词/字符串/注释/数字等语法高亮（服务端预生成）
- **练习导航** — 左右箭头切换练习，下拉菜单跳转

**页面间导航：** 每个练习页顶部有导航栏，支持「◂ 上一练习 | 下拉菜单选择 | 下一练习 ▸」。当前共 9 套练习：001 → 002 → 003 → 004 → 005 → 006 → 007 → 008 → 009。

### 做题记录与进度暂存

| 功能 | 说明 |
|------|------|
| **暂存进度** | 填写任意名称，保存当前所有已填答案到浏览器 localStorage |
| **加载进度** | 从已保存的存档列表中选择恢复，支持按编号或名称查找 |
| **提交自动存档** | 每次提交答案后自动生成存档（命名：`提交 HH:MM — 得分 X/Y`） |
| **做题记录** | 查看每次提交的历史记录：时间、得分、每题答案详情 |
| **从记录恢复** | 在历史详情中点击「加载此答案到页面」，可将当时的答案恢复到页面 |

数据存储在每个练习页独立的 localStorage key 中（`py_day0X_quiz_history` 和 `py_day0X_saves`），互不干扰。

### 关于·联系

- **关于我** — 个人介绍、技术理念
- **关于本站** — 技术架构速览
- **联系** — 邮箱、QQ、微信（带品牌色图标）

---

## 内容管理

### 添加博客文章

在 `content/` 目录下新建 `.md` 文件，添加 YAML 头即可：

```markdown
title: 新文章标题
date: 2026-06-01
badge: 技术文章    # 可选：首页卡片标签
summary: 文章摘要文字，显示在首页卡片上

文章正文...
```

首页会自动在「最新·博客」板块显示新文章卡片，按日期降序排列。

### 添加练习页面

1. 在 `static/` 下创建 `python_basic_test_00X.html`
2. 引入公用 CSS/JS：
   ```html
   <link rel="stylesheet" href="/static/css/quiz.css">
   <script>
   const STORAGE_KEY = 'py_day0X_quiz_history';
   const SAVE_KEY = 'py_day0X_saves';
   </script>
   <script src="/static/js/quiz-engine.js"></script>
   ```
3. 按照 001-005 的格式编写题目卡片 HTML（选择题/填空题/简答题/代码实操）
4. 更新 `templates/hub.html` 的练习区卡片，添加新练习条目
5. 更新所有练习页面的导航下拉菜单

---

## 部署架构

### 阿里云 ECS 部署

```
用户 → HTTPS → Nginx (443) → Gunicorn (8000) → Flask App
                         ↘ 静态文件 (/static/)
```

| 组件 | 配置 |
|------|------|
| 服务器 | 阿里云 ECS，1vCPU / 2GB |
| Web 服务器 | Nginx，反向代理 + 静态文件服务 |
| WSGI | Gunicorn，4 workers |
| 应用 | Flask 开发服务器仅用于本地调试 |
| SSL | Let's Encrypt，Certbot 自动续签 |
| 域名 | 829007.xyz（主），geolib.top（备用） |

### Nginx 配置

静态文件缓存 1 小时，动态请求转发到 Gunicorn。详见上方「Nginx 反向代理配置」。

### SSL 证书

通过 Certbot 自动申请和续签 Let's Encrypt 证书，每 90 天自动更新。

---

## 技术设计

### 前端架构

| 页面类型 | 样式来源 | JS 来源 | 模板继承 |
|---------|---------|---------|---------|
| 首页 (hub.html) | 内联 `<style>` | 无 | 独立页面 |
| 博客列表 (index.html) | style.css | main.js | 继承 base.html |
| 文章详情 (post.html) | style.css | main.js | 继承 base.html |
| 关于 (about.html) | style.css | main.js | 继承 base.html |
| 练习页面 | quiz.css | quiz-engine.js | 独立页面 |

### 练习引擎架构

`quiz-engine.js` 是 6 个练习页面的公用 JS 引擎，包含：

- **评分引擎** — `submitAll()` 遍历所有 `.card`，根据 `data-type` 和 `data-answer` 属性评分
- **进度管理** — `collectAnswers()` / `restoreAnswers()` 序列化/反序列化答题状态
- **存储层** — 使用 `localStorage`，每个练习独立 key
- **历史管理** — `saveRecord()` / `renderHistory()` / `showHistoryDetail()`
- **UI 组件** — `showToast()` 消息提示、`toggleDropdown()` 下拉菜单、`updateProgress()` 实时统计
- **辅助函数** — `normalize()` 模糊匹配、`toggleRef()` 参考答案显隐

每个练习页只需定义 `STORAGE_KEY` 和 `SAVE_KEY` 即可接入引擎。

### Bauhaus 设计风格

| 元素 | 说明 |
|------|------|
| **配色** | 蓝 `#2563eb`、紫 `#7c3aed`、金 `#d97706`、绿 `#059669` |
| **背景** | 浅灰 `#faf9f8`，白色卡片 `#ffffff` |
| **几何装饰** | 右侧大圆形描边、左下角模糊圆（CSS 伪元素） |
| **字体** | `system-ui` 无衬线字体，等宽字体用于代码 |
| **卡片** | 大圆角 `1.5rem`、柔和阴影 `box-shadow: 0 4px 12px rgba(0,0,0,0.04)` |
| **导航** | 毛玻璃效果 `backdrop-filter: blur(8px)`、渐变品牌文字 |
| **标题** | 蓝色左边框 `border-left: 5px solid var(--blue)` |
| **响应式** | 768px / 600px / 400px 三个断点 |

---

## API 参考

Flask 应用路由：

| 方法 | 路由 | 模板 | 说明 |
|------|------|------|------|
| GET | `/` | hub.html | 首页门户 |
| GET | `/hub` | hub.html | 同首页 |
| GET | `/<slug>/` | post.html | 文章详情 |
| GET | `/about` | about.html | 关于页面 |
| * | `*` | 404.html | 404 错误页 |

静态文件通过 `/static/<path>` 直接访问，无需经过 Flask 路由（由 Nginx 直接服务）。

---

## 常见问题

**Q: 为什么首页的博客卡片不是自动更新的？**

A: 首页的博客卡片区现在是动态的——从 `content/` 目录读取所有带 `date` 元数据的 Markdown 文件，按日期降序展示。添加新文章到 `content/` 后会自动显示。

**Q: 练习进度存在哪里？**

A: 浏览器的 `localStorage` 中，每个练习有独立的 key：`py_day0X_quiz_history`（提交记录）和 `py_day0X_saves`（存档数据）。清除浏览器缓存会丢失进度。

**Q: 如何修改 CSS？**

A: 博客样式在 `static/css/style.css`，练习样式在 `static/css/quiz.css`。修改 CSS 后清空浏览器缓存（Ctrl+Shift+R）查看效果。

**Q: 如何更新 SSL 证书？**

A: Let's Encrypt 证书自动续签。如需手动刷新，执行 `certbot renew`。

**Q: 如何添加新的练习页面？**

A: 在 `static/` 下创建 HTML 文件，引入 `quiz.css` 和 `quiz-engine.js`，按照现有页面格式填写题目数据。更新 `templates/hub.html` 添加卡片。

---

## 许可证

MIT License © 2026 [明屿 (Geoff)](https://github.com/L-yaoran)

本项目为个人学习项目，代码仅供学习参考。
