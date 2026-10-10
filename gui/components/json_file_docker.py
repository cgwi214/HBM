from modules.configs.MyConfig import MyConfigger
from modules.utils import logging
from pathlib import Path
from nicegui import ui
import os


DEFAULT_CONFIG_JSON_NAME = "config.json"

def get_json_list():
    """
    可以获得所有json文件名列表（如[xxx1. txt]）。如果不存在，则创建一个配置。在Json中，使列表不为空
    返回:
    HBM_CONFIGS目录下的所有json文件名的列表
    """
    arr = [i for i in os.listdir(MyConfigger.USER_CONFIG_FOLDER) if i.endswith(".json")]
    if len(arr) == 0:
        with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, DEFAULT_CONFIG_JSON_NAME), 'w') as f:
            f.write("{}")
        arr.append(DEFAULT_CONFIG_JSON_NAME)
    return arr


alljson_list = get_json_list()


async def add_new_config(configname):
    """
    点击加号后，创建新的json文件
    """
    configname = configname.strip()
    if not configname:
        ui.notify("配置名为空！/Config name is None!")
    else:
        configname = configname.replace(".json", "") + ".json"
        if configname in alljson_list:
            ui.notify("配置名已存在/Config name already exists")
        else:
            # 创建一个新的json文件
            with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, configname), 'w') as f:
                f.write("{}")
            ui.run_javascript('window.location.reload()')

def copy_and_rename_config(configname, rename_configname):
    """
    复制某个json文件，并重命名
    """
    configname = configname.strip()
    if configname not in alljson_list:
        ui.notify(f"配置 {configname} 不存在！/Config does not exist!")
        return
    if not rename_configname:
        ui.notify("缺少新文件名！/Missing new file name!")
        return
    rename_configname = rename_configname.strip().replace(".json", "") + ".json" # 确保结尾有且只有一个.json
    if rename_configname in alljson_list:
        ui.notify(f"配置名 {rename_configname} 已存在！/Config name already exists!")
        return
    # 复制并重命名
    with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, configname), 'r', encoding="utf-8") as f:
        content = f.read()
    with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, rename_configname), 'w', encoding="utf-8") as f:
        f.write(content)
    ui.notify(f"复制并重命名成功！/Copy and rename successfully!")
    # js等待1.5秒后刷新页面
    ui.run_javascript('setTimeout(() => {window.location.reload()}, 1500)')


def delete_config(config_name: str) -> bool:
    """安全删除配置文件"""
    config_dir = Path.cwd() / "HBM_CONFIGS"
    target_file = config_dir / config_name
    if target_file.exists() and target_file.is_file():
        try:
            os.remove(str(target_file))
            return True
        except Exception as e:
            logging.error(f"删除配置文件失败: {e}")
            return False
    return False