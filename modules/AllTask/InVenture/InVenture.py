
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep


class InVenture(Task):
    def __init__(self, name="冒险") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((1164,622)),
            lambda: Page.is_page(PageName.PAGE_VEN_FRAG),
            sleeptime=3
        ):
            # 如果没到冒险界面，返回主页
            return

        # 扫荡精英副本
        self.run_until(
            lambda: click(page_pic(PageName.PAGE_VEN_FRAG)),
            lambda: match(page_pic(PageName.PAGE_VEN_FRAG_UP))
        )
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_VEN_ALLSWEEP)),
            lambda: match(button_pic(ButtonName.BUTTON_VEN_CONFIRM))
        )
        sleep(1)
        click((568,596))
        sleep(1)
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_VEN_CONFIRM),sleeptime=2),
            lambda: match(button_pic(ButtonName.BUTTON_VEN_CONSWEEP))
        )

        self.run_until(
            lambda: (click(button_pic(ButtonName.BUTTON_VEN_CONSWEEP), sleeptime=4),
                     click(Page.MAGICPOINT, sleeptime=12)),
            lambda: match(popup_pic(PopupName.POPUP_VEN_NOMORE))
        )
        for _ in range(2):
            click(Page.TOPLEFTBACK)

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)