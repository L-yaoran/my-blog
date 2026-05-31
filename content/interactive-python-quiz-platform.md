title: 从零构建交互式 Python 练习平台：架构设计与技术实现
date: 2026-05-31
badge: 项目实践
summary: 详述如何用 Flask + 原生 JavaScript 构建一个包含选择题、填空题、简答题、代码实战的交互式练习平台，含评分引擎、进度管理、题库渲染等核心模块的设计思路。

## 背景

个人技术博客搭好后，我需要一套配套的 Python 练习系统。市面上有现成的在线判题平台，但它们面向算法竞赛，不适合课程练习——我需要的是：选择题自动评分、填空题模糊匹配、代码题有参考答案、每套练习有独立的做题记录。

于是我决定自己动手，用 Flask + 原生 JavaScript 从头构建这套系统。

## 技术选型：为什么不用数据库

最初考虑过几种方案：

| 方案 | 优点 | 缺点 |
|------|------|------|
| Django + PostgreSQL | 功能完善，ORM 强大 | 过于重量，数据库维护成本高 |
| Flask + SQLite | 轻量，但仍有数据库 | 部署麻烦，备份复杂 |
| Flask + JSON 文件 | 简单，备份就是复制文件 | 不适合频繁写入 |
| 纯静态 HTML + JS | 最简单，可直接托管 | 无法动态题库，代码重复 |

最终选择**静态 HTML 练习页 + Flask 博客路由共享**的混合方案：
- 练习页是纯静态 HTML，不需要服务端渲染，直接由 Nginx 提供
- 评分、进度、存档全部在前端用 JavaScript 完成（localStorage 持久化）
- 博客部分用 Flask + Flask-FlatPages，Markdown 写文章

这样博客和练习各自独立，部署简单，而且练习页天然支持 CDN 加速。

## 整体架构

```
用户浏览器
    │
    ├── Nginx (静态文件 + 反向代理)
    │       ├── /static/         → 直接返回 quiz HTML/CSS/JS（无 Flask 参与）
    │       └── /*              → 反向代理到 Gunicorn
    │
    └── Gunicorn (Flask App)
            ├── /              → hub.html（首页，含练习卡片）
            ├── /about         → about.html（关于页面）
            └── /<slug>/      → Flask-FlatPages 渲染 Markdown 文章
```

**核心设计原则：动静分离。** 练习页完全不经过 Flask，全部由 Nginx 直接服务，这意味着添加新练习页面只需要放一个 HTML 文件，不需要重启服务。

## 题库结构：HTML 还是 JSON

我最终选择把题目数据直接嵌入 HTML。每一道题是一个 `<div class="card">`，通过 `data-*` 属性标记题型和答案：

```html
<div class="card" data-qid="1" data-type="choice" data-answer="B">
  <div class="card-question">类是抽象模板，对象是由类创建出来的具体实例，对吗？</div>
  <div class="options">
    <div class="option" data-opt="A" onclick="selectOption(this)">
      <span class="option-letter">A</span> 错误，因为类不是模板
    </div>
    <!-- B/C/D... -->
  </div>
</div>
```

`data-type` 决定如何评分：

- `choice` — 用户选择的字母与 `data-answer` 比对
- `fill` — 答案规范化后（去空格、标点归一化）与用户输入比对
- `short` / `write` — 主观题，展示参考答案，不自动评分

这种结构的优势是**题目渲染完全由 HTML 控制**，不需要前端动态生成 DOM。如果未来迁移到其他平台，直接复制 HTML 即可，不需要导出题库格式。

## 评分引擎：JavaScript 在浏览器里跑

所有评分逻辑在 `quiz-engine.js` 中实现，提交时遍历所有 `.card`：

```javascript
document.querySelectorAll('.card').forEach(card => {
  const type = card.dataset.type;
  const answer = card.dataset.answer;

  if (type === 'choice') {
    const selected = card.querySelector('.option.selected');
    const isCorrect = selected?.dataset.opt === answer;
    // 标记正确/错误，加载解析
  } else if (type === 'fill') {
    const inputs = card.querySelectorAll('.blank-input');
    const userAnswer = normalize(collectInputs(inputs));
    const correct = normalize(answer);
    // 模糊匹配，去掉空格、中英文括号差异
  }
});
```

`normalize()` 函数处理填空题的匹配逻辑：

```javascript
function normalize(s) {
  return s
    .replace(/\s+/g, '')        // 去所有空格
    .replace(/[（）\(\)]/g, '()') // 统一括号
    .replace(/[；;]/g, ',')     // 分号变逗号
    .replace(/[。.]/g, '')       // 去句号
    .toLowerCase();
}
```

这样 `"  模板；  实例"` 和 `"模板;实例"` 都能匹配 `"模板；实例"`。

## 进度管理：localStorage 的边界

localStorage 有 5MB 限制，每个练习的记录需要独立 key。我用两个 key 分离存档和历史：

- `py_day01_saves` — 用户手动保存的存档（任意时刻可存/取）
- `py_day01_quiz_history` — 每次提交的记录列表（最多 30 条）

```javascript
// 保存手动存档
const saves = JSON.parse(localStorage.getItem(SAVE_KEY) || '{}');
saves[name] = { time: Date.now(), data: collectAnswers() };
localStorage.setItem(SAVE_KEY, JSON.stringify(saves));

// 提交时写历史
const records = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
records.unshift({ date, correct, total, answers: userAnswers });
if (records.length > 30) records.length = 30; // 最多保留 30 条
localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
```

localStorage 的局限：**换设备或清浏览器缓存记录全丢**。所以我加了导出/导入功能，将存档和历史合并为一个 JSON 文件下载：

```javascript
function exportProgress() {
  const exportData = {
    version: 1,
    exportedAt: new Date().toISOString(),
    saves: JSON.parse(localStorage.getItem(SAVE_KEY) || '{}'),
    records: JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  };
  const blob = new Blob([JSON.stringify(exportData)], { type: 'application/json' });
  // 触发下载...
}
```

用户可以定期导出备份，换设备后导入恢复。

## 代码编辑器：Tab 缩进与 CodeMirror

代码实战的 `<textarea>` 需要 Tab 缩进支持。在原生 textarea 上拦截 Tab 键：

```javascript
editor.addEventListener('keydown', e => {
  if (e.key === 'Tab' && !submitted) {
    e.preventDefault();
    const start = editor.selectionStart;
    editor.value = editor.value.substring(0, start) + '    ' + editor.selectionEnd;
    editor.selectionStart = editor.selectionEnd = start + 4;
  }
});
```

更进一步，如果页面加载了 CodeMirror CDN，则用 CodeMirror 替代原生 textarea，获得 Python 语法高亮和行号：

```javascript
if (typeof CodeMirror !== 'undefined') {
  const cm = CodeMirror.fromTextArea(editor, {
    mode: 'python',
    theme: 'monokai',
    lineNumbers: true,
    indentUnit: 4,
  });
  cm.on('change', () => { resizeEditor(); updateProgress(); });
}
```

## 导航与页面组织

6 套练习分布在静态 HTML 文件中，互相链接。我用固定格式的下拉菜单维护页面关系：

```html
<div class="quiz-dropdown">
  <button onclick="toggleDropdown(this)">练习 003 <span>▾</span></button>
  <div class="quiz-dropdown-menu">
    <a href="/static/python_basic_test_001.html">练习 001</a>
    <a href="/static/python_basic_test_002.html">练习 002</a>
    <!-- 所有练习... -->
  </div>
</div>
```

CSS 关闭其他下拉菜单，点击空白处自动收起。

## 深色模式：CSS 媒体查询

用 `prefers-color-scheme` 检测系统主题：

```css
@media (prefers-color-scheme: dark) {
  :root {
    --void: #0d0d0d;
    --surface: #1a1a1a;
    --text: #e5e5e5;
    --border: #333333;
  }
  .option.selected {
    background: rgba(37, 99, 235, 0.15);
    border-color: var(--blue);
  }
}
```

无需 JavaScript，系统切换主题自动生效。

## 部署：Gunicorn + Nginx

生产环境用 Gunicorn 管理 4 个 worker：

```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app --daemon
```

Nginx 配置反向代理并处理静态文件：

```nginx
location /static {
    alias /var/www/my_blog/static;
    expires 1h;  # 静态资源缓存 1 小时
}

location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

关键优化：**练习页的 CSS/JS 有缓存版本号**（`?v=20260531`），更新后改版本号即可绕过 CDN 和浏览器缓存。

## 总结

这套练习系统的核心设计哲学是**简单可维护**：

- **静态 HTML 题目** — 不依赖数据库，不依赖后端，随时可迁移
- **纯前端评分** — 无服务端计算资源，用户本地完成
- **localStorage 持久化** — 无数据库写入，备份就是下载 JSON
- **动静分离** — Nginx 直出静态文件，Gunicorn 只处理博客路由

这套架构适合个人开发者快速上线练习平台。如果你有类似需求，希望这篇文章提供了可参考的实现思路。