# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在本仓库中工作时提供指导。

## 语言要求

- 所有对话使用中文
- 所有文档使用中文
- 所有代码注释使用中文

## 执行要求

- 生成说明、总结、计划、提交说明时统一使用中文
- 新增或修改 Markdown 文档时统一使用中文
- 新增或修改代码注释时统一使用中文

---

## 项目概览

Flask 个人博客，部署于 https://829007.xyz，承载 9 套交互式 LLM 练习系统。无数据库；博客文章以 Markdown 文件存于 `content/`，由 Flask-FlatPages 管理。

---

## 常用命令

```bash
# 本地开发
cd my_blog
python app.py          # 启动 Flask 开发服务器，端口 5000

# 运行单元测试
cd my_blog
python -m unittest test_app

# 生成新的练习页面（从 Markdown 作业，脚本在 my_blog/scripts/）
cd my_blog/scripts
python gen007_clean.py   # 生成 python_basic_test_007.html（Day06 正则+MySQL）
python gen008.py         # 生成 python_basic_test_008.html（Day06 补充作业）
python gen009.py         # 生成 python_basic_test_009.html（Day06 正则表达式）

# 修复参考答案代码高亮
python fix_789_highlight.py  # 为 007/008/009 的参考代码添加语法高亮

# 部署到服务器
ssh root@120.24.229.113  # SSH 到服务器
nginx -s reload         # 重载 Nginx（CSS/JS 更新后清除缓存）
systemctl restart my_blog  # 重启 Gunicorn
```

---

## 架构说明

### 目录结构

```
VS_code/
├── my_blog/                    # Flask 应用（生产环境部署在 /var/www/my_blog）
│   ├── app.py                  # Flask 入口，路由 + FlatPages 配置
│   ├── content/                # Markdown 博客文章
│   │   ├── learning-python.md
│   │   ├── my-first-flask-app.md
│   │   ├── interactive-python-quiz-platform.md
│   │   └── ollama-guide.md
│   ├── templates/              # Jinja2 模板
│   │   ├── base.html           # 公共模板：导航栏 + 页脚 + CSS/JS 引用
│   │   ├── hub.html            # 首页（继承 base.html，内联样式）
│   │   ├── post.html           # 文章详情页
│   │   ├── about.html          # 关于页
│   │   ├── quiz.html           # 练习页模板（Jinja2 版，通过 Flask 路由渲染）
│   │   └── 404.html
│   ├── static/                 # 静态资源（Nginx 直出，不经过 Flask）
│   │   ├── css/
│   │   │   ├── variables.css   # 共享 CSS 变量（:root）
│   │   │   ├── style.css       # 博客样式（Bauhaus 浅色主题）
│   │   │   └── quiz.css        # 练习页样式
│   │   ├── js/
│   │   │   ├── main.js         # 导航栏交互（移动端 hamburger）
│   │   │   ├── quiz-engine.js  # 通用练习引擎（所有练习页共享）
│   │   │   └── codemirror/     # 本地 CodeMirror 文件（不用 CDN）
│   │   │       ├── codemirror.min.js      # ~170KB
│   │   │       ├── codemirror.min.css
│   │   │       ├── mode/python/python.min.js
│   │   │       └── theme/eclipse.min.css
│   │   └── python_basic_test_001~009.html  # 9 套练习页（静态 HTML）
│   ├── data/                   # 练习题配置数据（JSON）
│   │   └── quiz_001.json
│   ├── scripts/                # 生成/修复脚本
│   │   ├── gen007_clean.py     # 生成 007 练习页
│   │   ├── gen008.py           # 生成 008 练习页
│   │   ├── gen009.py           # 生成 009 练习页
│   │   ├── fix_789_highlight.py # 参考答案代码高亮修复
│   │   └── generate_day03~06.py # 早期生成脚本
│   ├── day_test_data_Markdown/ # 作业源数据
│   ├── test_app.py             # 单元测试
│   └── requirements.txt
└── coroutine-comic/            # 独立子项目（异步漫画阅读器）
```

### 动静分离

Nginx 直接服务 `/static/` 下的静态文件，Flask 只负责模板渲染和博客路由。练习页是纯静态 HTML，添加/修改练习不需要重启服务。

### 模板继承

所有页面继承 `base.html`，共享导航栏、页脚、CSS/JS 引用。`hub.html` 有自己的内联 `<style>` 块（不是用 `style.css`），修改首页样式时需两端同步。

### 练习页（静态 HTML + Flask 路由）

9 套练习页存在于 `static/`，由 Nginx 直接服务，不经过 Flask 路由：
- `python_basic_test_001.html` ~ `python_basic_test_009.html`

同时 `app.py` 提供了 `/practice/<quiz_id>/` 路由，可通过 Jinja2 模板 `quiz.html` 渲染练习页（目前仅 001 有 JSON 数据）。

每个练习页的 `<head>` 中引用：
```html
<link rel="stylesheet" href="/static/css/quiz.css?v=20260602">
<script src="/static/js/codemirror/codemirror.min.js?v=20260602"></script>
<script src="/static/js/codemirror/mode/python/python.min.js?v=20260602"></script>
<script>
  const STORAGE_KEY = 'py_day0X_quiz_history';  // 必须在 quiz-engine.js 之前定义
  const SAVE_KEY = 'py_day0X_saves';
</script>
<script src="/static/js/quiz-engine.js?v=20260602"></script>
```

### 练习题卡片结构

每道题是一个 `.card`，用 `data-*` 属性标记题型和答案：

| data-type | 说明 | data-answer |
|-----------|------|-------------|
| `choice` | 选择题 | 正确选项字母（如"A"） |
| `fill` | 填空题 | 正确答案 |
| `short` | 简答题 | 空（手动核对） |
| `write` | 代码实战题 | 空（手动核对） |

填空题的 `.blank-input` 是 `contenteditable` 的 `<span>`，不是 `<input>`。访问 value 时需兼容：
```javascript
var v = inp.value !== undefined ? inp.value.trim() : (inp.textContent || '').trim();
```

### CSS 缓存版本

当前版本：`?v=20260602`。修改 CSS/JS 后必须更新所有引用的版本号，否则浏览器使用缓存不更新。

### CodeMirror（本地文件，非 CDN）

CodeMirror 文件存于 `static/js/codemirror/`，避免 CDN 不稳定问题：
- `codemirror.min.js` — 编辑器核心（170535 bytes）
- `mode/python/python.min.js` — Python 语法高亮

**注意：** 从任何来源更新时务必验证文件完整性，被截断的版本会导致编辑器崩溃。

---

## 服务器信息

- **IP:** 120.24.229.113
- **SSH:** `root` / `lmw2625632443.`（记录在 memory/server_info.md）
- **部署路径:** `/var/www/my_blog`
- **Gunicorn:** 监听 `127.0.0.1:8000`，由 systemd 服务 `my_blog` 管理
- **Nginx:** 直接服务静态文件，反向代理动态请求给 gunicorn
- **域名:** 829007.xyz

### 服务器文件映射

| 本地路径 | 服务器路径 |
|----------|-----------|
| `my_blog/static/*.html` | `/var/www/my_blog/static/` |
| `my_blog/templates/*.html` | `/var/www/my_blog/templates/` |
| `my_blog/static/css/*.css` | `/var/www/my_blog/static/css/` |
| `my_blog/static/js/*.js` | `/var/www/my_blog/static/js/` |
| `my_blog/static/js/codemirror/*` | `/var/www/my_blog/static/js/codemirror/` |

---

## 练习题生成流程

### 添加新练习（DayXX）

1. 准备 Markdown 作业文件（格式：`DayXX_每日作业_codex.md`），存入 `my_blog/day_test_data_Markdown/`
2. 运行生成脚本（在 `my_blog/scripts/` 下）：
   - `python gen007_clean.py` — 从 Markdown 生成练习 007 HTML
   - `python gen008.py` — 生成练习 008
   - `python gen009.py` — 生成练习 009
3. 修复代码高亮：`python fix_789_highlight.py`
4. 上传到服务器（SSH/SFTP）
5. 更新 `hub.html` 的练习卡片区（添加新卡片）
6. 更新所有练习页的导航下拉菜单（上一练习/下一练习链接）

### 生成脚本工作原理

`scripts/` 包含用于生成练习 HTML 的脚本：
- `gen007_clean.py`、`gen008.py`、`gen009.py` — 生成 007~009 练习页
- `generate_day03.py` ~ `generate_day06.py` — 早期生成脚本
- `fix_*.py` — 开发中临时修复脚本

题源 Markdown 文件位于：`my_blog/day_test_data_Markdown/`

gen007/gen008/gen009 的工作方式：
1. 将问题数据（choices/fills/shorts/writes）定义在 Python 列表中
2. 读取一个已有的练习 HTML 作为模板（gen008 读取 007，gen009 读取 008）
3. 通过深度追踪 `<div class="section">` 嵌套边界来定位每个 section 的起止行
4. 用新题目内容替换对应 section 内的 `.card` HTML
5. 执行文本替换：标题、STORAGE_KEY、SAVE_KEY、题目数量、导航链接

### 参考答案代码高亮

`fix_789_highlight.py` 为填空题/简答题/代码实战题的参考答案添加 Python 语法高亮：
- Python 关键字（def/return/if/for/import 等）
- 内置函数（print/range/len 等）
- SQL 关键字（SELECT/INSERT/WHERE 等）
- 字符串、注释、数字、@装饰器

---

## 作业转换技能（add-homework-quiz）

完整流程记录在 `.claude/skills/add-homework-quiz.md`：
- 将 DayXX Markdown 作业转换为交互式测验页面
- 生成后部署到服务器
- 更新导航和 hub.html 卡片

---

## Git 工作流

当前使用 SFTP 直接部署（GitHub 网络不稳定）。

建议流程：
1. 本地修改测试
2. SFTP 上传到服务器验证
3. 网络稳定时 git push 到 GitHub

---

## CSS 架构

- `variables.css` — 共享 CSS 自定义属性（`:root` 变量）
- `style.css` — 博客样式，`@import variables.css`
- `quiz.css` — 练习页样式，`@import variables.css`

**重要：** 部署任何样式/JS 变更后必须更新缓存版本号 `?v=YYYYMMDD`，否则浏览器使用缓存不更新。`templates/base.html` 控制博客样式版本，各 quiz HTML 控制练习页版本。当前部署版本：`?v=20260602`。

---

## 重要注意事项

1. **CSS 缓存** — 浏览器缓存激进。修改 CSS/JS 后必须更新版本号 `?v=YYYYMMDD`，并执行 `nginx -s reload`。

2. **localStorage key** — 每套练习有独立的 `STORAGE_KEY`（做题历史）和 `SAVE_KEY`（手动存档）。必须在 `quiz-engine.js` 加载前定义。

3. **contenteditable 填空题** — `.blank-input` 是 `<span contenteditable>`，不是 `<input>`。读取值时需检查 `.value` 是否为 undefined。

4. **hub.html vs 其他模板** — hub.html 使用内联 `<style>`，修改首页样式时需同时修改两端。

5. **按钮 type 属性** — 所有 `<button class="score-btn">` 必须有 `type="button"`，否则可能触发表单提交行为。

6. **CodeMirror 文件完整性** — `codemirror.min.js` 应为 170535 bytes，被截断会导致 `SyntaxError: Unexpected end of input`。

7. **Flask secret_key** — `app.py` 中是占位符，生产环境需设置真实密钥。

---

## 近期修复记录

- **提交按钮无响应** — 原因是 contenteditable 的 `<span>` 没有 `.value` 属性，访问 `undefined.trim()` 报错。修复：先检查 `.value !== undefined`。
- **008/009 生成** — gen009.py 基于 gen008.py 的模板修改，gen008.py 基于 gen007.py 的模板修改。
- **hub.html 卡片排序** — 最新练习（009 → 008 → 007 → 006 ... → 001）排在最前面。