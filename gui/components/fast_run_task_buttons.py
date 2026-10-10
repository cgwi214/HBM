from gui.components.manage_hbm_in_gui import run_hbm_task_and_bind_log
from nicegui import ui, run
from modules.AllTask.myAllTask import TaskName

def show_fast_run_task_buttons(task_confname_list, config, real_taskname, logArea, show_title=True, show_desc=True):
    """
    展示快速运行任务按钮
    """
    if show_title:
        ui.label("快速执行任务").style('font-size: x-large')
    
    if show_desc:
        ui.label("配置过模拟器端口后，以下非日常类型的任务点击即可执行（推图任务需要配置推图起始关卡）")

    def gui_just_run_one_task(taskname):
        async def just_run_one_task():
            logArea.push(f"Task Running")
            config.save_user_config(config.nowuserconfigname)
            await run.io_bound(run_hbm_task_and_bind_log, logArea, config.nowuserconfigname, taskname)
        ui.button(real_taskname[taskname], on_click=just_run_one_task)
    
    # show buttons
    for t_cn_line in task_confname_list:
        with ui.row():
            if isinstance(t_cn_line, str):
                # 字符串
                gui_just_run_one_task(t_cn_line)
            else:
                # 列表
                for t_cn in t_cn_line:
                    gui_just_run_one_task(t_cn)