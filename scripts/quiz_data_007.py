#!/usr/bin/env python3
"""练习 007 的题目数据。"""

choices = [
    {'qid': 1, 'question': '正则表达式最适合解决下面哪类问题？', 'options': ['计算两个整数之和', '从一段文本中提取所有手机号', '创建 MySQL 数据库', '绘制折线图'], 'answer': 'B', 'analysis': '正则表达式专门用于从文本中提取符合某种规则的内容，如手机号、邮箱、订单号等。'},
    {'qid': 2, 'question': 'Python 中使用正则表达式通常需要导入哪个模块？', 'options': ['os', 'sys', 're', 'math'], 'answer': 'C', 'analysis': '<code>re</code> 是 Python 内置的正则表达式模块，使用前需要 <code>import re</code>。'},
    {'qid': 3, 'question': '<code>re.match()</code> 的主要特点是？', 'options': ['从字符串开头尝试匹配', '扫描全文并返回所有结果', '只能匹配数字', '专门用于替换字符串'], 'answer': 'A', 'analysis': '<code>re.match()</code> 只从字符串开头位置尝试匹配，不扫描全文。'},
    {'qid': 4, 'question': '想从全文中找出所有 11 位数字，最适合使用哪个函数？', 'options': ['re.match()', 're.findall()', 'print()', 'len()'], 'answer': 'B', 'analysis': '<code>re.findall()</code> 扫描整个字符串，返回所有符合规则的非重叠匹配列表。'},
    {'qid': 5, 'question': '正则表达式中，<code>\\d</code> 表示什么？', 'options': ['任意空白字符', '任意数字', '任意字母', '字符串结尾'], 'answer': 'B', 'analysis': '<code>\\d</code> 表示匹配一个数字字符，等价于 <code>[0-9]</code>。'},
    {'qid': 6, 'question': '正则表达式中，<code>^1\\d{10}$</code> 更适合用于校验什么？', 'options': ['是否是完整的 11 位手机号格式', '是否包含任意数字', '是否包含空格', '是否是 SQL 语句'], 'answer': 'A', 'analysis': '<code>^1\\d{10}$</code> 要求字符串以 1 开头、后面正好 10 位数字，从头到尾完整匹配。'},
    {'qid': 7, 'question': '<code>.*</code> 和 <code>.*?</code> 的主要区别是？', 'options': ['.* 是非贪婪，.*? 是贪婪', '.* 默认尽可能多匹配，.*? 尽可能少匹配', '二者完全一样', '二者都只能匹配数字'], 'answer': 'B', 'analysis': '<code>.*</code> 是贪婪匹配，<code>.*?</code> 是非贪婪（最小匹配）。'},
    {'qid': 8, 'question': 'SQL 中，DDL 主要负责什么？', 'options': ['查询表中数据', '定义数据库和表结构', '控制 Python 循环', '清洗文本'], 'answer': 'B', 'analysis': 'DDL（Data Definition Language）用于创建、修改、删除数据库和表结构，如 CREATE、DROP、ALTER。'},
    {'qid': 9, 'question': '对表记录进行新增、修改、删除，主要属于哪类 SQL？', 'options': ['DDL', 'DML', 'DQL', 'DCL'], 'answer': 'B', 'analysis': 'DML（Data Manipulation Language）负责对表中数据进行新增（INSERT）、修改（UPDATE）、删除（DELETE）。'},
    {'qid': 10, 'question': '多表查询中，如果漏写连接条件，最容易出现什么问题？', 'options': ['查询速度一定变快', '产生大量错误组合，也就是笛卡尔积', '自动删除重复数据', '自动创建外键'], 'answer': 'B', 'analysis': '多表查询缺少 JOIN 条件时会产生笛卡尔积（所有记录两两组合），数据量成倍放大。'},
]

fills = [
    {'qid': 11, 'question': '正则表达式的核心作用是用一套规则去匹配一类（________）。', 'answer': '字符串', 'analysis': '正则表达式用一套规则描述一类字符串模式，用来匹配和提取文本。'},
    {'qid': 12, 'question': '<code>re.search()</code> 会扫描整个字符串，并返回第（________）个匹配成功的结果。', 'answer': '一', 'analysis': '<code>re.search()</code> 扫描整个字符串，找到第一个匹配就返回，不是返回所有。'},
    {'qid': 13, 'question': '<code>re.findall()</code> 的常见返回结果是一个（________）。', 'answer': '列表', 'analysis': '<code>re.findall()</code> 返回所有匹配组成的列表，无匹配时返回空列表。'},
    {'qid': 14, 'question': '正则表达式中，<code>\\s</code> 表示匹配（________）字符。', 'answer': '空白', 'analysis': '<code>\\s</code> 匹配空白字符，包括空格、制表符、换行符等。'},
    {'qid': 15, 'question': '正则表达式中，<code>{m,n}</code> 表示前一个字符出现（________）到（________）次。', 'answer': 'm、n', 'analysis': '<code>{m,n}</code> 表示前一个字符出现至少 m 次、至多 n 次，如 <code>{2,5}</code>。'},
    {'qid': 16, 'question': '在手机号完整校验中，<code>^</code> 表示字符串（________），<code>$</code> 表示字符串（________）。', 'answer': '开头、结尾', 'analysis': '<code>^</code> 锚定字符串开头，<code>$</code> 锚定字符串结尾，二者配合实现完整校验。'},
    {'qid': 17, 'question': '正则表达式中，使用（________）可以把匹配结果中的一部分单独提取出来。', 'answer': '分组', 'analysis': '分组用小括号 <code>()</code> 构成捕获组，从匹配结果中单独提取某部分内容。'},
    {'qid': 18, 'question': 'SQL 中，<code>SELECT</code> 语句属于（________）语言，主要用于查询数据。', 'answer': 'DQL', 'analysis': 'SELECT 属于 DQL（Data Query Language），专门用于从数据库中查询数据。'},
    {'qid': 19, 'question': '更新或删除数据时，如果忘记写（________）条件，可能会影响整张表。', 'answer': 'WHERE', 'analysis': '<code>UPDATE</code> 和 <code>DELETE</code> 没有 WHERE 条件时，会作用于全部记录。'},
    {'qid': 20, 'question': '多表查询的核心思想是把多张表按照关系连接成一张（________）结果表，再进行查询。', 'answer': '临时', 'analysis': '多表查询在内存中按连接条件生成临时结果集，再从中筛选数据。'},
]

shorts = [
    {'qid': 21, 'question': '正则表达式相比普通字符串查找强在哪里？', 'reference': '普通字符串查找只能匹配固定内容，正则表达式可以描述一类规则（如所有手机号、所有邮箱、所有日期）。它支持<strong>模糊匹配</strong>、<strong>字符类</strong>、<strong>数量词</strong>、<strong>边界定位</strong>等，这是普通字符串查找做不到的。'},
    {'qid': 22, 'question': '请说明 <code>re.match()</code>、<code>re.search()</code>、<code>re.findall()</code> 的区别。', 'reference': '<code>re.match()</code> 从字符串开头匹配，不成功返回 None；<code>re.search()</code> 扫描整个字符串，返回第一个匹配；<code>re.findall()</code> 扫描整个字符串，返回所有匹配组成的列表。'},
    {'qid': 23, 'question': '为什么手机号校验不能只写 <code>\\d+</code>？', 'reference': '<code>\\d+</code> 只表示一个或多个连续数字，不限制位数，也不限制字符串边界。12 位数字也会被匹配，含有非数字字符的字符串也会匹配出其中的数字片段。完整手机号校验需要 <code>^1\\d{10}$</code>。'},
    {'qid': 24, 'question': '什么是正则分组？它有什么用？', 'reference': '分组用小括号 <code>()</code> 把正则的一部分规则包起来。它可以从完整匹配中<strong>单独提取</strong>子部分，例如从日期字符串 <code>2026-06-01</code> 中分别提取年、月、日。也便于<strong>分组引用</strong>和<strong>替换</strong>。'},
    {'qid': 25, 'question': '贪婪模式和非贪婪模式有什么区别？', 'reference': '贪婪模式在匹配成功的前提下会<strong>尽可能多</strong>地匹配字符；非贪婪模式会<strong>尽可能少</strong>匹配，只到满足匹配条件的最小长度。常见例子：<code>.*</code>（贪婪）vs <code>.*?</code>（非贪婪）。'},
    {'qid': 26, 'question': 'RAG 文档清洗中，正则表达式可以用来做什么？', 'reference': '可以删除页码、页眉页脚、内部标记（如【内部资料】）、重复空行；也可以提取标题，时间、编号、URL 等结构化信息；还能清洗特殊符号，统一文本格式，为后续向量化和检索做准备。'},
    {'qid': 27, 'question': '数据库、数据表和字段之间是什么关系？', 'reference': '<strong>数据库</strong>是存储和管理数据的容器；<strong>数据表</strong>是数据库中某一类数据的结构；<strong>字段</strong>是表中的列，描述每条记录的属性。关系：数据库包含多张表，一张表包含多个字段。'},
    {'qid': 28, 'question': 'DDL、DML、DQL 分别负责什么？', 'reference': '<strong>DDL</strong>（Data Definition Language）负责定义和管理数据库及表结构：CREATE、DROP、ALTER。<strong>DML</strong>（Data Manipulation Language）负责对表数据进行增删改：INSERT、UPDATE、DELETE。<strong>DQL</strong>（Data Query Language）负责查询数据：SELECT。'},
    {'qid': 29, 'question': '为什么 <code>UPDATE</code> 和 <code>DELETE</code> 必须谨慎使用 <code>WHERE</code>？', 'reference': '没有 WHERE 条件的 UPDATE 或 DELETE 会作用于表中<strong>所有记录</strong>，导致全部数据被修改或清空。生产环境中这是极其危险的操作，可能造成不可逆的数据损失。'},
    {'qid': 30, 'question': '多表查询为什么重要？它解决什么问题？', 'reference': '真实业务中，数据通常分散在多张表中（如商品表和分类表）。多表查询通过表之间的关系（外键）把数据<strong>连接</strong>起来，生成完整结果，避免数据冗余和一致性问题。'},
]

writes = [
    {'qid': 31, 'title': '提取手机号（模仿）', 'desc': '使用正则表达式从文本中提取所有 11 位手机号。', 'reference': 'import re\\n\\ntext = "联系人A: 13800138000, 联系人B: 13900139000, 编号: A1001"\\nphones = re.findall(r"\\\\d{11}", text)\\nprint(phones)'},
    {'qid': 32, 'title': '创建学生表（模仿）', 'desc': '创建 student 表，包含 id（主键自增）、name（非空字符串）、age（整数）、score（decimal）。', 'reference': 'CREATE TABLE student (\\n    id INT PRIMARY KEY AUTO_INCREMENT,\\n    name VARCHAR(50) NOT NULL,\n    age INT,\n    score DECIMAL(5, 2)\\n);'},
    {'qid': 33, 'title': '查询指定列（模仿）', 'desc': '从 product 表中查询商品名称 name 和价格 price。', 'reference': 'SELECT name, price FROM product;'},
    {'qid': 34, 'title': '提取订单号（变体）', 'desc': '从文本中提取所有以 P 开头、后面跟 4 位数字的订单号。', 'reference': 'import re\\n\\ntext = "订单号: P1001, P2030, X999, P8888"\\norders = re.findall(r"P\\\\d{4}", text)\\nprint(orders)'},
    {'qid': 35, 'title': '完整校验手机号（变体）', 'desc': '判断列表中哪些是完整合法的 11 位手机号格式。', 'reference': 'import re\\n\\nphones = ["13800138000", "电话13800138000", "13800138000123", "13900139000"]\\nfor phone in phones:\\n    if re.match(r"^1\\\\d{10}$", phone):\\n        print(phone)'},
    {'qid': 36, 'title': '条件查询加排序（变体）', 'desc': '查询 product 表中价格大于 100 的商品，并按价格从高到低排序。', 'reference': 'SELECT * FROM product WHERE price > 100 ORDER BY price DESC;'},
    {'qid': 37, 'title': 'RAG 文档清洗（综合）', 'desc': '提取手机号、删除页码、内部标记、页脚，压缩重复空行。', 'reference': 'import re\\n\\nraw = """第 1 页\\\\n【内部资料】课程答疑记录\\\\n\\\\n学生手机号：13800138000\\\\n问题：re.match 和 re.search 有什么区别？\\\\n\\\\n\\\\n页脚：仅供学习"""\\n\\nphones = re.findall(r"\\\\d{11}", raw)\\ncleaned = re.sub(r"第\\\\s*\\\\d+\\\\s*页", "", raw)\\ncleaned = re.sub(r"【.*?】", "", cleaned)\\ncleaned = re.sub(r"页脚：.*", "", cleaned)\\ncleaned = re.sub(r"\\\\n{2,}", "\\\\n", cleaned).strip()\\nprint(phones)\\nprint(cleaned)'},
    {'qid': 38, 'title': '电商商品数据查询（综合）', 'desc': '基于 category 和 product 表完成：1.商品名称+价格+分类名；2.价格>平均价的商品；3.每个分类商品数量；4.库存最低的前3个商品。', 'reference': '-- 1. 商品名称、价格、分类名称（INNER JOIN）\\nSELECT p.name, p.price, c.name FROM product p INNER JOIN category c ON p.category_id = c.id;\\n\\n-- 2. 价格高于平均价的商品（子查询）\\nSELECT * FROM product WHERE price > (SELECT AVG(price) FROM product);\\n\\n-- 3. 每个分类商品数量（GROUP BY）\\nSELECT category_id, COUNT(*) AS product_count FROM product GROUP BY category_id;\\n\\n-- 4. 库存最低的前3个商品（ORDER BY + LIMIT）\\nSELECT * FROM product ORDER BY stock ASC LIMIT 0, 3;'},
]

