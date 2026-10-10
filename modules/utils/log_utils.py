import sys
import os
from time import strftime
from modules.configs.MyConfig import config

import hashlib

# 构建日志类
class MyLogger:
    """
    日志类，包装常用的日志类方法，info, debug, warn, warning, error
    """
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARN"
    ERROR = "ERROR"
    
    def __init__(self) -> None:
        self.custom_log_list = []
        self.info_list = []
        self.debug_list = []
        self.warn_list = []
        self.error_list = []
        self.logqueue = None
        self.tick = False
        self.logfile = None

    def get_now_time_str(self):
        return strftime("%Y-%m-%d-%H-%M-%S")

    def tick_log_file_fd(self):
        """
        创建log文件fd，同一生命周期内只会创建一次
        """
        try:
            if self.tick:
                # 第一次尝试logging内容的时候创建fd，后面再触发不需要再创建
                return
            self.tick = True
            # 使用softwareconfigdict的配置来决定是否保存log到文件
            if config.softwareconfigdict["SAVE_LOG_TO_FILE"]:
                now_timestr = self.get_now_time_str()
                log_file_full_path = os.path.join(config.LOG_FOLDER, f"log_{now_timestr}.txt")
                self.logfile = open(log_file_full_path, "w", encoding="utf-8")
                print(f"track log file fd, log output to: {log_file_full_path}")
            else:
                self.logfile = None
                print("track log file switch off")
        except Exception as e:
            print(f"Create log file error: {e}")
            import traceback
            traceback.print_exc()
            self.logfile = None

    def save_custom_log_file(self):
        """
        保存发生了错误的全量custom日志到文件
        """
        if self.custom_log_list:
            try:
                now_timestr = self.get_now_time_str()
                file_short_name = f"custom_log_{now_timestr}.txt"
                file_full_path = os.path.join(config.LOG_FOLDER, file_short_name)
                with open(file_full_path, "w", encoding="utf-8") as f:
                    for line in self.custom_log_list:
                        f.write(line + "\n")
                logging.info("↓↓↓↓↓↓↓↓↓↓")
                logging.info(f"保存全量异常日志到文件: {file_full_path}")
                logging.info("↑↑↑↑↑↑↑↑↑↑")
            except Exception as e:
                logging.error(f"保存全量异常日志到文件失败: {e}")
                import traceback
                traceback.print_exc()

    # 析构函数
    def __del__(self):
        if self.logfile:
            self.logfile.close()
            self.logfile = None
    
    def set_log_queue(self, queue):
        self.logqueue = queue
        
    def hash_str(self, data):
        """得到字符串的哈希值"""
        return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

    def format_msg(self, msg, level):
        return f"{strftime('%M:%S')} - {level} : {str(msg)}"
    
    def colorful_print(self, msg, level):
        print(msg)
        # 打印出来的东西都保存到常规log file里
        self.tick_log_file_fd()
        if self.logfile:
            try:
                self.logfile.write(msg + "\n")
                self.logfile.flush()
            except Exception as e:
                print(f"log file exception: {e}")
                self.logfile = None
        if self.logqueue:
            try:
                self.logqueue.put_nowait(msg)
            except Exception as e:
                print(f"log queue exception: {e}")
                self.logqueue = None
        # flush
        sys.stdout.flush()
        
    
    def info(self, msg):
        formatted_msg = self.format_msg(msg, self.INFO)
        self.info_list.append(formatted_msg)
        self.custom_log_list.append(formatted_msg)
        self.colorful_print(formatted_msg, self.INFO)
    
    def debug(self, msg):
        formatted_msg = self.format_msg(msg, self.DEBUG)
        self.debug_list.append(formatted_msg)
        # debug只保存到custom log里，不打印也不保存到常规log里
        self.custom_log_list.append(formatted_msg)
        # self.colorful_print(formatted_msg, self.DEBUG)
    
    def warn(self, msg):
        formatted_msg = self.format_msg(msg, self.WARN)
        self.warn_list.append(formatted_msg)
        self.custom_log_list.append(formatted_msg)
        self.colorful_print(formatted_msg, self.WARN)
    
    def warning(self, msg):
        self.warn(msg)
        
    def error(self, msg):
        formatted_msg = self.format_msg(msg, self.ERROR)
        self.error_list.append(formatted_msg)
        self.custom_log_list.append(formatted_msg)
        self.colorful_print(formatted_msg, self.ERROR)
    
logging = MyLogger()