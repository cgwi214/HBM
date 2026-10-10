
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click_in_area, click, swipe, match, page_pic, button_pic, popup_pic, sleep


class CollectDailyRewards(Task):
    def __init__(self, name="活跃") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((1224,362)),
            lambda: Page.is_page(PageName.PAGE_REWARD),
            sleeptime=3
        ):
            # 如果没到活跃界面，返回主页
            return

        # 每日活跃
        button_data = [
            ((513, 567), ButtonName.BUTTON_REWARD_TEN),
            ((742, 567), ButtonName.BUTTON_REWARD_FORTY),
            ((1026, 567), ButtonName.BUTTON_REWARD_EIGHTY),
            ((1180, 567), ButtonName.BUTTON_REWARD_HUNDRED)
        ]

        for position, button_name in button_data:
            if not match(button_pic(button_name)):
                click(position)
            else:
                click(button_pic(button_name))

            for _ in range(2):
                click(Page.MAGICPOINT)


        logging.info("每日活跃奖励已领取")

        # 周活跃礼
        if click_in_area(button_pic(ButtonName.BUTTON_REWARD_WEEK),((1100,651),(1274,710)),threshold=0.8,sleeptime=3):
            self.run_until(
                lambda: (click(button_pic(ButtonName.BUTTON_REWARD_WEEK_YES)),click((645,467))),
                lambda: not match(button_pic(ButtonName.BUTTON_REWARD_WEEK_YES))
            )
        # if match(button_pic(ButtonName.BUTTON_REWARD_WEEK_YES)):
        #     logging.info("周活跃奖励已领取")
        for _ in range(2):
            click(Page.TOPLEFTBACK)

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)