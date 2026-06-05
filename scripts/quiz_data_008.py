#!/usr/bin/env python3
"""练习 008 的题目数据。"""

choices = [
    {'qid': 1, 'question': '正则表达式最典型的用途，<strong>不恰当</strong>的选项是（ ）', 'options': ['在一大段文本中检索符合某种模式的子串', '对匹配到的子串做替换或提取', '代替 <code>if-else</code> 完成所有业务分支判断', '表单、日志、爬虫等场景中的格式校验与抽取'], 'answer': 'C', 'analysis': '正则表达式用于文本模式匹配，不能替代 if-else 做业务分支判断。'},
    {'qid': 2, 'question': '<code>re.match(pattern, string)</code> 的功能描述最准确的是（ ）', 'options': ['在整段字符串中查找<strong>任意位置</strong>的第一个匹配', '从字符串<strong>起始位置</strong>尝试匹配；失败则返回 <code>None</code>', '返回字符串中<strong>所有</strong>匹配到的子串列表', '自动忽略大小写并支持多行'], 'answer': 'B', 'analysis': '<code>re.match()</code> 从字符串开头位置尝试匹配，匹配失败返回 <code>None</code>。'},
    {'qid': 3, 'question': '<code>re.search(pattern, string)</code> 与 <code>re.match</code> 相比，主要区别是（ ）', 'options': ['<code>search</code> 必须从行首匹配', '<code>search</code> 可在<strong>整串</strong>中找<strong>第一个</strong>成功匹配，<code>match</code> 侧重<strong>开头</strong>', '<code>search</code> 返回的一定是列表', '二者没有任何区别'], 'answer': 'B', 'analysis': '<code>re.search()</code> 扫描整个字符串找第一个匹配，<code>re.match()</code> 只从字符串开头匹配。'},
    {'qid': 4, 'question': '<code>re.findall</code> 的返回值特点正确的是（ ）', 'options': ['匹配失败时一般抛异常', '匹配成功返回 <strong>列表</strong>；无匹配常返回空列表', '必须用 <code>.group()</code> 取结果', '固定返回一个 <code>Match</code> 对象'], 'answer': 'B', 'analysis': '<code>re.findall()</code> 返回所有匹配组成的列表，无匹配时返回空列表 <code>[]</code>。'},
    {'qid': 5, 'question': '下列 SQL 分类与用途对应<strong>错误</strong>的是（ ）', 'options': ['<strong>DDL</strong>：定义库、表、列等对象（如 <code>CREATE</code>、<code>ALTER</code>、<code>DROP</code>）', '<strong>DML</strong>：对表<strong>记录</strong>增删改（如 <code>INSERT</code>、<code>UPDATE</code>、<code>DELETE</code>）', '<strong>DQL</strong>：查询记录（以 <code>SELECT</code> 为主）', '<strong>DCL</strong>：专门用来执行 <code>SELECT</code> 排序与分组'], 'answer': 'D', 'analysis': 'DCL（Data Control Language）负责权限管理（如 GRANT、REVOKE），不是排序分组。'},
    {'qid': 6, 'question': '执行 <code>DELETE FROM 某表;</code>（<strong>没有</strong> <code>WHERE</code>）时，通常表示（ ）', 'options': ['只删除主键为 0 的行', '删除整张表中<strong>所有</strong>行，表结构仍保留', '语法错误，无法执行', '只删除重复行'], 'answer': 'B', 'analysis': '没有 WHERE 条件的 DELETE 会删除表中所有行，但表结构（列定义等）仍然保留。'},
    {'qid': 7, 'question': '关于<strong>主键（PRIMARY KEY）</strong>，正确的是（ ）', 'options': ['允许整列为 <code>NULL</code>', '用于<strong>唯一标识</strong>表中的一行，通常每张表至少有一个主键习惯设计', '一张表可以有任意多个主键列且彼此无要求', '主键与"外键"是同一个概念'], 'answer': 'B', 'analysis': '主键用于唯一标识表中一行，不可重复且非空，通常每张表设计一个主键。'},
    {'qid': 8, 'question': '<strong>外键</strong>的主要作用是（ ）', 'options': ['加快所有查询，替代索引', '对<strong>关系字段</strong>做约束，写入值需在关联表中存在（否则失败）', '禁止执行 <code>JOIN</code>', '只能关联本表自己'], 'answer': 'B', 'analysis': '外键约束保证引用完整性，要求子表的外键值必须在父表的主键中存在。'},
    {'qid': 9, 'question': '分组查询中，<code>SELECT</code> 后的字段一般应满足（ ）', 'options': ['任意写字段都可以', '<strong>出现在 <code>GROUP BY</code> 中的字段</strong>，或出现在<strong>聚合函数</strong>中', '只能写一个字段', '禁止使用聚合函数'], 'answer': 'B', 'analysis': '分组查询中，SELECT 的字段要么在 GROUP BY 中声明，要么必须包裹在聚合函数内。'},
    {'qid': 10, 'question': '<code>HAVING</code> 与 <code>WHERE</code> 的典型区别是（ ）', 'options': ['完全相同，可互换', '<code>WHERE</code> 对<strong>分组前</strong>的行过滤；<code>HAVING</code> 对<strong>分组聚合后</strong>的结果过滤，且 <code>HAVING</code> 侧<strong>可以</strong>用聚合函数', '<code>HAVING</code> 只能用于 <code>DELETE</code>', '<code>WHERE</code> 后面必须跟 <code>ORDER BY</code>'], 'answer': 'B', 'analysis': 'WHERE 在分组前过滤原始数据，HAVING 在分组聚合后过滤结果，HAVING 可以使用聚合函数。'},
]

fills = [
    {'qid': 11, 'question': '在 Python 中，<code>re</code> 模块三种常用匹配方式为 <code>match</code>、<code>search</code> 和 ________。', 'answer': 'findall', 'analysis': 're 模块三种常用匹配方式：match（开头匹配）、search（全文第一个匹配）、findall（返回所有匹配列表）。'},
    {'qid': 12, 'question': '<code>match</code>/<code>search</code> 匹配成功时常返回 <strong>Match 对象</strong>，取出匹配文本常用方法 ________（无分组时）。', 'answer': 'group()', 'analysis': 'Match 对象的 <code>.group()</code> 方法用于取出匹配文本，<code>.group(0)</code> 或 <code>.group()</code> 取完整匹配。'},
    {'qid': 13, 'question': '正则中量词默认多为 <strong>________</strong> 模式；在其后加 <strong><code>?</code></strong> 常表示 <strong>________</strong> 模式。', 'answer': '贪婪、非贪婪', 'analysis': '量词默认贪婪（尽可能多匹配），加 <code>?</code> 变为非贪婪（尽可能少匹配）。'},
    {'qid': 14, 'question': '小括号 <code>(...)</code> 在正则中常用于 <strong>________</strong>，便于后续按序号取出子串。', 'answer': '分组（捕获组）', 'analysis': '小括号用于创建捕获组，可通过 <code>.group(1)</code>、<code>.group(2)</code> 分别提取第一组、第二组匹配内容。'},
    {'qid': 15, 'question': '常见修饰符：<code>re.I</code> 表示忽略大小写；<code>re.S</code> 常使 <strong>.</strong> 能匹配包括 ________ 在内的更多情况（与默认"点"行为相关，按课堂理解填写）。', 'answer': '换行', 'analysis': '<code>re.S</code>（即 re.DOTALL）使 <code>.</code> 能匹配包括换行符在内的任意字符，默认情况下 <code>.</code> 不匹配换行。'},
    {'qid': 16, 'question': '数据库按存储形式大致分为关系型（表格行列）与 ________ 型（如键值、文档等）。', 'answer': '非关系（NoSQL）', 'analysis': '数据库分为关系型（如 MySQL）和非关系型（NoSQL，如 Redis、MongoDB）。'},
    {'qid': 17, 'question': '创建数据表属于 ________（填 <code>DDL</code> / <code>DML</code> / <code>DQL</code>）范畴。', 'answer': 'DDL', 'analysis': 'DDL（Data Definition Language）负责定义数据库对象，创建表属于 DDL。'},
    {'qid': 18, 'question': '更新表记录的典型格式：<code>UPDATE 表名 SET 字段=值 [________ 条件];</code>。', 'answer': 'WHERE', 'analysis': 'UPDATE 语句必须带 WHERE 条件，否则会更新整张表所有记录。'},
    {'qid': 19, 'question': '分页查询中限制返回行数的关键字常写为：<code>LIMIT</code>（搭配 <code>OFFSET</code> 或双参数写法，按你课堂笔记填写一种即可）________。', 'answer': 'LIMIT 10 或 LIMIT 0,10', 'analysis': 'MySQL 分页用 LIMIT m,n 表示从第 m 条开始取 n 条，或 LIMIT n 等价于 LIMIT 0,n。'},
    {'qid': 20, 'question': '多表查询时，把两张表按关联条件连成结果集的语句中常出现关键字 <strong>________</strong>。', 'answer': 'JOIN', 'analysis': '多表查询通过 JOIN 关键字将表按关联条件连接，如 INNER JOIN、LEFT JOIN 等。'},
]

shorts = [
    {'qid': 21, 'question': '用自己的话说明：正则表达式主要解决什么问题？在哪些场景会用到？', 'reference': '正则表达式用一套模式描述"长什么样"的字符串，用于在大文本里做检索、校验、替换、提取。常见场景包括：手机号/邮箱/身份证等格式校验、日志与文本解析、爬虫从网页中批量抽取链接或标签内容等。'},
    {'qid': 22, 'question': '对比说明 <code>re.match</code>、<code>re.search</code>、<code>re.findall</code> 的匹配范围、返回值以及是否需要 <code>.group()</code>。', 'reference': '<strong>match</strong>：从字符串开头匹配，成功返回 Match 对象，失败 None，取内容用 .group()（需先判空）。<strong>search</strong>：在整串里找第一个匹配，返回值与 group 用法类似。<strong>findall</strong>：找所有匹配，通常返回字符串列表（或按分组规则返回元组列表），一般不再对单个结果调 .group()。'},
    {'qid': 23, 'question': '什么是正则的"贪婪"与"非贪婪"？为什么爬虫抽取时往往要注意二者区别？', 'reference': '贪婪：量词默认尽量多匹配；非贪婪：在量词后加 ? 尽量少匹配。爬虫里若模式写得太贪婪，可能一次吃掉过多 HTML，拿不到想要的每条细粒度内容；适当用非贪婪可一段段匹配标题、链接等。'},
    {'qid': 24, 'question': '关系型数据库里"库、表、行、列"分别对应什么含义？各举一句生活类或商品类例子说明。', 'reference': '库：一类业务的数据集合（如 shop）。表：同一类实体的二维表（如 goods 商品表）。行：表中的一条记录（如一件具体商品）。列：记录的属性字段（如 name、price）。例：goods 表一行就是一款商品，各列是它的名称、价格等。'},
    {'qid': 25, 'question': '简述 <code>DDL</code>、<code>DML</code>、<code>DQL</code> 各管什么，并各举一个关键字。', 'reference': '<strong>DDL</strong>：定义数据库对象（库/表/列），如 CREATE、DROP、ALTER。<strong>DML</strong>：对表中数据行做增删改，如 INSERT、UPDATE、DELETE。<strong>DQL</strong>：查询数据，核心 SELECT。'},
    {'qid': 26, 'question': '什么时候用 <code>WHERE</code>，什么时候用 <code>HAVING</code>？能否在 <code>WHERE</code> 里直接写 <code>COUNT(*) > 5</code> 这类条件？为什么？', 'reference': 'WHERE 在分组前过滤原始行。HAVING 在 GROUP BY 与聚合之后对分组结果再过滤，且 HAVING 中可以使用聚合函数。一般不能在 WHERE 里直接写 COUNT(*) > 5，因为 WHERE 阶段尚未完成分组聚合，聚合值尚未形成；课堂顺序常记为：WHERE → GROUP BY → 聚合 → HAVING。'},
    {'qid': 27, 'question': '主键与外键有什么区别？外键约束带来的直接好处是什么？', 'reference': '主键：本表内唯一标识一行，不可重复且非空。外键：本表某列取值须引用另一张表主键（或唯一键）已存在的值。好处是：保证引用完整性，减少"孤儿数据"，让表间关系在插入/更新时由数据库强制检查。'},
]

writes = [
    {'qid': 28, 'title': 're 三种匹配方式对比（必做）', 'desc': '准备同一长字符串（含重复关键词），分别调用 re.match、re.search、re.findall，打印返回值类型及内容。用注释说明：为何有些情况 match 得到 None 而 search 仍能匹配。', 'reference': 'import re\n\ns = "我学 Python，你也学 Python 吗？"\np = "Python"\n\nm = re.match(p, s)\nprint("match:", m)  # None（开头不是 Python）\n\nsr = re.search(p, s)\nif sr:\n    print("search:", sr.group())  # Python\n\nfa = re.findall(p, s)\nprint("findall:", fa)  # ["Python", "Python"]'},
    {'qid': 29, 'title': '分组提取（必做）', 'desc': '写一条正则，从示例串中提取区号和本地号码（如 010-12345678）。使用分组，通过 Match 的 group(0/1/2) 分别打印整段匹配、第一组、第二组。', 'reference': 'import re\n\ns = "客服电话：010-12345678"\nr = re.search(r"(\\d{3,4})-(\\d{6,8})", s)\nif r:\n    print(r.group(0))  # 010-12345678\n    print(r.group(1))  # 010\n    print(r.group(2))  # 12345678'},
    {'qid': 30, 'title': 'MySQL 建库建表与插入（必做）', 'desc': '设计一张商品表（至少含：id 主键、name、price、category_id）。写出 CREATE TABLE（类型与约束合理）、至少 2 条 INSERT。', 'reference': 'CREATE TABLE goods (\n    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,\n    name VARCHAR(100) NOT NULL,\n    price DECIMAL(10,2) NOT NULL,\n    category_id INT UNSIGNED NOT NULL\n);\n\nINSERT INTO goods (name, price, category_id) VALUES ("苹果", 5.50, 1);\nINSERT INTO goods (name, price, category_id) VALUES ("牛奶", 12.00, 2);'},
    {'qid': 31, 'title': 'MySQL 单表条件、排序与分页（必做）', 'desc': '基于上一题的表，写一条 SELECT：带 WHERE（如价格区间或分类）、ORDER BY、LIMIT 只取前几条。注释说明：无 WHERE 的 UPDATE/DELETE 在生产环境的风险。', 'reference': 'SELECT id, name, price\nFROM goods\nWHERE price BETWEEN 5 AND 20\nORDER BY price DESC\nLIMIT 10;\n-- 无 WHERE 的 UPDATE/DELETE 易误伤全表，生产环境须谨慎'},
    {'qid': 32, 'title': 'MySQL 两表关联查询（重点必做）', 'desc': '再建一张分类表（id、category_name），商品表的 category_id 引用分类表 id。写一条多表 JOIN 查询：查出商品名、价格、分类名称。', 'reference': 'CREATE TABLE category (\n    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,\n    category_name VARCHAR(50) NOT NULL\n);\n\nINSERT INTO category (id, category_name)\nVALUES (1, "水果"), (2, "乳品");\n\nSELECT g.name, g.price, c.category_name\nFROM goods g\nJOIN category c ON g.category_id = c.id;'},
]

