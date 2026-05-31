"""
Refactor all quiz pages to use external quiz.css and quiz-engine.js.
"""
import re, os

def refactor(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace inline <style> block with <link>
    style_start = html.find('<style>')
    style_end = html.find('</style>')
    if style_start >= 0 and style_end >= 0:
        css_link = '<link rel="stylesheet" href="/static/css/quiz.css">\n'
        html = html[:style_start] + css_link + html[style_end+8:]

    # 2. Find STORAGE_KEY and SAVE_KEY declarations (page-specific)
    # Extract the page-specific constants from the script
    sk_match = re.search(r"const STORAGE_KEY\s*=\s*'([^']+)'", html)
    sv_match = re.search(r"const SAVE_KEY\s*=\s*'([^']+)'", html)

    # 3. Replace inline <script> block with page config + external script
    # Find the last script block (the big one containing all JS functions)
    script_starts = [m.start() for m in re.finditer('<script>', html)]
    script_ends = [m.start() for m in re.finditer('</script>', html)]

    if len(script_starts) >= 2:
        # The last <script> block is the big JS engine
        last_script_start = script_starts[-1]
        last_script_end = [e for e in script_ends if e > last_script_start][0] + 9

        # Build page config
        config = '<script>\n'
        if sk_match:
            config += f"const STORAGE_KEY = '{sk_match.group(1)}';\n"
        if sv_match:
            config += f"const SAVE_KEY = '{sv_match.group(1)}';\n"
        if not sk_match and not sv_match:
            print(f'{os.path.basename(path)}: no STORAGE_KEY found!')
        config += '</script>\n<script src="/static/js/quiz-engine.js"></script>\n'

        # Replace the last script block
        html = html[:last_script_start] + config + html[last_script_end:]
        print(f'{os.path.basename(path)}: refactored OK')
    else:
        print(f'{os.path.basename(path)}: only {len(script_starts)} script blocks found')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

pages = ['001', '002', '003', '004', '005-1', '005-2']
for p in pages:
    path = fr'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_{p}.html'
    refactor(path)

print('All pages refactored')
