#!/usr/bin/env python3
"""Generate python_basic_test_010.html (Day08 PyMySQL + Redis)"""
import re

choices = [
    {'qid': 1, 'question': 'PyMySQL 的主要作用是（ ）', 'options': ['保存 MySQL 数据文件', '让 Python 连接并操作 MySQL', '替代 SQL 语句', '替代 Redis 服务'], 'answer': 'B', 'analysis': 'PyMySQL 是 Python 操作 MySQL 数据库的第三方库，负责连接 MySQL 并执行 SQL。'},
    {'qid': 2, 'question': '执行 SELECT 查询后，要把结果取回 Python，通常使用（ ）', 'options': ['commit()', 'rollback()', 'fetchall()', 'close()'], 'answer': 'C', 'analysis': 'fetchall() 用于获取查询结果的全部行。commit() 提交事务，rollback() 回滚，close() 关闭连接。'},
    {'qid': 3, 'question': '下列哪类 SQL 执行后通常需要 commit()？（ ）', 'options': ['SELECT', 'UPDATE', 'DESC 表名', 'SHOW DATABASES'], 'answer': 'B', 'analysis': 'UPDATE 会改变数据库内容，必须 commit() 后才真正保存。SELECT、DESC、SHOW 都是只读操作。'},
    {'qid': 4, 'question': 'rollback() 的作用是（ ）', 'options': ['提交事务', '撤销本次未提交的修改', '获取全部查询结果', '创建数据库连接'], 'answer': 'B', 'analysis': 'rollback() 撤销本次未提交的修改，常用于出错时回滚，保证数据一致性。'},
    {'qid': 5, 'question': 'Redis 主要基于（ ）读写，所以速度快', 'options': ['内存', '光盘', 'U 盘', '打印机'], 'answer': 'A', 'analysis': 'Redis 基于内存读写，速度远快于磁盘数据库，适合缓存和高速访问场景。'},
    {'qid': 6, 'question': 'pip install redis 安装的是（ ）', 'options': ['Redis 服务本身', 'Python 操作 Redis 的客户端库', 'MySQL 服务', 'PyMySQL'], 'answer': 'B', 'analysis': 'pip install redis 安装的是 redis-py，即 Python 操作 Redis 的客户端库，不是 Redis 服务本身。'},
    {'qid': 7, 'question': 'Redis 中适合做缓存和计数器的常见类型是（ ）', 'options': ['String', 'Hash', 'List', 'Set'], 'answer': 'A', 'analysis': 'Redis String 是最基本的数据类型，适合缓存、计数器、会话存储等场景。'},
    {'qid': 8, 'question': 'Redis 中适合存储用户对象多个字段的类型是（ ）', 'options': ['String', 'Hash', 'List', 'Sorted Set'], 'answer': 'B', 'analysis': 'Redis Hash 适合存储对象的多个字段，如用户信息（name、age、city）。'},
    {'qid': 9, 'question': 'Redis 中适合做排行榜的类型是（ ）', 'options': ['List', 'Set', 'Sorted Set', 'Hash'], 'answer': 'C', 'analysis': 'Sorted Set 每个成员都有分数，Redis 会按分数自动排序，天然适合排行榜场景。'},
    {'qid': 10, 'question': '缓存和会话数据通常需要设置（ ），避免长期占用内存或旧数据一直存在', 'options': ['主键', 'TTL 过期时间', 'SQL 语句', '外键'], 'answer': 'B', 'analysis': 'TTL（Time To Live）过期时间可以让 key 在指定时间后自动删除，避免内存浪费和旧数据残留。'},
]

fills = [
    {'qid': 11, 'question': 'PyMySQL 是 Python 操作________数据库的第三方库。', 'answer': 'MySQL', 'analysis': 'PyMySQL 是 Python 操作 MySQL 数据库的第三方库，提供连接、执行 SQL、获取结果等功能。'},
    {'qid': 12, 'question': '查询语句执行后，如果要获取全部结果，可以使用________方法。', 'answer': 'fetchall()', 'analysis': 'fetchall() 返回查询结果的所有行，每行是一个元组。'},
    {'qid': 13, 'question': 'INSERT、UPDATE、DELETE 会改变数据库内容，执行成功后通常需要________。', 'answer': 'commit()', 'analysis': '增删改操作必须 commit() 提交事务后，修改才会真正保存到数据库。'},
    {'qid': 14, 'question': '出错时撤销本次未提交修改，可以使用________。', 'answer': 'rollback()', 'analysis': 'rollback() 撤销当前事务中所有未提交的修改，常用于异常处理。'},
    {'qid': 15, 'question': '修改和删除语句必须写清楚________条件，避免误改或误删整张表。', 'answer': 'WHERE', 'analysis': 'UPDATE 和 DELETE 不带 WHERE 条件会影响全部记录，必须加上 WHERE 限定范围。'},
    {'qid': 16, 'question': 'Redis 是一种基于内存的________存储数据库。', 'answer': '键值对', 'analysis': 'Redis 是键值对（Key-Value）数据库，所有数据都以 key-value 形式存储。'},
    {'qid': 17, 'question': 'Python 操作 Redis 的客户端库通常叫 redis-py，安装命令是 pip install________。', 'answer': 'redis', 'analysis': 'pip install redis 安装的是 redis-py 客户端库，不是 Redis 服务本身。'},
    {'qid': 18, 'question': 'Redis 的 setex 可以设置值，并同时设置________时间。', 'answer': '过期', 'analysis': 'setex（Set EXpire）在设置值的同时指定过期秒数，到期后 key 自动删除。'},
    {'qid': 19, 'question': 'Redis 的 incr 常用于阅读数、点赞数等________场景。', 'answer': '计数', 'analysis': 'incr 对 key 的值加 1，原子操作，适合阅读量、点赞数等计数场景。'},
    {'qid': 20, 'question': 'Redis 的 ttl 用于查看 key 的剩余________时间。', 'answer': '生存', 'analysis': 'ttl（Time To Live）返回 key 的剩余生存时间，-1 表示永不过期，-2 表示已过期。'},
]

shorts = [
    {'qid': 21, 'question': '请说明 Python、PyMySQL、MySQL 三者关系。', 'reference': 'Python 负责业务逻辑，PyMySQL 负责连接 MySQL 并执行 SQL，MySQL 负责真正存储和管理数据。'},
    {'qid': 22, 'question': '为什么查询语句不需要 commit()，但增删改需要？', 'reference': '查询只是读取数据，不改变数据库内容，所以不需要提交；增删改会改变数据库内容，必须提交后才真正保存。'},
    {'qid': 23, 'question': 'fetchall() 和 commit() 分别适合什么场景？', 'reference': 'fetchall() 适合查询场景，用来把查询结果取回 Python；commit() 适合新增、删除、修改场景，用来提交事务。'},
    {'qid': 24, 'question': '为什么修改数据时要检查 row_count？', 'reference': '因为 row_count 可以确认本次操作影响了几行数据，避免没有修改到目标数据，或误改多行数据。'},
    {'qid': 25, 'question': '请用小明给小妹转账 520 的例子说明为什么需要事务。', 'reference': '转账 520 至少包含小明扣款和小妹加钱两步。如果小明扣款成功但小妹没收到，就出现数据错误。事务可以保证两步要么都成功，要么都失败。'},
    {'qid': 26, 'question': 'Redis 和 MySQL 的核心区别是什么？', 'reference': 'MySQL 是关系型数据库，适合存结构化核心数据，支持 SQL 和复杂查询；Redis 是基于内存的键值数据库，适合缓存、会话、计数、排行榜等高速访问场景。'},
    {'qid': 27, 'question': 'Redis 为什么常用于缓存？', 'reference': '因为 Redis 主要基于内存读写，速度快，适合保存热点数据，减少 MySQL 的重复查询压力。'},
    {'qid': 28, 'question': 'Redis 服务和 redis-py 有什么区别？', 'reference': 'Redis 服务是真正存储数据的数据库程序；redis-py 是 Python 操作 Redis 的客户端库。'},
    {'qid': 29, 'question': '请分别举例说明 Redis 的 String、Hash、List、Set、Sorted Set 适合什么场景。', 'reference': 'String 适合缓存和计数器；Hash 适合用户对象；List 适合任务队列；Set 适合去重和共同标签；Sorted Set 适合排行榜。'},
    {'qid': 30, 'question': '为什么缓存和会话通常要设置过期时间？', 'reference': '因为缓存和会话通常是临时数据，设置过期时间可以避免旧数据长期存在，也能减少 Redis 内存占用。'},
]

writes = [
    {'qid': 31, 'title': '模仿题 1：PyMySQL 查询 AI 工具', 'desc': '连接 ai_work_demo 数据库，查询 ai_tools 表中所有工具的 name 和 status。', 'reference': 'import pymysql\n\nconn = pymysql.connect(\n    host="127.0.0.1",\n    port=3306,\n    user="root",\n    password="123456",\n    database="ai_work_demo",\n    charset="utf8mb4"\n)\n\ncursor = conn.cursor()\n\ntry:\n    sql = "SELECT name, status FROM ai_tools;"\n    cursor.execute(sql)\n    rows = cursor.fetchall()\n\n    for name, status in rows:\n        status_text = "已启用" if status == 1 else "未启用"\n        print(f"工具：{name}，状态：{status_text}")\n\nfinally:\n    cursor.close()\n    conn.close()'},
    {'qid': 32, 'title': '模仿题 2：redis-py 连接测试', 'desc': '使用 redis-py 连接本机 Redis，执行 ping()，并设置 day08:name 为张三。', 'reference': 'import redis\n\nr = redis.Redis(\n    host="localhost",\n    port=6379,\n    db=0,\n    decode_responses=True\n)\n\ntry:\n    print(r.ping())\n    r.set("day08:name", "张三")\n    print(r.get("day08:name"))\n\nfinally:\n    r.close()'},
    {'qid': 33, 'title': '模仿题 3：Redis String 计数器', 'desc': '使用 Redis String 记录文章 1001 的阅读数，初始化为 0，然后自增 3 次。', 'reference': 'import redis\n\nr = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)\n\ntry:\n    view_key = "day08:article:1001:views"\n    r.set(view_key, "0")\n    r.incr(view_key)\n    r.incr(view_key)\n    r.incr(view_key)\n    print("当前阅读数：", r.get(view_key))\n\nfinally:\n    r.close()'},
    {'qid': 34, 'title': '变体题 1：PyMySQL 启用 LangChain', 'desc': '把 MySQL 中 LangChain 的状态从未启用改成已启用，要求使用 commit() 和 rollback()。', 'reference': 'import pymysql\n\nconn = pymysql.connect(\n    host="127.0.0.1",\n    port=3306,\n    user="root",\n    password="123456",\n    database="ai_work_demo",\n    charset="utf8mb4"\n)\n\ncursor = conn.cursor()\n\ntry:\n    sql = "UPDATE ai_tools SET status = %s WHERE name = %s AND status = %s;"\n    params = (1, "LangChain", 0)\n    row_count = cursor.execute(sql, params)\n\n    if row_count != 1:\n        raise Exception(f"期望修改 1 行，实际修改了 {row_count} 行")\n\n    conn.commit()\n    print("LangChain 已启用")\n\nexcept Exception as error:\n    conn.rollback()\n    print("启用失败，已回滚：", error)\n\nfinally:\n    cursor.close()\n    conn.close()'},
    {'qid': 35, 'title': '变体题 2：Redis Hash 存储用户信息', 'desc': '使用 Redis Hash 保存用户 user:2001 的 name、age、city，并打印完整用户信息。', 'reference': 'import redis\n\nr = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)\n\ntry:\n    user_key = "day08:user:2001"\n    r.hset(user_key, mapping={\n        "name": "王五",\n        "age": "28",\n        "city": "广州"\n    })\n    print(r.hgetall(user_key))\n\nfinally:\n    r.close()'},
    {'qid': 36, 'title': '变体题 3：Redis Set 做标签去重', 'desc': '向 Redis Set 中添加 python、redis、python、ai 四个标签，观察去重效果。', 'reference': 'import redis\n\nr = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)\n\ntry:\n    tag_key = "day08:tags"\n    r.delete(tag_key)\n    r.sadd(tag_key, "python", "redis", "python", "ai")\n    print(r.smembers(tag_key))\n\nfinally:\n    r.close()'},
    {'qid': 37, 'title': '综合案例 1：MySQL 查询 + Redis 缓存', 'desc': '先用 PyMySQL 查询 ai_tools 表中已启用的工具；再把查询结果写入 Redis，key 为 day08:enabled_tools，设置 60 秒过期时间。', 'reference': 'import json\nimport pymysql\nimport redis\n\nmysql_conn = pymysql.connect(\n    host="127.0.0.1",\n    port=3306,\n    user="root",\n    password="123456",\n    database="ai_work_demo",\n    charset="utf8mb4"\n)\nmysql_cursor = mysql_conn.cursor()\nredis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)\n\ntry:\n    sql = "SELECT name, scene FROM ai_tools WHERE status = %s;"\n    mysql_cursor.execute(sql, (1,))\n    rows = mysql_cursor.fetchall()\n\n    enabled_tools = []\n    for name, scene in rows:\n        enabled_tools.append({"name": name, "scene": scene})\n\n    cache_key = "day08:enabled_tools"\n    redis_client.setex(cache_key, 60, json.dumps(enabled_tools, ensure_ascii=False))\n    print("已启用工具已写入 Redis 缓存：", enabled_tools)\n\nfinally:\n    mysql_cursor.close()\n    mysql_conn.close()\n    redis_client.close()'},
    {'qid': 38, 'title': '综合案例 2：Redis 排行榜', 'desc': '使用 Redis Sorted Set 保存 AI 工具热度榜：ChatGPT 1000 分，DeepSeek 900 分，Dify 800 分；查询并打印热度从高到低的排行榜。', 'reference': 'import redis\n\nr = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)\n\ntry:\n    rank_key = "day08:ai_tool_hot_rank"\n    r.delete(rank_key)\n\n    r.zadd(rank_key, {\n        "ChatGPT": 1000,\n        "DeepSeek": 900,\n        "Dify": 800\n    })\n\n    ranks = r.zrevrange(rank_key, 0, -1, withscores=True)\n\n    for index, (tool_name, score) in enumerate(ranks, start=1):\n        print(f"第 {index} 名：{tool_name}，热度：{score}")\n\nfinally:\n    r.close()'},
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

with open('E:/AI_itheima/VS_code/my_blog/static/python_basic_test_009.html', 'r', encoding='utf-8') as f:
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

content = content.replace('<title>LLM 练习 009</title>', '<title>LLM 练习 010</title>')
content = content.replace('<h1>LLM 练习 009</h1>', '<h1>LLM 练习 010</h1>')
content = content.replace('30 道题', f'{total} 道题')
content = content.replace("const STORAGE_KEY = 'py_day06_sup_quiz_history';", "const STORAGE_KEY = 'py_day08_quiz_history';")
content = content.replace("const SAVE_KEY = 'py_day06_sup_saves';", "const SAVE_KEY = 'py_day08_saves';")
content = content.replace('<span id="objDone">0</span>/20', f'<span id="objDone">0</span>/{obj}')
content = content.replace('<span id="subjDone">0</span>/10', f'<span id="subjDone">0</span>/{subj}')
content = content.replace('一、单选题（10 题）', f'一、单选题（{len(choices)} 题）')
content = content.replace('二、填空题（10 题）', f'二、填空题（{len(fills)} 题）')
content = content.replace('三、简答题（5 题）', f'三、简答题（{len(shorts)} 题）')
content = content.replace('四、代码实战（5 题）', f'四、代码实战（{len(writes)} 题）')

# Navigation: prev=009, add 010 to dropdown, make 010 the last
content = content.replace(
    '<a href="/static/python_basic_test_008.html" class="quiz-arrow" title="上一练习">◂</a>',
    '<a href="/static/python_basic_test_009.html" class="quiz-arrow" title="上一练习">◂</a>')
content = content.replace(
    '<a href="/static/python_basic_test_009.html" class="active">练习 009</a>',
    '<a href="/static/python_basic_test_009.html">练习 009</a>\n        <a href="/static/python_basic_test_010.html" class="active">练习 010</a>')
content = content.replace(
    '<span class="quiz-arrow disabled" title="已是最后一个">▸</span>',
    '<span class="quiz-arrow disabled" title="已是最后一个">▸</span>')

out = 'E:/AI_itheima/VS_code/my_blog/static/python_basic_test_010.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

v = open(out, 'r', encoding='utf-8').read()
print(f'Output: {len(v)} chars, data-qid: {v.count("data-qid=")}, 练习 010: {"LLM 练习 010" in v}')
