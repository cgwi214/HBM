
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep


class InVIP(Task):
    def __init__(self, name="领vip礼包") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((304,67)),
            lambda: Page.is_page(PageName.PAGE_RECHARGE),
            sleeptime=3
        ):
            # 如果没到充值界面，返回主页
            return

        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_VIP_REWARD), sleeptime=2),
            lambda: match(button_pic(ButtonName.BUTTON_VIP_200))
        )

        self.run_until(
            lambda: (click(button_pic(ButtonName.BUTTON_VIP_200),sleeptime=2),
                     click(Page.MAGICPOINT)),
            lambda: not match(button_pic(ButtonName.BUTTON_VIP_REWARD))
        )


        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)