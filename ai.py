import requests
from langchain_community.llms.ollama import Ollama

import plugin
import ollama


def create():
    plugin.init()

    model_file = '''
    FROM qwen2.5
    SYSTEM ''' + plugin.prompt()
    return ollama.create(model='SodaAI', modelfile=model_file)

def ailist():
    import ollama
    return ollama.list

def chat(model, messages:list, stream=True, temperature=1, func="none"):
    if messages[-1]["content"][0] == "/":
        plugin.plugin_manager(messages[-1]["content"][1:].split(' '))
        return
    res = ollama.chat(model=model, messages=messages, stream=stream)
    # 迭代生成器并返回每个输出块
    cc = ""
    for chunk in res:
        cc += chunk["message"]["content"]
        yield chunk["message"]["content"]
    if func == "return":
        return
    plugin.chat(messages[-1]["content"], cc)