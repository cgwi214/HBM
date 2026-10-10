 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot, click_in_area

class CloseInform(Task):
    def __init__(self, name="CloseInform", pre_times = 3, post_times = 3) -> None:
        super().__init__(name, pre_times, post_times)

     
    def pre_condition(self) -> bool:
        sleep(1)
        screenshot()

    def try_jump_useless_pages(self):
        screenshot()

        if match (page_pic(PageName.PAGE_AD)):
             self.run_until(
                 lambda: click(button_pic(ButtonName.BUTTON_CLOSE2)),
                 lambda: not match(button_pic(ButtonName.BUTTON_CLOSE2)),
             )
             click((1065, 100))  # 点击公告弹窗区域

        if match(button_pic(ButtonName.BUTTON_LOGINREWARD)):# 点击领取登录奖励
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_LOGINREWARD)),
                lambda: not match(button_pic(ButtonName.BUTTON_LOGINREWARD)),
            )

        self.run_until(
            lambda: click_in_area(button_pic(ButtonName.BUTTON_CLOSE1),Page.TOPLEFT,threshold=0.8,sleeptime=3),
            lambda: not click_in_area(button_pic(ButtonName.BUTTON_CLOSE1),Page.TOPLEFT,threshold=0.8,sleeptime=3),
            times=20
        )

        click(Page.MAGICPOINT)



     
    def on_run(self) -> None:
        while not match(page_pic(PageName.PAGE_HOME), threshold=0.95):
            self.run_until(self.try_jump_useless_pages,
                           lambda: match(page_pic(PageName.PAGE_HOME), threshold=0.95),
                           times=300,
                           sleeptime=10)
            sleep(5)
            screenshot()

        click(Page.MAGICPOINT)

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)