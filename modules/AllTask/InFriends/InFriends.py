 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep

class InFriends(Task):
    def __init__(self, name="好友") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
    def button_friends(self):
        # 赠送和领取拉面
        if not match(button_pic(ButtonName.BUTTON_FRIENDS_ZengSong), threshold=0.8):
            # 赠送拉面
            click((403, 601))
        else:
            click(button_pic(ButtonName.BUTTON_FRIENDS_ZengSong), threshold=0.8)

        if not match(button_pic(ButtonName.BUTTON_FRIENDS_LingQu), threshold=0.8):
            # 收取拉面
            click((593, 598))
        else:
            click(button_pic(ButtonName.BUTTON_FRIENDS_LingQu), threshold=0.8)

        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_FRIENDS_GET), threshold=0.8),
            lambda: not match(button_pic(ButtonName.BUTTON_FRIENDS_GET), threshold=0.8)
        )
        logging.info("已领取好友赠送的拉面")





    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((55, 219)),
            lambda: Page.is_page(PageName.PAGE_FRIENDS),
            sleeptime=3
        ):
            # 如果没到好友界面，返回主页
            return

        self.button_friends()

        sleep(3)

        # 转换成qq好友界面
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_FRIENDS_B2)),
            lambda: match(button_pic(ButtonName.BUTTON_FRIENDS_B1))
        )

        self.button_friends()

        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)