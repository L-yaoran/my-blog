"""Fix 001 and 003: remove JS highlighter, use Python-side pre-highlighting."""
import re, html as html_mod

def highlight_python(code):
    KW_LIST = ['def','return','if','elif','else','for','while','import','from','class','True','False','None','self','nonlocal','global','in','not','and','or','is','with','as','try','except','finally','raise','pass','break','continue','yield','lambda']
    BI_LIST = ['print','range','len','type','int','str','list','dict','tuple','set','input','isinstance','super','open','enumerate','zip','map','filter','sorted','reversed','abs','min','max','sum','round','socket','Process','Queue','Pipe','Manager','multiprocessing','os']
    KW_PAT = re.compile(r'\b(' + '|'.join(KW_LIST) + r')\b')
    BI_PAT = re.compile(r'\b(' + '|'.join(BI_LIST) + r')\b')
    NUM_PAT = re.compile(r'\b(\d+\.?\d*)\b')
    STR_PAT = re.compile(r"(f?(?:\"\"\"[\s\S]*?\"\"\"|'''[\s\S]*?'''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'))")
    CM_PAT = re.compile(r'(#[^\n]*)')
    OP_PAT = re.compile(r'(@\w+)')

    code = STR_PAT.sub(r'<span class="str">\1</span>', code)
    code = CM_PAT.sub(r'<span class="cm">\1</span>', code)
    code = OP_PAT.sub(r'<span class="op">\1</span>', code)

    parts = re.split(r'(<span[^>]*>.*?</span>)', code)
    for i in range(len(parts)):
        if parts[i].startswith('<span'):
            continue
        tokens = []
        for m in KW_PAT.finditer(parts[i]):
            tokens.append((m.start(), m.end(), 'kw', m.group(1)))
        for m in BI_PAT.finditer(parts[i]):
            tokens.append((m.start(), m.end(), 'fn', m.group(1)))
        for m in NUM_PAT.finditer(parts[i]):
            tokens.append((m.start(), m.end(), 'num', m.group(1)))
        tokens.sort(key=lambda x: (x[0], -x[1]))
        result = []
        pos = 0
        for start, end, cls, text in tokens:
            if start < pos:
                continue
            result.append(html_mod.escape(parts[i][pos:start]))
            result.append(f'<span class="{cls}">{html_mod.escape(text)}</span>')
            pos = end
        result.append(html_mod.escape(parts[i][pos:]))
        parts[i] = ''.join(result)
    return ''.join(parts)

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all <pre> blocks inside code-block and replace with highlighted version
    def replace_pre(m):
        code = m.group(1)
        highlighted = highlight_python(code)
        return f'<div class="code-block">{highlighted}</div>'

    # Replace <div class="code-block"><pre>CODE</pre></div>
    html = re.sub(r'<div class="code-block"><pre>(.*?)</pre></div>', replace_pre, html, flags=re.DOTALL)

    # Remove the highlightPythonCode function
    html = re.sub(r'\s*function highlightPythonCode\(\) \{[^}]*?\n\s*\}', '', html, flags=re.DOTALL)
    html = re.sub(r'\s*highlightPythonCode\(\);?', '', html)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Verify
    has_js = 'highlightPythonCode' in html
    has_pre = '<div class="code-block"><pre>' in html
    has_corrupt = 'class=class' in html
    code_blocks = html.count('<div class="code-block"><span')
    print(f'{path.split(chr(92))[-1]}: JS removed={not has_js}, pre removed={not has_pre}, corrupt={has_corrupt}, code blocks={code_blocks}')

fix_file(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_001.html')
fix_file(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_003.html')
