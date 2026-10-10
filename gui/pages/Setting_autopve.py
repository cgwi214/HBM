from nicegui import ui

def set_autopve(config):
    with ui.row():
        ui.link_target("AUTOPVE_TASK")
        ui.label("小队突袭").style('font-size: x-large')

    ui.checkbox("选择金币翻倍").bind_value(config.userconfigdict, 'AUTOPVE_BUY')