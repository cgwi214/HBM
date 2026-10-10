
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep, advanced_hybrid_operation


class InActivity(Task):
    def __init__(self, name="活动") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)



    def mon_sgin(self):
        # 每月签到
        for i in range(3):
            switchres = self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_ACTIVITY_SIGN), threshold=0.85),
                lambda: match(button_pic(ButtonName.BUTTON_ACTIVITY_SIGNC), threshold=0.85),
                times=3
            )
            if not switchres:
                swipe((90, 590), (92, 228), 0.6)

        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ACTIVITY_SIGNIN)),
            lambda: not match(button_pic(ButtonName.BUTTON_ACTIVITY_SIGNIN))
        )
        if not match(button_pic(ButtonName.BUTTON_ACTIVITY_SIGNIN)):
            logging.info("已完成每月签到")

    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((1232,48)),
            lambda: Page.is_page(PageName.PAGE_ACTIVITY),
            sleeptime=2
        ):
            # 如果没到活动界面，返回主页
            return

        # 领取一乐拉面
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ACTIVITY_YILE)),
            lambda: not match(button_pic(ButtonName.BUTTON_ACTIVITY_YILE))
        )

        self.mon_sgin()

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)