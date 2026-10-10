from nicegui import ui

def set_organizaton(config):
    with ui.row():
        ui.link_target("ORGAN_TASK")
        ui.label("组织").style('font-size: x-large')

    def organ_rpay(e):
        config.userconfigdict['ORGAN_TYPE'] = e.value

    ui.label("组织祈福")
    rpay = ui.radio({
        "PAY": "焚香祈福",
        "GPAY": "纳贡祈福",
        "VPAY": "虔诚祈福"},
        value=config.userconfigdict['ORGAN_TYPE'], on_change=organ_rpay).props('inline')

