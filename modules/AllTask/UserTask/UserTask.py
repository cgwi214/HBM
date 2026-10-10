
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
from modules.AllTask.SubTask.ExecCode import ExecCode

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel
from modules.utils.log_utils import logging

class UserTask(Task):
    def __init__(self, name="自定义任务") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return True
    
     
    def on_run(self) -> None:
        content = config.userconfigdict["USER_DEF_TASKS"]
        runCode = ExecCode(content)
        runCode.run()
        if runCode.status == Task.STATUS_SUCCESS:
            logging.info("自定义任务执行成功")
        elif runCode.status == Task.STATUS_ERROR:
            logging.error("自定义任务执行错误，尝试返回游戏主页")
            self.back_to_home()

     
    def post_condition(self) -> bool:
        return True