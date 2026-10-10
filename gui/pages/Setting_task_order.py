from nicegui import ui, run
from gui.components.fast_run_task_buttons import show_fast_run_task_buttons, TaskName

def set_task_order(config, real_taskname, logArea):
    with ui.row():
        ui.link_target("TASK_ORDER")
        ui.label("任务执行顺序").style('font-size: x-large')
    
    
    def select_clear_all_and_refresh_task_order(type="select"):
        if type == "select":
            for i in range(0, len(config.userconfigdict["TASK_ACTIVATE"])):
                config.userconfigdict["TASK_ACTIVATE"][i] = True
        else:
            for i in range(0, len(config.userconfigdict["TASK_ACTIVATE"])):
                config.userconfigdict["TASK_ACTIVATE"][i] = False
        task_order.refresh()
    
    with ui.row():
        ui.button("全选", on_click=lambda: select_clear_all_and_refresh_task_order("select"))
        ui.button("全不选", on_click=lambda: select_clear_all_and_refresh_task_order("unselect"))
    
    @ui.refreshable
    def task_order():
        with ui.row():
            # 第一行添加上添加按钮
            ui.button(f'{"添加"} {"任务"}', on_click=lambda: add_task(0))
        for i in range(len(config.userconfigdict["TASK_ORDER"])):
            with ui.row():
                ui.label(f'{"任务"} {i+1}:')
                atask = ui.select(real_taskname,
                                  value=config.userconfigdict["TASK_ORDER"][i],
                                  on_change=lambda v,i=i: config.userconfigdict["TASK_ORDER"].__setitem__(i, v.value))
                acheck = ui.checkbox("启用", value=config.userconfigdict["TASK_ACTIVATE"][i], on_change=lambda v,i=i: config.userconfigdict["TASK_ACTIVATE"].__setitem__(i, v.value))
                ui.button(f'{"添加"} {"任务"}', on_click=lambda i=i+1: add_task(i))
                ui.button(f'{"删除"} {"任务"}', on_click=lambda i=i: del_task(i), color="red")

    def add_task(i):
        config.userconfigdict["TASK_ORDER"].insert(i, TaskName.MAIL)
        config.userconfigdict["TASK_ACTIVATE"].insert(i, True)
        task_order.refresh()
    
    def del_task(i):
        if len(config.userconfigdict["TASK_ORDER"]) == 0:
            # 空列表的话不删除
            return
        config.userconfigdict["TASK_ORDER"].pop(i)
        config.userconfigdict["TASK_ACTIVATE"].pop(i)
        task_order.refresh()
    
    
    # pre-run command
    with ui.row().style('display: none'):
        ui.input("任务开始前执行命令, 留空忽略", placeholder='start cmd /c "HBM.exe config1.json"').bind_value(config.userconfigdict, 'PRE_COMMAND').style('width: 300px')
    
    task_order()
    
    # post-run command
    with ui.row().style('display: none'):
        ui.input("任务结束后执行命令, 留空忽略", placeholder='start cmd /c "HBM.exe config2.json"').bind_value(config.userconfigdict, 'POST_COMMAND').style('width: 300px')
    
    # with ui.row():
    #     ui.link_target("NEXT_CONFIG")
    #     ui.label("后续配置文件")).style('font-size: x-large')
    
    # ui.label("如果你想在完成当前配置后继续执行其他配置文件，可以在这里添加。如果不需要，可以留空")).style('color: red')
        
    # ui.input("后续配置文件")).bind_value(config.userconfigdict, 'NEXT_CONFIG',forward=lambda v: v.replace("\\", "/")).style('width: 400px')

    # 快速调用任务
    show_fast_run_task_buttons([
        TaskName.PVP,TaskName.SWEEP,TaskName.TRAIN,
 ], config, real_taskname, logArea)

