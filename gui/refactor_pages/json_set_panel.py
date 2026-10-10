from ..components.exec_arg_parse import get_token
from ..components.manage_hbm_in_gui import run_hbm_task_and_bind_log, stop_hbm_task
from ..components.running_task_pool import RunningHBMProcess_instance



from ..pages.Setting_emulator import set_emulator
from ..pages.Setting_other import set_other
from ..pages.Setting_shop import set_shop
from ..pages.Setting_organizaton import set_organizaton
from ..pages.Setting_intraining import set_intraining
from ..pages.Setting_pvp import set_pvp
from ..pages.Setting_autopve import set_autopve
from ..pages.Setting_task_order import set_task_order
from ..pages.Setting_notification import set_notification
from ..pages.Setting_UserTask import set_usertask
from ..pages.Setting_dungeons import set_dungeons
from modules.AllTask.myAllTask import task_instances_map
from modules.configs.MyConfig import MyConfigger
from ..define import gui_shared_config, injectJSforTabs

from nicegui import ui, app, run
from typing import Callable
import os
import time


class ConfigPanel:
    """
    连接子页面的名称 与 渲染页面的函数

    func: 
        子页面渲染函数
    """
    def __init__(self, nameID: str, func: Callable[[], None]):
        self.name = nameID
        self.func = func
        self.tab = None
        self.nameID = nameID

    def set_tab(self, tab: ui.tab):
        self.tab = tab


def get_config_list(lst_config: MyConfigger, logArea) -> list:
    return [
        ConfigPanel("模拟器配置", lambda: set_emulator(lst_config)),
        ConfigPanel("任务执行顺序", lambda: set_task_order(lst_config, task_instances_map.task_config_name, logArea)),
        ConfigPanel("通知设置", lambda: set_notification(lst_config, gui_shared_config)),
        ConfigPanel("组织", lambda: set_organizaton(lst_config)),
        ConfigPanel("试炼之地", lambda: set_intraining(lst_config)),
        ConfigPanel("决斗场", lambda: set_pvp(lst_config)),
        ConfigPanel("小队突袭", lambda: set_autopve(lst_config)),
        ConfigPanel("商店", lambda: set_shop(lst_config)),
        ConfigPanel("秘境探险(试验)", lambda: set_dungeons(lst_config)),
        ConfigPanel("自定义任务", lambda: set_usertask(lst_config)),
        ConfigPanel("其他设置", lambda: set_other(lst_config, gui_shared_config))
    ]


@ui.page('/panel/{json_file_name}')
def show_json_panel(json_file_name: str):
    if get_token() is not None and get_token() != app.storage.user.get("token"):
        return
    curr_config: MyConfigger = MyConfigger()
    curr_config.parse_user_config(json_file_name)

    # 设置splitter高度使其占满全屏，减去2rem是content这个class的内边距
    with ui.splitter(value=15).classes('w-full h-full').style("height: calc(100vh - 2rem);") as splitter:

        # 创建logArea
        with ui.column().style('flex-grow: 1;width: 30vw;position:sticky; top: 0px;'):
            output_card = ui.card().style('width: 30vw; height: 80vh;overflow-y: auto;')
            with output_card:
                logArea = ui.log(max_lines=1000).classes('w-full h-full')

        # 获取tab列表，传参logArea以支持日志输出
        config_choose_list: list[ConfigPanel] = get_config_list(curr_config, logArea)

        with splitter.before:
            ui.button("<-", on_click=lambda: ui.run_javascript('window.history.back()'))
            # 便于js查找tabs
            with ui.tabs().props('vertical').classes('w-full loctabs') as tabs:
                for i, config_cls in enumerate(config_choose_list):
                    config_choose_list[i].set_tab(ui.tab(config_cls.name))

        with splitter.after:
            # 便于js查找被滚动元素
            with ui.tab_panels(tabs, value=config_choose_list[0].tab).props('vertical').classes('w-full h-full locscroll'):
                for cls in config_choose_list:
                    with ui.tab_panel(cls.tab):
                        ui.html("<div style='width: 1px;height: 20px'></div>")
                        cls.func()
                        ui.html("<div style='width: 1px;height: 200px'></div>")

        ui.add_head_html(injectJSforTabs)

        with ui.column().style(
                'width: 10vw; overflow: auto; position: fixed; bottom: 40px; right: 20px;min-width: 150px;'):
            def save_and_alert():
                curr_config.save_user_config(json_file_name)
                curr_config.save_software_config()
                gui_shared_config.save_software_config()
                ui.notify("保存成功")

            ui.button("保存", on_click=save_and_alert)

            def save_and_alert_and_run_in_terminal():
                curr_config.save_user_config(json_file_name)
                curr_config.save_software_config()
                gui_shared_config.save_software_config()
                ui.notify("保存成功")
                ui.notify("执行中...")
                # 打开同目录中的HBM.exe，传入当前config的json文件名
                os.system(f'start HBM.exe "{json_file_name}"')

            ui.button("保存并执行(终端)", on_click=save_and_alert_and_run_in_terminal)

            # ======Run in GUI======
            async def save_and_alert_and_run():
                curr_config.save_user_config(json_file_name)
                curr_config.save_software_config()
                gui_shared_config.save_software_config()
                ui.notify("保存成功")
                ui.notify("执行中...")
                await run.io_bound(run_hbm_task_and_bind_log, logArea, json_file_name)

            # log recovery
            msg_obj = RunningHBMProcess_instance.get_status_obj(configname=json_file_name)
            print(f"This config's ({json_file_name}) msg obj is {msg_obj}")
            # 如果此config相关任务正在运行，使用save_and_alert_and_run绑定日志输出到GUI日志窗口内
            if msg_obj["runing_signal"] == 1:
                track_logger_timer = ui.timer(0.5, save_and_alert_and_run, once=True)

            ui.button("保存并执行(GUI)", on_click=save_and_alert_and_run).bind_visibility_from(
                msg_obj, "runing_signal", backward=lambda x: x == 0)

            async def stop_run() -> None:
                stop_hbm_task(logArea, json_file_name)

            ui.button("停止执行", on_click=stop_run, color='red').bind_visibility_from(
                msg_obj, "runing_signal", backward=lambda x: x == 1)

            ui.button("...").bind_visibility_from(msg_obj, "runing_signal", backward=lambda x: x == 0.25)

            # ================


    # 加载完毕保存一下config，应用最新的对config的更改
    curr_config.save_user_config(json_file_name)
    curr_config.save_software_config()
