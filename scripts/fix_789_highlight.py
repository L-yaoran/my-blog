#!/usr/bin/env python3
"""Fix code highlighting for all quiz pages"""
import re, html as html_mod

PY_KW = ['def','return','if','elif','else','for','while','import','from','class','True','False','None','self','nonlocal','global','in','not','and','or','is','with','as','try','except','finally','raise','pass','break','continue','yield','lambda']
PY_BI = ['print','range','len','type','int','str','list','dict','tuple','set','input','isinstance','super','open','enumerate','zip','map','filter','sorted','reversed','abs','min','max','sum','round','socket','Process','Queue','multiprocessing','os','threading','time','re','findall','match','search','sub','group','count','keys','values','items','update','sleep']
SQL_KW = ['CREATE','TABLE','INSERT','INTO','UPDATE','DELETE','SELECT','FROM','WHERE','ORDER','BY','GROUP','HAVING','JOIN','ON','LIMIT','ASC','DESC','DISTINCT','AVG','COUNT','MAX','MIN','SUM','INNER','LEFT','RIGHT','OUTER','PRIMARY','KEY','FOREIGN','REFERENCES','NOT','NULL','AUTO_INCREMENT','VARCHAR','INT','DECIMAL','CHARSET','UTF8','USE','IF','EXISTS','VALUES','SET','BETWEEN','AND','OR','IN','LIKE','AS','INNER','OUTER','FULL','CROSS','UNION','ALL','LIMIT','OFFSET','DESC','ASC','COUNT','SUM','AVG','MAX','MIN','LIKE','IS','NULL','TRUE','FALSE','AUTO_INCREMENT','DEFAULT','CHARSET','ENGINE','DATABASE','SHOW','DESCRIBE','ALTER','DROP','INDEX','UNIQUE','CHECK','CONSTRAINT','FOREIGN','KEY','REFERENCES','CASCADE']
BASH_KW = ['cd','ls','pwd','mkdir','touch','rm','cp','mv','cat','more','head','tail','echo','clear','chmod','chown','grep','find','tar','wget','curl','ssh','scp','apt','yum','dnf','vim','vi','nano','man','history','whoami','df','du','ps','top','kill','ping','ifconfig','ip','systemctl','nginx','gunicorn','pip','python','python3','node','git','docker','make','sudo','su','exit','logout']

ALL_KW = PY_KW + SQL_KW + BASH_KW
KW_PAT = re.compile(r'\b(' + '|'.join(ALL_KW) + r')\b', re.IGNORECASE)
NUM_PAT = re.compile(r'\b(\d+\.?\d*)\b')
STR_PAT = re.compile(r"(f?\"\"\"[\s\S]*?\"\"\"|f?'''[\s\S]*?'''|f?\"(?:\\.|[^\"\\])*\"|f?'(?:\\.|[^'\\])*')")
CM_PAT = re.compile(r'(#[^\n]*)')
OP_PAT = re.compile(r'(@\w+)')

def clean_code(content):
    """将已高亮或已转义的代码块还原为纯文本代码。"""
    content = re.sub(r'<span class="(?:kw|str|cm|op|num)">', '', content)
    content = content.replace('</span>', '')
    return html_mod.unescape(content)


def highlight(code):
    """为代码块添加简单语法高亮，先转义源码再插入 span，避免 span 被当成源码显示。"""
    code = clean_code(code)
    token_pat = re.compile(
        r'(?P<str>f?"""[\s\S]*?"""|f?\'\'\'[\s\S]*?\'\'\'|f?"(?:\\.|[^"\\])*"|f?\'(?:\\.|[^\'\\])*\')'
        r'|(?P<cm>#[^\n]*)'
        r'|(?P<op>@\w+)'
        r'|(?P<kw>\b(' + '|'.join(ALL_KW) + r')\b)'
        r'|(?P<num>\b\d+\.?\d*\b)',
        re.IGNORECASE
    )

    result = []
    pos = 0
    for m in token_pat.finditer(code):
        if m.start() < pos:
            continue
        result.append(html_mod.escape(code[pos:m.start()]))
        cls = m.lastgroup
        result.append(f'<span class="{cls}">{html_mod.escape(m.group(0))}</span>')
        pos = m.end()
    result.append(html_mod.escape(code[pos:]))
    return ''.join(result)

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    def replace(m):
        content = m.group(1)
        if '<span class=' in content:
            return m.group(0)  # already highlighted
        highlighted = highlight(content)
        return f'<div class="code-block">{highlighted}</div>'

    new_html = re.sub(r'<div class="code-block">([^<]+(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*)</div>', replace, html, flags=re.DOTALL)

    # Also fix <pre> wrapped ones
    def replace_pre(m):
        content = m.group(1)
        if '<span class=' in content:
            return m.group(0)
        highlighted = highlight(content)
        return f'<div class="code-block">{highlighted}</div>'

    new_html = re.sub(r'<div class="code-block"><pre>(.*?)</pre></div>', replace_pre, new_html, flags=re.DOTALL)

    # Count
    highlighted = new_html.count('<span class="kw">')
    total_blocks = new_html.count('<div class="code-block">')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'{path.split(chr(92))[-1]}: {highlighted} spans, {total_blocks} blocks')

import os
base = os.path.join(os.path.dirname(__file__), '..', 'static')
for fname in sorted(os.listdir(base)):
    if fname.startswith('python_basic_test_') and fname.endswith('.html'):
        fix_file(os.path.join(base, fname))
