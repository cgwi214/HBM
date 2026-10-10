
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep


class InBet(Task):
    def __init__(self, name="招募") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((1221,157)),
            lambda: Page.is_page(PageName.PAGE_BET),
            sleeptime=3
        ):
            # 如果没到招募界面，返回主页
            return

        # 召集卷免费召唤
        if match(button_pic(ButtonName.BUTTON_BET_FREE)):
            logging.info("发现高招免费更新")
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_BET_FREE),sleeptime=5),
                lambda: not match(button_pic(ButtonName.BUTTON_BET_FREE))
            )

            if self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: not match(popup_pic(PopupName.POPUP_BET_JUMP),threshold=0.8),
                times=1,
            ):
                click((1039, 636))

            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_BET_REWARE)),
                lambda: not match(button_pic(ButtonName.BUTTON_BET_REWARE))
            )

        if not match(page_pic(PageName.PAGE_BET)):
            return

        # 普通招募
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_BET_NOM), sleeptime=1.5),
            lambda: match(button_pic(ButtonName.BUTTON_BET_NOM_IN), threshold=0.95)
        )

        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_BET_NOMFREE), sleeptime=10),
            lambda: not match(button_pic(ButtonName.BUTTON_BET_NOMFREE))
        )

        if self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: not match(popup_pic(PopupName.POPUP_BET_JUMP), threshold=0.8),
                times=1,
        ):
            click((1039, 636))

        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_BET_SURE)),
            lambda: not match(button_pic(ButtonName.BUTTON_BET_SURE))
        )


        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)