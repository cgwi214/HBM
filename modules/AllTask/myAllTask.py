from enum import Enum
from modules.AllTask import *

from modules.AllPage.Page import Page

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot
from modules.utils.log_utils import logging
from modules.configs.MyConfig import config

class TaskName():
    """
    配置文件里的task任务名称，此类下的属性可作为task标识符
    """
    LOGIN_GAME = "登录游戏"
    MONEY = "免费领铜币"
    FRIENDS = "好友"
    MAIL = "邮件"
    SHARE = "分享"            ##
    PASS = "战令"
    BET = "招募"
    NOBIE = "心悦"
    VIP = "vip"
    ACTIVITY = "活动"
    ADVENTURE = "冒险"
    STORE = "商店"
    DAILY = "活跃任务"
    BOOKIE = "积分赛"          
    RANKING = "排行榜"
    ATTIC = "任务集会所"
    ORGAN = "组织"
    SWEEP = "丰饶之间"
    TRAIN = "试炼之地"
    APVE = "小队突袭"
    PVP = "决斗场"
    # DUNGEONS = "秘境探险"
    CUSTOM = "自定义任务"

class TaskInstance:
    """
    连接配置文件里的task任务名称与i18n包里对应的翻译文字key

    task_config_name: 
        配置文件里的task任务名称
    take_key_name:
        i18n包里的翻译文字key
    task_module:
        该task对应模块
    task_params:
        该task对应模块入参
    """
    def __init__(self, task_config_name: str, task_module: Task, task_params: dict):
        self.task_config_name = task_config_name
        self.task_module = task_module
        self.task_params = task_params

class TaskInstanceMap:
    """
    可执行任务列表 包含所有脚本可以执行的一级任务
    """
    def __init__(self):
        self.taskmap = {
            TaskName.LOGIN_GAME:
                TaskInstance(
                    task_config_name = TaskName.LOGIN_GAME,
                    task_module = Task, # !EnterGame任务现在被config直接控制并添加在taskpool开头，忽略配置文件里的登录游戏任务，为了防止后面解析任务列表实例时缺少key导致exception，这里以空module Task代替
                    task_params = {}
                ),
            TaskName.MONEY: TaskInstance(
                    task_config_name = TaskName.MONEY,
                    task_module = FreeMoney,
                    task_params = {}
                ),
            TaskName.FRIENDS: TaskInstance(
                    task_config_name = TaskName.FRIENDS,
                    task_module = InFriends,
                    task_params = {}
                ),
            TaskName.MAIL: TaskInstance(
                    task_config_name = TaskName.MAIL,
                    task_module = CollectMails,
                    task_params = {}
                ),
            TaskName.SHARE: TaskInstance(
                    task_config_name = TaskName.SHARE,
                    task_module = InShare,
                    task_params = {}
                ),
            TaskName.PASS: TaskInstance(
                    task_config_name = TaskName.PASS,
                    task_module = QuarterTask,
                    task_params = {}
                ),
            TaskName.BET: TaskInstance(
                    task_config_name=TaskName.BET,
                    task_module=InBet,
                    task_params={}
                ),
            TaskName.NOBIE: TaskInstance(
                    task_config_name=TaskName.NOBIE,
                    task_module=CollectDiamond,
                    task_params={}
                ),
            TaskName.VIP: TaskInstance(
                    task_config_name=TaskName.VIP,
                    task_module=InVIP,
                    task_params={}
                ),
            TaskName.ACTIVITY: TaskInstance(
                    task_config_name=TaskName.ACTIVITY,
                    task_module=InActivity,
                    task_params={}
                ),
            TaskName.ADVENTURE: TaskInstance(
                    task_config_name=TaskName.ADVENTURE,
                    task_module=InVenture,
                    task_params={}
                ),
            TaskName.STORE: TaskInstance(
                    task_config_name=TaskName.STORE,
                    task_module=InShop,
                    task_params={}
                ),
            TaskName.DAILY: TaskInstance(
                    task_config_name=TaskName.DAILY,
                    task_module=CollectDailyRewards,
                    task_params={}
                ),
            TaskName.BOOKIE: TaskInstance(
                    task_config_name=TaskName.BOOKIE,
                    task_module=InEvent,
                    task_params={}
                ),
            TaskName.RANKING: TaskInstance(
                    task_config_name=TaskName.RANKING,
                    task_module=InRanking,
                    task_params={}
                ),
            TaskName.ATTIC: TaskInstance(
                    task_config_name=TaskName.ATTIC,
                    task_module=MissionMeeting,
                    task_params={}
                ),
            TaskName.ORGAN: TaskInstance(
                    task_config_name=TaskName.ORGAN,
                    task_module=Organization,
                    task_params={}
                ),
            TaskName.SWEEP: TaskInstance(
                    task_config_name=TaskName.SWEEP,
                    task_module=InAbundance,
                    task_params={}
                ),
            TaskName.TRAIN: TaskInstance(
                    task_config_name=TaskName.TRAIN,
                    task_module=InTraining,
                    task_params={}
                ),
            TaskName.APVE: TaskInstance(
                    task_config_name=TaskName.APVE,
                    task_module=InAutoPVE,
                    task_params={}
                ),
            TaskName.PVP: TaskInstance(
                    task_config_name=TaskName.PVP,
                    task_module=InPVP,
                    task_params={}
                ),
            # TaskName.DUNGEONS: TaskInstance(
            #         task_config_name=TaskName.DUNGEONS,
            #         task_module=InDungeons,
            #         task_params={}
            #     ),
            TaskName.CUSTOM: TaskInstance(
                task_config_name=TaskName.CUSTOM,
                task_module=UserTask,
                task_params={}
            ),
        }
        # 生成config task name映射表
        self.task_config_name = {conname: conname for conname in self.taskmap}


task_instances_map = TaskInstanceMap()

class AllTask:

    # 单例
    def __init__(self) -> None:
        pass
        
    def parse_task(self) -> None:
        """
        从config里解析任务列表，覆盖原有的任务列表
        """
        self.taskpool = []
        if config.userconfigdict["OPEN_GAME_APP_TASK"]:
            self.add_task(EnterGame())
        # GUI为了显示TaskName也会导入此文件，从而创建AllTask的实例，这边判断下如果config没有解析json就跳过
        if "TASK_ORDER" in config.userconfigdict and "TASK_ACTIVATE" in config.userconfigdict:
            # 把config的任务列表转换成任务实例列表
            for i in range(len(config.userconfigdict['TASK_ORDER'])):
                task_name = config.userconfigdict['TASK_ORDER'][i]
                if task_name not in task_instances_map.taskmap:
                    logging.error(f"任务名:<{task_name}>无法解析, 已知的任务名有: {[t.task_config_name for t in task_instances_map.taskmap.values()]}")
                    raise Exception("Task Name can not be recognized and parsed")
                # 如果任务对应的TASK_ACTIVATE为False，则不添加任务
                if config.userconfigdict['TASK_ACTIVATE'][i] == False:
                    continue
                self.add_task(task_instances_map.taskmap[task_name].task_module(**task_instances_map.taskmap[task_name].task_params))
        else:
            logging.warn("配置文件无TASK_ORDER和TASK_ACTIVATE解析")
        # 任务列表末尾添加一个PostAllTask任务，用于统计资源
        if config.userconfigdict["DO_POST_ALL_TASK"]:
            self.add_task(PostAllTask())
        
        
    
    def run(self):
        """
        运行任务
        """
        # 运行任务前解析
        self.parse_task()
        for task in self.taskpool:
            task.run()
    
    def add_task(self, task:Task) -> None:
        """
        添加任务
        """
        self.taskpool.append(task)


my_AllTask = AllTask()