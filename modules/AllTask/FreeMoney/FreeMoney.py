
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep


class FreeMoney(Task):
    def __init__(self, name="免费铜钱") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((773, 45)),
            lambda: Page.is_page(PageName.PAGE_FREEMONEY),
            sleeptime=2
        ):
            # 如果没到招财界面，返回主页
            return

        # 免费领铜钱
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_MONEY_FREE),sleeptime=1.5),
            lambda: not match(button_pic(ButtonName.BUTTON_MONEY_FREE)),
        )

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)