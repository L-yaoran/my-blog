#!/usr/bin/env python3
"""Generate python_basic_test_011.html (Day09 NumPy + Pandas + Matplotlib)"""

choices = [
    {'qid': 1, 'question': 'Python 数据分析三剑客通常指（ ）', 'options': ['NumPy、Pandas、Matplotlib', 'Flask、Django、FastAPI', 'MySQL、Redis、MongoDB', 'HTML、CSS、JavaScript'], 'answer': 'A', 'analysis': '数据分析三剑客是 NumPy（数值计算）、Pandas（表格处理）、Matplotlib（数据可视化）。'},
    {'qid': 2, 'question': 'NumPy 的核心数据结构是（ ）', 'options': ['list', 'dict', 'ndarray', 'DataFrame'], 'answer': 'C', 'analysis': 'ndarray 是 NumPy 的多维数组对象，支持向量化运算，效率远高于 Python 列表。'},
    {'qid': 3, 'question': 'Pandas 中的二维表格结构是（ ）', 'options': ['Series', 'DataFrame', 'ndarray', 'tuple'], 'answer': 'B', 'analysis': 'DataFrame 是 Pandas 的二维表格结构，Series 是一维带标签数组。'},
    {'qid': 4, 'question': 'Matplotlib 主要用于（ ）', 'options': ['数据存储', '数据可视化', '网络请求', '任务调度'], 'answer': 'B', 'analysis': 'Matplotlib 是 Python 最常用的绑图库，支持折线图、柱状图、散点图等。'},
    {'qid': 5, 'question': 'arr.shape 表示（ ）', 'options': ['数组元素总数', '数组形状', '数组数据类型', '数组最大值'], 'answer': 'B', 'analysis': 'shape 返回数组的形状（各维度大小），如 (3,4) 表示 3 行 4 列。'},
    {'qid': 6, 'question': 'NumPy 中，逐元素乘法使用（ ）', 'options': ['*', '@', 'and', 'loc'], 'answer': 'A', 'analysis': '* 是逐元素乘法（对应位置相乘），@ 是矩阵乘法。'},
    {'qid': 7, 'question': 'Pandas 中按整数位置取数据使用（ ）', 'options': ['loc', 'iloc', 'groupby', 'plot'], 'answer': 'B', 'analysis': 'iloc 按整数位置索引，loc 按标签索引。'},
    {'qid': 8, 'question': 'Pandas 多条件筛选时，条件之间通常使用（ ）', 'options': ['and', 'or', '&', 'then'], 'answer': 'C', 'analysis': 'Pandas 多条件筛选用 &（与）和 |（或），每个条件必须加括号。'},
    {'qid': 9, 'question': 'df.groupby("dept")["sal"].mean() 的作用是（ ）', 'options': ['按部门计算平均工资', '删除部门列', '绘制部门图表', '修改部门名称'], 'answer': 'A', 'analysis': 'groupby 按部门分组，["sal"].mean() 计算每个部门的平均工资。'},
    {'qid': 10, 'question': '折线图更适合展示（ ）', 'options': ['趋势变化', '文件路径', '数据类型', '数据库密码'], 'answer': 'A', 'analysis': '折线图适合展示数据随时间或顺序的变化趋势。'},
]

fills = [
    {'qid': 11, 'question': 'NumPy 通常使用 import numpy as________导入。', 'answer': 'np', 'analysis': '约定俗成的别名是 np，如 import numpy as np。'},
    {'qid': 12, 'question': 'Pandas 通常使用 import pandas as________导入。', 'answer': 'pd', 'analysis': '约定俗成的别名是 pd，如 import pandas as pd。'},
    {'qid': 13, 'question': 'Matplotlib 的 pyplot 通常使用 import matplotlib.pyplot as________导入。', 'answer': 'plt', 'analysis': '约定俗成的别名是 plt，如 import matplotlib.pyplot as plt。'},
    {'qid': 14, 'question': 'NumPy 中，ndim 表示数组的________。', 'answer': '维度数', 'analysis': 'ndim 返回数组的维度数，如一维数组返回 1，二维数组返回 2。'},
    {'qid': 15, 'question': 'NumPy 中，size 表示数组的________。', 'answer': '元素总数', 'analysis': 'size 返回数组中元素的总数，不关心数组是几行几列。'},
    {'qid': 16, 'question': 'reshape 改变数组形状时，前后元素总数必须________。', 'answer': '相等', 'analysis': 'reshape 前后的元素总数必须一致，否则会报错。'},
    {'qid': 17, 'question': 'Pandas 中，Series 是________维带标签数组。', 'answer': '一', 'analysis': 'Series 是一维的，类似带标签的列表或字典。'},
    {'qid': 18, 'question': 'Pandas 中，DataFrame 是________维表格结构。', 'answer': '二', 'analysis': 'DataFrame 是二维的，有行索引和列名，类似 Excel 表格。'},
    {'qid': 19, 'question': '缺失值统计常用 isnull().________。', 'answer': 'sum()', 'analysis': 'isnull() 返回布尔值，sum() 统计 True 的个数，即缺失值数量。'},
    {'qid': 20, 'question': 'Matplotlib 中，展示图形窗口通常使用 plt.________。', 'answer': 'show', 'analysis': 'plt.show() 打开图形窗口展示绘制的图表。'},
]

shorts = [
    {'qid': 21, 'question': '请分别说明 NumPy、Pandas、Matplotlib 的作用。', 'reference': 'NumPy 用于高效数值计算，Pandas 用于表格数据处理，Matplotlib 用于数据可视化。'},
    {'qid': 22, 'question': 'NumPy 数组相比 Python 列表，在数据分析中有什么优势？', 'reference': 'NumPy 数组支持向量化运算，底层效率高，适合大批量数值计算。'},
    {'qid': 23, 'question': 'shape、size、dtype 分别表示什么？', 'reference': 'shape 表示数组形状，size 表示元素总数，dtype 表示元素数据类型。'},
    {'qid': 24, 'question': 'reshape 使用时最容易犯什么错误？', 'reference': '最容易犯的错误是新形状需要的元素数量和原数组元素数量不一致。'},
    {'qid': 25, 'question': '* 和 @ 在 NumPy 中有什么区别？', 'reference': '* 是逐元素乘法，@ 是矩阵乘法。'},
    {'qid': 26, 'question': 'axis=0 和 axis=1 在二维数组统计中分别表示什么？', 'reference': 'axis=0 通常得到每列统计结果，axis=1 通常得到每行统计结果。'},
    {'qid': 27, 'question': 'Series 和 DataFrame 有什么区别？', 'reference': 'Series 是一维带标签数组，DataFrame 是二维表格结构。'},
    {'qid': 28, 'question': 'loc 和 iloc 的核心区别是什么？', 'reference': 'loc 按标签取数据，iloc 按整数位置取数据。'},
    {'qid': 29, 'question': 'Pandas 多条件筛选为什么每个条件都要加括号？', 'reference': '因为 & 的优先级会影响表达式计算，每个条件加括号可以明确每个布尔条件的范围。'},
    {'qid': 30, 'question': '缺失值处理时，为什么不能无脑删除所有缺失行？', 'reference': '因为缺失值可能有业务含义，无脑删除可能丢失大量有效数据，应该根据业务选择删除或填充。'},
]

writes = [
    {'qid': 31, 'title': '模仿题 1：创建 NumPy 数组', 'desc': '创建一维数组 [10, 20, 30, 40]，打印它的维度、形状、元素总数。', 'reference': 'import numpy as np\n\narr = np.array([10, 20, 30, 40])\n\nprint("维度：", arr.ndim)\nprint("形状：", arr.shape)\nprint("元素总数：", arr.size)'},
    {'qid': 32, 'title': '模仿题 2：创建 DataFrame', 'desc': '创建一个员工 DataFrame，包含 name、dept、sal 三列，并打印表格。', 'reference': 'import pandas as pd\n\ndf = pd.DataFrame({\n    "name": ["张三", "李四", "王五"],\n    "dept": ["技术部", "销售部", "技术部"],\n    "sal": [5000, 7000, 6000]\n})\n\nprint(df)'},
    {'qid': 33, 'title': '模仿题 3：绘制简单折线图', 'desc': '用 Matplotlib 绘制 1-6 月销量折线图。', 'reference': 'import matplotlib\nmatplotlib.use("TkAgg")\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nplt.rcParams["font.sans-serif"] = ["SimHei"]\nplt.rcParams["axes.unicode_minus"] = False\n\nmonth = np.array([1, 2, 3, 4, 5, 6])\nsales = np.array([100, 120, 90, 150, 180, 200])\n\nplt.plot(month, sales, marker="o", label="销量")\nplt.title("1-6 月销量折线图")\nplt.xlabel("月份")\nplt.ylabel("销量")\nplt.grid()\nplt.legend()\nplt.show()'},
    {'qid': 34, 'title': '变体题 1：NumPy 每行求和', 'desc': '创建 3 行 3 列数组，分别计算每列总和和每行总和。', 'reference': 'import numpy as np\n\narr = np.array([[1, 2, 3],\n                [4, 5, 6],\n                [7, 8, 9]])\n\nprint("每列总和：", np.sum(arr, axis=0))\nprint("每行总和：", np.sum(arr, axis=1))'},
    {'qid': 35, 'title': '变体题 2：Pandas 条件筛选', 'desc': '读取 emp.txt，筛选工资大于 6000 的员工。', 'reference': 'import pandas as pd\n\ndf = pd.read_csv("emp.txt", sep="-")\n\nresult = df[df["sal"] > 6000]\n\nprint(result)'},
    {'qid': 36, 'title': '变体题 3：Pandas 分组统计', 'desc': '读取 emp.txt，按部门统计平均工资。', 'reference': 'import pandas as pd\n\ndf = pd.read_csv("emp.txt", sep="-")\n\nresult = df.groupby("dept")["sal"].mean()\n\nprint(result)'},
    {'qid': 37, 'title': '综合案例 1：员工筛选和排序', 'desc': '读取 emp.txt，筛选销售部员工，并按工资降序排序。', 'reference': 'import pandas as pd\n\ndf = pd.read_csv("emp.txt", sep="-")\n\nsales_df = df[df["dept"] == "销售部"]\n\nresult = sales_df.sort_values("sal", ascending=False)\n\nprint(result)'},
    {'qid': 38, 'title': '综合案例 2：销量数据分析和绘图', 'desc': '创建 1-6 月销量数据，使用 Pandas 保存为 DataFrame，计算平均销量，并用 Matplotlib 画折线图。', 'reference': 'import matplotlib\nmatplotlib.use("TkAgg")\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\nplt.rcParams["font.sans-serif"] = ["SimHei"]\nplt.rcParams["axes.unicode_minus"] = False\n\nmonth = np.array([1, 2, 3, 4, 5, 6])\nsales = np.array([100, 120, 90, 150, 180, 200])\n\ndf = pd.DataFrame({\n    "月份": month,\n    "销量": sales\n})\n\nprint("平均销量：", df["销量"].mean())\n\nplt.plot(df["月份"], df["销量"], marker="o", label="销量")\nplt.title("1-6 月销量趋势")\nplt.xlabel("月份")\nplt.ylabel("销量")\nplt.grid()\nplt.legend()\nplt.show()'},
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

with open('E:/AI_itheima/VS_code/my_blog/static/python_basic_test_010.html', 'r', encoding='utf-8') as f:
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

content = content.replace('<title>LLM 练习 010</title>', '<title>LLM 练习 011</title>')
content = content.replace('<h1>LLM 练习 010</h1>', '<h1>LLM 练习 011</h1>')
content = content.replace('38 道题', f'{total} 道题')
content = content.replace("const STORAGE_KEY = 'py_day08_quiz_history';", "const STORAGE_KEY = 'py_day09_quiz_history';")
content = content.replace("const SAVE_KEY = 'py_day08_saves';", "const SAVE_KEY = 'py_day09_saves';")
content = content.replace('<span id="objDone">0</span>/20', f'<span id="objDone">0</span>/{obj}')
content = content.replace('<span id="subjDone">0</span>/18', f'<span id="subjDone">0</span>/{subj}')
content = content.replace('一、单选题（10 题）', f'一、单选题（{len(choices)} 题）')
content = content.replace('二、填空题（10 题）', f'二、填空题（{len(fills)} 题）')
content = content.replace('三、简答题（10 题）', f'三、简答题（{len(shorts)} 题）')
content = content.replace('四、代码实战（8 题）', f'四、代码实战（{len(writes)} 题）')

# Navigation: prev=010, add 011 to dropdown, make 011 the last
content = content.replace(
    '<a href="/static/python_basic_test_009.html" class="quiz-arrow" title="上一练习">◂</a>',
    '<a href="/static/python_basic_test_010.html" class="quiz-arrow" title="上一练习">◂</a>')
content = content.replace(
    '<a href="/static/python_basic_test_010.html" class="active">练习 010</a>',
    '<a href="/static/python_basic_test_010.html">练习 010</a>\n        <a href="/static/python_basic_test_011.html" class="active">练习 011</a>')
content = content.replace(
    '<span class="quiz-arrow disabled" title="已是最后一个">▸</span>',
    '<span class="quiz-arrow disabled" title="已是最后一个">▸</span>')

out = 'E:/AI_itheima/VS_code/my_blog/static/python_basic_test_011.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

v = open(out, 'r', encoding='utf-8').read()
print(f'Output: {len(v)} chars, data-qid: {v.count("data-qid=")}, 练习 011: {"LLM 练习 011" in v}')
