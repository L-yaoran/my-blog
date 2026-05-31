# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask personal blog deployed at https://829007.xyz — also serves as an interactive Python quiz platform with 6 exercise pages. No database; blog content lives in `content/` as Markdown files managed by Flask-FlatPages.

## Key Commands

```bash
# Local development
cd my_blog
python app.py          # starts Flask dev server on :5000

# Run unit tests
cd my_blog
python -m unittest test_app

# Deploy to server (requires SSH access to 120.24.229.113)
# 1. Commit changes to a branch
git checkout -b some-branch
git add . && git commit
git push -u origin some-branch
# 2. SSH to server and pull
ssh root@120.24.229.113
cd /var/www/my_blog
git pull origin some-branch
# 3. Restart gunicorn
systemctl restart my_blog
# Or: pkill -f gunicorn && gunicorn -w 4 -b 127.0.0.1:8000 app:app --daemon
```

## Architecture Notes

### Templates
- `templates/base.html` — shared nav bar, footer, CSS/JS links. All pages extend it except `hub.html` which is standalone with inline `<style>`.
- `templates/hub.html` — homepage, extends `base.html` via `{% extends "base.html" %}` + `{% block extra_css %}` for its inline styles.
- `templates/about.html` — about page, extends `base.html`, uses shared `style.css` contact styles.
- `templates/quiz.html` — Jinja2 quiz template (P2 work-in-progress, not yet used in production)

### Quiz Pages (static HTML)
Six exercise pages live in `static/` and are served directly by Nginx, NOT through Flask routes:
- `python_basic_test_001.html` through `python_basic_test_005-2.html`

Each quiz page has:
- `<link rel="stylesheet" href="/static/css/quiz.css">`
- `<script src="/static/js/quiz-engine.js">`
- Inline `<script>` defining `STORAGE_KEY` and `SAVE_KEY` constants

### Shared Quiz Engine
`static/js/quiz-engine.js` is loaded by ALL quiz pages. It handles:
- `selectOption()` — choice selection
- `submitAll()` / `resetAll()` — scoring and reset
- `saveProgress()` / `loadProgress()` — localStorage save/load
- `exportProgress()` / `importProgress()` — JSON export/import
- `renderHistory()` / `showHistoryDetail()` — history panel
- `toggleDropdown()` — nav dropdown
- CodeMirror init (if CDN is loaded)
- Keyboard shortcuts (J/K for prev/next question, Esc to close history modal)

### CSS Architecture
- `static/css/variables.css` — shared CSS custom properties (`:root` variables)
- `static/css/style.css` — blog styles, imports `variables.css`
- `static/css/quiz.css` — quiz page styles, imports `variables.css`

**Important:** Always update CSS cache version (`?v=YYYYMMDD`) when deploying style changes, or browsers will serve cached versions. Update in `templates/base.html` for blog styles, and in each quiz HTML file for quiz styles.

### Quiz Page HTML Structure
Each question card uses `data-type` and `data-answer` attributes:
- `data-type="choice"` — single choice, `data-answer` = correct letter
- `data-type="fill"` — fill-in-the-blank, `data-answer` = correct answer
- `data-type="short"` — short answer (manual review)
- `data-type="write"` — code exercise (manual review)

## Server Info

- **IP:** 120.24.229.113
- **SSH:** `root` / password in memory (`server_info.md`)
- **Deploy path:** `/var/www/my_blog`
- **Gunicorn:** runs on `127.0.0.1:8000`, managed by systemd service `my_blog`
- **Nginx:** serves static files directly, proxies to gunicorn
- **Domain:** 829007.xyz

## Quirks & Gotchas

1. **CSS caching** — Browser caches aggressively. After any CSS change, bump the version in both `base.html` (`style.css?v=...`) and all quiz HTML files (`quiz.css?v=...`, `quiz-engine.js?v=...`).

2. **localStorage keys** — Each quiz page has its own pair: `STORAGE_KEY` (history records) and `SAVE_KEY` (manual saves). They must be defined before `quiz-engine.js` loads.

3. **hub.html vs about.html** — hub.html has its own inline `<style>` block (NOT using `style.css` contact styles), while about.html uses shared `style.css`. When editing contact/footer styles, update both.

4. **Flask secret_key** — `app.py` has `app.secret_key = 'your-secret-key-change-in-production'`. This is a placeholder; set a real secret in production.

5. **Quiz pages are static HTML** — They are NOT rendered by Flask templates. To add/modify quiz pages, edit the HTML files directly in `static/` or use the generation scripts in `scripts/`.

## Quiz Generation Scripts

`scripts/` contains Python scripts that generate quiz HTML:
- `generate_day03.py`, `generate_day04.py`, `generate_day05_1.py`, `generate_day05_2.py` — generate quiz HTML from Markdown source files
- `fix_*.py` — ad-hoc fix scripts used during development

Source Markdown files for quiz content are in:
`E:\AI_itheima\Sync_file\sync_Phase_one\08_作业\Day0X\`
