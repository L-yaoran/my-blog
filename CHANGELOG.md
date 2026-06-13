# 更新日志

本文件记录项目的主要变更，格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

---

## [未发布]

### 计划
- 首页信息架构改版（v4 spec）
- 内容分类/标签/SEO/RSS（v4.1 spec）
- 练习平台独立入口（v4.2 spec）
- 站内 AI 学习助手（v5 spec）
- 练习平台增强：错题本/统计面板/随机顺序（quiz-enhancement-spec）

---

## [2026-06-12]

### 新增
- 练习 016：Coze 智能体开发（37 题，Phase2 Day04）
- 5 份 spec 规划文档（v4/v4.1/v4.2/v5/quiz-enhancement）
- 练习平台增强 spec（从 PRD 提取）

### 变更
- 项目文档全面更新（README.md / CLAUDE.md / CHANGELOG.md）
- README.md 重写（练习 11→16，项目结构更新，新增练习清单表格）
- CLAUDE.md 同步更新（根目录 + my_blog/ 两份）
- sitemap.xml 补充 007-016 + interactive-python-quiz-platform 文章
- hub.html 项目卡片更新为 16 套 570+ 道题
- quiz_001.json 导航更新到 012-016
- 服务器全量同步（35 个运行时文件）
- 清理服务器旧文件（static/static\ 双层目录、旧路径 quiz-engine.js/quiz.css）

### 清理
- 审查文档 v1/v2/v3 归档至回收站
- PRD 产品规划文档归档至回收站（练习站功能已提取为独立 spec）

---

## [2026-06-10]

### 新增
- 练习 015：提示词技术选型与金融场景（37 题，Phase2 Day03）

---

## [2026-06-09]

### 新增
- 练习 014：API 调用/链式提示（37 题，Phase2 Day02）

---

## [2026-06-08]

### 新增
- 练习 013：提示词工程基础（38 题，Phase2 Day01）
- 练习 012：Linux 基础（38 题，Phase1 Day10）

---

## [2026-06-07]

### 新增
- 统一模板系统（quiz_template.html + generate_quiz.py + update_navs.py）
- quiz_meta.py 练习元数据集中管理
- quiz_data_001~011.py 题目数据文件

### 变更
- 所有练习页由统一模板重新生成，消除骨架漂移
- 首页继承 base.html（原为独立页面）
- CodeMirror 改为本地文件托管
- 深色模式全面支持（style.css / quiz.css / hub.html）

### 清理
- 删除旧版 gen007~gen011 独立生成脚本
- scripts/ 目录精简为统一工具链

---

## [2026-06-05]

### 新增
- 练习 011：NumPy + Pandas + Matplotlib 数据分析三剑客（38 题）
- gen011.py 生成脚本
- 项目审查与改进建议 v2 文档

### 变更
- 页脚新增公安备案号（湘公网安备43042102000141号）
- 所有练习页下拉菜单更新至 011
- 主页新增 011 紫色卡片

### 清理
- 移除 12 个废弃脚本（generate_day03~06、fix_*、patch_*、refactor_*）
- 合并 my_blog/CLAUDE.md 到根目录 CLAUDE.md
- scripts/ 目录精简至 6 个文件

---

## [2026-06-04]

### 新增
- 练习 010：PyMySQL + Redis（38 题）
- gen010.py 生成脚本

### 修复
- 练习 010 下拉按钮文字错误

---

## [2026-06-03]

### 新增
- 主页练习卡片折叠/展开功能（通用化 data-collapsible）
- 练习/笔记 Tab 切换
- 实践项目卡片内容更新（LLM 交互练习平台）

### 变更
- 练习标题统一改为"LLM 练习"（原"Python 练习"）
- 博客文章标题同步更新
- 生成脚本中标题替换规则更新

### 修复
- 填空题 contenteditable 兼容性（quiz-engine.js 6 处）
- test_app.py 中 005-1/005-2 引用更新为 005~010
- quiz_001.json 导航更新为 001~010
- 缓存版本号统一为 20260602
- .gitignore 移除 data/ 排除，删除重复条目
- README.md 更新练习编号和数量

---

## [2026-06-02]

### 新增
- 练习 007/008/009：Day06 正则表达式 + MySQL（共 100 题）
- gen007_clean.py、gen008.py、gen009.py 生成脚本
- fix_789_highlight.py 代码高亮修复脚本

### 修复
- 提交按钮无响应（contenteditable span 的 .value 未定义）
- 按钮添加 type="button" 防止表单提交
- 主页练习卡片排序（最新在前：009→008→007→...→001）

### 变更
- CodeMirror 改为本地文件托管（避免 CDN 不稳定）
- hub.html 继承 base.html（统一导航/页脚）

---

## [2026-06-01]

### 新增
- 练习 005/006：Day05 多线程/生成器/协程
- variables.css 共享 CSS 变量
- quiz-engine.js 数据导出/导入功能

### 变更
- quiz.css 移动端适配（600px/480px 断点）
- quiz.css 深色模式支持

---

## [2026-05-31]

### 新增
- 练习 003/004：Day03 闭包/装饰器、Day04 网络编程
- 单元测试 test_app.py
- 博客文章：交互式练习平台搭建详解

---

## [2026-05-30]

### 新增
- 练习 001/002：Day01 类与对象、Day02 继承/多态
- 练习引擎 quiz-engine.js
- 练习页样式 quiz.css

---

## [2026-05-28]

### 新增
- Flask 博客基础架构
- 首页 hub.html
- 博客文章系统（Flask-FlatPages）
- 部署至阿里云 ECS（Nginx + Gunicorn）
