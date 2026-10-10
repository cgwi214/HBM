import inspect
from modules.AllPage.Page import Page
from DATA.assets.PageName import PageName
from DATA.assets.PopupName import PopupName
from DATA.assets.ButtonName import ButtonName


from modules.utils import click, swipe, match, page_pic, match_pixel, button_pic, popup_pic, sleep, screenshot, config, click_in_area

from modules.utils.adb_utils import check_app_running, open_app
from modules.utils.log_utils import logging



class Task:
    STATUS_SUCCESS = 0
    STATUS_ERROR = 1
    STATUS_SKIP = 2
    # 父类
    def __init__(self, name = "default Task", pre_times = 2, post_times = 4) -> None:
        self.name = name
        self.pre_times = pre_times
        self.post_times = post_times
        self.click_magic_when_run = True
        """运行时是否点击魔法点重置窗口状态到Page级别"""
        self.status = self.STATUS_SUCCESS
        
    def pre_condition(self) -> bool:
        """
        执行任务前的判断，判断现有情况，如果进行有效操作(截图或点击)，记得重新截图

        确认页面，是否需要做此任务，任务是否已经完成，这同时会试图点击魔法点重置页面状态到Page级别
        
        返回true表示可以执行任务，false表示不能执行任务
        """
        return True
        
    def on_run(self) -> None:
        """
        执行任务时需要做的事情，逻辑判断与操作
        
        如果是复杂的任务，尽量用run_until点击
        """
        pass
    
    def post_condition(self) -> bool:
        """
        执行任务后的判断，只判断现有情况，不要进行有效操作(截图或点击)

        看任务是否回到它该在的页面，这同时会试图点击魔法点重置页面状态到Page级别
        
        返回true表示回到它该在的页面成功，false表示回到它该在的页面失败
        """
        return True
    
    def run(self) -> None:
        """
        （不要重写）
        运行一个任务
        """
        logging.info("判断任务{}是否可以执行".format(self.name))
        if(Task.run_until(self.click_magic_sleep,self.pre_condition, self.pre_times)):
            logging.info("执行任务{}".format(self.name))
            self.on_run()
            logging.info("判断任务{}执行结果是否可控".format(self.name))
            if(Task.run_until(self.click_magic_sleep,self.post_condition, self.post_times)):
                logging.info("任务{}执行结束".format(self.name))
            else:
                logging.warn("任务{}执行后条件不成立或超时".format(self.name))
                if not self.back_to_home():
                    raise Exception("任务{}执行后条件不成立或超时，且无法正确返回主页，程序退出".format(self.name))
        else:
            logging.warn("任务{}执行前条件不成立或超时，跳过此任务".format(self.name))
            config.append_noti_sentence(key = self.name+"_SKIP", sentence = f"跳过{self.name}任务")

    @staticmethod
    def back_to_home(times = 10) -> bool:
        """
        尝试返回到游戏主页，如果游戏不在前台，会尝试打开游戏到前台，但不会等待登录加载，因此必须确保游戏在后台
        
        返回成功与否
        """
        logging.info("尝试返回主页")
        if not check_app_running(config.userconfigdict["ACTIVITY_PATH"]):
            open_app(config.userconfigdict["ACTIVITY_PATH"])
        for i in range(times):
            screenshot()

            click(Page.MAGICPOINT, sleeptime=1)

            if click_in_area(button_pic(ButtonName.BUTTON_CLOSE1),Page.TOPLEFT,threshold=0.8,sleeptime=3):
                click_in_area(button_pic(ButtonName.BUTTON_CLOSE1), Page.TOPLEFT, threshold=0.8,sleeptime=3)

            if match(button_pic(ButtonName.BUTTON_LOGIN)):
                click(button_pic(ButtonName.BUTTON_LOGIN))

            if match(button_pic(ButtonName.BUTTON_FIGHT),threshold=0.8):
                click(Page.TOPLEFTBACK, sleeptime=1)
                if match(button_pic(ButtonName.BUTTON_FIGHT_EXIT)):
                    Task.run_until(
                        lambda: click(button_pic(ButtonName.BUTTON_FIGHT_EXIT)),
                        lambda: not match(button_pic(ButtonName.BUTTON_FIGHT_EXIT))
                    )

            # if match(button_pic(ButtonName.BUTTON_CLOSE1),threshold=0.8):
            #     click(button_pic(ButtonName.BUTTON_CLOSE1), threshold=0.8,sleeptime=2)
            screenshot()
            if(Page.is_page(PageName.PAGE_HOME)):
                logging.info("返回主页成功")
                return True
            # 跳过故事
            screenshot()
            if match(button_pic(ButtonName.BUTTON_STORY_MENU)):
                click(button_pic(ButtonName.BUTTON_STORY_MENU))
        logging.error("返回主页失败")
        return False

    @staticmethod
    def close_any_select_popup(yn: bool = False) -> bool:
        """
        关闭任一有选择性按钮的弹窗（确认弹窗，是否弹窗）一次

        yorn: boolean
            True: 关闭所有弹窗, 遇到选择选是
            False: 关闭所有弹窗, 遇到选择选否

        返回是否产生了关闭动作
        """
        # ...
        pass

    def click_magic_sleep(self, sleeptime=3):
        if self.click_magic_when_run:
            click(Page.MAGICPOINT, sleeptime)
        else:
            sleep(sleeptime)
    
    @staticmethod
    def run_until(func1, func2, times=None, sleeptime = None) -> bool:
        """
        重复执行func1，至多times次或直到func2成立
        
        func1内部应当只产生有效操作一次或内部调用截图函数, func2判断前会先触发截图
        
        每次执行完func1后,等待sleeptime秒

        如果func2成立退出，返回true，否则返回false
        """
        # 设置times，如果传进来是None，就用config里的值
        if(times == None):
            times = config.userconfigdict["RUN_UNTIL_TRY_TIMES"]
        # 设置sleeptime，如果传进来是None，就用config里的值
        if(sleeptime == None):
            sleeptime = config.userconfigdict["RUN_UNTIL_WAIT_TIME"]
        for i in range(times):
            screenshot()
            if(func2()):
                return True
            func1()
            sleep(sleeptime)
        screenshot()
        if(func2()):
            return True
        logging.warning("超过执行任务最大时间")
        return False

    # @staticmethod
    # def scroll_right_up(scrollx=928, times=3):
    #     """
    #     scroll to top
    #     """
    #     for i in range(times):
    #         swipe((scrollx, 226), (scrollx, 561), sleeptime=0.2)
    #     sleep(0.5)


    def _navigate_to_subpage(self, target_button, target_page):
        """导航到指定子页面"""
        # 滑动屏幕定位目标按钮
        if not self.run_until(
                lambda: swipe((873, 352), (473, 358), 0.85),
                lambda: match(button_pic(target_button), threshold=0.8),
                sleeptime=3
        ):
            logging.warning("未找到{}按钮，返回主页".format(self.name))
            return False

        return self.run_until(
            lambda: click(button_pic(target_button), threshold=0.8),
            lambda: Page.is_page(target_page),
            sleeptime=3
        )