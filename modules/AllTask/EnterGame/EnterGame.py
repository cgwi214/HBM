from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, config, ocr_area, click_in_area, logging
# =====
from .Loginin import Loginin
from .CloseInform import CloseInform

class EnterGame(Task):
    def __init__(self, name="EnterGame" , pre_times = 1, post_times = 10) -> None:
        super().__init__(name, pre_times, post_times)
    
    def record_resources(self):
        """
        记录主页中的资源
        """
        # 记录主页中的资源
        power_num = ocr_area((430, 30), (550, 60))[0]
        # print("体力: ", power_num)
        copper_num = ocr_area((640, 30), (750, 60))[0]
        # print("铜币: ", copper_num)
        gold_num = ocr_area((850, 30), (970, 60))[0]
        # print("金币: ", gold_num)
        config.sessiondict["BEFORE_HBM_SOURCES"] = {"power": power_num, "copper": copper_num, "gold": gold_num}

        logging.info(f"体力: {power_num}")
        logging.info(f"铜币: {copper_num}")
        logging.info(f"金币: {gold_num}")

    def pre_condition(self):
        if Page.is_page(PageName.PAGE_HOME):
            # 直接就在主页，直接记录资源
            self.record_resources()
            return False

        while click_in_area(button_pic(ButtonName.BUTTON_CLOSE1),Page.TOPLEFT,threshold=0.8,sleeptime=3):  # 持续检测关闭按钮
            return_home = self.back_to_home()
            if return_home:
                # 如果成功返回主页，记录资源
                self.record_resources()
                return False  # 退出函数，表示不需要执行任务

        return True  # 退出循环后，继续任务

    def on_run(self) -> None:
        Loginin().run()
        # 如果登入到游戏，记录资源
        self.record_resources()
        
    
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)