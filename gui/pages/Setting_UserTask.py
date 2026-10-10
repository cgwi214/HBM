from nicegui import ui

def set_usertask(config):
    with ui.row():
        ui.link_target("USER_DEF_TASK")
        ui.label("自定义任务").style('font-size: x-large')
    
    with ui.row():
        ui.textarea(label = "自定义任务").bind_value(config.userconfigdict, "USER_DEF_TASKS").style('width: 40vw;')