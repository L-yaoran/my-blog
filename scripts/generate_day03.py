"""
Generate python_basic_test_003.html from Day03 homework markdown,
using python_basic_test_002.html as the structural template.
"""
import re

# Read Day02 template
with open(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_002.html', 'r', encoding='utf-8') as f:
    template = f.read()

# ============================================================
# Day03 Question Data
# ============================================================

# --- 单选题 (10题) ---
choices = [
    {'qid': 1, 'question': '闭包的三大构成条件是（ ）。',
     'options': [
         'A. 有循环、有判断、有返回',
         'B. 有嵌套、有引用、有返回',
         'C. 有参数、有注释、有调用',
         'D. 有类、有对象、有继承'],
     'answer': 'B',
     'analysis': '闭包三条件：有嵌套（外部函数包含内部函数）、有引用（内部函数引用外部变量）、有返回（外部函数返回内部函数名）。'},
    {'qid': 2, 'question': '下列属于闭包语法核心的是（ ）。',
     'options': [
         'A. 外部函数返回内部函数名',
         'B. 内部函数必须无参',
         'C. 外部函数必须是全局函数',
         'D. 内部函数必须使用 global'],
     'answer': 'A',
     'analysis': '闭包的核心是外部函数返回内部函数名（函数引用），这样外部才能调用内部函数并保留闭包环境。'},
    {'qid': 3, 'question': '闭包最典型的作用是（ ）。',
     'options': [
         'A. 提高网络速度',
         'B. 保存外层变量并延长其生命周期',
         'C. 自动生成类',
         'D. 替代 if 判断'],
     'answer': 'B',
     'analysis': '闭包让内部函数持有外层变量的引用，即使外层函数执行完毕，变量仍不会销毁，延长了其生命周期。'},
    {'qid': 4, 'question': '在内部函数中修改外层（非全局）变量应使用（ ）。',
     'options': [
         'A. <code>global</code>',
         'B. <code>nonlocal</code>',
         'C. <code>static</code>',
         'D. <code>lambda</code>'],
     'answer': 'B',
     'analysis': '<code>nonlocal</code> 用于在内部函数中声明要修改的外层（非全局）变量，<code>global</code> 用于全局变量。'},
    {'qid': 5, 'question': '装饰器的本质是（ ）。',
     'options': [
         'A. 继承',
         'B. 闭包函数',
         'C. 递归函数',
         'D. 抽象类'],
     'answer': 'B',
     'analysis': '装饰器本质是一个接收函数、返回新函数的闭包，利用闭包特性在原函数基础上增加额外功能。'},
    {'qid': 6, 'question': '装饰器的核心价值是（ ）。',
     'options': [
         'A. 修改原函数源码实现增强',
         'B. 不改原函数源码给函数增加额外功能',
         'C. 让函数无法调用',
         'D. 只能装饰无参函数'],
     'answer': 'B',
     'analysis': '装饰器的核心价值是"不改原函数源码"的前提下给函数增加额外功能，遵循开闭原则。'},
    {'qid': 7, 'question': '下列与 <code>@check</code> 等价的写法是（ ）。',
     'options': [
         'A. <code>check = check(func)</code>',
         'B. <code>func = @check(func)</code>',
         'C. <code>func = check(func)</code>',
         'D. <code>@func = check</code>'],
     'answer': 'C',
     'analysis': '<code>@check</code> 语法糖等价于 <code>func = check(func)</code>，即把被装饰函数传给装饰器，用返回值替换原函数。'},
    {'qid': 8, 'question': '多个装饰器装饰同一个函数时，正确描述是（ ）。',
     'options': [
         'A. 离函数最远的先装饰',
         'B. 离函数最近的先装饰',
         'C. 先写的先执行原函数',
         'D. 顺序固定与书写无关'],
     'answer': 'B',
     'analysis': '多个装饰器叠加时，离函数最近的（最下面）先装饰，执行时也先进入内层包装。'},
    {'qid': 9, 'question': '通用装饰器适配各种函数签名，推荐内部函数参数写为（ ）。',
     'options': [
         'A. <code>a, b</code>',
         'B. <code>x</code>',
         'C. <code>*args, **kwargs</code>',
         'D. 无参数'],
     'answer': 'C',
     'analysis': '<code>*args, **kwargs</code> 可以接收任意位置参数和关键字参数，使装饰器能适配各种函数签名。'},
    {'qid': 10, 'question': '带参数装饰器 <code>@logging(\"+\")</code> 通常需要（ ）。',
     'options': [
         'A. 一层函数',
         'B. 两层函数',
         'C. 三层函数',
         'D. 不需要函数'],
     'answer': 'C',
     'analysis': '带参数装饰器需要三层：最外层收装饰器参数，中间层收函数，最内层做包装。（外层收参数→中层收函数→内层做包装）'},
]

# --- 填空题 (10题) ---
fills = [
    {'qid': 11, 'question': '闭包定义中，外层函数返回的是内部函数的（<span class="blank" contenteditable="true"></span>），而不是执行结果。',
     'answer': '函数名（函数地址）',
     'analysis': '外层函数通过 <code>return func_inner</code> 返回内部函数的引用（函数名），而不是调用结果 <code>func_inner()</code>。'},
    {'qid': 12, 'question': '闭包三条件是有嵌套、有引用、有（<span class="blank" contenteditable="true"></span>）。',
     'answer': '返回',
     'analysis': '闭包三条件：有嵌套（外部含内部）、有引用（内部引用外部变量）、有返回（外部返回内部函数）。'},
    {'qid': 13, 'question': '在内部函数中修改外层变量时，需先用关键字（<span class="blank" contenteditable="true"></span>）声明。',
     'answer': 'nonlocal',
     'analysis': '<code>nonlocal</code> 告诉 Python 解释器"我要修改的是外层函数的变量，不是新建局部变量"。'},
    {'qid': 14, 'question': '装饰器是"接收函数并返回新函数"的一种（<span class="blank" contenteditable="true"></span>）。',
     'answer': '闭包',
     'analysis': '装饰器本质上是一种特殊的闭包，接收函数作为参数，返回增强后的新函数。'},
    {'qid': 15, 'question': '装饰器语法糖 <code>@deco</code> 等价于 <code>函数名 = （<span class="blank" contenteditable="true"></span>）</code>。',
     'answer': 'deco(函数名)',
     'analysis': '<code>@deco</code> 装饰 <code>func</code> 等价于 <code>func = deco(func)</code>，是语法层面的简化写法。'},
    {'qid': 16, 'question': '当原函数有返回值时，装饰器内部函数也应（<span class="blank" contenteditable="true"></span>）原函数结果。',
     'answer': '返回（return）',
     'analysis': '为保持原函数行为，装饰器内部函数必须 <code>return</code> 被装饰函数的返回值，否则会丢失数据。'},
    {'qid': 17, 'question': '多个装饰器修饰同一函数时，装饰过程是由（<span class="blank" contenteditable="true"></span>）到（<span class="blank" contenteditable="true"></span>）。',
     'answer': '内；外',
     'analysis': '装饰顺序由内到外（离函数最近的先装饰），但包裹后执行顺序也先进入最内层包装。'},
    {'qid': 18, 'question': '通用装饰器常见模板中，参数接收写成（<span class="blank" contenteditable="true"></span>）与（<span class="blank" contenteditable="true"></span>）。',
     'answer': '*args；**kwargs',
     'analysis': '<code>*args</code> 接收任意位置参数，<code>**kwargs</code> 接收任意关键字参数，确保装饰器通用性。'},
    {'qid': 19, 'question': '带参数装饰器语法糖通常是"外层收参数，中层收函数，内层做包装"的（<span class="blank" contenteditable="true"></span>）层结构。',
     'answer': '三',
     'analysis': '带参数装饰器需要三层嵌套：最外层接收装饰器参数 → 中间层接收函数 → 最内层实现包装逻辑。'},
    {'qid': 20, 'question': '装饰器常见业务场景包括日志、权限、（<span class="blank" contenteditable="true"></span>）统计。',
     'answer': '耗时',
     'analysis': '装饰器典型场景：登录校验、权限控制、日志记录、耗时统计、异常兜底等。'},
]

# --- 简答题 (6题) ---
shorts = [
    {'qid': 21, 'question': '用自己的话解释"为什么闭包能让外层变量在函数结束后仍可用"。',
     'answer': '内部函数持续引用外层变量,导致变量随闭包一起被保留,生命周期被延长',
     'reference': '内部函数持续引用外层变量，导致变量随闭包一起被保留，不会被垃圾回收，生命周期被延长。'},
    {'qid': 22, 'question': '<code>global</code> 和 <code>nonlocal</code> 有什么本质区别？分别作用于哪一层变量？',
     'answer': 'global操作全局变量,nonlocal操作外层函数非全局变量',
     'reference': '<code>global</code> 操作全局变量（模块级别），<code>nonlocal</code> 操作外层函数（非全局）变量。两者作用域层级不同。'},
    {'qid': 23, 'question': '为什么说"所有装饰器都是闭包，但不是所有闭包都是装饰器"？',
     'answer': '装饰器满足闭包结构且必须接收函数并增强返回,普通闭包不一定增强函数',
     'reference': '装饰器满足闭包结构（嵌套+引用+返回）且必须"接收函数并增强返回"。普通闭包不一定接收函数，也不一定增强行为。'},
    {'qid': 24, 'question': '装饰器在企业开发中有哪些典型应用场景？至少举 3 个。',
     'answer': '登录校验,权限控制,日志记录,耗时统计,异常兜底',
     'reference': '常见场景：登录校验、权限控制、日志记录、耗时统计、异常兜底。装饰器是 AOP（面向切面编程）在 Python 中的重要实现。'},
    {'qid': 25, 'question': '多个装饰器叠加时，书写顺序和执行顺序如何理解？',
     'answer': '书写从上到下,装饰从内到外,离函数最近的先装饰',
     'reference': '书写从上到下，装饰从内到外；离函数最近的先装饰，执行链也先进入内层包装。例如 <code>@deco1 @deco2</code>，deco2 先装饰。'},
    {'qid': 26, 'question': '为什么通用装饰器必须关注"参数对齐 + 返回值对齐"？',
     'answer': '不对齐会导致参数丢失或返回值被吞,破坏原函数行为',
     'reference': '不对齐会导致参数丢失或返回值被吞，原函数行为被破坏。通用装饰器必须用 <code>*args, **kwargs</code> 保证参数通透，用 <code>return</code> 保证返回值不丢失。'},
]

# --- 代码实操 (8题) ---
writes = [
    {'qid': 27, 'title': '闭包基础（必做）',
     'desc': '定义外部函数 <code>func_out(num1)</code>，内部函数 <code>func_inner(num2)</code>。<br>内部函数使用外部变量完成求和并打印。<br>外部函数返回内部函数，创建闭包并调用。<br>解释每一行如何对应"有嵌套/有引用/有返回"三条件。',
     'answer': '''def func_out(num1):
    def func_inner(num2):
        # 内部函数引用了外层变量 num1 ——"有引用"
        print("结果:", num1 + num2)
    # 外部函数返回内部函数名 ——"有返回"
    return func_inner

# 创建闭包：num1=10 被内部函数"记住"
f = func_out(10)
# 调用闭包，num2=5
f(5)   # 输出：结果: 15''',
     'expected': '定义func_out外函数嵌套func_inner内函数（有嵌套），内函数引用外变量num1（有引用），外函数返回内函数名（有返回），创建闭包调用'},
    {'qid': 28, 'title': 'nonlocal 闭包计数器（必做）',
     'desc': '编写 <code>counter()</code>，外层定义 <code>count = 0</code>。<br>内层函数每调用一次 <code>count + 1</code> 并返回新值。<br>必须使用 <code>nonlocal</code>，并连续调用至少 3 次验证状态被保存。',
     'answer': '''def counter():
    count = 0
    def add_one():
        # nonlocal 声明要修改外层变量
        nonlocal count
        count += 1
        return count
    return add_one

c = counter()
print(c(), c(), c())  # 输出: 1 2 3''',
     'expected': '定义counter外函数，count=0，内函数使用nonlocal累加count，返回内函数，连续调用3次验证状态保持'},
    {'qid': 29, 'title': '装饰器原始写法与语法糖（必做）',
     'desc': '定义登录校验装饰器 <code>check</code>。<br>用原始方式 <code>comment = check(comment)</code> 装饰一次。<br>再用 <code>@check</code> 语法糖装饰另一个函数。<br>对比两种写法并在注释中写出"等价关系"。',
     'answer': '''def check(fn):
    def inner():
        print("请先登录")
        fn()
    return inner

def comment():
    print("发表评论")

# 原始方式：手动调用装饰器
comment = check(comment)
comment()

# 语法糖方式：@check 等价于 like = check(like)
@check
def like():
    print("点赞")
like()''',
     'expected': '定义check装饰器，用原始方式comment=check(comment)和语法糖@check分别装饰两个函数，注释等价关系'},
    {'qid': 30, 'title': '通用装饰器（重点必做）',
     'desc': '编写一个通用装饰器，内部函数使用 <code>*args, **kwargs</code>。<br>要求可装饰四类函数：1) 无参无返回 2) 有参无返回 3) 无参有返回 4) 有参有返回（含关键字参数）。<br>演示调用结果，证明"参数和返回值都不丢失"。',
     'answer': '''def universal_decorator(func):
    def inner(*args, **kwargs):
        print(">>> 增强逻辑开始")
        # 透传所有参数并接收返回值
        result = func(*args, **kwargs)
        print(">>> 增强逻辑结束")
        # 必须 return 保证返回值不丢失
        return result
    return inner

# 测试四类函数
@universal_decorator
def test1(): print("无参无返回")
@universal_decorator
def test2(name): print(f"有参: {name}")
@universal_decorator
def test3(): return "有返回"
@universal_decorator
def test4(a, b, c=0): return a + b + c

test1()
test2("张三")
print(test3())  # 输出: 有返回
print(test4(1, 2, c=3))  # 输出: 6''',
     'expected': '定义通用装饰器使用*args/**kwargs透传参数并return返回值，测试四类函数证明参数和返回值不丢失'},
    {'qid': 31, 'title': '多装饰器执行顺序（重点必做）',
     'desc': '定义两个装饰器 <code>deco1</code>、<code>deco2</code>，分别打印"前/后"日志。<br>同时装饰一个函数，观察执行顺序。<br>用注释写清楚：谁先装饰、谁先执行。',
     'answer': '''def deco1(fn):
    def inner():
        print("deco1 前")
        fn()
        print("deco1 后")
    return inner

def deco2(fn):
    def inner():
        print("deco2 前")
        fn()
        print("deco2 后")
    return inner

# deco2 离函数最近，先装饰（先包裹）
# 执行顺序：deco1前 → deco2前 → 原函数 → deco2后 → deco1后
@deco1
@deco2
def work():
    print("原函数执行")

work()
# 输出：
# deco1 前
# deco2 前
# 原函数执行
# deco2 后
# deco1 后''',
     'expected': '定义deco1和deco2，@deco1在上@deco2在下，deco2先装饰，执行顺序为deco1前→deco2前→原函数→deco2后→deco1后'},
    {'qid': 32, 'title': '带参数装饰器（重点必做）',
     'desc': '编写 <code>logging(flag)</code>：当 flag 为 <code>\'+\'</code> 提示加法日志，<code>\'-\'</code> 提示减法日志。<br>用 <code>@logging(\'+\')</code> 装饰 <code>add(a,b)</code>。<br>用 <code>@logging(\'-\')</code> 装饰 <code>sub(a,b)</code>。<br>输出运算结果并验证装饰器参数生效。',
     'answer': '''def logging(flag):
    """最外层接收装饰器参数"""
    def decorator(fn):
        """中间层接收被装饰函数"""
        def inner(a, b):
            """最内层做实际包装"""
            if flag == "+":
                print("正在进行加法计算")
            elif flag == "-":
                print("正在进行减法计算")
            # 调用原函数并返回结果
            return fn(a, b)
        return inner
    return decorator

@logging("+")
def add(a, b):
    return a + b

@logging("-")
def sub(a, b):
    return a - b

print(add(1, 3))  # 输出: 正在进行加法计算 / 4
print(sub(5, 2))  # 输出: 正在进行减法计算 / 3''',
     'expected': '定义三层装饰器logging(flag)→decorator(fn)→inner(a,b)，用@logging("+")和@logging("-")分别装饰add和sub'},
    {'qid': 33, 'title': '挑战题：函数耗时统计装饰器',
     'desc': '实现一个"函数耗时统计装饰器"，输出函数名和执行时长。<br>提示：使用 <code>time.time()</code> 记录开始和结束时间，计算差值。',
     'answer': '''import time

def timer(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"函数 {func.__name__} 执行耗时: {end - start:.4f} 秒")
        return result
    return inner

@timer
def slow_func():
    total = 0
    for i in range(1000000):
        total += i
    return total

print(slow_func())''',
     'expected': '定义timer装饰器，使用time.time()记录开始和结束时间，输出函数名和执行耗时'},
    {'qid': 34, 'title': '挑战题：权限装饰器',
     'desc': '实现一个"权限装饰器"：未登录拒绝执行，登录后放行。<br>提示：用一个全局变量模拟登录状态，装饰器内部判断状态后决定是否调用原函数。',
     'answer': '''# 模拟登录状态
is_login = False

def login_required(func):
    def inner(*args, **kwargs):
        if is_login:
            return func(*args, **kwargs)
        else:
            print("请先登录后再操作！")
    return inner

@login_required
def view_secret():
    print("这是机密内容...")

# 未登录调用
view_secret()  # 输出: 请先登录后再操作！

# 登录后调用
is_login = True
view_secret()  # 输出: 这是机密内容...''',
     'expected': '定义login_required装饰器，根据is_login状态决定是执行原函数还是提示登录，测试登录前后不同结果'},
]

# ============================================================
# Card HTML Generation Functions
# ============================================================

def choice_card(c):
    opts_html = '\n'.join([
        f"""            <div class="option" data-opt="{chr(65+i)}" onclick="selectOption(this)">
              <span class="option-letter">{chr(65+i)}</span> {opt[3:]}
            </div>"""
        for i, opt in enumerate(c['options'])
    ])
    return f"""    <!-- Q{c['qid']}: 单选题 -->
    <div class="card" data-qid="{c['qid']}" data-type="choice" data-answer="{c['answer']}">
      <div class="card-header"><span class="card-qnum">第 {c['qid']} 题</span><span class="card-type choice">单选题</span></div>
      <div class="card-question">{c['question']}</div>
      <div class="options">
{opts_html}
      </div>
      <div class="feedback">
        <div class="result-tag correct-tag">✓ 正确</div>
        <strong>解析：</strong>{c['analysis']}
      </div>
    </div>"""


def fill_card(f):
    return f"""    <!-- Q{f['qid']}: 填空题 -->
    <div class="card" data-qid="{f['qid']}" data-type="fill" data-answer="{f['answer']}">
      <div class="card-header"><span class="card-qnum">第 {f['qid']} 题</span><span class="card-type fill">填空题</span></div>
      <div class="card-question">{f['question']}</div>
      <input type="text" class="fill-input" placeholder="请输入答案...">
      <div class="feedback">
        <div class="result-tag correct-tag">✓ 正确</div>
        <strong>解析：</strong>{f['analysis']}
      </div>
    </div>"""


def short_card(s):
    return f"""    <!-- Q{s['qid']}: 简答题 -->
    <div class="card" data-qid="{s['qid']}" data-type="short" data-answer="{s['answer']}">
      <div class="card-header"><span class="card-qnum">第 {s['qid']} 题</span><span class="card-type short">简答题</span></div>
      <div class="card-question">{s['question']}</div>
      <textarea class="fill-input" placeholder="请输入你的回答..." rows="3"></textarea>
      <span class="ref-toggle" onclick="toggleRef(this)">查看参考答案 ▼</span>
      <div class="ref-answer" style="margin-top:0.5rem; padding:0.6rem 0.8rem; background:var(--code-bg); border-radius:6px; font-size:0.85rem; line-height:1.6; color:var(--text);">{s['reference']}</div>
      <div class="feedback"><div class="result-tag correct-tag">✓ 正确</div><strong>参考答案：</strong>{s['reference']}</div>
    </div>"""


def write_card(w):
    code_html = w['answer'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f"""    <!-- Q{w['qid']}: 代码实战 -->
    <div class="card" data-qid="{w['qid']}" data-type="write" data-answer="{w['expected']}">
      <div class="card-header"><span class="card-qnum">第 {w['qid']} 题</span><span class="card-type write">代码实战</span></div>
      <div class="card-question"><strong>{w['title']}</strong></div>
      <div class="card-desc">{w['desc']}</div>
      <textarea class="code-editor" placeholder="# 请在此编写你的代码..." rows="10"></textarea>
      <span class="ref-toggle" onclick="toggleRef(this)">查看参考答案 ▼</span>
      <div class="ref-answer"><div class="code-block"><pre>{code_html}</pre></div></div>
    </div>"""


# ============================================================
# Build all card HTML
# ============================================================
all_cards = []

# Section 1: 单选题 (10题)
all_cards.append('  <!-- ====== 一、单选题 10题 ====== -->')
all_cards.append('  <div class="section">')
all_cards.append('    <div class="section-title"><span class="icon"></span>一、单选题（10 题）</div>')
for c in choices:
    all_cards.append(choice_card(c))
all_cards.append('  </div>')

# Section 2: 填空题 (10题)
all_cards.append('  <!-- ====== 二、填空题 10题 ====== -->')
all_cards.append('  <div class="section">')
all_cards.append('    <div class="section-title"><span class="icon"></span>二、填空题（10 题）</div>')
for f in fills:
    all_cards.append(fill_card(f))
all_cards.append('  </div>')

# Section 3: 简答题 (6题)
all_cards.append('  <!-- ====== 三、简答题 6题 ====== -->')
all_cards.append('  <div class="section">')
all_cards.append('    <div class="section-title"><span class="icon"></span>三、简答题（6 题）</div>')
for s in shorts:
    all_cards.append(short_card(s))
all_cards.append('  </div>')

# Section 4: 代码实操 (8题)
all_cards.append('  <!-- ====== 四、代码实操 8题 ====== -->')
all_cards.append('  <div class="section">')
all_cards.append('    <div class="section-title"><span class="icon"></span>四、代码实操（8 题）</div>')
for w in writes:
    all_cards.append(write_card(w))
all_cards.append('  </div>')

cards_html = '\n\n'.join(all_cards)

# ============================================================
# Extract template parts
# ============================================================
header_end = template.find('<!-- ====== 一、选择题')
header_part = template[:header_end]
footer_start = template.find('</div><!-- /container -->')
footer_part = template[footer_start:]

# Update header for Day03
header_part = header_part.replace('<h1>Python 练习 002</h1>', '<h1>Python 练习 003</h1>')
header_part = header_part.replace('38 道题 · 选择题 + 填空题 + 简答题 + 代码实战 · 即时反馈 · 记录保存',
                                   '34 道题 · 选择题 + 填空题 + 简答题 + 代码实战 · 即时反馈 · 记录保存')
# Update subjective count: 18 → 14
header_part = header_part.replace('<div class="score-item"><div class="score-label">主观题</div><div class="score-num"><span id="subjDone">0</span>/18</div></div>',
                                   '<div class="score-item"><div class="score-label">主观题</div><div class="score-num"><span id="subjDone">0</span>/14</div></div>')

# Combine
final_html = header_part + '\n\n' + cards_html + '\n\n' + footer_part

# Update STORAGE_KEY
final_html = final_html.replace("const STORAGE_KEY = 'py_oop_day02_quiz_history';",
                                 "const STORAGE_KEY = 'py_day03_quiz_history';")

# Update totalQuestions in JS (find the pattern: totalQuestions = 38 or similar)
final_html = final_html.replace('totalQuestions = 38', 'totalQuestions = 34')
# Also try another possible format
final_html = final_html.replace('"totalQuestions">38', '"totalQuestions">34')

# Update title tag
final_html = final_html.replace('<title>Python 练习 002</title>', '<title>Python 练习 003</title>')

# Update objective count label (Day02 also has /20 which is same)
# But there's a JS variable like "objTotal = 20" or similar — check
final_html = final_html.replace('subjTotal = 18', 'subjTotal = 14')

# Write output
output_path = r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_003.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f'Generated {output_path}')
print(f'Total cards: {len(choices) + len(fills) + len(shorts) + len(writes)}')
print('Scores: obj=20, subj=14')
