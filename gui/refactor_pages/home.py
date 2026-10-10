import subprocess
from ..components.json_file_docker import get_json_list, add_new_config, copy_and_rename_config, delete_config

from nicegui import ui, app
import os
import sys
from ..components.exec_arg_parse import check_token_dialog
from ..define import gui_shared_config

def get_base_path():
    if getattr(sys, 'frozen', False):
        # 打包后的资源路径
        base_path = sys._MEIPASS
    else:
        # 开发环境路径
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    return base_path


video_path = os.path.join(
    get_base_path(), "..", "DATA", "assets", "Demonstration.mp4"
)
video_path = os.path.normpath(video_path)



@ui.refreshable
def render_json_list():
    if check_token_dialog(render_json_list):
        # Set background
        ui.query('body').style(f"""
            background-image: url('https://cdn2.zzzmh.cn/wallpaper/origin/47482bcb3a294e868546d6c73f1e7ca8.jpg?response-content-disposition=attachment&auth_key=1746374400-dd47a3dc2710906622f2500e917285d2aa4fe38b-0-193357cfdd457e43e49db235d62af37a');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        """)

        with ui.column().classes('w-full h-full').style('background-color: rgba(255, 255, 255, 0.7)'):
            with ui.splitter(horizontal=True, value=65).classes('w-full h-full').style("height: calc(100vh - 2rem)") as splitter:
                with splitter.before:
                    with ui.column().classes('items-center').style("padding: 10px; height: 100%; width: 100%"):
                        ui.label(f"Huo Ban Manager").classes('text-center').style(
                            'font-size: xx-large; width: 100%')

                        # 基本介绍
                        with ui.row().style(
                                "display: flex; justify-content: space-between; align-items: center; width: 100%"):
                            ui.label("HBM可以帮助你完成火影忍者手游的每日任务。配置文件存放于HBM_CONFIGS文件夹内。")

                        # 重要设置提醒
                        ui.label("本项目仅限用于学术交流和研究目的，严禁任何形式的商业用途、非法传播及违法违规应用。使用者应自觉遵守所在国家/地区的法律法规，若因违规使用导致法律纠纷或责任事故，相关后果由使用者自行承担，项目方保留追究其法律责任的权利。").style('font-size: x-large; width: 100%;color: red;')

                        ui.label("如果在某下载渠道下载到这个项目，请在24小时内删除").style('font-size: x-large; width: 100%;color: red;')

                        ui.label("本工具不涉及逆向，破解，绕过权限，调用应用API等等侵犯行为").style('font-size: x-large; width: 100%;color: red;')

                        ui.label("使用前请将qq或微信和游戏安装好在模拟器里").style('font-size: x-large; width: 100%;')

                        ui.label("模拟器分辨率请设置为1280*720，240DPI!").style('font-size: x-large; width: 100%;')

                        ui.label("游戏画质设置：流畅").style('font-size: x-large; width: 100%;')

                        ui.video(video_path).style("width: 600px; margin: 5px 0;")

                        # print(f"[DEBUG] 视频路径: {video_path}")  # 调试输出
                        # if not os.path.exists(video_path):
                        #     print(f"[ERROR] 视频文件不存在: {video_path}")
                        # else:
                        #     print(f"[INFO] 视频文件加载成功")

                        ui.label("使用方法：").style('font-size: x-large; width: 100%;')

                        ui.label("创建多个快捷方式实现多开").style('font-size: x-large; width: 100%;color: red;')

                        ui.label("给hbm.exe创建快捷方式，在其属性中的“快捷方式”->“目标”后加空格和你已经配置好的配置文件文件,最后双击快捷方式即可").style('font-size: x-large; width: 100%;')

                        ui.label(r"例如：E:\HBM\hbm.exe example.json  E:\HBM\hbm.exe config.json").style('font-size: x-large; width: 100%;')

                        ui.label("创建定时任务方法：").style('font-size: x-large; width: 100%;')

                        ui.label("我的电脑右键->管理->计算机管理（本地)->系统工具->任务计划程序->任务计划程序库->创建基本任务").style('font-size: x-large; width: 100%;')

                        ui.label("创建基本任务按需填写，启动程序一栏：程序或脚本选择hbm.exe，添加参数填写配置文件，起始于填写hbm.exe所在文件目录").style('font-size: x-large; width: 100%;')

                        ui.label(r"例如:E:\HBM\hbm.exe example.json，程序或脚本（浏览）：E:\HBM\hbm.exe，添加参数：example.json， 起始于E:\HBM\ ").style('font-size: x-large; width: 100%;')


                with splitter.after:
                    with ui.column().style(
                            "padding: 20px; height: 100%; overflow-y: auto; background-color: rgba(255, 255, 255, 0.8)"):
                        # ============配置文件区域===========
                        with ui.row().classes("w-full justify-center"):
                            ui.label("配置文件").style("font-size: xx-large;")

                        # 复制操作的相关参数：被复制的文件名，新文件名
                        copy_related_params = {"old_name": "", "new_name": ""}
                        with ui.dialog() as dialog, ui.card():
                            ui.input("复制").bind_value_from(copy_related_params, "old_name").set_enabled(False)
                            ui.input("重命名").bind_value_to(copy_related_params, "new_name")
                            with ui.row():
                                ui.button("关闭", color="white", on_click=dialog.close)
                                ui.button("保存", on_click=lambda e: [
                                    copy_and_rename_config(copy_related_params["old_name"],
                                                           copy_related_params["new_name"]), dialog.close()])

                        # 配置文件名 卡片
                        with ui.row().style(
                                "display: flex; flex-wrap: wrap; gap: 20px; overflow-x: auto; width: 100%;"):
                            for config_name in get_json_list():
                                with ui.column().classes("items-center").style("min-width: 200px;") as col:
                                    current_config = config_name
                                    # config名
                                    with ui.link(target=f"/panel/{current_config}"):
                                        with ui.card().props('flat bordered').style(
                                                "width: 100%; background-color: rgba(255, 255, 255, 0.9)"):
                                            ui.label(current_config).style("font-size: large; text-align: center;")

                                    with ui.row().classes("items-center justify-center gap-2"):
                                        # 复制按钮 - centered below config name
                                        ui.button("复制", on_click=lambda e, c=current_config: [
                                            copy_related_params.update({"old_name": c, "new_name": ""}), dialog.open()])
                                        # 删除按钮
                                        with ui.dialog().classes("w-64") as delete_dialog:
                                            with ui.card():
                                                ui.label(f"是否删除配置文件【{current_config}】？").classes("text-red-500")
                                                with ui.row().classes("justify-end gap-2 mt-4"):
                                                    ui.button("取消", on_click=delete_dialog.close)
                                                    ui.button("删除",
                                                              color="negative",
                                                              on_click=lambda e, c=current_config: [
                                                                  delete_config(c),
                                                                  delete_dialog.close(),
                                                                  render_json_list.refresh()
                                                              ])
                                        ui.button(icon="delete",color="red",on_click=lambda e, d=delete_dialog: d.open())

                        # 添加配置
                        user_config_name = {"val": ""}
                        with ui.row().classes("flex items-center justify-center"):
                            ui.input("Name").bind_value(user_config_name, "val")
                            ui.button("添加", on_click=lambda: add_new_config(user_config_name["val"])).style(
                                "height: 30px; line-height: 30px; text-align: center; cursor: pointer;")


@ui.page("/")
def home_page():
    render_json_list()