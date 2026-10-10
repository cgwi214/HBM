
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, config, click, swipe, match, page_pic, button_pic, popup_pic, sleep, advanced_hybrid_operation, screenshot


class InTraining(Task):
    def __init__(self, name="试炼之地") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def _popup_operation1(self, reset_btn, confirm_btn):
        """通用重置操作"""
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match(button_pic(reset_btn), threshold=0.8)
        )

        self.run_until(
            lambda: click(button_pic(reset_btn), threshold=0.8, sleeptime=1.5),
            lambda: click(button_pic(confirm_btn), threshold=0.8, sleeptime=1.5),
            times=3,
        )
        logging.info("弹窗已点击")

    def Training1(self):
        """处理修行之路"""
        self.run_until(
            lambda: click(page_pic(PageName.PAGE_TRAINING1)),
            lambda: not match(page_pic(PageName.PAGE_TRAINING1))
        )
        sleep(2)
        logging.info("进入修行之路")
        if match(button_pic(ButtonName.BUTTON_TRAINING1_WARD), threshold=0.8):
            logging.info("领取修行之路奖励")
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING1_WARD)),
                lambda: not match(button_pic(ButtonName.BUTTON_TRAINING1_WARD))
            )

        for _ in range(3):  # 清理弹窗
            click(Page.MAGICPOINT)

        self._popup_operation1(
            ButtonName.BUTTON_TRAINING1_RESET,
            ButtonName.BUTTON_TRAINING1_SURE
        )
        if config.userconfigdict["TRAINING_ONE_SWEEP"]:
            self._popup_operation1(
                ButtonName.BUTTON_TRAINING1_SWEEP,
                ButtonName.BUTTON_TRAINING1_SWEEP_SURE
            )
            logging.info("修行之路正在扫荡")



    def _handle_battle_flow(self):
        """处理战斗流程核心逻辑"""

        def stop_condition():
            """战斗停止条件：胜利/失败/继续战斗"""
            screenshot()
            return any([
                match(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8),
                match(button_pic(ButtonName.BUTTON_TRAINING2_YESIN), threshold=0.8),
                match(popup_pic(PopupName.POPUP_TRAINING2_VICTORY)),
                match(popup_pic(PopupName.POPUP_TRAINING2_DEFEATED)),
                match(button_pic(ButtonName.BUTTON_TRAINING2_REWARD), threshold=0.8),
                match(button_pic(ButtonName.BUTTON_TRAINING2_START), threshold=0.8),
            ])

        # 开始战斗循环
        while True:
            if self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_START)),
                    lambda: (match(popup_pic(PopupName.POPUP_TRAINING2_NONE), threshold=0.8) or match(popup_pic(PopupName.POPUP_TRAINING2_CLEAR), threshold=0.8))
            ):
                break

            # 启动战斗
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_START)),
                lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8),
            )

            # 确认战斗
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8),
                lambda: not match(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8),
            )

            # 执行战斗操作
            self._execute_battle(stop_condition)

            for _ in range(5):          #清理弹窗
                click(Page.MAGICPOINT)

            sleep(3)

            for _ in range(5):          #清理弹窗
                click(Page.MAGICPOINT)

            # 领取奖励
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_REWARD),threshold=0.8),
                lambda: not match(button_pic(ButtonName.BUTTON_TRAINING2_REWARD),threshold=0.8),
            )
            logging.info("已完成本场轮次战斗并领取奖励")

            for _ in range(5):          #清理弹窗
                click(Page.MAGICPOINT,sleeptime=2)

    def _execute_battle(self, stop_cond):
        """执行单次战斗流程"""
        # 进入战斗界面
        if not self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match(button_pic(ButtonName.BUTTON_FIGHT)),
        ):
            return False

        # 持续战斗直到满足停止条件
        logging.info("开始战斗")
        while match(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8) or match(button_pic(ButtonName.BUTTON_FIGHT)):
            if match(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8):
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8),
                    lambda: not match(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8)
                )
            advanced_hybrid_operation(
                Page.fight_press,
                Page.fight_click,
                {Page.fight_click[0]: 2, Page.fight_click[1]: 2},
                stop_cond,
                120,
                check_interval=20,
                sleeptime=4.0  # 新增参数：战斗结束后等待2秒
            )
            sleep(0.5)
            screenshot()

        return True


    def _NORESET2(self):
        # 显示无重置次数,退出
        if self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_RESET), threshold=0.8),
                lambda: match(popup_pic(PopupName.POPUP_TRAINING2_NORESET), threshold=0.8)
        ):
            logging.info("无重置次数或已完成")
            return

    def _RESET2(self):
        # 重置
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_RESET), threshold=0.8),
            lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_REPLAY), threshold=0.8)
        )
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_REPLAY), threshold=0.8),
            lambda: not match(button_pic(ButtonName.BUTTON_TRAINING2_REPLAY), threshold=0.8)
        )

        self.run_until(
            lambda: click(Page.MAGICPOINT, sleeptime=1.5),
            lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_START))
        )

        if self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_START),sleeptime=2),
                lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_READY), threshold=0.8),
        ):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_READY), threshold=0.8),
                lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_SURE), threshold=0.8)
            )
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_SURE), threshold=0.8),
                lambda: not match(button_pic(ButtonName.BUTTON_TRAINING2_SURE), threshold=0.8)
            )
            logging.info("已重置战斗关卡并重新准备")
            for _ in range(3):
                click(Page.MAGICPOINT)









    def Training2(self):
        # 生存挑战
        self.run_until(
            lambda: click(page_pic(PageName.PAGE_TRAINING2)),
            lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_START))
        )

        for _ in range(3):
            click(Page.MAGICPOINT)

        if match(button_pic(ButtonName.BUTTON_TRAINING2_REWARD)):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_REWARD)),
                lambda: not match(button_pic(ButtonName.BUTTON_TRAINING2_REWARD)),
            )
            for _ in range(3):
                click(Page.MAGICPOINT)


        # 点击战斗但显示无人出击则点击重置
        if self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_START)),
            lambda: (match(popup_pic(PopupName.POPUP_TRAINING2_NONE), threshold=0.8) or match(popup_pic(PopupName.POPUP_TRAINING2_CLEAR), threshold=0.8)),
            times=3,
        ):
            self._NORESET2()

            for _ in range(3):
                click(Page.MAGICPOINT)

            self._RESET2()

            self._handle_battle_flow()

            for _ in range(3):
                click(Page.MAGICPOINT)

        elif self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_START),sleeptime=2),
                lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_YES), threshold=0.8),
                times=3,
        ):
            for _ in range(3):
                click(Page.MAGICPOINT)

            self._handle_battle_flow()

            self._RESET2()

            self._handle_battle_flow()


        elif self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_START),sleeptime=2),
                lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_READY), threshold=0.8),
        ):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_READY), threshold=0.8),
                lambda: match(button_pic(ButtonName.BUTTON_TRAINING2_SURE), threshold=0.8)
            )
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TRAINING2_SURE), threshold=0.8),
                lambda: not match(button_pic(ButtonName.BUTTON_TRAINING2_SURE), threshold=0.8)
            )
            for _ in range(3):
                click(Page.MAGICPOINT)

            self._handle_battle_flow()

    def on_run(self) -> None:
        for _ in range(5):
            swipe((259, 356), (774, 352), 0.85)

        self._navigate_to_subpage(ButtonName.BUTTON_VILLAGE_TRAINING, PageName.PAGE_TRAINING1)

        self.Training1()

        self.back_to_home()

        for _ in range(5):
            swipe((259, 356), (774, 352), 0.85)

        self._navigate_to_subpage(ButtonName.BUTTON_VILLAGE_TRAINING, PageName.PAGE_TRAINING1)

        self.Training2()

        click(Page.TOPLEFTBACK)
        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)