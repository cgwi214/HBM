from nicegui import ui
import os
def set_dungeons(config):
    with ui.row():
        ui.link_target("PVP_TASK")
        ui.label("秘境探险").style('font-size: x-large')

        ui.label("该功能只是一个demo").style('font-size: x-large; width: 100%;color: red;')

        ui.label("使用该功能时只允许使用一个设备(模拟器)").style('font-size: x-large; width: 100%;color: red;')

        ui.label("进入秘境探险战斗场景后再打开该功能").style('font-size: x-large; width: 100%;color: red;')

        ui.label("*使用YOLO").style('width: 100%;')

        def run_in_terminal():
            os.system(f'start HBM_YOLO.exe')

        def close_in_terminal():
            os.system('taskkill /IM HBM_YOLO.exe /F')

        ui.button("使用YOLO(终端)", on_click=run_in_terminal)

        ui.button("关闭YOLO(终端)", on_click=close_in_terminal)
