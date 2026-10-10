from nicegui import ui, run
from gui.components.cut_screenshot import cut_screenshot

import os
import subprocess
import time

from modules.utils import screencut_tool, connect_to_device, screen_shot_to_global

def set_other(config, gui_shared_config):
    with ui.row():
        ui.link_target("TOOL_PATH")
        ui.label("其他设置").style('font-size: x-large')

    ui.label("HBM Settings").style('font-size: x-large')
    
    with ui.row():
        # 日志保存
        ui.checkbox("是否输出日志到/DATA/LOGS/目录下").bind_value(gui_shared_config.softwareconfigdict, 'SAVE_LOG_TO_FILE')
    
    with ui.row():
        # 异常日志保存
        ui.checkbox("发生错误时是否保存日志").bind_value(gui_shared_config.softwareconfigdict, 'SAVE_ERR_CUSTOM_LOG')
    
    with ui.row():
        ui.number("config_run_until_try_times",
                  step=1,
                  min=3,
                  precision=0).bind_value(config.userconfigdict, 'RUN_UNTIL_TRY_TIMES', forward=lambda x:int(x), backward=lambda x:int(x))
        
    with ui.row():
        ui.number("循环等待时间",
                  suffix="s",
                  step=0.1,
                  min=0.1,
                  precision=1
                  ).bind_value(config.userconfigdict, 'RUN_UNTIL_WAIT_TIME')
    
    with ui.row():
        ui.number("点击后等待时间",
                    suffix="s",
                    step=0.1,
                    precision=1).bind_value(config.userconfigdict, 'TIME_AFTER_CLICK')
    
    ui.label("滑动过头此项调小60->40，滑动距离不够此项调大40->60")
    with ui.row():
        ui.number("滑动触发距离",
                    step=1,
                    min=1,
                    precision=0).bind_value(config.userconfigdict, 'RESPOND_Y', forward=lambda x:int(x), backward=lambda x:int(x)).bind_enabled(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y', forward=lambda v: not v, backward=lambda v: not v)
        ui.checkbox("与游戏绑定(40)").bind_value(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y')
    
    with ui.row():
        # 截图模式
        ui.select(options=["png", "pipe"], label="截图模式").bind_value(config.userconfigdict, 'SCREENSHOT_METHOD').style('width: 400px')

    ui.label("注意：以下设置不建议修改").style('color: red')

    with ui.row():
        # IP+端口
        ui.input("模拟器监听IP地址（此项不包含端口号）").bind_value(config.userconfigdict, 'TARGET_IP_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: not v)
        
        # 序列号
        ui.input("模拟器序列号，如emulator-5554").bind_value(config.userconfigdict, 'ADB_SEIAL_NUMBER').style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: v)
        
        # 切换使用序列号还是IP+端口
        ui.checkbox("直接使用序列号连接模拟器").bind_value(config.userconfigdict, 'ADB_DIRECT_USE_SERIAL_NUMBER')
    
    with ui.row():
        ui.input("ADB路径").bind_value(config.userconfigdict, 'ADB_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
    
    with ui.row():
        ui.input("截图文件名").bind_value(config.userconfigdict, 'SCREENSHOT_NAME',forward=lambda v: v.replace("\\", "/")).style('width: 400px').set_enabled(False)

    ui.label("Test").style('font-size: x-large')
    
    async def test_screencut():
        await cut_screenshot(
            inconfig=config,
            left_click=True,
            right_click=True,
            quick_return=False
            )
    
    # 将截图功能内嵌进GUI
    with ui.row():
        ui.button("测试截图/screencut test", on_click=test_screencut)

    async def restart_adb_server():
        subprocess.run([config.userconfigdict['ADB_PATH'], "kill-server"])
        time.sleep(0.5)
        subprocess.run([config.userconfigdict['ADB_PATH'], "start-server"])
        print("adb server restarted")
        ui.notify("adb server resstarted")

    # adb kill-server
    with ui.row():
        ui.button("button_kill_adb_server", on_click=restart_adb_server, color="red")