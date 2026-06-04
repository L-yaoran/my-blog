#!/usr/bin/env python3
"""Generate python_basic_test_009.html (Day06 supplementary - regex + MySQL)"""
import re

choices = [
    {'qid': 1, 'question': '在 Python 中，正则表达式（Regular Expression）的主要作用是（ ）', 'options': ['操作系统的文件管理', '控制网页的样式表现', '描述字符串的匹配模式，用于检索、替换和提取子串', '连接和管理关系型数据库'], 'answer': 'C', 'analysis': '正则表达式用于描述字符串的匹配模式，进行检索、替换和提取子串。'},
    {'qid': 2, 'question': '使用 re 模块时，能够匹配任意数字（即0-9）的特殊字符是（ ）', 'options': ['\\d', '\\D', '\\w', '\\s'], 'answer': 'A', 'analysis': '\\d 匹配任意数字字符 0-9，\\D 匹配非数字，\\w 匹配字母数字下划线，\\s 匹配空白字符。'},
    {'qid': 3, 'question': '关于 re.match() 和 re.search() 的区别，下列说法正确的是（ ）', 'options': ['match 返回列表，search 返回对象', 'match 只能从字符串的起始位置进行匹配，search 扫描整个字符串并返回第一个成功匹配', '两者没有任何区别，可以混用', 'search 只能匹配一次，match 可以匹配多次'], 'answer': 'B', 'analysis': 're.match() 从字符串开头匹配，re.search() 扫描整个字符串返回第一个匹配。'},
    {'qid': 4, 'question': '在 MySQL 中，用于创建、修改、删除数据库或表等对象结构（如 CREATE、ALTER、DROP）的语句所属类别是（ ）', 'options': ['DML（数据操纵语言）', 'DQL（数据查询语言）', 'DDL（数据定义语言）', 'DCL（数据控制语言）'], 'answer': 'C', 'analysis': 'DDL（Data Definition Language）负责定义和管理数据库对象结构，如 CREATE、ALTER、DROP。'},
    {'qid': 5, 'question': '若要向 MySQL 数据表中插入一条新的数据记录，应该使用的关键字是（ ）', 'options': ['UPDATE', 'SELECT', 'INSERT', 'DELETE'], 'answer': 'C', 'analysis': 'INSERT INTO 用于向表中插入新记录。'},
    {'qid': 6, 'question': '在 SQL 查询中，GROUP BY 分组聚合后的结果如果需要进一步过滤，应该使用哪个关键字？（ ）', 'options': ['WHERE', 'HAVING', 'ORDER BY', 'LIMIT'], 'answer': 'B', 'analysis': 'HAVING 在 GROUP BY 聚合后对结果进行过滤，可以配合聚合函数使用。'},
    {'qid': 7, 'question': '关于 SQL 语句的执行顺序，下列正确的是（ ）', 'options': ['SELECT -> FROM -> WHERE', 'FROM -> WHERE -> GROUP BY -> SELECT', 'WHERE -> FROM -> ORDER BY', 'GROUP BY -> HAVING -> WHERE'], 'answer': 'B', 'analysis': 'SQL 执行顺序：FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT。'},
    {'qid': 8, 'question': '在正则表达式中，用来匹配前一个字符出现 1 次或者无限次（即至少有 1 次）的符号是（ ）', 'options': ['*', '?', '+', '{m}'], 'answer': 'C', 'analysis': '+ 匹配前一个字符 1 次或无限次（至少 1 次）。* 匹配 0 次或无限次，? 匹配 0 次或 1 次。'},
    {'qid': 9, 'question': '要查询 MySQL 商品表（goods）中所有商品的总数，最常用的聚合函数是（ ）', 'options': ['MAX()', 'SUM()', 'AVG()', 'COUNT()'], 'answer': 'D', 'analysis': 'COUNT() 用于统计行数/记录总数，MAX() 求最大值，SUM() 求和，AVG() 求平均值。'},
    {'qid': 10, 'question': '在进行多表查询时，能够返回左表的所有数据以及右表中满足关联条件的数据（右表不满足则填充 NULL）的连接方式是（ ）', 'options': ['内连接 (INNER JOIN)', '左外连接 (LEFT JOIN)', '右外连接 (RIGHT JOIN)', '全连接 (FULL JOIN)'], 'answer': 'B', 'analysis': 'LEFT JOIN 返回左表全部数据，右表中不满足条件的填充 NULL。'},
]

fills = [
    {'qid': 11, 'question': '在正则表达式中，匹配字符串开头的符号是________，匹配字符串结尾的符号是________。', 'answer': '^、$', 'analysis': '^ 匹配字符串开头，$ 匹配字符串结尾。'},
    {'qid': 12, 'question': '如果想提取正则表达式匹配到的特定部分数据，可以使用 () 将目标字符作为一个________。', 'answer': '分组', 'analysis': '小括号 () 用于创建捕获组，可通过 group(1)、group(2) 提取各组数据。'},
    {'qid': 13, 'question': '正则表达式中 .* 默认是________模式（尽可能多地匹配），如果在后面加上 ? 变成 .*?，则变成了________模式。', 'answer': '贪婪、非贪婪', 'analysis': '.* 默认贪婪（尽可能多匹配），.*? 非贪婪（尽可能少匹配）。'},
    {'qid': 14, 'question': 'MySQL 数据库默认的服务端口号通常是________。', 'answer': '3306', 'analysis': 'MySQL 默认监听 3306 端口。'},
    {'qid': 15, 'question': 'SQL 语句根据功能分类，SELECT 属于________语言（数据查询语言）。', 'answer': 'DQL', 'analysis': 'SELECT 是数据查询语言，属于 DQL（Data Query Language）。'},
    {'qid': 16, 'question': '如果要查询数据时消除重复的行，可以在 SELECT 后面加上________关键字。', 'answer': 'DISTINCT', 'analysis': 'DISTINCT 用于消除查询结果中的重复行。'},
    {'qid': 17, 'question': '在使用 ORDER BY 进行排序时，升序的关键字是________，降序的关键字是________。', 'answer': 'ASC、DESC', 'analysis': 'ORDER BY 升序用 ASC，降序用 DESC。'},
    {'qid': 18, 'question': '想要实现网页上的"分页效果"，在 SQL 中通常使用________关键字来限制查询的起始行和行数。', 'answer': 'LIMIT', 'analysis': 'LIMIT 用于限制返回的行数，可配合 OFFSET 实现分页。'},
    {'qid': 19, 'question': '在两张表建立多对多关系时，通常需要引入一张________表来记录两张表之间的数据联系。', 'answer': '中间关系（或关系表）', 'analysis': '多对多关系通过中间表（关联表）实现，记录两张表之间的对应关系。'},
    {'qid': 20, 'question': 're.findall(pattern, string) 方法如果在字符串中匹配不到任何结果，会返回一个________。', 'answer': '空列表（[]）', 'analysis': 're.findall() 无匹配时返回空列表 []，不会抛出异常。'},
]

shorts = [
    {'qid': 21, 'question': '请简述正则表达式中 *、+、? 这三个量词的具体匹配规则。', 'reference': '*：匹配前一个字符 0 次或无限次（可有可无）。+：匹配前一个字符 1 次或无限次（至少 1 次）。?：匹配前一个字符 0 次或 1 次（可选）。'},
    {'qid': 22, 'question': '什么是正则表达式的分组？在 re 模块中如何实现并提取分组的数据？', 'reference': '用 () 将正则表达式中的部分字符括起来作为一个分组。匹配成功后，可以使用 result.group(1)、result.group(2) 等按顺序提取对应括号内匹配到的独立数据。'},
    {'qid': 23, 'question': '简述 SQL 中 WHERE 和 HAVING 的核心区别。', 'reference': 'WHERE 是在分组（GROUP BY）前对数据进行过滤，且不能使用聚合函数；HAVING 是在分组后对聚合出来的结果进行过滤，可以使用聚合函数。'},
    {'qid': 24, 'question': '请列举关系型数据库中表与表之间的三种常见关系，并各举一个简单的例子。', 'reference': '(1) 一对多：商品分类表和商品表；(2) 多对多：学生表和课程表（需中间表）；(3) 一对一：用户基本信息表和身份证详情表。'},
    {'qid': 25, 'question': '什么是笛卡尔积（交叉连接）？在实际开发中为什么通常需要使用"有条件连接"（如内连接、左连接）来代替笛卡尔积？', 'reference': '笛卡尔积是将左表的每一行与右表的每一行无差别连接，结果行数是两表行数的乘积。在实际开发中，笛卡尔积结果数量庞大且含大量无意义组合，因此需要通过 ON 限定主外键关联条件的有条件连接来只保留满足逻辑关系的正确数据。'},
]

writes = [
    {'qid': 26, 'title': '正则表达式：手机号码验证', 'desc': '使用 re.match() 严格匹配以 1 开头、第二位 3-9、后面 9 位数字的手机号（^1[3-9]\\d{9}$），测试合法和非合法号码。', 'reference': 'import re\n\npattern = r"^1[3-9]\\d{9}$"\n\nresult1 = re.match(pattern, "13812345678")\nprint(result1.group() if result1 else "匹配失败")\n\nresult2 = re.match(pattern, "23812345678")\nprint(result2.group() if result2 else "匹配失败")'},
    {'qid': 27, 'title': '正则表达式：提取邮箱信息', 'desc': '使用 re.search() 和分组从"我的工作邮箱是 admin@heima.com，请查收。"中提取用户名和域名。', 'reference': 'import re\n\ntext = "我的工作邮箱是 admin@heima.com，请查收。"\npattern = r"([a-zA-Z0-9_]+)@([a-zA-Z0-9_]+\\.[a-zA-Z0-9_]+)"\n\nresult = re.search(pattern, text)\nif result:\n    print(f"完整邮箱: {result.group(0)}")\n    print(f"用户名: {result.group(1)}")\n    print(f"域名: {result.group(2)}")'},
    {'qid': 28, 'title': 'MySQL 基础：库与表的 DDL/DML 操作', 'desc': '创建 school_db 数据库和 students 表，包含 id、name、age 字段，完成 INSERT、UPDATE、DELETE 各一条。', 'reference': 'CREATE DATABASE IF NOT EXISTS school_db CHARSET=utf8;\nUSE school_db;\n\nCREATE TABLE students(\n    id INT PRIMARY KEY,\n    name VARCHAR(50) NOT NULL,\n    age INT\n);\n\nINSERT INTO students(id, name, age) VALUES(1, "张三", 20);\nUPDATE students SET age = 21 WHERE name = "张三";\nDELETE FROM students WHERE age > 25;'},
    {'qid': 29, 'title': 'MySQL 查询：单表综合查询', 'desc': '基于 products 表（id, name, price, category_id）完成：价格>100查询、分组统计、排序取前3。', 'reference': 'SELECT name, price FROM products WHERE price > 100;\n\nSELECT category_id, COUNT(*) FROM products GROUP BY category_id;\n\nSELECT * FROM products ORDER BY price DESC LIMIT 0, 3;'},
    {'qid': 30, 'title': 'MySQL 查询：多表关联查询', 'desc': '基于 users 和 orders 表，用 INNER JOIN 和 LEFT JOIN 查询用户订单。', 'reference': 'SELECT u.username, o.order_no\nFROM users u\nINNER JOIN orders o ON u.id = o.user_id;\n\nSELECT u.username, o.order_no\nFROM users u\nLEFT JOIN orders o ON u.id = o.user_id;'},
]

def gc(q):
    letters = 'ABCD'
    opts = '\n'.join(f'            <div class="option" data-opt="{letters[i]}" onclick="selectOption(this)">\n              <span class="option-letter">{letters[i]}</span> {o}\n            </div>' for i,o in enumerate(q['options']))
    return f'''    <div class="card" data-qid="{q["qid"]}" data-type="choice" data-answer="{q["answer"]}">
      <div class="card-header"><span class="card-qnum">第 {q["qid"]} 题</span><span class="card-type choice">单选题</span></div>
      <div class="card-question">{q["question"]}</div>
      <div class="options">
{opts}
      </div>
      <div class="feedback">
        <div class="result-tag correct-tag">正确</div>
        <strong>解析：</strong>{q["analysis"]}
      </div>
    </div>'''

def gf(q):
    qt = q['question'].replace('________', '<span class="blank-input" contenteditable="true"></span>')
    return f'''    <div class="card" data-qid="{q["qid"]}" data-type="fill" data-answer="{q["answer"]}">
      <div class="card-header"><span class="card-qnum">第 {q["qid"]} 题</span><span class="card-type fill">填空题</span></div>
      <div class="card-question">{qt}</div>
      <div class="feedback">
        <div class="result-tag correct-tag">正确</div>
        <strong>解析：</strong>{q["analysis"]}
      </div>
    </div>'''

def gs(q):
    return f'''    <div class="card" data-qid="{q["qid"]}" data-type="short" data-answer="">
      <div class="card-header"><span class="card-qnum">第 {q["qid"]} 题</span><span class="card-type short">简答题</span></div>
      <div class="card-question">{q["question"]}</div>
      <textarea class="fill-input" placeholder="请输入你的回答..." rows="3"></textarea>
      <span class="ref-toggle" onclick="toggleRef(this)">查看参考答案</span>
      <div class="ref-answer" style="margin-top:0.5rem; padding:0.6rem 0.8rem; background:var(--code-bg); border-radius:6px; font-size:0.85rem; line-height:1.6; color:var(--text);">{q["reference"]}</div>
      <div class="feedback"><div class="result-tag correct-tag">正确</div><strong>参考答案：</strong>{q["reference"]}</div>
    </div>'''

def gw(q):
    ref = q['reference'].replace('\\n', '\n')
    return f'''    <div class="card" data-qid="{q["qid"]}" data-type="write" data-answer="">
      <div class="card-header"><span class="card-qnum">第 {q["qid"]} 题</span><span class="card-type write">代码实战</span></div>
      <div class="card-question"><strong>{q["title"]}</strong></div>
      <div class="card-desc">{q["desc"]}</div>
      <textarea class="code-editor" placeholder="# 请在此编写你的代码..." rows="10"></textarea>
      <span class="ref-toggle" onclick="toggleRef(this)">查看参考答案</span>
      <div class="ref-answer"><div class="code-block">{ref}</div></div>
      <div class="feedback"><div class="result-tag correct-tag">正确</div><strong>参考答案：</strong><div class="code-block">{ref}</div></div>
    </div>'''

choice_cards = '\n'.join(gc(q) for q in choices)
fill_cards = '\n'.join(gf(q) for q in fills)
short_cards = '\n'.join(gs(q) for q in shorts)
write_cards = '\n'.join(gw(q) for q in writes)

total = len(choices) + len(fills) + len(shorts) + len(writes)
obj = len(choices) + len(fills)
subj = len(shorts) + len(writes)

with open('E:/AI_itheima/VS_code/my_blog/static/python_basic_test_008.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

sec_info = []
for i, l in enumerate(lines):
    if '<div class="section">' in l:
        depth = 0
        for k in range(i, len(lines)):
            depth += lines[k].count('<div')
            depth -= lines[k].count('</div>')
            if depth == 0 and k > i:
                sec_info.append((i, k))
                break

ranges = []
for idx, (sec_start, sec_end) in enumerate(sec_info):
    first_card = None
    for k in range(sec_start + 1, sec_end):
        if '<div class="card"' in lines[k]:
            first_card = k
            break
    ranges.append((first_card, sec_end))

new_cards_list = [choice_cards, fill_cards, short_cards, write_cards]
for (fc, ed), nc in sorted(zip(ranges, new_cards_list), key=lambda x: -x[0][0] if x[0][0] is not None else 999999):
    if fc is None: continue
    lines = lines[:fc] + nc.split('\n') + lines[ed:]

content = '\n'.join(lines)

content = content.replace('<title>LLM 练习 008</title>', '<title>LLM 练习 009</title>')
content = content.replace('<h1>LLM 练习 008</h1>', '<h1>LLM 练习 009</h1>')
content = content.replace('32 道题', f'{total} 道题')
content = content.replace("const STORAGE_KEY = 'py_day06_new_quiz_history';", "const STORAGE_KEY = 'py_day06_sup_quiz_history';")
content = content.replace("const SAVE_KEY = 'py_day06_new_saves';", "const SAVE_KEY = 'py_day06_sup_saves';")
content = content.replace('<span id="objDone">0</span>/20', f'<span id="objDone">0</span>/{obj}')
content = content.replace('<span id="subjDone">0</span>/12', f'<span id="subjDone">0</span>/{subj}')
content = content.replace('一、单选题（10 题）', f'一、单选题（{len(choices)} 题）')
content = content.replace('二、填空题（10 题）', f'二、填空题（{len(fills)} 题）')
content = content.replace('三、简答题（7 题）', f'三、简答题（{len(shorts)} 题）')
content = content.replace('四、代码实战（5 题）', f'四、代码实战（{len(writes)} 题）')

content = content.replace(
    '<a href="/static/python_basic_test_007.html" class="quiz-arrow" title="上一练习">◂</a>',
    '<a href="/static/python_basic_test_008.html" class="quiz-arrow" title="上一练习">◂</a>')
content = content.replace(
    '<a href="/static/python_basic_test_008.html" class="active">练习 008</a>',
    '<a href="/static/python_basic_test_008.html">练习 008</a>\n        <a href="/static/python_basic_test_009.html" class="active">练习 009</a>')
content = content.replace(
    '<span class="quiz-arrow disabled" title="已是最后一个">▸</span>',
    '<a href="/static/python_basic_test_009.html" class="quiz-arrow" title="下一练习">▸</a>')

out = 'E:/AI_itheima/VS_code/my_blog/static/python_basic_test_009.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

v = open(out, 'r', encoding='utf-8').read()
print(f'Output: {len(v)} chars, data-qid: {v.count("data-qid=")}, 练习 009: {"LLM 练习 009" in v}')
