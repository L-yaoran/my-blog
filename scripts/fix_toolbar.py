"""
Replace broken toolbar in 001-003 with working toolbar from 004.
"""
import re

# Read the working toolbar template
with open(r'E:\AI_itheima\VS_code\my_blog\static\_toolbar_template.txt', 'r', encoding='utf-8') as f:
    toolbar = f.read()

files_scores = [
    (r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_001.html', '18'),
    (r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_002.html', '18'),
    (r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_003.html', '14'),
]

for path, subj_score in files_scores:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Customize template for this file
    t = toolbar.replace('/13', '/' + subj_score)

    # Find old toolbar to replace
    start = html.find('class=\"sticky-toolbar\"')
    if start == -1:
        print(f'{path}: no toolbar found')
        continue

    # Go back to beginning of line
    start = html.rfind('\n', 0, start) + 1

    # Find first section to know where toolbar ends
    end = html.find('<!-- ======', start)
    if end == -1:
        end = html.find('<div class=\"section\"', start)
    if end == -1:
        print(f'{path}: no section marker found')
        continue

    old_toolbar = html[start:end]

    # Replace
    html = html[:start] + t + html[end:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Verify
    has_overlay_inside = html.find('history-detail-overlay') > html.find('sticky-toolbar"') + 50
    print(f'{path}: overlay inside toolbar = {has_overlay_inside}, subjScore = {subj_score}')

print('Done')
