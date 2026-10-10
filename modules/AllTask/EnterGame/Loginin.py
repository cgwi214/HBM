import time

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils.log_utils import logging

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, check_app_running, open_app, config, screenshot, EmulatorBlockError, click_in_area

# =====

class Loginin(Task):
    def __init__(self, name="登陆游戏", pre_times = 3, post_times = 10) -> None:
        super().__init__(name, pre_times, post_times)

     
    def pre_condition(self):
        if(self.post_condition()):
            return False
        return True

    def try_jump_useless_pages(self):
        # 判断超时
        if time.time() - self.task_start_time > config.userconfigdict["GAME_LOGIN_TIMEOUT"]:
            if config.sessiondict["RESTART_EMULATOR_TIMES"] >= config.userconfigdict["MAX_RESTART_EMULATOR_TIMES"]:
                # 无重启次数剩余
                raise Exception("超时：无法进入游戏主页，无剩余重启次数")
            else:
                # 有重启次数剩余，尝试重启
                raise EmulatorBlockError("模拟器卡顿，重启模拟器")

        # 检查各个登录页面按钮
        if match(button_pic(ButtonName.BUTTON_LOGIN)):# 点击登录按钮
            click(button_pic(ButtonName.BUTTON_LOGIN))
        elif match(button_pic(ButtonName.BUTTON_ANDROID_QQ)):# 选择点击安卓QQ登录
            click((101, 615))
            sleep(2)
            click(button_pic(ButtonName.BUTTON_ANDROID_QQ))
            sleep(25)
            screenshot()
            if match(button_pic(ButtonName.BUTTON_QQ_LOGIN)):  # 点击登录QQ
                self.run_until(
                    lambda: (click((467, 307),sleeptime=2) and click(button_pic(ButtonName.BUTTON_QQ_LOGIN))),
                    lambda: not match(button_pic(ButtonName.BUTTON_QQ_LOGIN))
                )
                sleep(25)
            screenshot()
            if match(button_pic(ButtonName.BUTTON_QQ_AGREE)):  # 点击同意QQ协议
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_QQ_AGREE)),
                    lambda: not match(button_pic(ButtonName.BUTTON_QQ_AGREE)),
                )
                sleep(10)
        elif match(button_pic(ButtonName.BUTTON_QQ)):# 选择点击QQ登录_2
            click((101, 615))
            click(button_pic(ButtonName.BUTTON_QQ))
            sleep(25)
            screenshot()
            if match(button_pic(ButtonName.BUTTON_QQ_LOGIN)):# 点击登录QQ
                self.run_until(
                    lambda: (click((467, 307),sleeptime=2) and click(button_pic(ButtonName.BUTTON_QQ_LOGIN))),
                    lambda: not match(button_pic(ButtonName.BUTTON_QQ_LOGIN))
                )
                sleep(25)
            screenshot()
            if match(button_pic(ButtonName.BUTTON_QQ_AGREE)):# 点击同意QQ协议
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_QQ_AGREE)),
                    lambda: not match(button_pic(ButtonName.BUTTON_QQ_AGREE)),
                )
                sleep(10)
        elif match(button_pic(ButtonName.BUTTON_UPDATE)):# 点击进行更新
            click(button_pic(ButtonName.BUTTON_UPDATE))
        elif match(button_pic(ButtonName.BUTTON_LOGINREWARD)):# 点击领取登录奖励
            click(button_pic(ButtonName.BUTTON_LOGINREWARD))
        elif match(page_pic(PageName.PAGE_AD)):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CLOSE2)),
                lambda: not match(button_pic(ButtonName.BUTTON_CLOSE2)),
            )
            click((1065, 100))# 点击公告弹窗区域
        elif click_in_area(button_pic(ButtonName.BUTTON_CLOSE1),Page.TOPLEFT,threshold=0.8,sleeptime=3):#关闭广告弹窗
            click_in_area(button_pic(ButtonName.BUTTON_CLOSE1), Page.TOPLEFT, threshold=0.8,sleeptime=3)
        else:
            click((135, 676))  # 如果没有匹配到，点击活动弹窗区域
            sleep(1)
            click((1250,17))

        # 确认处在游戏界面
        if not check_app_running(config.userconfigdict['ACTIVITY_PATH']):
            open_app(config.userconfigdict['ACTIVITY_PATH'])
            logging.warn("游戏未在前台，尝试打开游戏")
            sleep(3)
            screenshot()


    def on_run(self):
        self.task_start_time = time.time()

        while not match(page_pic(PageName.PAGE_HOME), threshold=0.95):
            # 计数器，记录连续匹配成功的次数
            success_count = 0

            def check_condition():
                nonlocal success_count
                if match(page_pic(PageName.PAGE_HOME), threshold=0.95):
                    success_count += 1
                    sleep(5)
                    screenshot()
                    # 只有当连续匹配成功两次才返回True
                else:
                    # 如果匹配失败，重置计数器
                    success_count = 0
                    return False

                if success_count >= 2:
                    return True

            self.run_until(
                self.try_jump_useless_pages,
                check_condition,
                times=300,
                sleeptime=10
            )
            sleep(5)
            screenshot()

        click(Page.MAGICPOINT)

     
    def post_condition(self):
        return Page.is_page(PageName.PAGE_HOME)