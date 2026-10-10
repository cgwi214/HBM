from modules.configs.settingMaps import *

from time import time

# 用户的脚本config里的默认值以及可选值
# 如果用户的config里没有某个值，先看能否用settingMaps里映射出来，如果不能，就用默认值代替
# 注意解析链：(default/map/read) -> post parse


# d: default value 默认值
# s: selective value 可选值
# m: map value 映射方法
# from: map value的来源key
# map: map value的映射函数，默认是 lambda x=parsedjson[from]: ...
# p: post parse action 后解析方法，默认是lambda value, parsedjson: ...，如果需要在解析后对值执行一些固定的判断和替换，可以在这重写

# selective value作为提醒值存在，主要的map映射应当在settingMaps里，-》myAllTask.parse_task

defaultUserDict = {
    "TASK_ORDER": {"d": []},
    "TASK_ACTIVATE": {"d": []},
    "SHOP_VIP_FREE":{"d": False},
    "SHOP_VIP_SWITCH": {"d": False},
    "SHOP_VIP_AP": {"d": False},
    "AP_TICKET_BUY_TIMES":{"d":1},
    "SHOP_ORGAN": {
        "d": [
            {'enabled': False, 'col': col, 'row': row}
            for col in range(1, 8)  # 7列
            for row in (1, 2) # 2行
        ]
    },
    'SHOP_ORGAN_SWITCH': {"d": False},
    "SHOP_ORGAN_BUYALL": {"d": False},
    "ORGAN_TYPE":{
        "d":"PAY",
        "s":["PAY","GPAY","VPAY"]
    },
    "TRAINING_ONE_SWEEP":{"d":True},
    "AUTOPVE_BUY":{"d": False},
    "PVP_MAX_TIMES":{"d":8},
    "PVP_VICTORY_TIMES":{"d":2},
    "TARGET_EMULATOR_PATH": {"d": ""},
    "CLOSE_EMULATOR_HBM": {"d": False},
    "CLOSE_EMULATOR_FINISH": {
        "d": False,
        "m": {
            "from": "CLOSE_EMULATOR_HBM",
            "map": lambda x: x
        }
    },
    "CLOSE_GAME_FINISH": {
        "d": False,
        "m": {
            "from": "CLOSE_EMULATOR_HBM",
            "map": lambda x: x
        }
    },
    "CLOSE_HBM_FINISH": {
        "d": False,
        "m": {
            "from": "CLOSE_EMULATOR_HBM",
            "map": lambda x: x
        }
    },
    "PIC_PATH": {"d": "./DATA/assets"},
    "ACTIVITY_PATH": {"d": "com.tencent.KiHan/com.tencent.KiHan.MainActivity"},
    "NEXT_CONFIG": {"d": ""},
    "ADB_PATH": {"d": "./tools/adb/adb.exe"},
    "SCREENSHOT_NAME": {
        "d": "screenshot.png"
    },
    "TARGET_IP_PATH": {"d": "127.0.0.1"},
    "TARGET_PORT": {"d": 5555},
    "KILL_PORT_IF_EXIST": {"d": False},
    "TIME_AFTER_CLICK": {"d": 0.7},
    "RESPOND_Y": {"d": 40},

    "LOCK_SERVER_TO_RESPOND_Y": {"d": True},
    "ENABLE_MAIL_NOTI": {"d": False},

    # 邮件相关
    "MAIL_USER": {"d": ""},
    "MAIL_PASS": {"d": ""},
    "ADVANCED_EMAIL": {"d": False},
    "SENDER_EMAIL": {"d": ""},
    "RECEIVER_EMAIL": {"d": ""},
    "MAIL_HOST": {"d": ""},


    "RUN_UNTIL_TRY_TIMES": {"d": 9},
    "RUN_UNTIL_WAIT_TIME": {"d": 0.6},

    # 是否直接使用emulator-5554这种序列号
    "ADB_DIRECT_USE_SERIAL_NUMBER": {"d": False},
    "ADB_SEIAL_NUMBER": {"d": "emulator-5554"},

    # 是否Http通知
    "ENABLE_HTTP_NOTI": {"d": False},
    "TARGET_HTTP_URL": {"d": ""},
    "TARGET_HTTP_TOKEN": {"d": ""},

    # 是否直接在内存中获取图像数据
    "USE_MEMORY_IMAGE": {"d": False},

    # 任务运行前后的命令
    "PRE_COMMAND": {"d": ""},
    "POST_COMMAND": {"d": ""},

    # 自定义任务
    "USER_DEF_TASKS": {"d": ""},

    # 游戏启动超时时间，秒。防止意料之外的错误判断（超时会触发error），默认超时时间设长点
    "GAME_LOGIN_TIMEOUT": {"d": 600},
    # 游戏卡启动时的重新启动模拟器最多尝试次数
    "MAX_RESTART_EMULATOR_TIMES": {"d": 0},

    # 截图模式, png：保存/读取png图片，pipe读取/单例化管道内数据
    "SCREENSHOT_METHOD": {
        "d": "pipe",
        "s": ["png", "pipe"]
    },

    # 是否执行游戏登录任务（与游戏打开登录，统计消耗的体力，铜币，金币有关）
    "OPEN_GAME_APP_TASK": {
        "d": True
    },
    # 是否执行所有任务结束后的尾部任务（与统计消耗的体力，铜币，金币有关）
    "DO_POST_ALL_TASK": {
        "d": True
    }
}

# 软件的config里的默认值

defaultSoftwareDict = {
    "DUMMYKEY": {"d": "passwd"},

    "ENCRYPT_KEY": {
        "d": "54321",
        "m": {
            "from": "DUMMYKEY",  # 使用现在的时间戳作为加密key，长度截取最后五位，字符串！
            "map": lambda x: str(int(time()))[-5:]
        }},
    # 用户在GUI里的各种备注
    "NOTE": {"d": {
        "HARD_NOTE": "",
    }},
    # 是否输出日志
    "SAVE_LOG_TO_FILE": {"d": False},
    # 发生错误时，是否输出custom日志
    "SAVE_ERR_CUSTOM_LOG": {"d": True},
}

# sessiondict是一个dict，存储一个HBM配置任务的运行时信息，每次运行的时候都会按照以下内容初始化一个新的sessiondict
defaultSessionDict = {
    "PORT_IS_USED": {"d": False},
    "EMULATOR_PROCESS_PID": {"d": None},
    "GUI_OPEN_IN_WEB": {"d": True},
    "HBM_START_TIME": {"d": ""},
    "BEFORE_HBM_SOURCES": {"d": {"power": 0, "copper": 0, "gold": 0}},
    "AFTER_HBM_SOURCES": {"d": {"power": 0, "copper": 0, "gold": 0}},
    "INFO_DICT": {"d": {}},
    # 截图文件读取失败的次数
    "SCREENSHOT_READ_FAIL_TIMES": {"d": 0},
    # 当前尝试重启模拟器次数
    "RESTART_EMULATOR_TIMES": {"d": 0},
    # 截图数据，当SCREENSHOT_METHOD为pipe时使用
    "SCREENSHOT_DATA": {"d": None},
}
