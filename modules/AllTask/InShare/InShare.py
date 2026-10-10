
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep


class InShare(Task):
    def __init__(self, name="分享") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((101, 55)),
            lambda: not Page.is_page(PageName.PAGE_HOME),
            sleeptime=3
        ):
            # 如果没到个人界面，返回主页
            return

        # 点击个人界面分享按钮
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_SHARE_WEEK)),
            lambda: match(button_pic(ButtonName.BUTTON_SHARE)),
        )

        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_SHARE)),
            lambda: match(button_pic(ButtonName.BUTTON_SHARE_QQ)),
        )
        self.run_until(
            lambda: match(button_pic(ButtonName.BUTTON_SHARE_QQ), threshold=0.8),
            lambda: click(button_pic(ButtonName.BUTTON_SHARE_QQ), threshold=0.8, sleeptime=15)
        )
        #click((1206, 655))

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)