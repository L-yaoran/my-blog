#!/usr/bin/env python3
"""
批量更新所有练习页的导航下拉菜单。
新增练习后运行此脚本，所有已有页面的导航会自动更新。
"""
import os
import re
from quiz_meta import QUIZZES

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(SCRIPT_DIR, '..', 'static')


def build_nav_dropdown(current_id):
    """生成下拉菜单 HTML。"""
    lines = []
    for q in QUIZZES:
        qid = q['id']
        label = f'练习 {qid}'
        active = ' class="active"' if qid == current_id else ''
        lines.append(f'        <a href="/static/python_basic_test_{qid}.html"{active}>{label}</a>')
    return '\n'.join(lines)


def build_prev_next(current_id):
    """生成 prev/next 箭头 HTML。"""
    idx = next(i for i, q in enumerate(QUIZZES) if q['id'] == current_id)

    if idx > 0:
        prev_id = QUIZZES[idx - 1]['id']
        prev_link = f'<a href="/static/python_basic_test_{prev_id}.html" class="quiz-arrow" title="上一练习">◂</a>'
    else:
        prev_link = '<span class="quiz-arrow disabled" title="已是第一个">◂</span>'

    if idx < len(QUIZZES) - 1:
        next_id = QUIZZES[idx + 1]['id']
        next_link = f'<a href="/static/python_basic_test_{next_id}.html" class="quiz-arrow" title="下一练习">▸</a>'
    else:
        next_link = '<span class="quiz-arrow disabled" title="已是最后一个">▸</span>'

    return prev_link, next_link


def update_file(filepath, quiz_id):
    """更新单个 HTML 文件的导航。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换下拉菜单内容（从 menu 开始到 </div> 结束）
    nav_dropdown = build_nav_dropdown(quiz_id)
    content = re.sub(
        r'(<div class="quiz-dropdown-menu">\n)(.*?)(      </div>)',
        lambda m: m.group(1) + nav_dropdown + '\n' + m.group(3),
        content,
        flags=re.DOTALL
    )

    # 替换按钮文字
    content = re.sub(
        r'练习 \d{3} <span class="arrow-icon">▾</span>',
        f'练习 {quiz_id} <span class="arrow-icon">▾</span>',
        content
    )

    # 替换 prev 箭头
    prev_link, next_link = build_prev_next(quiz_id)
    content = re.sub(
        r'(<div class="quiz-nav">\n)\s*(<a href[^>]*class="quiz-arrow"[^>]*title="上一练习">◂</a>|<span class="quiz-arrow disabled"[^>]*title="已是第一个">◂</span>)',
        r'\g<1>    ' + prev_link,
        content
    )

    # 替换 next 箭头
    content = re.sub(
        r'(<a href[^>]*class="quiz-arrow"[^>]*title="下一练习">▸</a>|<span class="quiz-arrow disabled"[^>]*title="已是最后一个">▸</span>)',
        next_link,
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    files = sorted(f for f in os.listdir(STATIC_DIR) if f.startswith('python_basic_test_') and f.endswith('.html'))
    print(f'找到 {len(files)} 个练习页文件')

    for fname in files:
        quiz_id = fname.replace('python_basic_test_', '').replace('.html', '')
        filepath = os.path.join(STATIC_DIR, fname)
        update_file(filepath, quiz_id)
        print(f'  已更新: {fname}')

    print(f'\n全部 {len(files)} 个文件的导航已更新，当前共 {len(QUIZZES)} 个练习。')


if __name__ == '__main__':
    main()
