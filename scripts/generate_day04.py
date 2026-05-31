"""
Generate python_basic_test_004.html from Day04 homework,
using python_basic_test_003.html as structural template.
"""
import re, html as html_mod

def highlight_python(code):
    """Pre-highlight Python code for inline HTML display (like 002).
    Uses a tokenizer approach to avoid regex-on-HTML corruption."""
    KW_LIST = ['def','return','if','elif','else','for','while','import','from','class','True','False','None','self','nonlocal','global','in','not','and','or','is','with','as','try','except','finally','raise','pass','break','continue','yield','lambda']
    BI_LIST = ['print','range','len','type','int','str','list','dict','tuple','set','input','isinstance','super','open','enumerate','zip','map','filter','sorted','reversed','abs','min','max','sum','round','socket','Process','Queue','Pipe','Manager','multiprocessing','os']
    KW_PAT = re.compile(r'\b(' + '|'.join(KW_LIST) + r')\b')
    BI_PAT = re.compile(r'\b(' + '|'.join(BI_LIST) + r')\b')
    NUM_PAT = re.compile(r'\b(\d+\.?\d*)\b')
    STR_PAT = re.compile(r"(f?(?:\"\"\"[\s\S]*?\"\"\"|'''[\s\S]*?'''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'))")
    CM_PAT = re.compile(r'(#[^\n]*)')
    OP_PAT = re.compile(r'(@\w+)')

    # Phase 1: wrap strings, comments, decorators
    code = STR_PAT.sub(r'<span class="str">\1</span>', code)
    code = CM_PAT.sub(r'<span class="cm">\1</span>', code)
    code = OP_PAT.sub(r'<span class="op">\1</span>', code)

    # Phase 2: split by existing spans, process text segments uniformly
    parts = re.split(r'(<span[^>]*>.*?</span>)', code)
    for i in range(len(parts)):
        if parts[i].startswith('<span'):
            continue
        # Find all token positions in this text segment
        tokens = []
        for m in KW_PAT.finditer(parts[i]):
            tokens.append((m.start(), m.end(), 'kw', m.group(1)))
        for m in BI_PAT.finditer(parts[i]):
            tokens.append((m.start(), m.end(), 'fn', m.group(1)))
        for m in NUM_PAT.finditer(parts[i]):
            tokens.append((m.start(), m.end(), 'num', m.group(1)))
        # Sort by position, resolve overlaps (earlier wins)
        tokens.sort(key=lambda x: (x[0], -x[1]))
        # Build highlighted segment
        result = []
        pos = 0
        for start, end, cls, text in tokens:
            if start < pos:
                continue  # skip overlapping
            result.append(html_mod.escape(parts[i][pos:start]))
            result.append(f'<span class="{cls}">{html_mod.escape(text)}</span>')
            pos = end
        result.append(html_mod.escape(parts[i][pos:]))
        parts[i] = ''.join(result)
    return ''.join(parts)

# Read 003 as template
with open(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_003.html', 'r', encoding='utf-8') as f:
    template = f.read()

# ============================================================
# Day04 Question Data
# ============================================================

choices = [
    {'qid': 1, 'question': '在网络通信中，<b>IP 地址</b>的主要作用是（ ）。',
     'options': ['标识一台主机上的某个应用程序', '在网络中标识一台设备（大致唯一）', '规定数据编码格式', '替代端口号'],
     'answer': 'B', 'analysis': 'IP 地址用于在网络中标识一台设备（主机），大致唯一。标识应用程序的是端口号。'},
    {'qid': 2, 'question': '<b>端口号</b>的主要作用是（ ）。',
     'options': ['替代 IP 地址', '同一台机器上区分不同程序（进程）使用的"窗口"', '保证传输一定可靠', '只能是 0～255'],
     'answer': 'B', 'analysis': '端口号用于在同一台机器上区分不同程序（进程），范围 0~65535。'},
    {'qid': 3, 'question': '下列关于 <b>TCP</b> 特点的描述，错误的是（ ）。',
     'options': ['面向连接', '可靠传输（有确认、重传、有序等机制）', '面向字节流', '无连接、发完就走'],
     'answer': 'D', 'analysis': 'TCP 三大特点：面向连接、可靠传输、面向字节流。"无连接、发完就走"是 UDP 的特点。'},
    {'qid': 4, 'question': '创建 <b>IPv4 + TCP</b> 套接字时，正确的参数组合是（ ）。',
     'options': ['<code>socket.AF_INET, socket.SOCK_DGRAM</code>', '<code>socket.AF_INET, socket.SOCK_STREAM</code>', '<code>socket.AF_UNIX, socket.SOCK_STREAM</code>', '<code>socket.AF_INET6, socket.SOCK_DGRAM</code>'],
     'answer': 'B', 'analysis': 'IPv4 用 <code>AF_INET</code>，TCP 用 <code>SOCK_STREAM</code>。DGRAM 对应 UDP，AF_UNIX 用于本地通信。'},
    {'qid': 5, 'question': 'TCP <b>服务端</b>建立连接并收发数据，<b>不需要</b>调用的是（ ）。',
     'options': ['<code>bind</code>', '<code>listen</code>', '<code>accept</code>', '<code>connect</code>'],
     'answer': 'D', 'analysis': '<code>connect</code> 是客户端主动连接服务端用的，服务端不需要调用它。'},
    {'qid': 6, 'question': 'TCP <b>客户端</b>与服务器通信时，通常使用（ ）。',
     'options': ['<code>bind</code>', '<code>listen</code>', '<code>connect</code>', '<code>accept</code>'],
     'answer': 'C', 'analysis': '客户端用 <code>connect</code> 主动发起连接；<code>bind/listen/accept</code> 是服务端的方法。'},
    {'qid': 7, 'question': '服务端调用 <code>accept()</code> 成功后，应与<b>哪一个套接字</b>进行 <code>recv</code> / <code>send</code>？（ ）。',
     'options': ['监听套接字（<code>listen</code> 用的那个）', '<code>accept</code> 返回的新套接字', '任意一个都可以', '必须先 <code>shutdown</code> 再用监听套接字'],
     'answer': 'B', 'analysis': '<code>accept</code> 返回的新套接字是已建立连接的通信套接字，后续收发数据都用它。监听套接字只负责接受新连接。'},
    {'qid': 8, 'question': 'Python 3 中通过 TCP 发送字符串 <code>"你好"</code>，正确写法是（ ）。',
     'options': ['<code>sock.send("你好")</code>', '<code>sock.send("你好".encode(\'utf-8\'))</code>', '<code>sock.write("你好")</code>', '<code>sock.send(bytes("你好"))</code> 且不指定编码'],
     'answer': 'B', 'analysis': 'Python 3 中 socket 发送的是 bytes，必须先用 <code>encode(\'utf-8\')</code> 将字符串编码。'},
    {'qid': 9, 'question': '下列关于 TCP <code>recv</code> 的说法，正确的是（ ）。',
     'options': ['一次 <code>recv</code> 一定能收到对方一次 <code>send</code> 的完整"一条消息"', '返回 <code>b\'\'</code>（长度为 0）通常表示对端已关闭连接', '应对监听套接字调用 <code>recv</code>', '<code>recv</code> 在 Python 3 中返回 <code>str</code> 类型'],
     'answer': 'B', 'analysis': '返回 <code>b\'\'</code> 表示对端关闭连接（FIN）。TCP 是字节流，不保证消息边界。recv 返回 bytes 类型。'},
    {'qid': 10, 'question': '关于 <code>multiprocessing.Process</code>，下列说法正确的是（ ）。',
     'options': ['<code>target=coding()</code> 与 <code>target=coding</code> 没有区别', '创建后调用 <code>start()</code> 才会真正启动子进程', 'Windows 下可以不写 <code>if __name__ == \'__main__\':</code>', '多个进程默认共享同一个全局列表的修改'],
     'answer': 'B', 'analysis': '<code>start()</code> 才启动子进程。<code>target=coding()</code> 会在主进程中先执行函数。Windows 必须写 <code>if __name__</code> 保护。进程默认不共享全局变量。'},
]

fills = [
    {'qid': 11, 'question': '一句话概括：<b>IP 找 <span class="blank" contenteditable="true"></span>，端口找 <span class="blank" contenteditable="true"></span></b>。',
     'answer': '机器、程序', 'analysis': 'IP 地址定位设备（机器），端口号定位该设备上的具体应用（程序）。'},
    {'qid': 12, 'question': 'TCP 三大特点：面向连接、可靠传输、面向 <span class="blank" contenteditable="true"></span>。',
     'answer': '字节流', 'analysis': 'TCP 的三大特点：面向连接（三次握手建立连接）、可靠传输（确认/重传机制）、面向字节流（不保留消息边界）。'},
    {'qid': 13, 'question': '服务端典型流程口诀：创建 → 绑定 → 监听 → <span class="blank" contenteditable="true"></span> → recv/send → close。',
     'answer': 'accept', 'analysis': '服务端调用 <code>accept()</code> 等待客户端连接，返回新的通信套接字用于后续数据收发。'},
    {'qid': 14, 'question': '<code>bind</code> 的参数必须是 <span class="blank" contenteditable="true"></span>，形如 <code>(host, port)</code>，其中 <code>port</code> 为 <span class="blank" contenteditable="true"></span> 类型。',
     'answer': '元组、整数', 'analysis': '<code>bind</code> 接收一个元组 <code>(host, port)</code>，port 必须是整数类型。'},
    {'qid': 15, 'question': '网络上传输的是 <span class="blank" contenteditable="true"></span> 类型，接收后常用 <span class="blank" contenteditable="true"></span> 还原成字符串。',
     'answer': 'bytes、decode', 'analysis': '网络传输的是字节（bytes），接收后用 <code>.decode(\'utf-8\')</code> 还原为字符串。'},
    {'qid': 16, 'question': '单元素元组传参给 <code>args</code> 时应写成 <span class="blank" contenteditable="true"></span>。',
     'answer': '(x,)', 'analysis': '单元素元组必须加逗号 <code>(x,)</code>，否则 <code>(x)</code> 只是括号表达式，不是元组。'},
    {'qid': 17, 'question': '查看当前进程编号常用 <code>os.<span class="blank" contenteditable="true"></span>()</code>。',
     'answer': 'getpid', 'analysis': '<code>os.getpid()</code> 返回当前进程的 PID（进程标识符）。'},
    {'qid': 18, 'question': '子进程中要执行的函数应传给 <code>Process</code> 的 <span class="blank" contenteditable="true"></span> 参数，且不要加括号写成"先执行再传"。',
     'answer': 'target', 'analysis': '<code>Process(target=func)</code> 传函数引用，<code>Process(target=func())</code> 会在主进程先执行函数。'},
    {'qid': 19, 'question': '默认情况下，多个进程之间 <span class="blank" contenteditable="true"></span>（共享/不共享）全局变量。',
     'answer': '不共享', 'analysis': '进程有独立的内存地址空间，全局变量是各自进程的副本，修改不会互相影响。'},
    {'qid': 20, 'question': '<code>recv</code> 返回长度为 0 的字节 <code>b\'\'</code>，通常表示对端已 <span class="blank" contenteditable="true"></span> 连接。',
     'answer': '关闭', 'analysis': '<code>recv</code> 返回 <code>b\'\'</code> 是对端发送了 FIN 包关闭连接，本端应退出接收循环并关闭套接字。'},
]

shorts = [
    {'qid': 21, 'answer': 'TCP在传输数据前先经过三次握手建立一条逻辑连接，双方确认就绪后才传数据',
     'question': '用自己的话说明：为什么 TCP 叫"面向连接"，和"打电话"有什么类比？',
     'reference': 'TCP 在真正传输应用数据之前，要先经过三次握手在客户端和服务器之间<strong>建立一条逻辑上的连接</strong>，双方都确认"对方愿意通信、状态就绪"之后，才在这条连接上传字节。这和<strong>打电话</strong>很像：先拨号、对方接听、双方确认线路通了再说话；而不是像发短信那样随手发出去就不管对方是否收到（那更接近无连接的 UDP）。'},
    {'qid': 22, 'answer': '双方互相确认愿意通信，对齐初始序号等连接状态，降低旧连接干扰',
     'question': '三次握手要解决什么问题？（可只答要点）',
     'reference': '<strong>①</strong> 让通信双方互相知道对方在线且愿意建立连接；<strong>②</strong> 同步双方的初始序号（seq）等连接状态，为后面可靠传输、按序重组打基础；<strong>③</strong> 减少历史残留的旧连接请求或重复报文对本次连接的干扰。三次是在工程上既能完成双方确认、又能对齐状态的一种<strong>最小可行</strong>握手次数。'},
    {'qid': 23, 'answer': '监听套接字负责持续accept新连接，每个已连接客户端对应单独的通信套接字',
     'question': '为什么服务端 <code>accept</code> 后会得到"新套接字"，而客户端通常只有一个套接字？',
     'reference': '服务端需要<strong>分工</strong>：原来的监听套接字专门负责在门口排队接听新的连接请求（listen + 反复 accept）；每成功接入一个客户端，accept 会再生成一个<strong>已与该客户端建立好连接的新套接字</strong>，此后的 recv/send 都在这条"专线"上进行。客户端是主动发起 connect 的一方，从头到尾只用一个套接字与服务器通信。'},
    {'qid': 24, 'answer': 'TCP传输连续字节序列不保证消息边界，需自定分包规则',
     'question': '为什么说 TCP 是"面向字节流"？对 <code>send</code> / <code>recv</code> 有什么实际影响？',
     'reference': 'TCP 上传输的是<strong>连续的字节序列</strong>，协议本身<strong>不保证"一条业务消息"的边界</strong>——你 send 两次，对端不一定两次 recv 各对齐一次发送。实际影响：应用层要自己约定<strong>分包规则</strong>（如固定长度、先发长度再发内容、用特定分隔符、或短连接一次发完就关）。'},
    {'qid': 25, 'answer': 'args必须为元组单参加逗号，kwargs键名必须与形参一致',
     'question': '<code>args</code> 与 <code>kwargs</code> 给子进程传参时各要注意什么？',
     'reference': '<code>args</code> 必须是<strong>元组</strong>，按位置对应 target 函数的形参；若只有一个参数，必须写成 <strong><code>(x,)</code></strong>（逗号不能省）。<code>kwargs</code> 是<strong>字典</strong>，<strong>键名必须与被调用函数的参数名完全一致</strong>，值类型也要合法。'},
    {'qid': 26, 'answer': '进程有独立地址空间全局变量是副本，需用Queue/Pipe等IPC手段',
     'question': '为什么默认多个进程不共享全局变量？若要进程间通信通常需要什么思路？',
     'reference': '操作系统以<strong>进程</strong>为单位分配地址空间，创建子进程时会把父进程的内存做<strong>各自独立的拷贝</strong>，全局变量在每个进程里其实是自己的一份副本。要在进程间交换数据，需要<strong>进程间通信（IPC）</strong>手段，例如 <code>multiprocessing</code> 提供的 <code>Queue</code>、<code>Pipe</code>，或 <code>Manager</code> 托管对象、共享内存等。'},
    {'qid': 27, 'answer': 'TCP全双工通信每个方向需独立关闭，收到FIN后可能还有数据要传',
     'question': '阅读笔记中"四次挥手"表格，用一段话说明：为什么是四次而不是三次？',
     'reference': '因为 TCP 是<strong>全双工</strong>通信，每个方向的数据传输需要独立关闭。一方发送 FIN 只表示"我没有数据要发了"，但对方可能还有数据要传。因此关闭过程需要四步：<br>① 客户端发 FIN（我没数据了）<br>② 服务端回 ACK（我知道了）——此时服务端可能还在发剩余数据<br>③ 服务端发 FIN（我也没有数据了）<br>④ 客户端回 ACK（我知道了）<br>其中②和③不能合并，因为服务端收到 FIN 后可能还需要时间处理并发送剩余数据。而三次握手时双方状态同步可以合并（SYN+ACK），所以是三次而不是四次。'},
]

writes = [
    {'qid': 27, 'answer': '使用socket创建TCP服务端和客户端，完成一问一答',
     'title': '最简 TCP 一问一答（必做）',
     'desc': '编写服务端：<code>socket</code> → <code>bind</code> → <code>listen</code> → <code>accept</code> → <code>recv</code> 打印 → <code>send</code> 回复 → <code>close</code> 通信套接字。<br>编写客户端：<code>socket</code> → <code>connect</code> → <code>send</code> → <code>recv</code> 打印 → <code>close</code>。<br>必须使用 <code>encode(\'utf-8\')</code> / <code>decode(\'utf-8\')</code>。',
     'reference': '# 服务端\nimport socket\ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ns.bind((\'127.0.0.1\', 9000))\ns.listen(128)\nconn, addr = s.accept()\ndata = conn.recv(1024).decode(\'utf-8\')\nprint("收到:", data)\nconn.send("服务器已收到".encode(\'utf-8\'))\nconn.close()\ns.close()\n\n# 客户端\nimport socket\nc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nc.connect((\'127.0.0.1\', 9000))\nc.send("你好".encode(\'utf-8\'))\nprint(c.recv(1024).decode(\'utf-8\'))\nc.close()'},
    {'qid': 28, 'answer': '使用while True循环accept，每接入一个客户端收发一次后关闭通信套接字',
     'title': '循环 accept 接待多个客户端（重点必做）',
     'desc': '用 <code>while True</code> 循环 <code>accept</code>，每接入一个客户端：收一条短消息、回一条"已收到"、关闭与该客户端的通信套接字。<br>监听套接字可保持不关闭，便于继续接下一个。',
     'reference': 'while True:\n    conn, addr = server.accept()\n    data = conn.recv(1024).decode(\'utf-8\')\n    print(addr, data)\n    conn.send(b\'ok\')\n    conn.close()'},
    {'qid': 29, 'answer': '服务端循环recv写文件，客户端分块读文件循环send',
     'title': '文件上传骨架（重点必做）',
     'desc': '服务端：<code>accept</code> 后以 <code>wb</code> 打开目标文件，循环 <code>recv</code>，将收到的 bytes <code>write</code> 进文件；当 <code>recv</code> 得到 <code>b\'\'</code> 时退出循环并关闭。<br>客户端：以 <code>rb</code> 读本地小文件，循环 <code>send</code> 分块发送，发完 <code>close</code>。<br>说明"为什么要分块"的原因（注释）。',
     'reference': '# 服务端\nconn, _ = server.accept()\nwith open("recv.bin", "wb") as f:\n    while True:\n        chunk = conn.recv(4096)\n        if not chunk:\n            break\n        f.write(chunk)\nconn.close()\n\n# 客户端\nwith open("src.bin", "rb") as f:\n    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    sock.connect(("127.0.0.1", 9000))\n    while True:\n        chunk = f.read(4096)\n        if not chunk:\n            break\n        sock.send(chunk)\n    sock.close()\n\n# 分块原因：大文件无法一次读入内存，\n# 分块发送可控制内存占用，避免网络拥塞。'},
    {'qid': 30, 'answer': '使用multiprocessing.Process创建两个子进程并start',
     'title': '多进程入门（必做）',
     'desc': '定义两个函数，分别打印不同前缀的循环输出。<br>用 <code>multiprocessing.Process</code> 创建两个子进程并 <code>start()</code>。<br>代码放在 <code>if __name__ == \'__main__\':</code> 中。',
     'reference': 'import multiprocessing\n\ndef job_a():\n    for i in range(3):\n        print("A", i)\n\ndef job_b():\n    for i in range(3):\n        print("B", i)\n\nif __name__ == "__main__":\n    p1 = multiprocessing.Process(target=job_a)\n    p2 = multiprocessing.Process(target=job_b)\n    p1.start()\n    p2.start()'},
    {'qid': 31, 'answer': '定义work函数接收name和n参数，分别用args和kwargs传参启动子进程',
     'title': '进程传参与 PID（必做）',
     'desc': '编写 <code>work(name, n)</code>，打印 <code>name</code> 和循环序号。<br>分别用 <code>args=(\'张三\', 5)</code> 与 <code>kwargs</code> 形式各启动一个子进程。<br>在子进程内打印 <code>os.getpid()</code>，在主进程打印子进程的 <code>pid</code>。',
     'reference': 'import os\nimport multiprocessing\n\ndef work(name, n):\n    print(os.getpid(), name, n)\n\nif __name__ == "__main__":\n    p1 = multiprocessing.Process(target=work, args=("张三", 5))\n    p2 = multiprocessing.Process(target=work, kwargs={"name": "李四", "n": 10})\n    p1.start()\n    p2.start()\n    print("main:", os.getpid())'},
    {'qid': 32, 'answer': '在accept后创建子进程处理每个客户端，主进程继续accept',
     'title': '多进程/多线程处理客户端（选做）',
     'desc': '尝试在服务端 <code>accept</code> 后使用子进程（或线程）处理单个客户端，避免"一个人聊很久别人排队"（写出思路或伪代码即可）。',
     'reference': '# 思路：每 accept 一个客户端就 fork 一个子进程去处理\n# 主进程继续 accept，子进程负责与该客户端通信\n\nimport socket\nimport multiprocessing\n\ndef handle_client(conn, addr):\n    """子进程：处理单个客户端的通信"""\n    print(f"[子进程] 处理 {addr}")\n    while True:\n        data = conn.recv(1024)\n        if not data:\n            break\n        print(f"{addr}: {data.decode(\'utf-8\')}")\n        conn.send(b"received")\n    conn.close()\n    print(f"[子进程] {addr} 断开")\n\nif __name__ == "__main__":\n    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    server.bind((\'0.0.0.0\', 9000))\n    server.listen(128)\n    print("服务器启动，等待连接...")\n    while True:\n        conn, addr = server.accept()\n        # 创建子进程处理该客户端\n        p = multiprocessing.Process(target=handle_client, args=(conn, addr))\n        p.start()\n        # 主进程继续 accept，不阻塞\n\n# 也可以用 threading.Thread 替代 Process，\n# 线程更轻量但受 GIL 限制；进程隔离更好但开销更大。'},
]

# ============================================================
# Generate Card HTML (matching 003 format)
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

# Remove the JavaScript highlight function (we pre-highlight via Python)
html = re.sub(r'function highlightPythonCode\(\) \{[^}]*?\n\}', '', html, flags=re.DOTALL)
# Remove the DOMContentLoaded call to highlightPythonCode
html = re.sub(r'\s+highlightPythonCode\(\);', '', html)

# Page-level replacements
html = html.replace('Python 练习 003', 'Python 练习 004')
html = html.replace('python_basic_test_003.html', 'python_basic_test_004.html')
html = html.replace('34 道题 · 选择题 + 填空题 + 简答题 + 代码实战 · 即时反馈 · 记录保存',
                      '33 道题 · 选择题 + 填空题 + 简答题 + 代码实战 · 即时反馈 · 记录保存')
html = html.replace('py_day03_quiz_history', 'py_day04_quiz_history')
html = html.replace('/20</span></div>\n      <div class="score-item"><div class="score-label">主观题</div><div class="score-num"><span id="subjDone">0</span>/14',
                      '/20</span></div>\n      <div class="score-item"><div class="score-label">主观题</div><div class="score-num"><span id="subjDone">0</span>/13')

# Replace quiz nav
old_nav = '''<div class="quiz-nav">
    <a href="/static/python_basic_test_002.html" class="quiz-arrow" title="上一练习">◂</a>
    <div class="quiz-dropdown">
      <button class="quiz-dropdown-btn" onclick="toggleDropdown(this)">练习 003 <span class="arrow-icon">▾</span></button>
      <div class="quiz-dropdown-menu">
        <a href="/static/python_basic_test_001.html">练习 001</a>
        <a href="/static/python_basic_test_002.html">练习 002</a>
        <a href="/static/python_basic_test_003.html" class="active">练习 003</a>
      </div>
    </div>
    <span class="quiz-arrow disabled" title="已是最后一个">▸</span>
  </div>'''

new_nav = '''<div class="quiz-nav">
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

html = html.replace(old_nav, new_nav)

# Replace body content using line-based slicing
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

    <div class="section-title"><span class="icon"></span>三、简答题（6 题）</div>

{short_cards}
</div>

<!-- ====== 四、代码实操 6题 ====== -->

<div class="section">

    <div class="section-title"><span class="icon"></span>四、代码实操（7 题）</div>

{write_cards}
</div>

'''
    html = html[:p1] + new_body + html[p_end:]
else:
    print(f'ERROR: p1={p1}, p_end={p_end}')

# Write output
output_path = r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_004.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Generated: {output_path}')
print(f'Size: {len(html)} bytes')
print(f'Choices: {len(choices)}, Fills: {len(fills)}, Shorts: {len(shorts)}, Writes: {len(writes)}')

# Verify
has_old = '闭包' in html or '装饰器' in html
has_new = 'TCP' in html and 'socket' in html
has_fill_input = 'fill-input' in html
has_ref_toggle = 'ref-toggle' in html
has_code_editor = 'code-editor' in html
has_data_qid = 'data-qid' in html
print(f'Old content removed: {not has_old}')
print(f'New content present: {has_new}')
print(f'fill-input class: {has_fill_input}')
print(f'ref-toggle: {has_ref_toggle}')
print(f'code-editor: {has_code_editor}')
print(f'data-qid attrs: {has_data_qid}')
print(f'Q6 (四次挥手): {"四次挥手" in html}')
print(f'Q7 (多进程客户端): {"多进程/多线程" in html}')
