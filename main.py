import os
import json
import ai

if os.path.exists("config.json"):
    with open("config.json", "r", encoding="utf-8") as cfg:
        config = json.load(cfg)
else:
    print("所有模型:", end=' ')
    for i in ai.ailist()["models"]:
        print(i['name'], end=' ')
    print(end='\n')
    print('如果你使用SodaAI以外的其他模型，你将无法使用插件功能')
    model = input("请输入你想使用的模型 (SodaAI:latest)：")
    if model == "":
        model = "SodaAI:latest"
    with open("config.json", "w", encoding="utf-8") as cfg:
        config = {"model": model}
        cfg.write(json.dumps(config))


# 创建模型
if ai.create()['status'] == 'success':
    print('SodaAI 模型成功初始化')
else:
    print('未知错误：模型创建失败')
    print(ai.create())
    exit()


# 欢迎语
print(fr'[{config["model"]}]', end=' ', flush=True)
for chunk in ai.chat(config["model"], [{'role': 'user', 'content': '你好~'}]):
    print(chunk, end='', flush=True)
print(end='\n', flush=False)

# 循环用户输入
while True:
    # 用户输入
    message = [{'role': 'user', 'content': input("[user] ")}]
    # AI输出
    print(fr'[{config["model"]}]', end=' ', flush=True)
    for chunk in ai.chat(config["model"], message, stream=True):
        if isinstance(chunk, list):
            print(chunk)
        else:
            print(chunk, end='', flush=True)
    # 断行
    print(end='\n', flush=False)
