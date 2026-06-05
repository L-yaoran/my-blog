#!/usr/bin/env python3
"""
统一练习页生成脚本。
用法: python generate_quiz.py <quiz_id>
示例: python generate_quiz.py 011

需要在同一目录下有:
- quiz_template.html  (骨架模板)
- quiz_meta.py        (练习元数据)
- quiz_data_<id>.py   (题目数据，每个练习一个文件)
"""
import sys
import os
from quiz_meta import QUIZZES

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(SCRIPT_DIR, '..', 'static')
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'quiz_template.html')


def build_nav_html(quizzes, current_id):
    """生成导航下拉菜单 HTML 和 prev/next 箭头。"""
    lines = []
    for q in quizzes:
        qid = q['id']
        label = f"练习 {qid}"
        active = ' class="active"' if qid == current_id else ''
        lines.append(f'        <a href="/static/python_basic_test_{qid}.html"{active}>{label}</a>')
    nav_dropdown = '\n'.join(lines)

    idx = next(i for i, q in enumerate(quizzes) if q['id'] == current_id)

    if idx > 0:
        prev_id = quizzes[idx - 1]['id']
        prev_link = f'<a href="/static/python_basic_test_{prev_id}.html" class="quiz-arrow" title="上一练习">◂</a>'
    else:
        prev_link = '<span class="quiz-arrow disabled" title="已是第一个">◂</span>'

    if idx < len(quizzes) - 1:
        next_id = quizzes[idx + 1]['id']
        next_link = f'<a href="/static/python_basic_test_{next_id}.html" class="quiz-arrow" title="下一练习">▸</a>'
    else:
        next_link = '<span class="quiz-arrow disabled" title="已是最后一个">▸</span>'

    return nav_dropdown, prev_link, next_link


def gc(q):
    """生成选择题卡片 HTML。"""
    letters = 'ABCD'
    opts = '\n'.join(
        f'            <div class="option" data-opt="{letters[i]}" onclick="selectOption(this)">\n'
        f'              <span class="option-letter">{letters[i]}</span> {o}\n'
        f'            </div>'
        for i, o in enumerate(q['options'])
    )
    return f'''    <div class="card" data-qid="{q["qid"]}" data-type="choice" data-answer="{q["answer"]}">
      <div class="card-header"><span class="card-qnum">第 {q["qid"]} 题</span><span class="card-type choice">单选题</span></div>
      <div class="card-question">{q["question"]}</div>
      <div class="options">
{opts}
      </div>
      <div class="feedback">
        <div class="result-tag correct-tag">✓ 正确</div>
        <strong>解析：</strong>{q["analysis"]}
      </div>
    </div>'''


def gf(q):
    """生成填空题卡片 HTML。"""
    qt = q['question'].replace('________', '<span class="blank-input" contenteditable="true"></span>')
    return f'''    <div class="card" data-qid="{q["qid"]}" data-type="fill" data-answer="{q["answer"]}">
      <div class="card-header"><span class="card-qnum">第 {q["qid"]} 题</span><span class="card-type fill">填空题</span></div>
      <div class="card-question">{qt}</div>
      <div class="feedback">
        <div class="result-tag correct-tag">✓ 正确</div>
        <strong>解析：</strong>{q["analysis"]}
      </div>
    </div>'''


def gs(q):
    """生成简答题卡片 HTML。"""
    return f'''    <div class="card" data-qid="{q["qid"]}" data-type="short" data-answer="">
      <div class="card-header"><span class="card-qnum">第 {q["qid"]} 题</span><span class="card-type short">简答题</span></div>
      <div class="card-question">{q["question"]}</div>
      <textarea class="fill-input" placeholder="请输入你的回答..." rows="3"></textarea>
      <span class="ref-toggle" onclick="toggleRef(this)">查看参考答案 ▼</span>
      <div class="ref-answer" style="margin-top:0.5rem; padding:0.6rem 0.8rem; background:var(--code-bg); border-radius:6px; font-size:0.85rem; line-height:1.6; color:var(--text);">{q["reference"]}</div>
      <div class="feedback"><div class="result-tag correct-tag">✓ 正确</div><strong>参考答案：</strong>{q["reference"]}</div>
    </div>'''


def gw(q):
    """生成代码实战卡片 HTML。"""
    ref = q['reference'].replace('\\n', '\n')
    return f'''    <div class="card" data-qid="{q["qid"]}" data-type="write" data-answer="">
      <div class="card-header"><span class="card-qnum">第 {q["qid"]} 题</span><span class="card-type write">代码实战</span></div>
      <div class="card-question"><strong>{q["title"]}</strong></div>
      <div class="card-desc">{q["desc"]}</div>
      <textarea class="code-editor" placeholder="# 请在此编写你的代码..." rows="10"></textarea>
      <span class="ref-toggle" onclick="toggleRef(this)">查看参考答案 ▼</span>
      <div class="ref-answer"><div class="code-block">{ref}</div></div>
      <div class="feedback"><div class="result-tag correct-tag">✓ 正确</div><strong>参考答案：</strong><div class="code-block">{ref}</div></div>
    </div>'''


def build_section(title, cards_html):
    """将卡片列表包装成一个 section。"""
    return f'''<div class="section">

    <div class="section-title"><span class="icon"></span>{title}</div>

{cards_html}
</div>'''


def generate_quiz(quiz_id):
    """生成指定 ID 的练习页 HTML。"""
    # 查找元数据
    meta = next((q for q in QUIZZES if q['id'] == quiz_id), None)
    if not meta:
        print(f"错误: quiz_meta.py 中找不到 ID={quiz_id}")
        return False

    # 加载题目数据
    data_file = os.path.join(SCRIPT_DIR, f'quiz_data_{quiz_id}.py')
    if not os.path.exists(data_file):
        print(f"错误: 找不到题目数据文件 {data_file}")
        return False

    data = {}
    with open(data_file, 'r', encoding='utf-8') as f:
        exec(f.read(), data)

    choices = data.get('choices', [])
    fills = data.get('fills', [])
    shorts = data.get('shorts', [])
    writes = data.get('writes', [])

    # 生成卡片 HTML
    choice_cards = '\n'.join(gc(q) for q in choices)
    fill_cards = '\n'.join(gf(q) for q in fills)
    short_cards = '\n'.join(gs(q) for q in shorts)
    write_cards = '\n'.join(gw(q) for q in writes)

    # 生成 section
    section_1 = build_section(f'一、单选题（{len(choices)} 题）', choice_cards)
    section_2 = build_section(f'二、填空题（{len(fills)} 题）', fill_cards)
    section_3 = build_section(f'三、简答题（{len(shorts)} 题）', short_cards)
    section_4 = build_section(f'四、代码实战（{len(writes)} 题）', write_cards)

    # 生成导航
    nav_dropdown, prev_link, next_link = build_nav_html(QUIZZES, quiz_id)

    # 读取模板
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    # 替换占位符
    html = template
    html = html.replace('{{TITLE}}', meta['title'])
    html = html.replace('{{SUBTITLE}}', meta['subtitle'])
    html = html.replace('{{OBJ_TOTAL}}', str(meta['obj_total']))
    html = html.replace('{{SUBJ_TOTAL}}', str(meta['subj_total']))
    html = html.replace('{{STORAGE_KEY}}', meta['storage_key'])
    html = html.replace('{{SAVE_KEY}}', meta['save_key'])
    html = html.replace('{{DROPDOWN_LABEL}}', f'练习 {quiz_id}')
    html = html.replace('{{PREV_LINK}}', prev_link)
    html = html.replace('{{NEXT_LINK}}', next_link)
    html = html.replace('{{NAV_DROPDOWN}}', nav_dropdown)
    html = html.replace('{{SECTION_1}}', section_1)
    html = html.replace('{{SECTION_2}}', section_2)
    html = html.replace('{{SECTION_3}}', section_3)
    html = html.replace('{{SECTION_4}}', section_4)

    # 输出
    out_path = os.path.join(STATIC_DIR, f'python_basic_test_{quiz_id}.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    total = len(choices) + len(fills) + len(shorts) + len(writes)
    print(f'生成完成: {out_path}')
    print(f'  题目总数: {total} (选择{len(choices)} + 填空{len(fills)} + 简答{len(shorts)} + 代码{len(writes)})')
    print(f'  文件大小: {len(html)} 字符')
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python generate_quiz.py <quiz_id>')
        print('示例: python generate_quiz.py 011')
        sys.exit(1)

    quiz_id = sys.argv[1]
    success = generate_quiz(quiz_id)
    sys.exit(0 if success else 1)
