"""
Generate python_basic_test_005-2.html from Day05 supplementary homework.
"""
import re, html as html_mod, shutil, os

def highlight_python(code):
    KW_LIST = ['def','return','if','elif','else','for','while','import','from','class','True','False','None','self','nonlocal','global','in','not','and','or','is','with','as','try','except','finally','raise','pass','break','continue','yield','lambda','await','async']
    BI_LIST = ['print','range','len','type','int','str','list','dict','tuple','set','input','isinstance','super','open','enumerate','zip','map','filter','sorted','reversed','abs','min','max','sum','round','socket','Process','Queue','Pipe','Manager','multiprocessing','os','threading','asyncio','next','random','time']
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
        if parts[i].startswith('<span'): continue
        tokens = []
        for m in KW_PAT.finditer(parts[i]): tokens.append((m.start(), m.end(), 'kw', m.group(1)))
        for m in BI_PAT.finditer(parts[i]): tokens.append((m.start(), m.end(), 'fn', m.group(1)))
        for m in NUM_PAT.finditer(parts[i]): tokens.append((m.start(), m.end(), 'num', m.group(1)))
        tokens.sort(key=lambda x: (x[0], -x[1]))
        result, pos = [], 0
        for start, end, cls, text in tokens:
            if start < pos: continue
            result.append(html_mod.escape(parts[i][pos:start]))
            result.append(f'<span class="{cls}">{html_mod.escape(text)}</span>')
            pos = end
        result.append(html_mod.escape(parts[i][pos:]))
        parts[i] = ''.join(result)
    return ''.join(parts)

# Read 005-1 as template
with open(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_005-1.html', 'r', encoding='utf-8') as f:
    template = f.read()

# ============================================================
# Day05-2 Question Data
# ============================================================

choices = [
    {'qid': 1, 'question': '在 Python 中提供多线程支持的模块是（ ）。',
     'options': ['<code>multiprocessing</code>', '<code>threading</code>', '<code>asyncio</code>', '<code>subprocess</code>'],
     'answer': 'B', 'analysis': '<code>threading</code> 是 Python 标准库中提供多线程支持的模块。'},
    {'qid': 2, 'question': '下面哪一项是正确的创建线程对象并启动的写法（ ）。',
     'options': ['<code>t = threading.Thread(target=func); t.start()</code>', '<code>t = threading.Thread(target=func()); t.start()</code>', '<code>t = threading.start(target=func)</code>', '<code>t = threading.Thread(); t.run()</code>'],
     'answer': 'A', 'analysis': 'Thread 的 target 参数传函数引用（不加括号），创建后调用 start() 启动。'},
    {'qid': 3, 'question': '如果线程任务函数定义是 <code>def work(a, b)</code>，以下传参方式正确的是（ ）。',
     'options': ['<code>args=[1,2]</code>', '<code>args=(1,2)</code>', '<code>kwargs=(a:1,b:2)</code>', '<code>target=work(1,2)</code>'],
     'answer': 'B', 'analysis': 'args 参数接收元组。<code>(1,2)</code> 是元组，多个元素按位置对应函数形参。'},
    {'qid': 4, 'question': '关于 Python 线程间共享全局变量，说法正确的是（ ）。',
     'options': ['线程之间不能共享全局变量', '线程之间共享全局变量且任何操作都不需额外同步', '线程之间共享全局变量但多线程修改同一变量时可能引发数据错误', '必须使用 global 关键字声明后线程才能共享全局变量'],
     'answer': 'C', 'analysis': '线程共享全局变量，但多线程同时修改同一变量时可能出现数据竞争，需加锁同步。'},
    {'qid': 5, 'question': '互斥锁对象的类型是（ ）。',
     'options': ['<code>threading.Mutex</code>', '<code>threading.Locker</code>', '<code>threading.Lock</code>', '<code>threading.Semaphore</code>'],
     'answer': 'C', 'analysis': '<code>threading.Lock</code> 是互斥锁类，调用 <code>threading.Lock()</code> 创建锁对象。'},
    {'qid': 6, 'question': '死锁发生时的典型现象是（ ）。',
     'options': ['线程正常运行结束', '多个线程互相等待对方释放锁，程序无法继续', '程序中所有锁同时被释放', '线程自动放弃锁并退出'],
     'answer': 'B', 'analysis': '死锁是指多个线程互相等待对方持有的资源，导致所有线程都无法继续执行。'},
    {'qid': 7, 'question': '关于 CPython 的 GIL（全局解释器锁），说法错误的是（ ）。',
     'options': ['GIL 使得同一时刻通常只有一个线程执行 Python 字节码', 'GIL 可以自动保护所有共享变量，多线程编程不需要额外加锁', 'GIL 是 CPython 解释器层面的设计，与用户主动创建的 Lock 不同', '受 GIL 影响多线程不能有效利用多核做计算密集型任务'],
     'answer': 'B', 'analysis': 'GIL 只保证字节码级别的安全，但 non-atomic 操作仍可能出问题，仍需要用户加 Lock 保护共享数据。'},
    {'qid': 8, 'question': '生成器推导式使用的括号是（ ）。',
     'options': ['中括号 []', '大括号 {}', '小括号 ()', '尖括号 <>'],
     'answer': 'C', 'analysis': '生成器推导式使用<code>()</code>，列表推导式用<code>[]</code>，集合/字典推导式用<code>{}</code>。'},
    {'qid': 9, 'question': '在 <code>def</code> 函数内使用 <code>yield</code> 关键字，该函数调用时返回的是（ ）。',
     'options': ['最后一个 yield 表达式的值', '一个生成器对象', '一个迭代完成的列表', '一个线程对象'],
     'answer': 'B', 'analysis': '含 yield 的函数是生成器函数，调用时返回生成器对象，不立即执行函数体。'},
    {'qid': 10, 'question': '在 Python 3.5+ 中，定义协程函数使用的关键字是（ ）。',
     'options': ['<code>def</code>', '<code>async def</code>', '<code>coroutine def</code>', '<code>await def</code>'],
     'answer': 'B', 'analysis': 'Python 3.5+ 使用 <code>async def</code> 定义协程函数。'},
]

fills = [
    {'qid': 11, 'question': '创建线程需要先导入模块 <span class="blank" contenteditable="true"></span>。',
     'answer': 'threading', 'analysis': '使用 <code>import threading</code> 导入多线程模块。'},
    {'qid': 12, 'question': '线程的执行顺序由 <span class="blank" contenteditable="true"></span> 调度决定，多次运行可能不同。',
     'answer': 'CPU（操作系统）', 'analysis': '线程执行顺序由 CPU 调度决定，具有不确定性。'},
    {'qid': 13, 'question': '设置子线程为 <span class="blank" contenteditable="true"></span> 后，主线程退出时子线程会自动销毁。',
     'answer': '守护线程（daemon）', 'analysis': '<code>daemon=True</code> 设为守护线程，主线程退出时自动销毁。'},
    {'qid': 14, 'question': '互斥锁获取锁的方法为 <span class="blank" contenteditable="true"></span>，释放锁的方法为 <span class="blank" contenteditable="true"></span>。',
     'answer': 'acquire()、release()', 'analysis': '<code>lock.acquire()</code> 获取锁，<code>lock.release()</code> 释放锁，推荐用 <code>with lock:</code>。'},
    {'qid': 15, 'question': '进程是操作系统 <span class="blank" contenteditable="true"></span> 分配的基本单位；线程是 <span class="blank" contenteditable="true"></span> 调度的基本单位。',
     'answer': '资源、CPU', 'analysis': '进程管理资源，线程负责执行。'},
    {'qid': 16, 'question': '获取生成器下一个值可以使用内置函数 <span class="blank" contenteditable="true"></span>，或使用 <span class="blank" contenteditable="true"></span> 循环遍历所有值。',
     'answer': 'next()、for', 'analysis': '<code>next()</code> 手动获取，<code>for</code> 自动遍历。'},
    {'qid': 17, 'question': '<code>yield</code> 关键字的作用是 <span class="blank" contenteditable="true"></span> 和 <span class="blank" contenteditable="true"></span>。',
     'answer': '返回后面的值、暂停', 'analysis': 'yield 返回一个值并暂停函数执行，下次从暂停处继续。'},
    {'qid': 18, 'question': '使用 <code>async def</code> 定义的函数称为 <span class="blank" contenteditable="true"></span> 函数，调用它返回一个 <span class="blank" contenteditable="true"></span>。',
     'answer': '协程（异步）、协程对象', 'analysis': 'async def 定义协程函数，调用返回协程对象。'},
    {'qid': 19, 'question': '在协程中等待一个可等待对象时，使用 <span class="blank" contenteditable="true"></span> 关键字挂起当前协程。',
     'answer': 'await', 'analysis': '<code>await</code> 挂起当前协程等待可等待对象完成。'},
    {'qid': 20, 'question': '启动事件循环的最常用顶层入口是 <span class="blank" contenteditable="true"></span>。',
     'answer': 'asyncio.run()', 'analysis': '<code>asyncio.run(main())</code> 启动事件循环运行协程。'},
]

shorts = [
    {'qid': 21, 'answer': '核心步骤：import → Thread() → start()',
     'question': '简述使用 <code>threading</code> 模块创建并启动多个线程的三个核心步骤，并说明要注意什么。',
     'reference': '三大步骤：① <code>import threading</code>；② 创建线程对象 <code>t = threading.Thread(target=函数名, args=(...), kwargs={...})</code>；③ <code>t.start()</code>。注意：<code>target</code> 传函数名<strong>不要加括号</strong>；多线程建议写在 <code>if __name__ == \'__main__\':</code> 下。'},
    {'qid': 22, 'answer': '数据竞争导致更新丢失，互斥锁保证同一时刻只有一个线程进入临界区',
     'question': '为什么线程之间共享全局变量可能导致数据错误？互斥锁如何解决该问题？',
     'reference': '多线程同时读写全局变量时，可能出现"读—改—写"交错执行，导致实际更新丢失。互斥锁保证<strong>同一时刻只有一个线程</strong>能进入上锁区域，避免交错修改。'},
    {'qid': 23, 'answer': '生成器按需生成数据，两种方式：推导式()和yield函数；yield暂停并返回',
     'question': '解释什么是生成器？生成器有哪两种创建方式？<code>yield</code> 关键字在生成器函数中有什么作用？',
     'reference': '生成器是按规则<strong>逐个生成数据</strong>的机制，不一次性全部生成，可<strong>节省内存</strong>。两种创建方式：生成器推导式 <code>(表达式 for 变量 in 可迭代对象)</code> 和含 <code>yield</code> 的函数。<code>yield</code> 的作用：① 返回后面的值；② <strong>暂停</strong>函数执行，下次从暂停处继续。'},
    {'qid': 24, 'answer': '协程是协作式并发的执行单元，由生成器发展而来；三要素：async def/await/asyncio.run',
     'question': '什么是协程？它和生成器存在怎样的发展关系？协程的三要素分别是什么？',
     'reference': '协程是<strong>协作式并发</strong>的执行单元。Python 协程由生成器发展而来：最初用 <code>yield</code> 暂停和恢复，后引入 <code>yield from</code>，最终发展为 <code>async/await</code> 语法。协程三要素：① <code>async def</code>；② <code>await</code>；③ <code>asyncio.run()</code>。'},
    {'qid': 25, 'answer': '进程开销大隔离好；线程开销较小共享数据需同步；协程开销最小大量I/O并发',
     'question': '从 Python 的角度，比较进程、线程和协程在资源开销、数据共享、适用场景上的主要区别。',
     'reference': '<strong>进程</strong>：资源开销大，进程间不共享全局变量，可利用多核并行，稳定性好。<strong>线程</strong>：资源开销较小，线程间共享全局变量（需注意同步），受 GIL 限制不适合 CPU 密集型计算。<strong>协程</strong>：运行在单线程内，通过事件循环调度，资源开销极小，适合大量 I/O 密集任务的并发。'},
]

writes = [
    {'qid': 26, 'answer': '多线程基础：定义函数分别打印数字和字母，创建线程并启动',
     'title': '多线程基础练习',
     'desc': '导入 <code>threading</code> 模块。<br>定义两个函数 <code>print_numbers()</code> 和 <code>print_letters()</code>，分别输出 1~5 和 A~E。<br>分别创建两个线程执行上述两个函数，并启动线程。<br>多次运行，观察输出顺序是否每次相同。',
     'reference': 'import threading\nimport time\n\ndef print_numbers():\n    for i in range(1, 6):\n        print(i)\n        time.sleep(0.1)\n\ndef print_letters():\n    for ch in ["A", "B", "C", "D", "E"]:\n        print(ch)\n        time.sleep(0.1)\n\nt1 = threading.Thread(target=print_numbers)\nt2 = threading.Thread(target=print_letters)\nt1.start()\nt2.start()\nt1.join()\nt2.join()\n# 观察结论：多次运行数字和字母的输出顺序不固定，体现线程执行的无序性。'},
    {'qid': 27, 'answer': '线程传参：args元组按位置传参，kwargs字典按关键字传参',
     'title': '线程传参',
     'desc': '定义一个函数 <code>show_info(name, age)</code>，打印"姓名：xx，年龄：yy"。<br>创建两个子线程：一个用 <code>args</code> 元组方式传递参数；另一个用 <code>kwargs</code> 字典方式传递参数。',
     'reference': 'import threading\n\ndef show_info(name, age):\n    print(f"姓名：{name}，年龄：{age}")\n\n# args 元组传参\nt1 = threading.Thread(target=show_info, args=("张三", 20))\n# kwargs 字典传参\nt2 = threading.Thread(target=show_info, kwargs={"name": "李四", "age": 22})\n\nt1.start()\nt2.start()\nt1.join()\nt2.join()'},
    {'qid': 28, 'answer': '互斥锁解决数据竞争：两个线程各加10万次，加锁后结果稳定200000',
     'title': '互斥锁解决数据竞争',
     'desc': '定义全局变量 <code>counter = 0</code>。<br>创建互斥锁 <code>lock = threading.Lock()</code>。<br>定义 <code>increase()</code> 循环 100000 次加 1，使用互斥锁保证安全。<br>创建两个子线程执行，等待结束后打印 counter。',
     'reference': 'import threading\n\ncounter = 0\nlock = threading.Lock()\n\ndef increase():\n    global counter\n    for _ in range(100000):\n        lock.acquire()\n        counter += 1\n        lock.release()\n\nt1 = threading.Thread(target=increase)\nt2 = threading.Thread(target=increase)\nt1.start()\nt2.start()\nt1.join()\nt2.join()\nprint(f"最终计数值：{counter}")  # 预期 200000'},
    {'qid': 29, 'answer': '生成器函数：fibonacci生成器，for遍历和next手动获取',
     'title': '生成器函数',
     'desc': '定义生成器函数 <code>fibonacci(n)</code>，生成前 n 个斐波那契数。<br>用 for 循环遍历生成器并打印。<br>再用 next() 手动获取前三个值。<br>主动尝试取值超过上限时观察 StopIteration 异常。',
     'reference': 'def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b\n\n# for 循环遍历\nfor num in fibonacci(10):\n    print(num, end=" ")\nprint()\n\n# 手动使用 next\ngen = fibonacci(10)\nprint(next(gen))  # 0\nprint(next(gen))  # 1\nprint(next(gen))  # 1\n# 连续调用 10 次后再 next 会抛出 StopIteration'},
    {'qid': 30, 'answer': '协程并发：create_task并发调度两个task，await等待完成',
     'title': '协程并发',
     'desc': '使用 <code>asyncio</code> 模块。<br>定义协程函数 <code>task(name, delay)</code>，输出"开始"→ sleep →"结束"。<br>定义 main()，用 create_task 创建两个任务，await 等待完成。<br>用 asyncio.run(main()) 启动。观察并发效果。',
     'reference': 'import asyncio\nimport time\n\nasync def task(name, delay):\n    print(f"开始：{name}")\n    await asyncio.sleep(delay)\n    print(f"结束：{name}")\n\nasync def main():\n    t1 = asyncio.create_task(task("A", 1))\n    t2 = asyncio.create_task(task("B", 1))\n    await t1\n    await t2\n\nstart = time.time()\nasyncio.run(main())\nprint(f"总耗时：{time.time() - start:.2f}秒")\n# 观察：两个任务几乎同时完成，总耗时约1秒'},
    {'qid': 31, 'answer': '线程安全卖票系统：随机卖1-3张，互斥锁防止超卖',
     'title': '线程安全卖票系统（挑战）',
     'desc': '共有 10 张票，多个线程模拟售卖窗口。<br>每个线程循环卖票，每次 1~3 张，若剩余不够则卖完为止。<br>使用互斥锁防止超卖。<br>最终输出每个窗口卖出的票数。',
     'reference': 'import threading\nimport random\nimport time\n\ntickets = 10\nlock = threading.Lock()\n\ndef sell(window_name):\n    global tickets\n    sold = 0\n    while True:\n        lock.acquire()\n        if tickets <= 0:\n            lock.release()\n            break\n        sell_num = min(random.randint(1, 3), tickets)\n        tickets -= sell_num\n        sold += sell_num\n        print(f"{window_name} 卖出了 {sell_num} 张票，剩余 {tickets} 张")\n        lock.release()\n        time.sleep(0.1)\n    print(f"{window_name} 总共卖出 {sold} 张票")\n\nthreads = []\nfor i in range(3):\n    t = threading.Thread(target=sell, args=(f"窗口{i+1}",))\n    threads.append(t)\n    t.start()\nfor t in threads:\n    t.join()\nprint("所有票已售罄或卖完")'},
    {'qid': 32, 'answer': '无限素数生成器：yield无限生成素数，next手动控制',
     'title': '无限素数生成器（挑战）',
     'desc': '编写生成器函数 <code>prime_generator()</code>，无限生成素数（从 2 开始）。<br>使用循环输出前 10 个素数。<br>再用 next() 获取第 11 个素数。',
     'reference': 'def prime_generator():\n    num = 2\n    while True:\n        is_prime = True\n        for i in range(2, int(num**0.5) + 1):\n            if num % i == 0:\n                is_prime = False\n                break\n        if is_prime:\n            yield num\n        num += 1\n\n# 输出前10个素数\ngen = prime_generator()\nprint("前10个素数：", end="")\nfor _ in range(10):\n    print(next(gen), end=" ")\nprint()\n\n# 获取第11个素数\nprint(f"第11个素数：{next(gen)}")'},
]

# ============================================================
# Generate Card HTML
# ============================================================

def gen_choice_card(q):
    letters = 'ABCD'
    opts_html = '\n'.join(
        f'            <div class="option" data-opt="{letters[i]}" onclick="selectOption(this)">\n              <span class="option-letter">{letters[i]}</span> {o}\n            </div>'
        for i, o in enumerate(q['options'])
    )
    return f'''    <!-- Q{q['qid']}: 单选题 -->
    <div class="card" data-qid="{q['qid']}" data-type="choice" data-answer="{q['answer']}">
      <div class="card-header"><span class="card-qnum">第 {q['qid']} 题</span><span class="card-type choice">单选题</span></div>
      <div class="card-question">{q['question']}</div>
      <div class="options">
{opts_html}
      </div>
      <div class="feedback">
        <div class="result-tag correct-tag">✓ 正确</div>
        <strong>解析：</strong>{q['analysis']}
      </div>
    </div>'''

def gen_fill_card(q):
    return f'''    <!-- Q{q['qid']}: 填空题 -->
    <div class="card" data-qid="{q['qid']}" data-type="fill" data-answer="{q['answer']}">
      <div class="card-header"><span class="card-qnum">第 {q['qid']} 题</span><span class="card-type fill">填空题</span></div>
      <div class="card-question">{q['question']}</div>
      <input type="text" class="fill-input" placeholder="请输入答案...">
      <div class="feedback">
        <div class="result-tag correct-tag">✓ 正确</div>
        <strong>解析：</strong>{q['analysis']}
      </div>
    </div>'''

def gen_short_card(q):
    return f'''    <!-- Q{q['qid']}: 简答题 -->
    <div class="card" data-qid="{q['qid']}" data-type="short" data-answer="{q['answer']}">
      <div class="card-header"><span class="card-qnum">第 {q['qid']} 题</span><span class="card-type short">简答题</span></div>
      <div class="card-question">{q['question']}</div>
      <textarea class="fill-input" placeholder="请输入你的回答..." rows="3"></textarea>
      <span class="ref-toggle" onclick="toggleRef(this)">查看参考答案 ▼</span>
      <div class="ref-answer" style="margin-top:0.5rem; padding:0.6rem 0.8rem; background:var(--code-bg); border-radius:6px; font-size:0.85rem; line-height:1.6; color:var(--text);">{q['reference']}</div>
      <div class="feedback"><div class="result-tag correct-tag">✓ 正确</div><strong>参考答案：</strong>{q['reference']}</div>
    </div>'''

def gen_write_card(q):
    highlighted = highlight_python(q['reference'])
    return f'''    <!-- Q{q['qid']}: 代码实战 -->
    <div class="card" data-qid="{q['qid']}" data-type="write" data-answer="{q['answer']}">
      <div class="card-header"><span class="card-qnum">第 {q['qid']} 题</span><span class="card-type write">代码实战</span></div>
      <div class="card-question"><strong>{q['title']}</strong></div>
      <div class="card-desc">{q['desc']}</div>
      <textarea class="code-editor" placeholder="# 请在此编写你的代码..." rows="10"></textarea>
      <span class="ref-toggle" onclick="toggleRef(this)">查看参考答案 ▼</span>
      <div class="ref-answer"><div class="code-block">{highlighted}</div></div>
      <div class="feedback"><div class="result-tag correct-tag">✓ 正确</div><strong>参考答案：</strong><div class="code-block">{highlighted}</div></div>
    </div>'''

choice_cards = '\n'.join(gen_choice_card(q) for q in choices)
fill_cards = '\n'.join(gen_fill_card(q) for q in fills)
short_cards = '\n'.join(gen_short_card(q) for q in shorts)
write_cards = '\n'.join(gen_write_card(q) for q in writes)

# ============================================================
# Replace into template
# ============================================================
html = template
html = html.replace('Python 练习 005-1', 'Python 练习 005-2')
html = html.replace('python_basic_test_005-1.html', 'python_basic_test_005-2.html')
html = html.replace('34 道题 · 选择题 + 填空题 + 简答题 + 代码实战 · 即时反馈 · 记录保存',
                     '32 道题 · 选择题 + 填空题 + 简答题 + 代码实战 · 即时反馈 · 记录保存')
html = html.replace('py_day05_1_quiz_history', 'py_day05_2_quiz_history')
html = html.replace('py_day05_1_saves', 'py_day05_2_saves')
html = html.replace('/14</span></div>\n      <div class="score-item" id="scoreResult"',
                     '/12</span></div>\n      <div class="score-item" id="scoreResult"')

# Replace quiz nav
old_nav = '''  <div class="quiz-nav">
    <a href="/static/python_basic_test_004.html" class="quiz-arrow" title="上一练习">◂</a>
    <div class="quiz-dropdown">
      <button class="quiz-dropdown-btn" onclick="toggleDropdown(this)">练习 005-1 <span class="arrow-icon">▾</span></button>
      <div class="quiz-dropdown-menu">
        <a href="/static/python_basic_test_001.html">练习 001</a>
        <a href="/static/python_basic_test_002.html">练习 002</a>
        <a href="/static/python_basic_test_003.html">练习 003</a>
        <a href="/static/python_basic_test_004.html">练习 004</a>
        <a href="/static/python_basic_test_005-1.html" class="active">练习 005-1</a>
      </div>
    </div>
    <span class="quiz-arrow disabled" title="已是最后一个">▸</span>
  </div>'''

new_nav = '''  <div class="quiz-nav">
    <a href="/static/python_basic_test_005-1.html" class="quiz-arrow" title="上一练习">◂</a>
    <div class="quiz-dropdown">
      <button class="quiz-dropdown-btn" onclick="toggleDropdown(this)">练习 005-2 <span class="arrow-icon">▾</span></button>
      <div class="quiz-dropdown-menu">
        <a href="/static/python_basic_test_001.html">练习 001</a>
        <a href="/static/python_basic_test_002.html">练习 002</a>
        <a href="/static/python_basic_test_003.html">练习 003</a>
        <a href="/static/python_basic_test_004.html">练习 004</a>
        <a href="/static/python_basic_test_005-1.html">练习 005-1</a>
        <a href="/static/python_basic_test_005-2.html" class="active">练习 005-2</a>
      </div>
    </div>
    <span class="quiz-arrow disabled" title="已是最后一个">▸</span>
  </div>'''
html = html.replace(old_nav, new_nav)

# Replace body content
p1 = html.find('<!-- ====== 一、单选题')
p_end = html.find('</div>\n\n<script>')
if p_end == -1:
    p_end = html.find('</div>\n<script>')

if p1 != -1 and p_end != -1:
    p1 = html.rfind('\n', 0, p1) + 1
    new_body = f'''<!-- ====== 一、单选题 10题 ====== -->
<div class="section">

    <div class="section-title"><span class="icon"></span>一、单选题（10 题）</div>

{choice_cards}
</div>

<!-- ====== 二、填空题 10题 ====== -->

<div class="section">

    <div class="section-title"><span class="icon"></span>二、填空题（10 题）</div>

{fill_cards}
</div>

<!-- ====== 三、简答题 5题 ====== -->

<div class="section">

    <div class="section-title"><span class="icon"></span>三、简答题（5 题）</div>

{short_cards}
</div>

<!-- ====== 四、代码实操 7题 ====== -->

<div class="section">

    <div class="section-title"><span class="icon"></span>四、代码实操（7 题）</div>

{write_cards}
</div>

'''
    html = html[:p1] + new_body + html[p_end:]
else:
    print(f'ERROR: p1={p1}, p_end={p_end}')

# Write
output = r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_005-2.html'
with open(output, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Generated: {output}')
print(f'Size: {len(html)} bytes')
print(f'Choices: {len(choices)}, Fills: {len(fills)}, Shorts: {len(shorts)}, Writes: {len(writes)}')
has_old = '闭包' in html or '装饰器' in html
has_new = '卖票' in html and '素数' in html
print(f'Old removed: {not has_old}')
print(f'New present: {has_new}')
print(f'Covers Q1-Q32: Q32={"Q32" in html or "素数" in html}')
