from nicegui import ui

def set_intraining(config):
    with ui.row():
        ui.link_target("TRAINING_TASK")
        ui.label("试炼之地").style('font-size: x-large')

    ui.checkbox("修行之路扫荡").bind_value(config.userconfigdict, 'TRAINING_ONE_SWEEP')