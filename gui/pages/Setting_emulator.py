from nicegui import ui, run
from modules.utils import check_connect, connect_to_device


def set_emulator(config):
    
    ui.link_target("EMULATOR")
    ui.label("模拟器配置").style('font-size: x-large')

    with ui.row():
        # IP+端口
        ui.number("模拟器端口",
                step=1,
                precision=0,
                ).bind_value(config.userconfigdict, 'TARGET_PORT', forward=lambda v: int(v), backward=lambda v:int(v)).style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: not v)
        # 序列号
        ui.input("模拟器序列号，如emulator-5554").bind_value(config.userconfigdict, 'ADB_SEIAL_NUMBER').style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: v)
        
        # 切换使用序列号还是IP+端口
        ui.checkbox("直接使用序列号连接模拟器").bind_value(config.userconfigdict, 'ADB_DIRECT_USE_SERIAL_NUMBER')
        
    
    with ui.row():
        kill_port = ui.checkbox("模拟器启动前强制释放端口").bind_value(config.userconfigdict, "KILL_PORT_IF_EXIST")
        kill_port.set_value(False)
        kill_port.set_enabled(False)
    
    with ui.row():    
        ui.input("模拟器路径",
                    ).bind_value(config.userconfigdict, 'TARGET_EMULATOR_PATH',forward=lambda v: v.replace("\\", "/").replace('"','')).style('width: 400px')
    
    ui.checkbox("运行结束后关闭模拟器").bind_value(config.userconfigdict, 'CLOSE_EMULATOR_FINISH')
    ui.checkbox("运行结束后关闭游戏").bind_value(config.userconfigdict, 'CLOSE_GAME_FINISH')
    ui.checkbox("运行结束后关闭HBM").bind_value(config.userconfigdict, 'CLOSE_HBM_FINISH')

    # 登录超时重启模拟器
    ui.number("登录游戏超时时间（秒）", min=180, precision=0, step=1).bind_value(config.userconfigdict, "GAME_LOGIN_TIMEOUT", forward= lambda x: int(x)).style("width: 200px")
    ui.number("登录超时后模拟器最多重启次数，0为不重启", min=0, max=10, precision=0, step=1).bind_value(config.userconfigdict, "MAX_RESTART_EMULATOR_TIMES", forward= lambda x: int(x)).style("width: 400px")

    ui.label("模拟器路径获取方法").style('font-size: x-large; width: 100%;')
    ui.label("1.为该模拟器创建快捷方式 2.对该快捷方式鼠标右键—>属性 3.在属性窗口中的“快捷方式”找到“目标”，“目标”中的地址就是模拟器路径").style('font-size: x-large; width: 100%;')
    ui.label("模拟器端口获取方法").style('font-size: x-large; width: 100%;')
    ui.label("1.以mumu模拟器为例，在多开器右上一栏，有着“ADB”的图标，点击则可获取").style('font-size: x-large; width: 100%;')
    ui.label("2.雷电模拟器获取adb教程：https://help.ldmnq.com/docs/LD9adbserver").style('font-size: x-large; width: 100%;')
    ui.label(r"3.进入软件文件夹下的\tools\adb文件夹，在文件夹空白处按住shift右键，选择“在终端中打开”，或直接使用cmd到该文件夹路径；在终端输入“adb devices”可获取").style('font-size: x-large; width: 100%;')