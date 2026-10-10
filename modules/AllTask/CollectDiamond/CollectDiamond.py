
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep


class CollectDiamond(Task):
    def __init__(self, name="心悦") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((56,158)),
            lambda: Page.is_page(PageName.PAGE_SET),
            sleeptime=3
        ):
            # 如果没到心悦界面，返回主页
            return

        while not match(button_pic(ButtonName.BUTTON_XINYUE)):
            self.run_until(
                lambda: click((1100,318)),
                lambda: match(button_pic(ButtonName.BUTTON_XINYUE))
            )

        #跳转到心悦页面
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_XINYUE), sleeptime=20),
            lambda: not Page.is_page(PageName.PAGE_SET)
        )
        #领取奖励
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_XINYUE_REWARD),sleeptime=2,threshold=0.95) and click((1206,50), sleeptime=2),
            lambda: not match(button_pic(ButtonName.BUTTON_XINYUE_REWARD), threshold=0.95)
        )
        click((73,75))
        click((73, 75), sleeptime=15)
        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)