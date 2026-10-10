
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot


class QuarterTask(Task):
    def __init__(self, name="战令") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((1229,453)),
            lambda: Page.is_page(PageName.PAGE_ZHANLING),
            sleeptime=3
        ):
            # 如果没到忍法帖界面，返回主页
            return

        if match(button_pic(ButtonName.BUTTON_STORY_MENU)):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_STORY_MENU)),
                lambda: not match(button_pic(ButtonName.BUTTON_STORY_MENU))
            )

        sleep(2)
        for i in range(3):
            click(Page.MAGICPOINT)

        for i in range(3):
            click((991,109))
        self.run_until(
            lambda: click((1180,244)),
            lambda: not match(button_pic(ButtonName.BUTTON_ZHANLING_DIANZAN)),
            sleeptime = 1.5
        )# 排行榜界面点赞
        for i in range(3):
            click(Page.MAGICPOINT)

        for i in range(3):
            click((709, 111))
        # screenshot()
        # if match(button_pic(ButtonName.BUTTON_ZHANLING_EX), threshold=0.8):
        #     for i in range(5):
        #         self.run_until(
        #             lambda: (click(button_pic(ButtonName.BUTTON_ZHANLING_EX),sleeptime=3, threshold=0.8),click(Page.MAGICPOINT, sleeptime=2)),
        #             lambda: not match(button_pic(ButtonName.BUTTON_ZHANLING_EX), threshold=0.8),
        #             sleeptime=3
        #         )# 周活跃领取
        #         if not match(button_pic(ButtonName.BUTTON_ZHANLING_EX), threshold=0.8):
        #             break
        for i in range(3):# 周活跃领取
            click((509,339),sleeptime=3)
        for i in range(3):
            click(Page.MAGICPOINT)
        for i in range(3):  # 周活跃领取
            click((642, 358), sleeptime=3)
        for i in range(3):
            click(Page.MAGICPOINT)
        for i in range(3):  # 周活跃领取
            click((821, 382), sleeptime=3)
        for i in range(3):
            click(Page.MAGICPOINT)
        for i in range(3):  # 周活跃领取
            click((995, 346), sleeptime=3)
        for i in range(3):
            click(Page.MAGICPOINT)
        for i in range(3):# 周活跃领取
            click((1153,380),sleeptime=3)
        for i in range(3):
            click(Page.MAGICPOINT)
        for i in range(3):
            click(Page.MAGICPOINT)

        for i in range(3):
            click((556, 111))
        if self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_ZHANLING_REWARD), threshold=0.9),
                lambda: click(button_pic(ButtonName.BUTTON_ZHANLING_SURE), sleeptime=3, threshold=0.8),
                times=1,
                sleeptime=3
            ):
            for i in range(3):
                click(Page.MAGICPOINT)
            self.run_until(
                lambda: (click(button_pic(ButtonName.BUTTON_ZHANLING_REWARD), sleeptime=3, threshold=0.9),click(Page.MAGICPOINT, sleeptime=2)),
                lambda: not match(button_pic(ButtonName.BUTTON_ZHANLING_REWARD), threshold=0.9),
                sleeptime=3
            )  # 周任务领取
        # for i in range(3):  # 周活跃领取
        #     click((468, 579), sleeptime=3)
        # for i in range(3):
        #     click(Page.MAGICPOINT)
        # for i in range(3):  # 周活跃领取
        #     click((703, 576), sleeptime=3)
        # for i in range(3):
        #     click(Page.MAGICPOINT)
        # for i in range(3):  # 周活跃领取
        #     click((947, 569), sleeptime=3)
        # for i in range(3):
        #     click(Page.MAGICPOINT)
        # for i in range(3):# 周活跃领取
        #     click((1203,570),sleeptime=3)
        # for i in range(3):
        #     click(Page.MAGICPOINT)

        for i in range(3):
            click((415,110))
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ZHANLING_SHARE), sleeptime=5, threshold=0.8),
            lambda: match(button_pic(ButtonName.BUTTON_ZLSHARE_QQ), threshold=0.8)
        )  # 分享
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ZLSHARE_QQ), threshold=0.8),
            lambda: not match(button_pic(ButtonName.BUTTON_ZLSHARE_QQ), threshold=0.8),
            sleeptime=15
        )  # 分享
        # for i in range(3):
        #     click((981,203))
        # for i in range(3):
        #     click((981,203))
        # for i in range(3):
        #     click((1127,610))

        sleep(15)

        self.back_to_home()

        click(Page.TOPLEFTBACK)

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)