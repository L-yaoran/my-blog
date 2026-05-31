title: 用 Flask 搭建这个博客
date: 2026-05-26
badge: 项目实践
summary: 介绍如何使用 Flask + Flask-FlatPages 搭建一个轻量级个人博客，无需数据库。

## 为什么要用 Flask？

学了 Python 基础之后，我一直想做一个能真正在浏览器里看到的东西。Flask 是 Python 的一个轻量级 Web 框架，非常适合初学者。

### 为什么不用数据库？

很多博客教程都会教你用数据库存储文章，但对于一个个人博客来说，**Markdown 文件 + Flask-FlatPages** 是更好的选择：

- 文章就是 `.md` 文件，用任何编辑器都能写
- 不需要配置数据库
- 版本管理方便（可以用 Git 追踪文章变化）
- 备份简单 —— 复制文件夹就行

### 核心代码

整个应用的核心只有几十行代码：

```python
from flask import Flask, render_template
from flask_flatpages import FlatPages

app = Flask(__name__)
app.config['FLATPAGES_ROOT'] = 'content'
app.config['FLATPAGES_EXTENSION'] = '.md'
pages = FlatPages(app)


def get_posts():
    posts = [p for p in pages if p.meta.get('date')]
    posts.sort(key=lambda p: p.meta['date'], reverse=True)
    return posts


@app.route('/')
def index():
    return render_template('index.html', posts=get_posts())
```

### 部署到公网

写完代码之后，我把项目推送到 GitHub，然后在 Render.com 上创建了一个免费的 Web Service。Render 会自动检测 Python 项目并部署，几分钟后就能通过公网 URL 访问了。

这就是你正在浏览的网站！从零开始搭建一个真正能访问的网站，这种感觉真的很棒。
