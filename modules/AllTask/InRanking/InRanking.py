
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep


class InRanking(Task):
    def __init__(self, name="排行榜") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:

        for _ in range(5):
            swipe((259, 356), (774, 352), 0.85),

        self._navigate_to_subpage(ButtonName.BUTTON_VILLAGE_RANKING, PageName.PAGE_RANKING)

        # 点赞
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_RANKING_DIANZAN)),
            lambda: not match(button_pic(ButtonName.BUTTON_RANKING_DIANZAN))
        )

        click(Page.TOPLEFTBACK)

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)