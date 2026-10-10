
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep


class MissionMeeting(Task):
    def __init__(self, name="任务集会所") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def reward(self):
        # 领取任务奖励
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_TASKS_REWARDS), sleeptime=1.5, threshold=0.8),
            lambda: click(button_pic(ButtonName.BUTTON_TASKS_CONFIRM)),
            times=2,
            sleeptime=2
        )
        for _ in range(4):
            click(Page.MAGICPOINT)
        self.run_until(
            lambda: (click(button_pic(ButtonName.BUTTON_TASKS_REWARDS), sleeptime=1.5, threshold=0.8),
                     click(Page.MAGICPOINT, sleeptime=1.5)),
            lambda: not match(button_pic(ButtonName.BUTTON_TASKS_REWARDS), threshold=0.8)
        )
        for _ in range(4):
            click(Page.MAGICPOINT)

        logging.info("已领取所有任务奖励")



    def accept_all(self):
        # 接取所有任务
        for _ in range(3):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TASKS_SURE), sleeptime=1.5),
                lambda: not match(button_pic(ButtonName.BUTTON_TASKS_SURE))
            )
            if match((button_pic(ButtonName.BUTTON_TASKS_ONE))):
                click((870, 145))
                click(button_pic(ButtonName.BUTTON_TASKS_ONE))
            else:
                click((870, 145))
                click((928,577))
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TASKS_START)),
                lambda: not match(button_pic(ButtonName.BUTTON_TASKS_START))
            )






    def on_run(self) -> None:

        for _ in range(5):
            swipe((259, 356), (774, 352), 0.85),

        self._navigate_to_subpage(ButtonName.BUTTON_VILLAGE_RENWUJIHUISUO, PageName.PAGE_RENWUJIHUISUO)

        self.reward()

        self.accept_all()
        logging.info("已接取所有任务")

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)