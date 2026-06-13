# AI幻世录·GeoLib — 个人博客与交互练习平台

> 用代码构建 · 用文字记录 · 用实践验证  
> 一个与 AI 共进化的开发者，记录技术探索与项目实践的个人网站。

**线上地址：** [https://829007.xyz](https://829007.xyz)

---

## 目录

- [项目概述](#项目概述)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [功能详解](#功能详解)
- [内容管理](#内容管理)
- [部署架构](#部署架构)
- [技术设计](#技术设计)
- [API 参考](#api-参考)
- [许可证](#许可证)

---

## 项目概述

AI幻世录·GeoLib 是一个轻量级个人技术博客，兼具交互式编程练习功能。使用 **Flask** + **Flask-FlatPages** 驱动，内容以 Markdown 存储，无需数据库。

项目亮点：

- 📝 **Markdown 写作** — 博文用 Markdown 撰写，支持表格、代码高亮
- 🎯 **16 套 LLM 交互练习** — 570+ 道题，选择题/填空题/简答题/代码实操
- 📊 **自动评分与做题记录** — 提交后自动打分，历史记录可回溯
- 💾 **进度暂存与恢复** — 手动存档 + 自动存档，支持导入/导出
- 🎨 **深色/浅色模式** — 全站支持主题切换，跟随系统偏好
- 🔧 **统一模板生成** — 骨架模板 + 生成脚本，新增练习只需写题目数据

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端框架** | Flask | Python Web 框架 |
| **内容管理** | Flask-FlatPages | Markdown 驱动的无数据库 CMS |
| **模板引擎** | Jinja2 | 服务器端模板渲染 |
| **Markdown** | Python-Markdown | 支持 tables、fenced_code、codehilite |
| **前端样式** | 自定义 CSS | 浅色/深色主题 + 响应式布局 |
| **前端交互** | 原生 JavaScript | 练习引擎、题目评分、暂存/加载 |
| **代码编辑** | CodeMirror（本地托管） | 代码实操题的编辑器 |
| **生产服务器** | Gunicorn | WSGI HTTP 服务器 |
| **反向代理** | Nginx | 静态文件服务 + SSL 终端 |
| **SSL 证书** | Let's Encrypt (Certbot) | 自动续签 |
| **云服务器** | 阿里云 ECS | 120.24.229.113 |
| **域名** | 829007.xyz | 备案号：湘ICP备2026020338号 |

---

## 项目结构

```
my_blog/
├── app.py                        # Flask 应用入口
├── requirements.txt              # Python 依赖
├── CLAUDE.md                     # Claude Code 项目指引
├── CHANGELOG.md                  # 更新日志
├── README.md                     # 本文件
│
├── content/                      # Markdown 博客文章（4 篇）
│   ├── learning-python.md
│   ├── my-first-flask-app.md
│   ├── ollama-guide.md
│   └── interactive-python-quiz-platform.md
│
├── templates/                    # Jinja2 模板
│   ├── base.html                 #   公共模板（导航栏 + 页脚 + 主题切换）
│   ├── hub.html                  #   首页（继承 base.html）
│   ├── post.html                 #   文章详情页
│   ├── quiz.html                 #   练习页 Jinja2 模板（Flask 路由用）
│   ├── about.html                #   关于页面
│   └── 404.html                  #   404 错误页
│
├── static/
│   ├── css/
│   │   ├── variables.css         #   共享 CSS 变量（蓝/紫/金/绿配色）
│   │   ├── style.css             #   博客样式 + 深色模式
│   │   └── quiz.css              #   练习页样式 + 深色模式
│   │
│   ├── js/
│   │   ├── main.js               #   导航交互 + 主题切换逻辑
│   │   ├── quiz-engine.js        #   练习引擎（16 个页面共用）
│   │   └── codemirror/           #   CodeMirror 本地文件（~170KB）
│   │
│   ├── images/ollama/            #   Ollama 文章配图
│   │
│   └── python_basic_test_001~016.html  # 16 套静态练习页
│
├── scripts/                      # 生成与维护脚本
│   ├── quiz_template.html        #   骨架模板（唯一维护点）
│   ├── quiz_meta.py              #   练习元数据（16 条）
│   ├── quiz_data_001~016.py      #   题目数据（每套一个文件）
│   ├── generate_quiz.py          #   统一生成脚本
│   ├── update_navs.py            #   批量导航更新
│   └── fix_789_highlight.py      #   代码高亮修复
│
├── data/
│   └── quiz_001.json             # Flask 路由用（仅 001）
│
└── docs/specs/                   # 规划文档
    ├── v4-home-ia-spec.md        #   首页信息架构改版规划
    ├── v4.1-content-seo-spec.md  #   内容系统与 SEO 规划
    ├── v4.2-quiz-subsite-spec.md #   练习平台子站规划
    └── v5-ai-assistant-spec.md   #   AI 助手规划
```

---

## 快速开始

### 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/L-yaoran/my-blog.git
cd my-blog/my_blog

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动开发服务器
python app.py

# 4. 浏览器打开 http://127.0.0.1:5000
```

### 新增练习

```bash
# 1. 创建题目数据
#    scripts/quiz_data_0XX.py（choices/fills/shorts/writes）

# 2. 添加元数据
#    scripts/quiz_meta.py 中添加一条记录

# 3. 生成页面
cd my_blog/scripts
python generate_quiz.py 0XX

# 4. 更新所有页面导航
python update_navs.py

# 5. 修复代码高亮（如有参考答案代码块）
python fix_789_highlight.py

# 6. 更新主页卡片
#    编辑 templates/hub.html 添加新练习卡片
```

---

## 功能详解

### 首页（Hub）

主页是单页式门户，继承 `base.html`，包含四大板块：

1. **个人 Hero** — 自我介绍、标语、技术标签
2. **最新·博客** — 动态读取 `content/` 目录，按日期排序
3. **学习·练习** — 练习卡片网格（折叠/展开 + Tab 切换）
4. **实践·项目** — 项目作品展示
5. **关于·联系** — 个人简介、技术架构、联系方式

### 博客文章

使用 Flask-FlatPages 管理，每篇文章是带 YAML 头的 Markdown 文件：

```yaml
title: 文章标题
date: 2026-05-28
badge: 项目实践
summary: 文章摘要
```

支持 Markdown 扩展：tables、fenced_code、codehilite。

### 交互式练习

16 套 LLM 练习页面，每套包含四种题型：

| 题型 | 评分方式 | 说明 |
|------|---------|------|
| 单选题 | 自动评分 | 四选一，点击选择 |
| 填空题 | 自动评分 | contenteditable span，支持模糊匹配 |
| 简答题 | 主观核对 | 文本框输入，点击查看参考答案 |
| 代码实操 | 主观核对 | CodeMirror 编辑器，查看参考代码 |

所有练习页共用 `quiz-engine.js` 引擎，功能包括：

- **自动评分** — 客观题自动批改，标记对错并显示解析
- **做题记录** — 每次提交自动保存到 localStorage
- **进度暂存** — 手动命名存档，可恢复继续做题
- **导入/导出** — 支持 JSON 格式的做题数据导出和导入
- **代码高亮** — Python/SQL/Bash 语法高亮（服务端预生成）
- **深色模式** — 跟随系统或手动切换

### 练习清单

| 编号 | 主题 | 题量 | 来源 |
|------|------|------|------|
| 001 | 类与对象 | 38 | Phase1 Day01 |
| 002 | 继承/多态 | 38 | Phase1 Day02 |
| 003 | 闭包/装饰器 | 34 | Phase1 Day03 |
| 004 | 网络编程/多进程 | 33 | Phase1 Day04 |
| 005 | 线程/生成器/协程 | 34 | Phase1 Day05 |
| 006 | 线程/锁/GIL 补充 | 32 | Phase1 Day05 补充 |
| 007 | 正则表达式/MySQL | 38 | Phase1 Day06 |
| 008 | 正则/MySQL 补充 | 32 | Phase1 Day06 补充 |
| 009 | 正则/MySQL 综合 | 30 | Phase1 Day06 综合 |
| 010 | PyMySQL + Redis | 38 | Phase1 Day08 |
| 011 | NumPy/Pandas/Matplotlib | 38 | Phase1 Day09 |
| 012 | Linux 基础 | 38 | Phase1 Day10 |
| 013 | 提示词工程基础 | 38 | Phase2 Day01 |
| 014 | API 调用/链式提示 | 37 | Phase2 Day02 |
| 015 | 提示词技术选型/金融场景 | 37 | Phase2 Day03 |
| 016 | Coze 智能体开发 | 37 | Phase2 Day04 |

**共计 16 套练习，570+ 道题。**

---

## 内容管理

### 添加博客文章

在 `content/` 下新建 `.md` 文件，添加 YAML 头。首页会自动显示新文章。

### 添加练习页面

详见上方「新增练习」流程。核心原则：**只需写题目数据和元数据，运行脚本即可生成完整页面。**

---

## 部署架构

```
用户 → HTTPS → Nginx (443) → Gunicorn (8000) → Flask App
                     ↘ 静态文件 (/static/) 直出
```

| 组件 | 说明 |
|------|------|
| 服务器 | 阿里云 ECS，120.24.229.113 |
| Web 服务器 | Nginx，反向代理 + 静态文件服务 |
| WSGI | Gunicorn，绑定 127.0.0.1:8000 |
| SSL | Let's Encrypt，Certbot 自动续签 |
| 部署方式 | paramiko SFTP 上传 + SSH 重启服务 |
| 域名 | 829007.xyz |

**动静分离：** Nginx 直出静态文件（练习页、CSS、JS），Flask 只负责模板渲染。练习页修改后不需要重启服务。

---

## 技术设计

### 前端架构

| 页面类型 | 样式来源 | JS 来源 | 模板 |
|---------|---------|---------|------|
| 首页 | 内联 style | main.js | 继承 base.html |
| 文章详情 | style.css | main.js | 继承 base.html |
| 关于 | style.css | main.js | 继承 base.html |
| 练习页面 | quiz.css | quiz-engine.js | 独立静态 HTML |

### 练习引擎架构

`quiz-engine.js` 是 16 个练习页面的公用引擎（约 500 行），包含：

- **评分引擎** — `submitAll()` 遍历所有题目卡片评分
- **进度管理** — `collectAnswers()` / `restoreAnswers()` 序列化答题状态
- **存储层** — localStorage，每个练习独立 key
- **历史管理** — `saveRecord()` / `renderHistory()` / `showHistoryDetail()`
- **导入导出** — `exportProgress()` / `importProgress()` JSON 格式
- **主题切换** — `toggleTheme()` 深色/浅色模式
- **代码高亮** — Python 关键词/字符串/注释语法着色

### 统一模板系统

```
quiz_template.html（骨架模板）
       ↓
generate_quiz.py（读取 quiz_meta.py + quiz_data_XXX.py）
       ↓
python_basic_test_XXX.html（输出完整页面）
       ↓
update_navs.py（批量更新所有页面导航下拉菜单）
```

---

## API 参考

| 方法 | 路由 | 模板 | 说明 |
|------|------|------|------|
| GET | `/` | hub.html | 首页 |
| GET | `/hub` | hub.html | 同首页 |
| GET | `/practice/<quiz_id>/` | quiz.html | Flask 渲染练习页（仅 001） |
| GET | `/<slug>/` | post.html | 文章详情 |
| GET | `/about` | about.html | 关于页面 |
| GET | `/robots.txt` | — | robots 文件 |
| GET | `/sitemap.xml` | — | 站点地图（静态） |
| * | `*` | 404.html | 404 错误页 |

---

## 许可证

MIT License © 2026 [明屿 (Geoff)](https://github.com/L-yaoran)

本项目为个人学习项目，代码仅供学习参考。
