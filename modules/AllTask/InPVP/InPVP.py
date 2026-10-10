import time

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep, advanced_hybrid_operation, screenshot, click_in_area, config


class InPVP(Task):
    def __init__(self, name="决斗场") -> None:
        super().__init__(name)
        self.max_victory = config.userconfigdict.get("PVP_VICTORY_TIMES")  # 最大胜利次数


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)

    def lv(self):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_PVP_LV)),
                lambda: click(button_pic(ButtonName.BUTTON_PVP_LV_REWARD)),
                times=2,
            )

    def _handle_pvp_match(self):
        """处理PVP匹配流程"""

        # 进入匹配界面
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match(button_pic(ButtonName.BUTTON_PVP_START),threshold=0.95),
            times = 60,
            sleeptime = 3
        )

        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_PVP_ERR), threshold=0.85),
            lambda: not match(button_pic(ButtonName.BUTTON_PVP_ERR), threshold=0.85)
        )

        # 拒绝可能存在的弹窗
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_PVP_REJECT)),
            lambda: not match(button_pic(ButtonName.BUTTON_PVP_REJECT))
        )

        self.pvp_fun()

        # 开始匹配
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_PVP_START)),
            lambda: not match(button_pic(ButtonName.BUTTON_PVP_START)),
            times=80,
            sleeptime=3
        )

    def _execute_pvp_battle(self):
        """执行PVP战斗核心逻辑"""
        victory_count = 0  # 胜利计数器
        battle_round = 0  # 战斗轮次计数器

        BATTLE_TIMEOUT = 400

        def stop_condition():
            """战斗停止条件（包含胜利次数计数）"""
            nonlocal victory_count  # 声明引用外部作用域的计数器
            # 截图
            screenshot()
            # 定义条件列表（参数形式）
            conditions = [
                (ButtonName.BUTTON_PVP_START, "button", 0.95, "开始按钮"),
                (PopupName.POPUP_PVP_VICTORY, "popup", 0.8, "胜利弹窗"),
                (PopupName.POPUP_PVP_WIN, "popup", 0.8, "战斗胜利"),
                (PopupName.POPUP_PVP_DEFEATED, "popup", 0.8, "战斗失败"),
                # (PopupName.POPUP_RUNNING, "popup", 0.95, "运行中弹窗"),
                (ButtonName.BUTTON_PVP_ERR, "button", 0.95, "错误按钮")
            ]

            # 遍历检查每个条件
            for name, cond_type, threshold, cond_name in conditions:
                # 生成图片路径
                if cond_type == "popup":
                    pic_path = popup_pic(name)
                elif cond_type == "button":
                    pic_path = button_pic(name)

                # 执行匹配
                match_result = match(pic_path, threshold=threshold)

                if match_result:
                    # 如果是胜利弹窗则增加计数器
                    if name == PopupName.POPUP_PVP_VICTORY or name == PopupName.POPUP_PVP_WIN:
                        victory_count += 1
                    #     logging.debug(f"检测到胜利弹窗，当前胜利次数: {victory_count}")
                    #
                    # logging.info(f"触发停止条件: {cond_name}")
                    return True

            return False


        while battle_round < config.userconfigdict.get("PVP_MAX_TIMES"):
            round_start_time = time.time()  # 记录单场战斗开始时间

            try:
                self._handle_pvp_match()  # 匹配流程

                # 进入战斗界面（带超时检测）
                if not self.run_until(
                        lambda: click(Page.MAGICPOINT),
                        lambda: match(button_pic(ButtonName.BUTTON_FIGHT)),
                        times=60,
                        sleeptime=5,
                ):
                    logging.warning("匹配超时，跳过本场战斗")
                    continue

                while match(button_pic(ButtonName.BUTTON_FIGHT), 0.9):
                    # 核心战斗循环添加时间检查
                    if time.time() - round_start_time > BATTLE_TIMEOUT:
                        logging.warning("单场战斗超时，强制终止")
                        break

                    advanced_hybrid_operation(
                        Page.fight_press,
                        Page.fight_click,
                        {Page.fight_click[0]: 5, Page.fight_click[1]: 20},
                        stop_condition,
                        check_interval=15,
                        sleeptime=5.0
                    )

                    # 错误处理
                    self.run_until(
                        lambda: click(button_pic(ButtonName.BUTTON_PVP_ERR), threshold=0.85),
                        lambda: not match(button_pic(ButtonName.BUTTON_PVP_ERR), threshold=0.85),
                        times=1,
                    )

            except Exception as e:
                logging.error(f"战斗流程异常: {str(e)}")

            finally:

                for _ in range(5):
                    click(Page.MAGICPOINT)
                battle_round += 1
                logging.info(f"第{battle_round}场战斗结束")

                # 胜利次数或总次数达到限制
                if victory_count >= self.max_victory or battle_round >= config.userconfigdict.get("PVP_MAX_TIMES"):
                    break



    def _claim_rewards(self):
        # 领取任务奖励
        if self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_PVP_TASK),threshold=0.8),
                lambda: match(popup_pic(PopupName.POPUP_PVP_TASK),threshold=0.9),
                times=3,
            ):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_PVP_REWARD), threshold=0.8),
                lambda: not match(button_pic(ButtonName.BUTTON_PVP_REWARD), threshold=0.8)
            )
            self.run_until(
                lambda: click_in_area(button_pic(ButtonName.BUTTON_PVP_ACTIVITY),((452,525),(1082,599)),threshold=0.8,sleeptime=3),
                lambda: not click_in_area(button_pic(ButtonName.BUTTON_PVP_ACTIVITY),((452,525),(1082,599)),threshold=0.8,sleeptime=3)
            )

            logging.info("已领取决斗场任务奖励")
        for _ in range(5):
            click(Page.MAGICPOINT)

    def pvp_fun(self):
        screenshot()
        if not match(button_pic(ButtonName.BUTTON_PVP_START),threshold=0.8):
            click_in_area(button_pic(ButtonName.BUTTON_CLOSE1), Page.TOPLEFT, threshold=0.8, sleeptime=3)
            screenshot()
            if match(button_pic(ButtonName.BUTTON_PVP_FUN)):
                click(button_pic(ButtonName.BUTTON_PVP_FUN),threshold=0.8)
            elif match(button_pic(ButtonName.BUTTON_VILLAGE_PVP), threshold=0.8):
                click(button_pic(ButtonName.BUTTON_VILLAGE_PVP))
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_PVP_FUN)),
                    lambda: not match(button_pic(ButtonName.BUTTON_PVP_FUN))
                )
            else:
                self.run_until(
                    lambda: click_in_area(button_pic(ButtonName.BUTTON_CLOSE1), Page.TOPLEFT, threshold=0.8, sleeptime=3),
                    lambda: not click_in_area(button_pic(ButtonName.BUTTON_CLOSE1), Page.TOPLEFT, threshold=0.8, sleeptime=3)
                )

                for _ in range(5):
                    swipe((259, 356), (774, 352), 0.85)

                if not self.run_until(
                        lambda: swipe((873, 352), (573, 358), 0.85),
                        lambda: match(button_pic(ButtonName.BUTTON_VILLAGE_PVP), threshold=0.8),
                        sleeptime=3
                ):
                    return

                if not self.run_until(
                        lambda: click(button_pic(ButtonName.BUTTON_VILLAGE_PVP)),
                        lambda: not match(button_pic(ButtonName.BUTTON_VILLAGE_PVP), threshold=0.8),
                        sleeptime=3
                ):
                    # 如果没到决斗场界面，返回主页
                    return

                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_PVP_FUN)),
                    lambda: not match(button_pic(ButtonName.BUTTON_PVP_FUN))
                )


    def on_run(self) -> None:

        try:

            for _ in range(5):
                swipe((259, 356), (774, 352), 0.85)

            if not self.run_until(
                lambda: swipe((873, 352), (573, 358), 0.85),
                lambda: match(button_pic(ButtonName.BUTTON_VILLAGE_PVP), threshold=0.8),
                sleeptime=3
            ):
                # 如果没找到决斗场按钮，返回主页
                return

            if not self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_VILLAGE_PVP)),
                    lambda: not match(button_pic(ButtonName.BUTTON_VILLAGE_PVP), threshold=0.8),
                    sleeptime=3
            ):
                # 如果没到决斗场界面，返回主页
                return

            sleep(3)

            self.lv()

            # 进入忍术对战界面
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_PVP_FUN)),
                lambda: not match(button_pic(ButtonName.BUTTON_PVP_FUN))
            )

            self._execute_pvp_battle()

            self.run_until(
                lambda: click(Page.MAGICPOINT,sleeptime=2),
                lambda: match(button_pic(ButtonName.BUTTON_PVP_START)),
                times=80,
                sleeptime=5,
            )

            self._claim_rewards()

        except Exception as e:
            logging.error(f"任务执行异常：{str(e)}")

        finally:
            self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)