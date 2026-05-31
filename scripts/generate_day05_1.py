"""
Generate python_basic_test_005-1.html from Day05 homework.
"""
import re, html as html_mod

def highlight_python(code):
    KW_LIST = ['def','return','if','elif','else','for','while','import','from','class','True','False','None','self','nonlocal','global','in','not','and','or','is','with','as','try','except','finally','raise','pass','break','continue','yield','lambda','await']
    BI_LIST = ['print','range','len','type','int','str','list','dict','tuple','set','input','isinstance','super','open','enumerate','zip','map','filter','sorted','reversed','abs','min','max','sum','round','socket','Process','Queue','Pipe','Manager','multiprocessing','os','threading','asyncio','next']
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

# Read 004 as template
with open(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_004.html', 'r', encoding='utf-8') as f:
    template = f.read()

# ============================================================
# Day05-1 Question Data
# ============================================================

choices = [
    {'qid': 1, 'question': '在 Python 中，<b>线程</b>相对<b>进程</b>，更准确的描述是（ ）。',
     'options': ['线程是资源分配的基本单位', '线程是 CPU 调度的基本单位，依附于进程存在', '线程可以脱离进程单独运行', '进程与线程都不共享内存'],
     'answer': 'B', 'analysis': '线程是 CPU 调度的基本单位，必须依附于进程存在。进程才是资源分配的基本单位。'},
    {'qid': 2, 'question': '创建并启动子线程的正确三步<b>不包含</b>（ ）。',
     'options': ['<code>import threading</code>', '<code>threading.Thread(target=func, ...)</code>', '<code>线程对象.start()</code>', '<code>threading.spawn(func)</code>'],
     'answer': 'D', 'analysis': '<code>threading.spawn()</code> 不是 Python threading 模块的 API。正确三步：import → Thread() → start()。'},
    {'qid': 3, 'question': '关于 <code>Thread</code> 的 <code>target</code> 参数，正确的是（ ）。',
     'options': ['应写成 <code>target=func()</code>', '应写成 <code>target=func</code>', '<code>target</code> 必须是 lambda', '<code>target</code> 只能是字符串函数名'],
     'answer': 'B', 'analysis': '<code>target=func</code> 传函数引用。<code>target=func()</code> 会在主线程先执行函数，把返回值传给 target。'},
    {'qid': 4, 'question': '对<b>只有一个参数</b>的任务函数，使用 <code>args</code> 传参时应写成（ ）。',
     'options': ['<code>args=(5)</code>', '<code>args=(5,)</code>', '<code>args=5</code>', '<code>args=[5]</code>'],
     'answer': 'B', 'analysis': '单元素元组必须加逗号 <code>(5,)</code>。<code>(5)</code> 只是括号表达式，不是元组。'},
    {'qid': 5, 'question': '同一进程内多个线程对<b>全局列表</b>执行 <code>append</code>，一般（ ）。',
     'options': ['不需要也不应该共享', '可以共享，能看到同一份列表', '每个线程有独立副本', '必须先 <code>fork</code> 才能共享'],
     'answer': 'B', 'analysis': '线程共用同一地址空间，全局列表只有一份，所有线程都能看到。',
    },
    {'qid': 6, 'question': '多个线程并发对同一整型全局变量做 <code>count = count + 1</code> 可能出现结果小于理论值，主要是因为（ ）。',
     'options': ['Python 版本太低', '<code>+1</code> 非原子操作，存在调度交错导致丢更新', '<code>global</code> 写多了', '线程不能访问全局变量'],
     'answer': 'B', 'analysis': 'count += 1 实际是 读取→计算→写入 三步非原子操作，线程可能在中间被切换导致更新丢失。'},
    {'qid': 7, 'question': '互斥锁的典型用法正确的是（ ）。',
     'options': ['每个线程各自 <code>threading.Lock()</code> 一把新锁', '多个线程共用<b>同一把</b> Lock 对象，在临界区 acquire/release 或用 <code>with lock:</code>', '上锁后不必释放', 'Lock 只能用于进程'],
     'answer': 'B', 'analysis': '多个线程必须共用同一把 Lock 对象，配合 <code>with lock:</code> 或 acquire/release 保护共享数据。'},
    {'qid': 8, 'question': '<b>CPython</b> 中的 <b>GIL</b> 主要指（ ）。',
     'options': ['用户创建的 <code>threading.Lock</code>', '解释器层的全局锁，同一时刻通常只有一个线程执行 Python 字节码', '网络全局 IP', '生成器的全局变量'],
     'answer': 'B', 'analysis': 'GIL（全局解释器锁）是 CPython 解释器层的锁，限制同一时刻只有一条线程执行 Python 字节码。'},
    {'qid': 9, 'question': '下列能得到一个<b>生成器对象</b>的是（ ）。',
     'options': ['<code>g = [i for i in range(3)]</code>', '<code>g = (i for i in range(3))</code>', '<code>g = {i for i in range(3)}</code>', '<code>g = list(range(3))</code>'],
     'answer': 'B', 'analysis': '列表推导式用[]、集合推导式用{}，生成器推导式用()括号。'},
    {'qid': 10, 'question': '关于 <code>async</code> / <code>await</code> 与 <code>asyncio.run</code>，正确的是（ ）。',
     'options': ['<code>async def</code> 定义的函数一调用就会执行完', '<code>await</code> 用于等待可等待对象并把控制权交回事件循环', '<code>asyncio.run</code> 可以在任意嵌套函数里随意连续调用', '协程运行在独立进程里'],
     'answer': 'B', 'analysis': '<code>await</code> 挂起当前协程等待可等待对象，同时把控制权交回事件循环。'},
]

fills = [
    {'qid': 11, 'question': '进程是操作系统________分配的基本单位；线程是________调度的基本单位。', 'blanks': ['资源', 'CPU'],
     'answer': '资源、CPU', 'analysis': '进程是资源分配的基本单位；线程是 CPU 调度的基本单位，依附于进程存在。'},
    {'qid': 12, 'question': '创建线程类：<code>threading.Thread(target=________, args=..., kwargs=...)</code>。', 'blanks': ['函数名'],
     'answer': '函数名', 'analysis': 'target 参数传函数引用（可调用对象），不加括号。'},
    {'qid': 13, 'question': '主线程默认会等待所有________线程结束后再结束进程（常规情况）。', 'blanks': ['子'],
     'answer': '子', 'analysis': '主线程默认等待所有非守护子线程结束。'},
    {'qid': 14, 'question': '若希望主线程结束时子线程不再继续执行，可设置________线程（<code>daemon=True</code>）。', 'blanks': ['守护'],
     'answer': '守护', 'analysis': 'daemon=True 将线程设为守护线程，主线程结束时守护线程自动终止。'},
    {'qid': 15, 'question': '线程之间与进程相比，________之间默认共享进程内全局数据；进程之间默认________共享。', 'blanks': ['线程', '不'],
     'answer': '线程、不', 'analysis': '线程共享地址空间；进程有独立地址空间，默认不共享。'},
    {'qid': 16, 'question': '互斥锁对象的创建方式常为 <code>lock = threading.________()</code>。', 'blanks': ['Lock'],
     'answer': 'Lock', 'analysis': '<code>threading.Lock()</code> 创建互斥锁对象。'},
    {'qid': 17, 'question': '含 <code>yield</code> 的函数称为生成器函数，调用该函数得到的是________。', 'blanks': ['生成器对象'],
     'answer': '生成器对象', 'analysis': '调用生成器函数返回生成器对象，不是立即执行函数体。'},
    {'qid': 18, 'question': '生成器耗尽后再 <code>next</code>，会抛出________异常；<code>for</code> 遍历时会自动处理。', 'blanks': ['StopIteration'],
     'answer': 'StopIteration', 'analysis': '生成器元素耗尽后调用 next() 抛出 StopIteration 异常，for 循环自动捕获。'},
    {'qid': 19, 'question': '协程三要素：<code>async def</code>、________、顶层常用 <code>asyncio.run(...)</code>。', 'blanks': ['await'],
     'answer': 'await', 'analysis': '协程三要素：async def 定义、await 挂起等待、asyncio.run 启动事件循环。'},
    {'qid': 20, 'question': '在同一协程函数里要<b>并发</b>执行多个协程，常用 <code>asyncio.________</code> 包装成任务。', 'blanks': ['create_task'],
     'answer': 'create_task', 'analysis': '<code>asyncio.create_task()</code> 将协程包装为任务实现并发调度。'},
]

shorts = [
    {'qid': 21, 'answer': '线程必须依附在进程里运行',
     'question': '进程与线程是什么关系？为什么说"没有进程就没有线程"？',
     'reference': '线程必须<strong>依附在进程</strong>里运行：进程向操作系统申请地址空间、文件描述符等资源，线程是在该进程内部被调度执行的执行流。没有进程作为"容器"和资源边界，线程无法单独存在，因此说没有进程就没有线程。'},
    {'qid': 22, 'answer': '多个线程的调度顺序由操作系统决定不确定',
     'question': '为什么多线程执行时，打印顺序可能每次运行都不一样？',
     'reference': '多个线程<strong>谁先获得 CPU、执行到哪一行</strong>，由操作系统和解释器的<strong>调度策略</strong>决定，不是代码书写顺序保证的。因此并发时输出顺序<strong>不确定</strong>属正常现象。'},
    {'qid': 23, 'answer': '线程共用同一地址空间，进程有独立地址空间',
     'question': '线程之间共享全局变量与进程之间不共享，区别的原因是什么？',
     'reference': '同一进程内的线程共用<strong>同一地址空间</strong>，全局变量在同进程内<strong>只有一份</strong>；而每个进程有<strong>独立的虚拟地址空间</strong>，子进程是父进程内存的拷贝，因此各进程的全局变量互不天然共享。'},
    {'qid': 24, 'answer': '互斥锁保证同一时刻只有一个线程进入临界区，with自动释放',
     'question': '互斥锁要解决什么问题？使用 <code>with lock:</code> 有什么好处？',
     'reference': '互斥锁用于<strong>线程同步</strong>，保证<strong>同一时刻只有一个线程</strong>进入临界区操作共享数据，避免"读—改—写"被抢占导致的数据竞争。<code>with lock:</code> 在离开代码块时<strong>自动释放锁</strong>，减少忘记 release() 造成的<strong>死锁</strong>问题。'},
    {'qid': 25, 'answer': 'GIL是解释器全局锁，Lock是用户级锁；字节码间仍可能切换',
     'question': '简要说明 GIL 与 <code>threading.Lock</code> 的区别；为什么在 CPython 里有时仍要给共享数据加 Lock？',
     'reference': '<strong>GIL</strong> 是 CPython 解释器层的<strong>全局解释器锁</strong>，限制同一时刻通常只有一条线程在执行 Python 字节码。<code>threading.Lock</code> 是程序员为保护自己共享数据创建的<strong>显式锁</strong>。即使有 GIL，一条源码语句可能对应<strong>多条字节码</strong>，线程仍可能在中间被切换，因此<strong>业务上的非原子更新</strong>仍可能出错。'},
    {'qid': 26, 'answer': '生成器按需产出节省内存，yield暂停产出，return结束函数',
     'question': '生成器相对一次性构造完整列表，主要优点是什么？<code>yield</code> 与 <code>return</code> 在生成器函数中的典型区别？',
     'reference': '生成器<strong>按需产出</strong>元素，不一次性把所有结果放进内存，<strong>节省内存</strong>。<code>yield</code> 会<strong>暂停</strong>当前函数、向外产出一个值，下次从暂停处继续；<code>return</code> 用于<strong>结束</strong>生成器函数（结束迭代）。'},
    {'qid': 27, 'answer': 'async def/await/asyncio.run三要素，run顶层启动，create_task并发包装',
     'question': '协程三要素是什么？<code>asyncio.run</code> 与 <code>asyncio.create_task</code> 分别适合什么场景？',
     'reference': '三要素：<code>async def</code> 定义协程函数、<code>await</code> 等待可等待对象、<code>asyncio.run</code> 启动事件循环。<code>asyncio.run</code> 常用于<strong>最外层</strong>启动整个异步程序；在同一 async def 里要对多个协程<strong>并发</strong>时，用 <code>create_task</code> 将协程包装为任务。'},
]

writes = [
    {'qid': 28, 'answer': '多线程入门：定义两个任务函数，用threading.Thread创建并start',
     'title': '多线程入门（必做）',
     'desc': '定义两个无参任务函数（如模拟"写代码""听音乐"打印若干行）。<br>创建两个 <code>threading.Thread</code>，指定 <code>target</code>，调用 <code>start()</code>。<br>观察多次运行输出顺序是否可能不同。',
     'reference': 'import threading\n\ndef coding():\n    for i in range(3):\n        print("coding", i)\n\ndef music():\n    for i in range(3):\n        print("music", i)\n\nt1 = threading.Thread(target=coding)\nt2 = threading.Thread(target=music)\nt1.start()\nt2.start()'},
    {'qid': 29, 'answer': '线程传参：args按位置传参，kwargs按关键字传参',
     'title': '线程传参（必做）',
     'desc': '使用 <code>args=(\'小明\', 3)</code> 按位置传参。<br>使用 <code>kwargs={...}</code> 按关键字传参。<br>说明 args 单元素必须加逗号的原因（注释）。',
     'reference': 'def greet(name, times):\n    for i in range(times):\n        print(name, i)\n\ndef show(**kwargs):\n    print(kwargs)\n\nt1 = threading.Thread(target=greet, args=("小明", 3))\nt2 = threading.Thread(target=show, kwargs={"a": 1, "b": 2})\nt1.start()\nt2.start()\n# 单元素元组: args=(5,) 不能写成 args=(5)'},
    {'qid': 30, 'answer': '全局变量与互斥锁：不加锁结果不稳定，加锁后稳定为预期值',
     'title': '全局变量与互斥锁（重点必做）',
     'desc': '定义全局整型 <code>count = 0</code>，两个线程各循环较大次数（如 10 万次）执行 <code>count += 1</code>。<br>先不加锁运行，观察结果是否小于预期。<br>再用同一把 <code>threading.Lock</code> 包裹临界区。',
     'reference': 'import threading\n\ncount = 0\nlock = threading.Lock()\nN = 100000\n\ndef add():\n    global count\n    for _ in range(N):\n        with lock:\n            count += 1\n\nt1 = threading.Thread(target=add)\nt2 = threading.Thread(target=add)\nt1.start()\nt2.start()\nt1.join()\nt2.join()\nprint(count)  # 200000'},
    {'qid': 31, 'answer': '生成器：推导式创建生成器，yield生成器函数',
     'title': '生成器（必做）',
     'desc': '用生成器推导式创建生成器，并用 for 遍历打印。<br>再写一个含 yield 的生成器函数，用 next 至少取两次，说明每次从何处继续执行（注释）。',
     'reference': 'g = (x * 2 for x in range(4))\nfor v in g:\n    print(v)\n\ndef gen(n):\n    for i in range(n):\n        yield i\n\nit = gen(3)\nprint(next(it))  # 0\nprint(next(it))  # 1'},
    {'qid': 32, 'answer': 'asyncio入门：create_task并发调度，await等待完成',
     'title': 'asyncio 入门与并发任务（重点必做）',
     'desc': '定义 <code>async def work(name):</code> 内 print 开始，<code>await asyncio.sleep(1)</code>，print 结束。<br>定义 async def main()，用 create_task 同时调度至少两个 work，再 await 等待。<br>最外层用 asyncio.run(main())。注释说明并发 vs 串行的耗时区别。',
     'reference': 'import asyncio\n\nasync def work(name):\n    print("start", name)\n    await asyncio.sleep(1)\n    print("end", name)\n\nasync def main():\n    t1 = asyncio.create_task(work("A"))\n    t2 = asyncio.create_task(work("B"))\n    await t1\n    await t2\n\nasyncio.run(main())'},
    {'qid': 33, 'answer': 'CPU密集型更适合多进程，I/O密集型更适合协程',
     'title': 'CPU 密集型 vs I/O 密集型（选做）',
     'desc': '用一段话对比：CPU 密集型任务在 CPython 下更适合多进程还是多线程？I/O 密集型更适合线程还是协程？简要说明理由。',
     'reference': '<strong>CPU 密集型</strong>：在 CPython 下多线程受 GIL 影响，纯 Python 计算往往难以吃满多核，更适合用<strong>多进程</strong>将任务分配到多核。<strong>I/O 密集型</strong>：线程可在 I/O 阻塞时让出 CPU；<strong>协程</strong>在单线程事件循环里通过 await 挂起等待，大量 I/O 并发时开销更小，适合高并发网络/等待场景。'},
    {'qid': 34, 'answer': 'join等待线程结束，锁保护临界区；join整条线程串行，锁只串行临界区',
     'title': 'join() vs 互斥锁（选做）',
     'desc': '查阅或回忆：<code>join()</code> 等待子线程结束与用互斥锁保护临界区，在"牺牲并行度"方面有何异同（各写一两句）。',
     'reference': '<code>join()</code>：让调用方<strong>等待某个线程先跑完</strong>，其他线程期间是否并行取决于你 join 的方式，容易写成阶段性串行。<strong>互斥锁</strong>：只保证<strong>临界区串行</strong>，锁外其他线程仍可并行，并行度通常好于整条线程顺序 join 的写法，但锁粒度过大也会接近单线程。'},
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
html = template.replace('Python 练习 004', 'Python 练习 005-1')
html = html.replace('python_basic_test_004.html', 'python_basic_test_005-1.html')
html = html.replace('33 道题 · 选择题 + 填空题 + 简答题 + 代码实战 · 即时反馈 · 记录保存',
                     '34 道题 · 选择题 + 填空题 + 简答题 + 代码实战 · 即时反馈 · 记录保存')
html = html.replace('py_day04_quiz_history', 'py_day05_1_quiz_history')
html = html.replace('py_day04_saves', 'py_day05_1_saves')
html = html.replace('/13</span></div>\n      <div class="score-item" id="scoreResult"',
                     '/14</span></div>\n      <div class="score-item" id="scoreResult"')

# Replace quiz nav
old_nav = '''  <div class="quiz-nav">
    <a href="/static/python_basic_test_003.html" class="quiz-arrow" title="上一练习">◂</a>
    <div class="quiz-dropdown">
      <button class="quiz-dropdown-btn" onclick="toggleDropdown(this)">练习 004 <span class="arrow-icon">▾</span></button>
      <div class="quiz-dropdown-menu">
        <a href="/static/python_basic_test_001.html">练习 001</a>
        <a href="/static/python_basic_test_002.html">练习 002</a>
        <a href="/static/python_basic_test_003.html">练习 003</a>
        <a href="/static/python_basic_test_004.html" class="active">练习 004</a>
      </div>
    </div>
    <span class="quiz-arrow disabled" title="已是最后一个">▸</span>
  </div>'''

new_nav = '''  <div class="quiz-nav">
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

<!-- ====== 三、简答题 7题 ====== -->

<div class="section">

    <div class="section-title"><span class="icon"></span>三、简答题（7 题）</div>

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

# Write output
output_path = r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_005-1.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Generated: {output_path}')
print(f'Size: {len(html)} bytes')
print(f'Choices: {len(choices)}, Fills: {len(fills)}, Shorts: {len(shorts)}, Writes: {len(writes)}')

# Verify
has_old = '闭包' in html or '装饰器' in html
has_new = '线程' in html and 'GIL' in html
print(f'Old content removed: {not has_old}')
print(f'New content present: {has_new}')
print(f'7 shorts: {"Q27" in html}')
print(f'7 writes (Q28-Q34): {"Q34" in html}')
