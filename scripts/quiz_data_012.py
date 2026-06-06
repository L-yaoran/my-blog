#!/usr/bin/env python3
"""练习 012 的题目数据（Day10 Linux 基础知识）。"""

choices = [
    {'qid': 1, 'question': '计算机系统通常由（ ）组成。', 'options': ['硬件资源和软件资源', '鼠标和键盘', '浏览器和数据库', '微信和 PyCharm'], 'answer': 'A', 'analysis': '计算机系统由硬件资源（CPU、内存、硬盘等）和软件资源（操作系统、应用软件等）组成。'},
    {'qid': 2, 'question': '操作系统的主要作用是（ ）', 'options': ['只负责画图', '管理硬件和软件资源', '只负责聊天', '只负责写 Python 代码'], 'answer': 'B', 'analysis': '操作系统负责管理计算机的硬件和软件资源，让应用软件能够使用 CPU、内存、硬盘、网络等资源。'},
    {'qid': 3, 'question': 'Linux 在真实工作中最常见的使用场景是（ ）', 'options': ['服务器', '游戏手柄', '纸质文档', '鼠标垫'], 'answer': 'A', 'analysis': 'Linux 在服务器领域占据主导地位，大多数互联网公司的后端服务都运行在 Linux 服务器上。'},
    {'qid': 4, 'question': 'Ubuntu 和 CentOS 都属于（ ）', 'options': ['Linux 发行版', 'Python 库', '浏览器插件', '数据库表'], 'answer': 'A', 'analysis': 'Ubuntu 和 CentOS 都是 Linux 的发行版，基于 Linux 内核，搭配不同的软件包和桌面环境。'},
    {'qid': 5, 'question': 'SSH 默认端口通常是（ ）', 'options': ['21', '22', '80', '3306'], 'answer': 'B', 'analysis': 'SSH 默认使用 22 端口。21 是 FTP，80 是 HTTP，3306 是 MySQL。'},
    {'qid': 6, 'question': 'Linux 的根目录是（ ）', 'options': ['C:\\', 'D:\\', '/', 'root:'], 'answer': 'C', 'analysis': 'Linux 只有一个根目录 /，所有文件和目录都在根目录下。Windows 有多个盘符如 C:\\、D:\\。'},
    {'qid': 7, 'question': '查看当前所在目录的命令是（ ）', 'options': ['pwd', 'mkdir', 'touch', 'rm'], 'answer': 'A', 'analysis': 'pwd（Print Working Directory）显示当前所在目录的完整路径。'},
    {'qid': 8, 'question': '创建多级目录时，常用的命令是（ ）', 'options': ['mkdir -p a/b/c', 'touch -p a/b/c', 'cat -p a/b/c', 'clear -p a/b/c'], 'answer': 'A', 'analysis': 'mkdir -p 会在父目录不存在时自动创建，可以一次性创建多级目录。'},
    {'qid': 9, 'question': '> 和 >> 的区别是（ ）', 'options': ['> 追加，>> 覆盖', '> 覆盖，>> 追加', '两者完全一样', '两者都只能删除文件'], 'answer': 'B', 'analysis': '> 覆盖写入（替换原内容），>> 追加写入（保留原内容，在末尾添加）。'},
    {'qid': 10, 'question': 'vim 中按 i 的作用是（ ）', 'options': ['进入输入模式', '直接退出', '删除文件', '打包文件'], 'answer': 'A', 'analysis': '在 vim 的命令模式下按 i 进入输入模式（Insert mode），可以开始编辑文本。'},
]

fills = [
    {'qid': 11, 'question': 'Linux 常用于________场景。', 'answer': '服务器', 'analysis': 'Linux 在服务器领域占据主导地位，大多数互联网公司的后端服务都运行在 Linux 上。'},
    {'qid': 12, 'question': 'Ubuntu 常用的软件包管理工具是________。', 'answer': 'apt', 'analysis': 'Ubuntu 使用 apt（Advanced Package Tool）管理软件包，如 apt install、apt update。'},
    {'qid': 13, 'question': 'CentOS 传统上常用的软件包管理工具是________。', 'answer': 'yum', 'analysis': 'CentOS 传统上使用 yum 管理软件包，新版本（CentOS 8+）改用 dnf。'},
    {'qid': 14, 'question': 'SSH 连接云服务器通常需要公网 IP、端口、用户名和________。', 'answer': '认证方式（或密码/密钥）', 'analysis': 'SSH 连接需要认证方式，可以是密码或密钥对。'},
    {'qid': 15, 'question': 'Linux 路径使用________作为分隔符。', 'answer': '/', 'analysis': 'Linux 使用 / 作为路径分隔符，如 /home/user/file.txt。Windows 使用 \\。'},
    {'qid': 16, 'question': 'ls 命令用于查看当前目录下的________。', 'answer': '文件和目录', 'analysis': 'ls 列出当前目录下的所有文件和目录，加 -l 显示详细信息，加 -a 显示隐藏文件。'},
    {'qid': 17, 'question': 'cd .. 表示回到________目录。', 'answer': '上一级', 'analysis': 'cd .. 切换到当前目录的父目录（上一级目录）。'},
    {'qid': 18, 'question': 'touch file.txt 的作用是创建一个________。', 'answer': '文件', 'analysis': 'touch 命令创建空文件，如果文件已存在则更新修改时间。'},
    {'qid': 19, 'question': 'rm 删除文件后通常不会进入________。', 'answer': '回收站', 'analysis': 'Linux 的 rm 命令直接删除文件，不经过回收站，删错很难恢复。'},
    {'qid': 20, 'question': 'vim 中 :wq 表示________。', 'answer': '保存并退出', 'analysis': ':w 表示保存（write），:q 表示退出（quit），:wq 表示保存并退出。'},
]

shorts = [
    {'qid': 21, 'question': '请说明操作系统的作用。', 'reference': '操作系统负责管理计算机硬件和软件资源，让应用软件能够使用 CPU、内存、硬盘、网络等资源。'},
    {'qid': 22, 'question': '为什么 Day10 选择用云服务器演示 Linux，而不是只使用本地虚拟机？', 'reference': '因为虚拟机安装耗时较长，且不同电脑可能遇到配置问题；云服务器创建更快，也更接近真实工作中的服务器使用方式。'},
    {'qid': 23, 'question': 'Ubuntu 和 CentOS 有哪些区别？至少说出两点。', 'reference': 'Ubuntu 常用 apt，新手资料和 AI 开发资料较多；CentOS 传统服务器教程较多，常用 yum 或 dnf，和 RedHat 生态关系更密切。'},
    {'qid': 24, 'question': 'SSH 连接 Linux 服务器需要哪些关键信息？', 'reference': '需要公网 IP、SSH 端口、用户名、认证方式，认证方式可以是密码或密钥。'},
    {'qid': 25, 'question': 'Linux 路径和 Windows 路径有什么区别？', 'reference': 'Windows 常见多个盘符，如 C 盘、D 盘，路径使用 \\；Linux 只有一个根目录 /，路径使用 /。'},
    {'qid': 26, 'question': 'pwd、ls、cd、clear 分别有什么作用？', 'reference': 'pwd 查看当前目录，ls 查看目录内容，cd 切换目录，clear 清屏。'},
    {'qid': 27, 'question': 'mkdir 和 touch 有什么区别？', 'reference': 'mkdir 用于创建目录，touch 用于创建文件。'},
    {'qid': 28, 'question': 'cat、more、head、tail 分别适合什么查看场景？', 'reference': 'cat 适合查看小文件；more 适合分页查看大文件；head 查看文件开头；tail 查看文件结尾。'},
    {'qid': 29, 'question': '为什么执行 rm 前要先确认当前目录和目标文件？', 'reference': '因为 rm 删除后通常没有回收站，删错文件可能很难恢复，所以要先确认当前目录和目标文件。'},
    {'qid': 30, 'question': 'vim 的三种模式分别是什么？如何保存退出？', 'reference': 'vim 有命令模式、输入模式、底线命令模式。打开文件后按 i 进入输入模式，编辑完按 Esc 回到命令模式，再输入 :wq 保存退出。'},
]

writes = [
    {'qid': 31, 'title': '模仿题 1：创建课堂目录', 'desc': '在家目录下创建 linux_homework 目录，进入该目录，并查看当前位置。', 'reference': 'cd ~\nmkdir linux_homework\ncd linux_homework\npwd'},
    {'qid': 32, 'title': '模仿题 2：创建文件并写入内容', 'desc': '在 linux_homework 目录下创建 notes.txt，写入一行内容：Linux homework day10，然后查看文件内容。', 'reference': 'cd ~/linux_homework\ntouch notes.txt\necho "Linux homework day10" > notes.txt\ncat notes.txt'},
    {'qid': 33, 'title': '模仿题 3：创建多级目录', 'desc': '在 linux_homework 目录下创建 project/data/raw 多级目录，并查看 project 下的内容。', 'reference': 'cd ~/linux_homework\nmkdir -p project/data/raw\nls project'},
    {'qid': 34, 'title': '变体题 1：追加内容', 'desc': '向 notes.txt 中追加一行内容：Linux is useful for AI deployment，然后查看文件内容。', 'reference': 'cd ~/linux_homework\necho "Linux is useful for AI deployment" >> notes.txt\ncat notes.txt'},
    {'qid': 35, 'title': '变体题 2：复制和移动文件', 'desc': '把 notes.txt 复制到 project/data/raw/notes_copy.txt，再把它移动为 project/data/raw/notes_final.txt。', 'reference': 'cd ~/linux_homework\ncp notes.txt project/data/raw/notes_copy.txt\nmv project/data/raw/notes_copy.txt project/data/raw/notes_final.txt\nls project/data/raw'},
    {'qid': 36, 'title': '变体题 3：打包目录', 'desc': '把 project 目录打包成 project.tar.gz。', 'reference': 'cd ~/linux_homework\ntar -zcvf project.tar.gz project\nls'},
    {'qid': 37, 'title': '综合案例 1：整理 AI 项目日志目录', 'desc': '创建 ai_app/logs、ai_app/config、ai_app/scripts 目录结构，在 logs 下创建 app.log，写入 app started，追加 first request success，查看日志内容。', 'reference': 'cd ~/linux_homework\nmkdir -p ai_app/logs ai_app/config ai_app/scripts\ntouch ai_app/logs/app.log\necho "app started" > ai_app/logs/app.log\necho "first request success" >> ai_app/logs/app.log\ncat ai_app/logs/app.log'},
    {'qid': 38, 'title': '综合案例 2：使用 vim 创建配置文件', 'desc': '在 ai_app/config 下使用 vim 创建 app.conf，写入 port=8000 和 env=dev，保存退出后用 cat 查看内容。', 'reference': 'cd ~/linux_homework\nvim ai_app/config/app.conf\n# 按 i 进入输入模式，输入:\n# port=8000\n# env=dev\n# 按 Esc，输入 :wq 保存退出\n\ncat ai_app/config/app.conf'},
]
