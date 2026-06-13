# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在本仓库中工作时提供指导。

## 语言要求

- 所有对话、文档、代码注释、提交说明统一使用中文

---

## 项目概览

Flask 个人博客，部署于 https://829007.xyz，承载 16 套交互式 LLM 练习系统（570+ 道题）。无数据库；博客文章以 Markdown 存于 `content/`，由 Flask-FlatPages 管理。

---

## 常用命令

```bash
# 本地开发
cd my_blog && python app.py

# 生成新练习（在 my_blog/scripts/ 下）
python generate_quiz.py 012     # 生成练习 012
python update_navs.py           # 更新所有页面导航
python fix_789_highlight.py     # 为所有练习页添加代码高亮

# 部署（通过 paramiko SFTP）
# 上传 static/*.html、templates/hub.html、js/css 文件
# 然后 nginx -s reload && systemctl restart my_blog
```

---

## 架构

```
my_blog/
├── app.py                  # Flask 入口
├── content/                # Markdown 博客文章（4 篇）
├── templates/
│   ├── base.html           # 公共模板（导航栏 + 页脚）
│   ├── hub.html            # 首页（继承 base.html，内联样式）
│   ├── quiz.html           # 练习页 Jinja2 模板（Flask 路由用）
│   └── post.html / about.html / 404.html
├── static/
│   ├── css/
│   │   ├── variables.css   # 共享 CSS 变量
│   │   ├── style.css       # 博客样式 + 深色模式
│   │   └── quiz.css        # 练习页样式 + 深色模式
│   ├── js/
│   │   ├── main.js         # 导航 + 主题切换
│   │   ├── quiz-engine.js  # 练习引擎（16 个页面共用）
│   │   └── codemirror/     # 本地 CodeMirror（~170KB）
│   └── python_basic_test_001~016.html  # 16 套练习页
├── scripts/
│   ├── quiz_template.html  # 骨架模板（唯一维护点）
│   ├── quiz_meta.py        # 练习元数据
│   ├── quiz_data_001~016.py # 题目数据
│   ├── generate_quiz.py    # 统一生成脚本
│   ├── update_navs.py      # 批量导航更新
│   └── fix_789_highlight.py # 代码高亮修复
└── data/quiz_001.json      # Flask 路由用（仅 001）
```

**动静分离：** Nginx 直出静态文件，Flask 只负责模板渲染。练习页修改后不需要重启服务。

---

## 新增练习流程

1. 创建 `scripts/quiz_data_0XX.py`（题目数据：choices/fills/shorts/writes）
2. 在 `scripts/quiz_meta.py` 添加元数据
3. 运行 `python generate_quiz.py 0XX`
4. 运行 `python update_navs.py`
5. 运行 `python fix_789_highlight.py`
6. 在 `hub.html` 添加练习卡片
7. 上传服务器，`nginx -s reload && systemctl restart my_blog`

---

## 服务器

- **IP:** 120.24.229.113 / **域名:** 829007.xyz
- **SSH:** root（密码通过环境变量 `SERVER_SSH_PASS` 获取，不在代码中存储）
- **部署路径:** `/var/www/my_blog`
- **架构:** Nginx(443) → Gunicorn(127.0.0.1:8000) → Flask
- **部署方式:** paramiko SFTP 上传 + SSH 重启服务

---

## 重要注意事项

1. **CSS 缓存** — 修改 CSS/JS 后必须更新 `?v=YYYYMMDD` 版本号
2. **localStorage key** — 每套练习独立的 `STORAGE_KEY` / `SAVE_KEY`，必须在 quiz-engine.js 前定义
3. **contenteditable 填空题** — `.blank-input` 是 `<span contenteditable>`，读取值需检查 `.value !== undefined`
4. **hub.html 内联样式** — 修改首页样式时需同步 hub.html 的 `<style>` 块
5. **按钮 type** — 所有 `<button class="score-btn">` 必须有 `type="button"`
6. **CodeMirror** — `codemirror.min.js` 应为 170535 bytes，截断会导致崩溃
