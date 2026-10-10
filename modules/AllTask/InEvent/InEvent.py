
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep


class InEvent(Task):
    def __init__(self, name="积分赛") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:

        for _ in range(5):
            swipe((259, 356), (774, 352), 0.85),

        self._navigate_to_subpage(ButtonName.BUTTON_VILLAGE_JIFENSAI, PageName.PAGE_JIFENSAI)

        # 假设没有领取段位奖励
        for _ in range(4):
            click(Page.MAGICPOINT, sleeptime=1.5)

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)