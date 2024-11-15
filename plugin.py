promptv = "You are a assistant, Your name is 酸钠酱, You answer in Chinese. "
PluginDir = './plugins'
plugins = []

def init():
    import os
    import json
    global promptv
    files = os.listdir(PluginDir)
    for file in files:
        if file != "__pycache__" and file.split('.')[-1] != "disable":
            if file.split('.')[-1] == "json":
                with open(PluginDir + "/" + file, "r", encoding="utf-8") as f:
                    plug = json.load(f)
                    for module in plug["modules"]:
                        if module == "prompt":
                            promptv += plug["prompt"]
                        print(plug["name"] + f"({file})插件已加载")
            else:
                import importlib
                global plugins
                try:
                    plugin = importlib.import_module(PluginDir.split("./")[-1] + "." + file.split(".")[0])
                    plugins.append(plugin)
                    print(plugin.init()["name"] + f"({file})高级插件已加载")
                except ImportError as e:
                    print(e)
                    input("插件导入失败 按回车退出程序")
                    exit()

def plugin_manager(command):
    import os
    if len(command) > 1:
        if command[0] == "plugin":
            if command[1] == "disable":
                if os.path.exists(PluginDir + "/" + command[2]):
                    os.rename(PluginDir + "/" + command[2], PluginDir + "/" + command[2] + ".disable")
                    print(f"成功禁用插件{command[2]}", end=" ")
                else: print("插件不存在~", end=" ")
            elif command[1] == "enable":
                if os.path.exists(PluginDir + "/" + command[2] + ".disable"):
                    os.rename(PluginDir + "/" + command[2] + ".disable", PluginDir + "/" + command[2])
                    print(f"成功启用插件{command[2]}", end=" ")
                else: print("插件不存在或已经被启用~", end=" ")
            elif command[1] == "list":
                files = os.listdir(PluginDir)
                for file in files:
                    if file.split('.')[-1] != "disable" and file != "__pycache__":
                        print(file, end=",", flush=True)


def prompt():
    global promptv
    for plugin in plugins:
        try:
            promptv += plugin.prompt()
        except:
            pass
    return promptv

def chat(input_messages, messages):
    for plugin in plugins:
        plugin.chat(input_messages, messages)
def before_chat(model, messages):
    for plugin in plugins:
        try:
            plugin.before_chat(messages)
        except:
            pass