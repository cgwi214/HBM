
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep, multi_press_until, screenshot


class InAbundance(Task):
    def __init__(self, name="丰饶之间") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def fight_AS(self):
        if not self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match(button_pic(ButtonName.BUTTON_FIGHT), threshold=0.8),
        ):
            # 如果没到战斗界面，返回主页
            return


        def stop_condition():
            """战斗停止条件：胜利/失败/继续战斗"""
            screenshot()
            return any([
                match(popup_pic(PopupName.POPUP_FENGRAO_END), threshold=0.8),
                match(page_pic(PageName.PAGE_FENGRAOZHIJIAN)),
            ])

        fight_IA = multi_press_until(
            Page.fight_press,
            stop_condition,
            sleeptime=2
        )
        # 战斗结束
        if fight_IA:
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match(page_pic(PageName.PAGE_FENGRAOZHIJIAN))
            )
        else:
            logging.error("丰饶之间战斗失败")







    def on_run(self) -> None:
        for _ in range(5):
            swipe((259, 356), (774, 352), 0.85),

        self._navigate_to_subpage(ButtonName.BUTTON_VILLAGE_FENGRAOZHIJIAN, PageName.PAGE_FENGRAOZHIJIAN)

        # 开始
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_FENGRAO_START)),
            lambda: not match(button_pic(ButtonName.BUTTON_FENGRAO_START))
        )

        self.fight_AS()

        screenshot()
        if match(button_pic(ButtonName.BUTTON_FENGRAO_START)):
            click(button_pic(ButtonName.BUTTON_FENGRAO_START))
            self.fight_AS()

        screenshot()
        if match(button_pic(ButtonName.BUTTON_FENGRAO_START)):
            logging.error("丰饶之间任务执行失败")


        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)