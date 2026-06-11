#!/usr/bin/env python3
"""练习 014 的题目数据（Day02 大模型提示词 - API调用与提示词技巧）。"""

choices = [
    {'qid': 1, 'question': '在真实项目中，使用 Python 调用大模型 API 的主要目的是什么？', 'options': ['让学生少写代码', '让程序自动把问题发送给模型并处理结果', '替代所有数据库操作', '让模型自动保存 API Key'], 'answer': 'B', 'analysis': 'API 调用的核心是让程序自动化地与模型交互，包括发送问题、接收结果、解析处理。'},
    {'qid': 2, 'question': 'api_key 的主要作用是？', 'options': ['指定模型名称', '指定输出语言', '证明调用者有权限访问模型服务', '控制是否流式输出'], 'answer': 'C', 'analysis': 'API Key 是身份凭证，用于证明调用者有权访问模型服务，类似账户密码。'},
    {'qid': 3, 'question': 'base_url 的主要作用是？', 'options': ['指定请求发往哪个模型服务地址', '指定用户输入内容', '指定返回结果的字体', '指定代码文件保存路径'], 'answer': 'A', 'analysis': 'base_url 指定 API 请求的目标地址，不同平台有不同的兼容接口地址。'},
    {'qid': 4, 'question': '关于批处理和流式输出，下列说法正确的是？', 'options': ['批处理必须使用 stream=True', '流式输出会一次性返回完整答案', '批处理通常一次性返回完整结果', '流式输出不能用于聊天场景'], 'answer': 'C', 'analysis': '批处理等模型生成完毕后一次性返回；流式输出逐段返回，适合聊天等需要即时反馈的场景。'},
    {'qid': 5, 'question': '在 OpenAI 兼容接口中开启流式输出的常见参数是？', 'options': ['fast=True', 'stream=True', 'flow=False', 'print=True'], 'answer': 'B', 'analysis': 'stream=True 开启流式输出，返回值变为可迭代的流式对象。'},
    {'qid': 6, 'question': 'zero-shot 的含义是？', 'options': ['给模型很多示例', '不给示例，直接让模型完成任务', '训练一个新模型', '删除所有提示词'], 'answer': 'B', 'analysis': 'zero-shot 表示不提供任何示例，直接让模型根据指令完成任务。'},
    {'qid': 7, 'question': 'few-shot 更适合下列哪个场景？', 'options': ['固定格式的文本分类', '关闭电脑', '修改 Python 解释器', '安装操作系统'], 'answer': 'A', 'analysis': 'few-shot 通过提供少量示例让模型模仿格式，非常适合需要固定输出格式的任务。'},
    {'qid': 8, 'question': 'CoT 思维链最适合用于？', 'options': ['简单问候', '简单翻译一个词', '多步骤推理问题', '输出当前时间'], 'answer': 'C', 'analysis': 'CoT（思维链）通过要求模型逐步推理，适合数学、逻辑等需要多步骤思考的问题。'},
    {'qid': 9, 'question': 'ReAct 中的 Action 指什么？', 'options': ['模型输出最终答案', '模型决定调用某个工具或执行某个动作', '程序删除提示词', '用户关闭浏览器'], 'answer': 'B', 'analysis': 'ReAct 中 Action 是模型决定调用工具或执行操作的步骤。'},
    {'qid': 10, 'question': '提示词注入攻击的典型特征是？', 'options': ['用户输入中包含试图覆盖原始规则的恶意指令', '用户正常提问天气', '程序正常读取环境变量', '模型正常返回 JSON'], 'answer': 'A', 'analysis': '提示词注入是用户输入中嵌入恶意指令，试图覆盖系统规则，让模型执行非预期操作。'},
]

fills = [
    {'qid': 11, 'question': '大模型 API 调用的四个基本步骤是：导包、________、发送消息、________。', 'answer': '创建客户端、解析结果', 'analysis': '标准流程：导入库 → 创建客户端（配置 base_url 等）→ 发送 messages → 解析返回结果。'},
    {'qid': 12, 'question': 'messages 是大模型接口中的________列表。', 'answer': '对话消息', 'analysis': 'messages 是一个列表，包含 system/user/assistant 等角色的消息字典。'},
    {'qid': 13, 'question': 'OpenAI 兼容接口的好处是可以用类似写法调用不同平台的________。', 'answer': '云端模型', 'analysis': 'OpenAI 兼容接口统一了调用方式，只需更换 base_url 和 api_key 就能切换不同平台。'},
    {'qid': 14, 'question': '流式输出通常需要使用________循环逐段读取模型返回内容。', 'answer': 'for', 'analysis': 'for chunk in stream 循环遍历流式对象，逐段读取并打印内容。'},
    {'qid': 15, 'question': 'end="" 的作用是让 print() 打印后不自动________。', 'answer': '换行', 'analysis': '默认 print() 末尾会加换行符，end="" 让内容连续显示，模拟打字效果。'},
    {'qid': 16, 'question': 'zero-shot 表示不给模型________，直接让模型完成任务。', 'answer': '示例', 'analysis': 'zero-shot 零样本学习，不提供任何示例，完全依赖模型自身的理解能力。'},
    {'qid': 17, 'question': 'few-shot 表示给模型少量________，让模型模仿格式或判断标准。', 'answer': '示例', 'analysis': 'few-shot 少样本学习，通过 1-3 个示例引导模型理解任务格式和要求。'},
    {'qid': 18, 'question': 'CoT 的中文名称是________。', 'answer': '思维链', 'analysis': 'CoT（Chain of Thought）思维链，通过要求模型逐步推理来提高复杂任务的准确率。'},
    {'qid': 19, 'question': 'Self-Consistency 可以理解为多条思路生成答案后进行________或比较。', 'answer': '投票', 'analysis': 'Self-Consistency 通过多条推理路径生成答案，再投票选出最常见的结果。'},
    {'qid': 20, 'question': 'ReAct 的核心循环可以概括为：思考、行动、________、再思考。', 'answer': '观察', 'analysis': 'ReAct 循环：Thought（思考）→ Action（行动）→ Observation（观察）→ 再思考。'},
]

shorts = [
    {'qid': 21, 'question': '为什么真实项目中不能只依赖网页端和大模型聊天？', 'reference': '因为真实项目需要程序自动调用模型、自动处理用户输入、自动解析模型结果，并把结果展示、保存或交给后续流程处理。网页聊天适合体验模型能力，但不适合做自动化业务系统。'},
    {'qid': 22, 'question': '批处理和流式输出有什么区别？', 'reference': '批处理是模型生成完整答案后一次性返回，适合短回答和后台任务；流式输出是一段一段返回内容，适合聊天、长文本生成和需要改善用户等待体验的场景。'},
    {'qid': 23, 'question': '如果模型返回结果取不到，应该如何排查？', 'reference': '应先打印完整响应对象，查看真实返回结构，再根据字段层级取值。不要直接猜字段，也不要在换模型后继续照搬旧的解析路径。'},
    {'qid': 24, 'question': 'zero-shot 和 few-shot 的区别是什么？', 'reference': 'zero-shot 是不给示例，直接让模型完成任务；few-shot 是给模型少量示例，让模型模仿示例的格式、风格或判断标准。'},
    {'qid': 25, 'question': 'few-shot 为什么不是训练模型？', 'reference': 'few-shot 只是把示例放进提示词上下文中，让模型临时参考，不会修改模型参数，也不会让模型永久学会这些示例。'},
    {'qid': 26, 'question': 'CoT 适合什么任务？为什么简单任务不一定适合 CoT？', 'reference': 'CoT 适合数学题、逻辑题、多步骤任务、代码分析等复杂推理任务。简单任务不一定适合 CoT，因为它会增加 token 消耗和响应时间。'},
    {'qid': 27, 'question': '链式提示和 CoT 有什么区别？', 'reference': 'CoT 多数是在一个提示词中要求模型分步推理；链式提示更偏工程实现，是把一个大任务拆成多个子任务，让前一步结果作为下一步输入。'},
    {'qid': 28, 'question': 'Self-Consistency 的优点和代价分别是什么？', 'reference': 'Self-Consistency 的优点是提高复杂推理任务的稳定性；代价是需要多次调用模型，会增加 token 成本、运行时间和代码复杂度。'},
    {'qid': 29, 'question': 'ReAct 中模型和程序分别负责什么？', 'reference': '模型负责思考下一步、选择工具、总结工具结果；程序负责提供工具、执行工具、校验工具调用和返回结果。'},
    {'qid': 30, 'question': '提示词注入攻击应该如何防御？', 'reference': '可以通过分隔符隔离用户输入、明确任务边界、不把敏感信息放入提示词、限制工具调用权限、对输出进行安全检查等方式防御。'},
]

writes = [
    {'qid': 31, 'title': '基础练习：大模型基础调用', 'desc': '使用 OpenAI 兼容接口调用云端模型，让模型回答"请用三句话说明 Python 程序员为什么要学习大模型 API 调用"。', 'reference': 'from openai import OpenAI\n\nclient = OpenAI(\n    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"\n)\n\nresponse = client.chat.completions.create(\n    model="qwen-plus",\n    messages=[\n        {\n            "role": "user",\n            "content": "请用三句话说明 Python 程序员为什么要学习大模型 API 调用。"\n        }\n    ]\n)\n\nanswer = response.choices[0].message.content\nprint(answer)'},
    {'qid': 32, 'title': '基础练习：流式输出', 'desc': '在上一题基础上开启流式输出（stream=True），使用 for 循环逐段读取，用 end="" 和 flush=True 实现实时输出效果。', 'reference': 'from openai import OpenAI\n\nclient = OpenAI(\n    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"\n)\n\nstream = client.chat.completions.create(\n    model="qwen-plus",\n    messages=[\n        {\n            "role": "user",\n            "content": "请用通俗语言解释什么是大模型流式输出。"\n        }\n    ],\n    stream=True\n)\n\nfor chunk in stream:\n    content = chunk.choices[0].delta.content\n    if content:\n        print(content, end="", flush=True)'},
    {'qid': 33, 'title': 'Few-shot 翻译', 'desc': '使用 few-shot 提示词，system 中提供一个英文到中文的翻译示例，user 中提供新的英文句子，让模型参考示例格式翻译。', 'reference': 'from openai import OpenAI\n\nclient = OpenAI(\n    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"\n)\n\nsystem_prompt = """\n你是一个英文到中文的翻译助手。\n请参考下面的示例进行翻译，只输出中文结果，不要输出多余解释。\n\n示例：\n英文：I love Python.\n中文：我喜欢 Python。\n"""\n\nresponse = client.chat.completions.create(\n    model="qwen-plus",\n    messages=[\n        {"role": "system", "content": system_prompt},\n        {"role": "user", "content": "Large models can call external tools."}\n    ]\n)\n\nprint(response.choices[0].message.content)'},
    {'qid': 34, 'title': 'Zero-shot CoT', 'desc': '让模型回答年龄题（小明6岁妹妹一半，哥哥大4岁，现在70岁），要求"请一步一步思考"，打印推理过程和最终答案。', 'reference': 'from openai import OpenAI\n\nclient = OpenAI(\n    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"\n)\n\nquestion = """\n当小明 6 岁时，他的妹妹年龄是他的一半。他的哥哥比小明大 4 岁。\n现在小明 70 岁了，请问他的妹妹和哥哥年龄加起来是多少？\n"""\n\nprompt = f"""\n请解决下面的问题。\n\n题目：\n{question}\n\n要求：\n1. 请一步一步思考。\n2. 先写出推理过程。\n3. 最后单独给出最终答案。\n"""\n\nresponse = client.chat.completions.create(\n    model="qwen-plus",\n    messages=[\n        {"role": "user", "content": prompt}\n    ]\n)\n\nprint(response.choices[0].message.content)'},
    {'qid': 35, 'title': '链式提示', 'desc': '完成三步链式任务：从文本中抽取要点 → 根据要点写摘要 → 优化摘要语言。前一步结果作为下一步输入，每步都打印。', 'reference': 'from openai import OpenAI\n\nclient = OpenAI(\n    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"\n)\n\ndef ask_model(prompt):\n    response = client.chat.completions.create(\n        model="qwen-plus",\n        messages=[{"role": "user", "content": prompt}]\n    )\n    return response.choices[0].message.content\n\narticle = """\n近年来，大模型在客服、教育、办公和数据分析等场景中应用越来越广。\n企业在使用大模型时，通常需要通过 Prompt 工程约束模型输出格式，\n并结合知识库、外部工具和安全审核来提高回答可靠性。\n"""\n\n# 第一步：抽取要点\npoints = ask_model(f\'请从下面文本中抽取 3 个关键要点。\\n\\n文本：\\n"""{article}"""\')\nprint("第一步：抽取要点")\nprint(points)\n\n# 第二步：生成摘要\nsummary = ask_model(f\'请根据下面的要点，生成一段 100 字以内的摘要。\\n\\n要点：\\n"""{points}"""\')\nprint("第二步：生成摘要")\nprint(summary)\n\n# 第三步：优化摘要\nfinal = ask_model(f\'请优化下面这段摘要，使语言更简洁、正式。\\n\\n摘要：\\n"""{summary}"""\')\nprint("第三步：优化摘要")\nprint(final)'},
    {'qid': 36, 'title': 'Self-Consistency 简化实现', 'desc': '让模型针对同一个问题生成 3 个不同思路（输出 JSON 数组），再让模型从多个答案中选出最合理的结果。不使用 eval()。', 'reference': 'import json\nfrom openai import OpenAI\n\nclient = OpenAI(\n    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"\n)\n\ndef ask_model(prompt):\n    response = client.chat.completions.create(\n        model="qwen-plus",\n        messages=[{"role": "user", "content": prompt}]\n    )\n    return response.choices[0].message.content\n\nquestion = "当小明 6 岁时，妹妹 3 岁。现在小明 70 岁，妹妹多少岁？"\n\n# 第一步：生成 3 个思路\nideas_text = ask_model(f\'"""\n请针对下面问题，给出 3 个不同的解题思路。\n问题：{question}\n输出要求：只输出 JSON 数组，格式：["思路1", "思路2", "思路3"]\n"""\')\nideas = json.loads(ideas_text)\n\n# 第二步：按每个思路回答\nanswers = []\nfor idea in ideas:\n    answer = ask_model(f\'请按照思路"{idea}"解决问题。问题：{question}\')\n    answers.append(answer)\n\n# 第三步：评审选出最终答案\nfinal = ask_model(f\'请从下面多个答案中选出最合理的答案。\\n问题：{question}\\n候选答案：{answers}\')\nprint("最终结果：", final)'},
    {'qid': 37, 'title': 'ReAct 简化工具调用', 'desc': '实现简化版 ReAct 天气查询：定义 get_weather(city) 模拟工具，让模型判断需要查询哪个城市，程序调用工具，再把结果交给模型生成自然语言回答。', 'reference': 'from openai import OpenAI\n\nclient = OpenAI(\n    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"\n)\n\ndef get_weather(city):\n    weather_data = {\n        "深圳": "小雨，25-29℃，湿度较高，建议带伞。",\n        "北京": "晴，18-27℃，空气较干燥，适合出行。",\n        "上海": "多云，22-28℃，体感舒适。"\n    }\n    return weather_data.get(city, "暂时没有查询到该城市的天气。")\n\ndef ask_model(prompt):\n    response = client.chat.completions.create(\n        model="qwen-plus",\n        messages=[{"role": "user", "content": prompt}]\n    )\n    return response.choices[0].message.content\n\nuser_question = "我明天去深圳上课，需要带伞吗？"\n\n# 第一步：让模型提取城市\ncity = ask_model(f\'从问题中提取城市名，只输出城市名。\\n问题：{user_question}\').strip()\nprint("城市：", city)\n\n# 第二步：调用工具\nweather = get_weather(city)\nprint("天气：", weather)\n\n# 第三步：生成最终回答\nanswer = ask_model(f\'用户问题：{user_question}\\n天气结果：{weather}\\n请用自然语言回答。\')\nprint("回答：", answer)'},
]
