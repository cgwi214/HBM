
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel
from modules.utils.log_utils import logging

class PostAllTask(Task):
    def __init__(self, name="PostAllTask") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return self.back_to_home()
    
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
        config.sessiondict["AFTER_HBM_SOURCES"] = {"power": power_num, "copper": copper_num, "gold": gold_num}

        logging.info(f"体力: {power_num}")
        logging.info(f"铜币: {copper_num}")
        logging.info(f"金币: {gold_num}")
     
    def on_run(self) -> None:
        self.record_resources()

     
    def post_condition(self) -> bool:
        return self.back_to_home()