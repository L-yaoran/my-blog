title: 从零搭建 Flask 博客：架构、部署与设计思路
date: 2026-05-26
badge: 项目实践
summary: 详述如何用 Flask + Flask-FlatPages 从零构建一个无数据库的轻量级博客，包含模板继承、Markdown 文章管理、样式设计、生产部署等完整流程。

## 为什么要自己搭博客

市面上有太多博客平台——CSDN、掘金、知乎。但它们有几个共同的问题：

- 文章归平台管，不归你管
- 样式受平台限制，无法自定义
- 发布流程繁琐，登录才能写

对于一个写技术文章的人来说，**自己的服务器、自己写的样式、自己管理的文章**，才是真正可控的。更重要的是，搭建过程本身就是一次完整的 Web 开发实践。

## 技术选型：为什么是 Flask + Markdown

Web 框架的选择：

| 框架 | 重量 | 适合场景 |
|------|------|---------|
| Django | 重，ORM/Admin/模板全自带 | 中大型项目，需要数据库 |
| FastAPI | 轻，ASGI | API 服务，即时响应 |
| Flask | 轻，灵活可扩展 | 中小型 Web 应用 |
| Next.js | 重，SSR/静态生成 | 静态内容为主 |

最终选择 **Flask**，理由是：足够轻量、生态成熟、有 Blueprints 扩展性。

内容管理有两个选择：

- **数据库存储文章** — 需要设计表结构、ORM 映射，写文章要登录后台
- **Markdown 文件** — 直接用编辑器写，Git 版本跟踪，备份就是复制文件夹

我选择 **Flask-FlatPages**，它让 Markdown 文件直接变成动态路由。写文章 = 写 `.md` 文件放到 `content/` 目录，无需任何后台操作。

## 项目结构

```
my_blog/
├── app.py              # Flask 应用入口，路由 + 配置
├── content/             # Markdown 文章目录（Flask-FlatPages 读取）
│   ├── my-first-flask-app.md
│   └── ollama-guide.md
├── templates/           # Jinja2 模板
│   ├── base.html       # 公共模板（导航栏 + 页脚）
│   ├── hub.html       # 首页
│   ├── post.html      # 文章详情页
│   ├── about.html      # 关于页
│   └── 404.html
├── static/            # 静态资源（Nginx 直出，不经过 Flask）
│   ├── css/style.css   # 博客样式
│   └── js/main.js     # 导航交互
└── requirements.txt
```

**动静分离是核心设计。** Nginx 直接服务 `/static/` 下的静态文件，Flask 只负责模板渲染和博客路由。

## 核心代码：不到 50 行

整个博客的核心代码非常少：

```python
from flask import Flask, render_template
from flask_flatpages import FlatPages
from datetime import datetime

app = Flask(__name__)
app.config['FLATPAGES_ROOT'] = 'content'
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['tables', 'fenced_code', 'codehilite']
pages = FlatPages(app)

def get_posts():
    posts = [p for p in pages if p.meta.get('date')]
    posts.sort(key=lambda p: p.meta['date'], reverse=True)
    return posts

@app.route('/')
def index():
    return render_template('hub.html', posts=get_posts())

@app.route('/<path:slug>/')
def post(slug):
    article = pages.get_or_404(slug)
    return render_template('post.html', post=article)
```

Flask-FlatPages 自动扫描 `content/` 目录下的 `.md` 文件，文件名（不含扩展名）即路由 slug。Markdown 中的 YAML 头自动解析为 `meta` 字典。

## 模板继承：base.html 的设计

博客所有页面的公共部分（导航栏、页脚、CSS 引用）统一放在 `base.html`：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AI幻世录{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar">...</nav>
    <main>{% block content %}{% endblock %}</main>
    <footer class="footer">...</footer>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

其他模板继承 `base.html`，只需替换 `{% block title %}` 和 `{% block content %}`：

```html
{% extends "base.html" %}

{% block title %}文章标题 — AI幻世录{% endblock %}

{% block content %}
<article>
    {{ post.body }}   <!-- Flask-FlatPages 渲染后的 HTML
</article>
{% endblock %}
```

这样导航栏改一次，全站生效。

## Markdown 文章的格式

文章是一个带 YAML 头的 Markdown 文件：

```markdown
title: Django vs Flask，我选 Flask
date: 2026-05-20
badge: 技术对比
summary: 两个主流 Python 框架的对比，以及我的选型理由。

## 正文开始了

Django 是一个**全功能**框架...
```

`date` 和 `summary` 是自定义字段，在首页文章卡片里展示。`badge` 是卡片的标签颜色。

Flask-FlatPages 支持 Markdown 扩展：`tables` 渲染表格，`fenced_code` 支持围栏代码块，`codehilite` 语法高亮（需要安装 Pygments）。

## 样式设计：包豪斯风格

设计原则：**简单、留白、几何感**。

配色来自包豪斯运动的三原色：

```css
:root {
    --blue: #2563eb;
    --purple: #7c3aed;
    --gold: #d97706;
    --green: #059669;
    --void: #faf9f8;
}
```

页面背景是 `#faf9f8`（暖白），正文 `#1a1a1a`（近黑），装饰元素用蓝/紫/金三色点缀。

响应式布局用 CSS Grid + Flexbox，三档断点：

```css
@media (max-width: 768px) { /* 平板 */ }
@media (max-width: 600px) { /* 手机导航收起 */ }
@media (max-width: 400px) { /* 小屏进一步调整 */ }
```

导航栏用 `position: fixed` 固定在顶部，配合 `backdrop-filter: blur(8px)` 毛玻璃效果。

## 生产部署：Gunicorn + Nginx

本地开发用 Flask 自带的 debug 服务器：

```bash
python app.py   # 自动热重载，:5000 端口
```

生产环境用 Gunicorn 管理多个 worker：

```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app --daemon
```

`-w 4` 启动 4 个 worker 进程，处理并发请求。`-b 127.0.0.1:8000` 绑定本地端口，Nginx 在 80/443 端口接收外部请求后转发给 Gunicorn。

Nginx 配置核心逻辑：

```nginx
server {
    listen 80;
    server_name 829007.xyz;

    # 静态文件直接服务，不走 Flask
    location /static/ {
        alias /var/www/my_blog/static/;
        expires 1h;      # 浏览器缓存 1 小时
    }

    # 动态请求转发给 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**动静分离的意义**：Nginx 处理静态文件效率极高（epoll 多路复用），无需经过 Python 进程；Flask 只处理模板渲染，最大化利用 Python 的模板渲染能力。

## SEO 与可发现性

博客上线后，需要让搜索引擎收录。做了这几件事：

1. **语义化 HTML** — `<article>`、`<nav>`、`<main>`、`<footer>` 代替 `<div>`
2. **sitemap.xml** — 主动提交所有页面 URL 给搜索引擎
3. **robots.txt** — 允许爬虫抓取
4. **响应式设计** — 移动端可读，Google 会降权移动不友好的站点
5. **页面标题** — 每篇文章有独立 `<title>`，不重复

```xml
<!-- sitemap.xml -->
<url>
    <loc>https://829007.xyz/my-first-flask-app/</loc>
    <changefreq>monthly</changefreq>
</url>
```

## 总结

从零搭建一个个人博客，本质上是一次**前端 + 后端 + 部署**的完整链路练习。

这套架构的核心优势是**简单可维护**：
- 文章就是 Markdown，Git 管理版本
- 样式全部自定义，不受平台限制
- 动静分离，Nginx 直出静态，Gunicorn 只处理动态
- 无数据库，备份就是复制文件夹

如果你也想拥有自己的技术博客，希望这篇文章提供了从选型到上线的完整思路。