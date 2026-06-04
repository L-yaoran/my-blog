# day05_多线程生成器协程课后作业

## 一、单选题

1. 在 Python 中，**线程**相对**进程**，更准确的描述是（ ）  
A. 线程是资源分配的基本单位  
B. 线程是 CPU 调度的基本单位，依附于进程存在  
C. 线程可以脱离进程单独运行  
D. 进程与线程都不共享内存

2. 创建并启动子线程的正确三步不包含（ ）  
A. `import threading`  
B. `threading.Thread(target=func, ...)`  
C. `线程对象.start()`  
D. `threading.spawn(func)`

3. 关于 `Thread` 的 `target` 参数，正确的是（ ）  
A. 应写成 `target=func()`  
B. 应写成 `target=func`  
C. `target` 必须是 lambda  
D. `target` 只能是字符串函数名

4. 对**只有一个参数**的任务函数，使用 `args` 传参时应写成（ ）  
A. `args=(5)`  
B. `args=(5,)`  
C. `args=5`  
D. `args=[5]`

5. 同一进程内多个线程对**全局列表**执行 `append`，一般（ ）  
A. 不需要也不应该共享  
B. 可以共享，能看到同一份列表  
C. 每个线程有独立副本  
D. 必须先 `fork` 才能共享

6. 多个线程并发对同一整型全局变量做 `count = count + 1` 可能出现结果小于理论值，主要是因为（ ）  
A. Python 版本太低  
B. `+1` 非原子操作，存在调度交错导致丢更新  
C. `global` 写多了  
D. 线程不能访问全局变量

7. 互斥锁的典型用法正确的是（ ）  
A. 每个线程各自 `threading.Lock()` 一把新锁保护同一变量  
B. 多个线程共用**同一把** `Lock` 对象，在临界区 `acquire`/`release` 或用 `with lock:`  
C. 上锁后不必释放，程序结束自动释放  
D. `Lock` 只能用于进程不能用于线程

8. **CPython** 中的 **GIL** 主要指（ ）  
A. 用户为共享变量自己创建的 `threading.Lock`  
B. 解释器层的全局锁，同一时刻通常只有一个线程执行 Python 字节码  
C. 网络全局 IP  
D. 生成器的全局变量

9. 下列能得到一个**生成器对象**的是（ ）  
A. `g = [i for i in range(3)]`  
B. `g = (i for i in range(3))`  
C. `g = {i for i in range(3)}`  
D. `g = list(range(3))`

10. 关于 `async` / `await` 与 `asyncio.run`，正确的是（ ）  
A. `async def` 定义的函数一调用就会从头执行完整个函数体  
B. `await` 用于等待可等待对象并把控制权交回事件循环  
C. `asyncio.run` 可以在任意嵌套函数里随意连续调用实现并发  
D. 协程运行在独立进程里，与线程无关

## 二、填空题

1. 进程是操作系统________分配的基本单位；线程是________调度的基本单位。  
2. 创建线程类：`threading.Thread(target=________, args=..., kwargs=...)`。  
3. 主线程默认会等待所有________线程结束后再结束进程（常规情况）。  
4. 若希望主线程结束时子线程不再继续执行，可设置________线程（`daemon=True`）。  
5. 线程之间与进程相比，________之间默认共享进程内全局数据；进程之间默认________共享。  
6. 互斥锁对象的创建方式常为 `lock = threading.________()`。  
7. 含 `yield` 的函数称为生成器函数，调用该函数得到的是________。  
8. 生成器耗尽后再 `next`，会抛出________异常；`for` 遍历时会自动处理该结束。  
9. 协程三要素：`async def`、________、顶层常用 `asyncio.run(...)`。  
10. 在同一协程函数里要**并发**执行多个协程，常用 `asyncio.________` 包装成任务后再 `await`。  

## 三、简答题

1. 进程与线程是什么关系？为什么说“没有进程就没有线程”？

   **答：** 线程必须**依附在进程**里运行：进程向操作系统申请地址空间、文件描述符等资源，线程是在该进程内部被调度执行的执行流。没有进程作为“容器”和资源边界，线程无法单独存在，因此说没有进程就没有线程。

2. 为什么多线程执行时，打印顺序可能每次运行都不一样？

   **答：** 多个线程**谁先获得 CPU、执行到哪一行**，由操作系统和解释器的**调度策略**决定，不是代码书写的先后顺序保证的。因此并发时输出顺序**不确定**属正常现象；若要固定顺序需用 `join`、同步原语或单线程逻辑等显式协调。

3. 线程之间共享全局变量与进程之间不共享，区别的原因是什么？

   **答：** 同一进程内的线程共用**同一地址空间**，模块级全局变量在同进程内**只有一份**；而每个进程有**独立的虚拟地址空间**，子进程往往是父进程内存的拷贝或隔离视图，因此**各进程的全局变量互不天然共享**，这是二者内存模型不同的结果。

4. 互斥锁要解决什么问题？使用 `with lock:` 有什么好处？

   **答：** 互斥锁用于**线程同步**，保证**同一时刻只有一个线程**进入临界区操作共享数据，避免“读—改—写”被抢占导致的数据竞争。`with lock:` 在离开代码块时**自动释放锁**，可减少忘记 `release()` 造成的**死锁**或长期持锁问题。

5. 简要说明 GIL 与 `threading.Lock` 的区别；为什么在 CPython 里有时仍要给共享数据加 Lock？

   **答：** **GIL** 是 CPython 解释器层的**全局解释器锁**，限制**同一时刻通常只有一条线程在执行 Python 字节码**。`threading.Lock` 是程序员为保护**自己的共享数据结构**而创建的**显式锁**。即使存在 GIL，一条源码语句也可能对应**多条字节码**，线程仍可能在中间被切换，因此**业务上的非原子更新**仍可能出错，该加 Lock 仍需加。

6. 生成器相对一次性构造完整列表，主要优点是什么？`yield` 与 `return` 在生成器函数中的典型区别？

   **答：** 生成器**按需产出**元素，不一次性把所有结果放进内存，**节省内存**，适合大数据或惰性计算。`yield` 会**暂停**当前函数、向外产出一个值，下次从暂停处继续；`return` 用于**结束**生成器函数（结束迭代），语义上不同于中途反复产出的 `yield`。

7. 协程三要素是什么？`asyncio.run` 与 `asyncio.create_task` 分别适合什么场景？

   **答：** 三要素：**`async def` 定义协程函数**、函数内对可等待对象使用 **`await`**、程序入口用 **`asyncio.run`** 启动事件循环。`asyncio.run` 常用于**最外层**启动整个异步程序；在同一 `async def` 里要对多个协程**并发**时，用 **`create_task`** 将协程包装为任务，再配合 `await` 等待完成；**连续两次**对同一入口 `asyncio.run` 往往是**串行**的两次运行。

## 四、代码实操

### 1. 多线程入门（必做）

**任务要求：**

- 定义两个无参任务函数（如模拟“写代码”“听音乐”打印若干行）。  
- 创建两个 `threading.Thread`，指定 `target`，调用 `start()`。  
- 观察多次运行输出顺序是否可能不同。  

### 2. 线程传参（必做）

**任务要求：为一个带两个位置参数的任务创建线程；再为一个用关键字参数更合适的任务创建线程。**

- 使用 `args=('小明', 3)`（或自拟）按位置传参。  
- 使用 `kwargs={...}` 按关键字传参。  
- 说明 `args` 单元素必须加逗号的原因（注释）。  

### 3. 全局变量与互斥锁（重点必做）

**任务要求：**

- 定义全局整型 `count = 0`，两个线程各循环较大次数（如 10 万次）执行 `count += 1`（注意函数内需 `global count`）。  
- 先**不加锁**运行，观察结果是否可能小于 `2 * 次数`。  
- 再用**同一把** `threading.Lock` 包裹 `count += 1` 临界区（推荐 `with lock:`），使结果稳定为预期值。  

### 4. 生成器（必做）

**任务要求：**

- 用**生成器推导式**创建生成器，并用 `for` 遍历打印。  
- 再写一个含 **`yield`** 的生成器函数，用 `next` 至少取两次，说明每次从何处继续执行（注释）。  

### 5. asyncio 入门与并发任务（重点必做）

**任务要求：**

- 定义 `async def work(name):` 内 `print` 开始，`await asyncio.sleep(1)`，`print` 结束。  

- 定义 `async def main():`，使用 **`asyncio.create_task`** 同时调度至少两个 `work`，再 **`await`** 等待它们完成。  

- 最外层使用 **`asyncio.run(main())`**。  

- 注释说明：若把两个协程改成**连续两次** `await work(...)`（不用 `create_task`），与并发版耗时区别。  

  ### 6.**CPU 密集型**任务

  用一段话对比：**CPU 密集型**任务在 CPython 下更适合多进程还是多线程？**I/O 密集型**更适合线程还是协程简要说明理由。

  ### 7.查阅或回忆

  查阅或回忆：`join()` 等待子线程结束与用互斥锁保护临界区，在“牺牲并行度”方面有何异同（各写一两句）。  

## 五、参考答案

### 单选题答案

1.B  2.D  3.B  4.B  5.B  6.B  7.B  8.B  9.B  10.B

### 填空题参考答案

1. 资源；CPU  
2. 函数名（可调用对象，不加括号）  
3. 非守护（子）  
4. 守护  
5. 线程；不  
6. `Lock`  
7. 生成器（生成器对象）  
8. `StopIteration`  
9. `await`  
10. `create_task`

### 简答题参考答案（与第三节一致，可单独印）

1. 线程依附进程；进程提供资源与地址空间，无线程则无线程执行载体。  
2. 调度无序，顺序不保证。  
3. 同进程共享地址空间；进程隔离。  
4. 防竞争；`with` 自动释放。  
5. GIL 解释器级；Lock 用户级；字节码间仍可切换。  
6. 省内存、惰性；`yield` 暂停产出，`return` 结束。  
7. `async`/`await`/`asyncio.run`；`run` 顶层启动，`create_task` 并发包装。  

### 代码实操参考关键代码

**第1题：多线程**

```python
import threading

def coding():
    for i in range(3):
        print("coding", i)

def music():
    for i in range(3):
        print("music", i)

t1 = threading.Thread(target=coding)
t2 = threading.Thread(target=music)
t1.start()
t2.start()
```

**第2题：传参**

```python
def greet(name, times):
    for i in range(times):
        print(name, i)

def show(**kwargs):
    print(kwargs)

t1 = threading.Thread(target=greet, args=("小明", 3))
t2 = threading.Thread(target=show, kwargs={"a": 1, "b": 2})
t1.start()
t2.start()
# 单元素元组: args=(5,) 不能写成 args=(5)
```

**第3题：互斥锁**

```python
import threading

count = 0
lock = threading.Lock()
N = 100000

def add():
    global count
    for _ in range(N):
        with lock:
            count += 1

t1 = threading.Thread(target=add)
t2 = threading.Thread(target=add)
t1.start()
t2.start()
t1.join()
t2.join()
print(count)  # 200000
```

**第4题：生成器**

```python
g = (x * 2 for x in range(4))
for v in g:
    print(v)

def gen(n):
    for i in range(n):
        yield i

it = gen(3)
print(next(it))  # 0
print(next(it))  # 1
```

**第5题：asyncio**

```python
import asyncio

async def work(name):
    print("start", name)
    await asyncio.sleep(1)
    print("end", name)

async def main():
    t1 = asyncio.create_task(work("A"))
    t2 = asyncio.create_task(work("B"))
    await t1
    await t2

asyncio.run(main())
```

### 挑战题参考答案

6. **CPU 密集型**：在 **CPython** 下多线程受 **GIL** 影响，纯 Python 计算往往**难以吃满多核**，更适合用**多进程**把任务分到多核。**I/O 密集型**：线程可在 I/O 阻塞时让出，仍有价值；**协程**在单线程事件循环里通过 `await` 挂起等待，**大量 I/O 并发**时开销往往更小，适合高并发网络/等待场景（与多进程分工不同）。

7. **`join()`**：让调用方**等待某个线程先跑完**，其它线程期间是否并行取决于你是否只 join 一个；容易写成**阶段性串行**。**互斥锁**：只保证**临界区串行**，锁外其它线程仍可并行，并行度通常**好于“整条线程顺序 join”**的简单写法，但锁粒度过大也会接近单线程。
