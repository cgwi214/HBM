import os
import subprocess
import threading
import traceback
from modules.configs.MyConfig import config
from modules.utils.log_utils import logging
from modules.utils.subprocess_helper import subprocess_run
import time
import numpy as np
import cv2
import platform
import socket


def check_adb_binding():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', 5555))  # 测试是否可绑定到 0.0.0.0
        sock.close()
        logging.warn("警告：ADB 端口可能暴露到外部网络！")
    except OSError:
        logging.info("安全：ADB 端口未开放到公网")

def getNewestSeialNumber(use_config=None):
    # 如果传入指定的配置文件，就使用指定的配置文件
    target_config = config
    if use_config:
        target_config = use_config

    if target_config.userconfigdict["ADB_DIRECT_USE_SERIAL_NUMBER"]:
        # 得到完整的序列号，emulator-5554
        return target_config.userconfigdict["ADB_SEIAL_NUMBER"]
    elif target_config.userconfigdict["TARGET_PORT"] and target_config.userconfigdict["TARGET_IP_PATH"]:
        # 从配置文件里得到模拟器IP和端口
        return "{}:{}".format(target_config.userconfigdict["TARGET_IP_PATH"],
                              target_config.userconfigdict["TARGET_PORT"])
    else:
        logging.error("TARGET_IP_PATH或TARGET_PORT未设置")
        logging.warn("使用默认值：127.0.0.1:5555")
        return "127.0.0.1:5555"


def get_config_adb_path(use_config=None):
    target_config = config
    # 如果传入指定的配置文件，就使用指定的配置文件
    if use_config:
        target_config = use_config
    return target_config.userconfigdict['ADB_PATH']


# 判断是否有TARGET_PORT这个配置项
def disconnect_this_device():
    """断开这个设备"""
    subprocess_run([get_config_adb_path(), "disconnect", getNewestSeialNumber()])


def kill_adb_server():
    """终止adb服务"""
    subprocess_run([get_config_adb_path(), "kill-server"])


def connect_to_device(use_config=None):
    """用给定的设备端口连接到一个设备"""
    if use_config:
        subprocess_run([get_config_adb_path(use_config), "connect", getNewestSeialNumber(use_config)])
    else:
        subprocess_run([get_config_adb_path(), "connect", getNewestSeialNumber()])


def click_on_screen(x, y):
    """点击给定的坐标"""
    subprocess_run(
        [get_config_adb_path(), "-s", getNewestSeialNumber(), "shell", "input", "tap", str(int(x)), str(int(y))])


def swipe_on_screen(x1, y1, x2, y2, ms):
    """从给定坐标滑动到另一个给定坐标"""
    subprocess_run(
        [get_config_adb_path(), "-s", getNewestSeialNumber(), "shell", "input", "swipe", str(int(x1)), str(int(y1)),
         str(int(x2)), str(int(y2)), str(int(ms))])


def convert_img(path):
    with open(path, "rb") as f:
        bys = f.read()
        bys_ = bys.replace(b"\r\n", b"\n")  # 二进制流中的"\r\n" 替换为"\n"
    with open(path, "wb") as f:
        f.write(bys_)


def screen_shot_to_global(use_config=None, output_png=False):
    """
    获取屏幕截图并保存到GlobalState。

    use_config: 期望使用的config对象，为None则使用全局导入的config
    output_png: 使用pipe截图方法时是否保存png图片。截图方法为png时永远会输出png
    """
    target_config = config
    if use_config:
        target_config = use_config
    whether_pipe = target_config.userconfigdict["SCREENSHOT_METHOD"] == "pipe"
    if not whether_pipe:
        # 方法一，重定向输出到文件
        filename = target_config.userconfigdict['SCREENSHOT_NAME']
        with open("./{}".format(filename), "wb") as out:
            subprocess_run(
                [get_config_adb_path(target_config), "-s", getNewestSeialNumber(target_config), "shell", "screencap",
                 "-p"], stdout=out)
        # adb 命令有时直接截图保存到电脑出错的解决办法-加下面一段即可
        if (platform.system() != "Linux"):
            convert_img("./{}".format(filename))
    else:
        # 方法二，使用cv2提取PIPE管道中的数据
        # 使用subprocess的Popen调用adb shell命令，并将结果保存到PIPE管道中
        process = subprocess.run(
            [get_config_adb_path(target_config), "-s", getNewestSeialNumber(target_config), "shell", "screencap", "-p"],
            stdout=subprocess.PIPE)
        # 读取管道中的数据
        screenshot = process.stdout
        # 将读取的字节流数据的回车换行替换成'\n'
        if platform.system() not in ["Linux", "Darwin"]:
            binary_screenshot = screenshot.replace(b'\r\n', b'\n')
        else:
            # Linux和Macos系统不需要替换
            binary_screenshot = screenshot
        # 使用numpy和imdecode将二进制数据转换成cv2的mat图片格式
        if (binary_screenshot == b''):
            logging.error("pipe截图失败")
            target_config.sessiondict["SCREENSHOT_DATA"] = None
            return
        img_screenshot = cv2.imdecode(np.frombuffer(binary_screenshot, np.uint8), cv2.IMREAD_COLOR)
        target_config.sessiondict["SCREENSHOT_DATA"] = img_screenshot
        if output_png:
            cv2.imwrite("./{}".format(target_config.userconfigdict['SCREENSHOT_NAME']), img_screenshot)


def get_now_running_app(use_config=None):
    """
    获取当前运行的app的前台activity
    """
    if use_config:
        output = subprocess_run(
            [get_config_adb_path(use_config), "-s", getNewestSeialNumber(use_config), 'shell', 'dumpsys',
             'window']).stdout
    else:
        output = subprocess_run(
            [get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'dumpsys', 'window']).stdout
    # adb shell "dumpsys window | grep mCurrentFocus"
    for sentence in output.split("\n"):
        if "mCurrentFocus" in sentence:
            # 找到当前运行的app那行
            output = sentence
            if "null" in output:
                logging.warn(">>> MUMU模拟器需要设置里关闭保活！ <<<")
                break
    # 截取app activity
    try:
        app_activity = output.split(" ")[-1].split("}")[0]
    except Exception as e:
        logging.warn("截取当前运行的app名失败：{}".format(output))
        return output
    return app_activity


def get_now_running_app_entrance_activity(use_config=None):
    """
    得到当前app的入口activity
    """
    # 先获取当前运行的app的前台activity
    front_activity = get_now_running_app(use_config)
    logging.info("当前运行的app的前台activity是：{}".format(front_activity))
    # 提取出包名
    package_name = front_activity.split("/")[0]
    if use_config:
        output = subprocess_run(
            [get_config_adb_path(use_config), "-s", getNewestSeialNumber(use_config), 'shell', 'cmd', 'package',
             'resolve-activity', '--brief', package_name]).stdout
    else:
        output = subprocess_run(
            [get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'cmd', 'package', 'resolve-activity',
             '--brief', package_name]).stdout
    # 提取出入口activity
    strlist = output.split()
    entrance_activity = strlist[-1]
    if "/" not in entrance_activity:
        logging.error(f"获取入口activity失败：{output}")
        return entrance_activity
    return entrance_activity


def check_app_running(activity_path: str) -> bool:
    """
    检查app是否在运行，不校验app的activity,只校验app的名字
    """
    try:
        app_name = activity_path.split("/")[0]
    except Exception as e:
        logging.error("activity_path格式错误")
        return False
    # 获取当前运行的app
    output = get_now_running_app()
    logging.info("运行中...当前运行的app是：{}".format(output))
    if app_name in output:
        return True
    else:
        return False


def open_app(activity_path: str):
    """
    使用adb打开app
    """
    brand_waydroid = False
    try:
        # 检查waydroid，全屏打开
        check_brand = subprocess_run(
            [get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'getprop', 'ro.product.brand']).stdout
        if "waydroid" in check_brand.lower():
            brand_waydroid = True
            logging.info("waydroid detected")
    except Exception as e:
        logging.error(f"Error when check brand: {e}")
        pass
    # ==============================
    if brand_waydroid:
        subprocess_run(
            [get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'start', '--windowingMode', '4',
             activity_path], isasync=True)
    else:
        subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'start', activity_path],
                       isasync=True)
    time.sleep(1)
    # 加-n参数，可以在已经启动的时候，切换activity而不只是包
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'start', '-n', activity_path],
                   isasync=True)
    time.sleep(1)
    appname = activity_path.split("/")[0]
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'monkey', '-p', appname, '1'],
                   isasync=True)


def close_app(activity_path: str):
    """
    使用adb关闭app
    """
    appname = activity_path.split("/")[0]
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'force-stop', appname],
                   isasync=True)


def get_wm_size(use_config=None):
    """
    获取屏幕分辨率结果，例如 Physical size: 720x1280
    """
    if not use_config:
        use_config = config
    # 只关注最后一行
    wmres = subprocess_run([get_config_adb_path(use_config), "-s", getNewestSeialNumber(use_config), "shell", "wm",
                            "size"]).stdout.strip().split("\n")[-1]
    return wmres


def get_dpi(use_config=None):
    """
    获取屏幕dpi结果，例如 Physical density: 320
    """
    if not use_config:
        use_config = config
    # 只关注最后一行（物理密度，覆盖密度）
    dpires = subprocess_run([get_config_adb_path(use_config), "-s", getNewestSeialNumber(use_config), "shell", "wm",
                             "density"]).stdout.strip().split("\n")[-1]
    return dpires


def set_dpi(target_dpi, use_config=None):
    """
    set DPI
    """
    if not use_config:
        use_config = config
    if isinstance(target_dpi, float):
        target_dpi = int(target_dpi)
    subprocess_run([get_config_adb_path(use_config), "-s", getNewestSeialNumber(use_config), "shell", "wm", "density",
                    str(target_dpi)], isasync=True)

class MultiTouchUtils:
    """
    使用multitouch的工具类，初始化后需要call load_config()方法
    """

    def __init__(self):
        self.config = None
        self.adb_path = None
        self.adb_serial = None
        self.multitouch_process = None
        self.fail_init = False
        self.time_step = 20  # 细粒度20ms

    def load_config(self, config):
        self.config = config
        self.adb_path = get_config_adb_path(config)
        self.adb_serial = getNewestSeialNumber(config)

    def _initialize(self):
        """初始化multitouch，如果已经初始化过了就不再初始化，返回multiTouch控制进程是否可用"""
        if self.multitouch_process and self.multitouch_process.poll() is None:
            # 运行中
            return True
        if self.fail_init:
            # 初始化失败过，不再初始化
            return False
        # 检查在/data/local/tmp是否有touch.jar
        jar_name = "_touch.jar"
        completed_process = subprocess_run([self.adb_path, "-s", self.adb_serial, "shell", "ls", "/data/local/tmp"])
        if jar_name not in completed_process.stdout:
            # 没有的话，需要推送
            logging.info("没有touch.jar，需要推送")
            # 检查本地是否有touch.zip
            if not os.path.exists("./DATA/touch.zip"):
                logging.error("本地没有touch.zip")
                self.fail_init = True
                return False
            # 推送touch.zip
            completed_process = subprocess_run(
                [self.adb_path, "-s", self.adb_serial, "push", "./DATA/touch.zip", f"/data/local/tmp/{jar_name}"])
            logging.info(completed_process.stdout)
        # 给予执行权限
        completed_process = subprocess_run(
            [self.adb_path, "-s", self.adb_serial, "shell", "chmod", "755", f"/data/local/tmp/{jar_name}"])
        # 启动multitouch
        self.multitouch_process = subprocess_run([self.adb_path, "-s", self.adb_serial, "shell",
                                                  f'export CLASSPATH=/data/local/tmp/{jar_name}; app_process /data/local/tmp com.shxyke.touchevent.App'],
                                                 isasync=True)
        # logging.info(f"multitouch pid: {self.multitouch_process.pid}")
        time.sleep(0.5)
        # 检查是否启动成功
        if self.multitouch_process.poll() is None:  # poll()返回None表示进程正在运行
            # logging.info("multitouch启动成功")
            return True
        else:
            # logging.error("multitouch启动失败")
            self.fail_init = True
            return False

    def _check_init(func):
        """封装装饰器，检查是否初始化成功"""

        def wrapper(self, *args, **kwargs):
            if not self._initialize():
                # logging.error("multitouch初始化失败")
                return None
            else:
                res = func(self, *args, **kwargs)
                return res

        return wrapper

    # ===============析构函数===================
    def __del__(self):
        if self.multitouch_process and self.multitouch_process.poll() is None:
            self.multitouch_process.terminate()
            # logging.info("multitouch进程已终止")

    # ===============操作函数===================

    @_check_init
    def _press_down(self, id: int, x, y, pressure):
        assert isinstance(id, int)
        x = int(x)
        y = int(y)
        pressure = int(pressure)
        finger_str = f"d {id} {x} {y} {pressure}\nc\n"
        self.multitouch_process.stdin.write(finger_str)
        self.multitouch_process.stdin.flush()

    @_check_init
    def _press_up(self, id: int):
        assert isinstance(id, int)
        finger_str = f"u {id}\nc\n"
        self.multitouch_process.stdin.write(finger_str)
        self.multitouch_process.stdin.flush()

    # @_check_init
    # def multi_press(self, positions: list):
    #     """同时按下多个坐标点"""
    #     for idx, (x, y) in enumerate(positions):
    #         self._press_down(idx, x, y, 100)
    #     self.multitouch_process.stdin.write("c\n")
    #     self.multitouch_process.stdin.flush()
    #     time.sleep(0.05)
    #     for idx in range(len(positions)):
    #         self._press_up(idx)

    @_check_init
    def press_and_hold(self, positions: list[tuple]):
        """同时长按多个坐标点（持续按压）"""
        for idx, (x, y) in enumerate(positions):
            self._press_down(idx, x, y, 100)
        self.multitouch_process.stdin.write("c\n")  # 提交操作
        self.multitouch_process.stdin.flush()

    @_check_init
    def sequential_click(self, positions: list[tuple], interval: float):
        """在独立线程中周期性轮询点击坐标"""
        import threading
        self._click_stop_event = threading.Event()

        def _click_loop():
            idx = 0
            while not self._click_stop_event.is_set():
                x, y = positions[idx % len(positions)]
                self.click(x, y)
                idx += 1
                time.sleep(interval)

        self.click_thread = threading.Thread(target=_click_loop, daemon=True)
        self.click_thread.start()

    def stop_sequential_click(self):
        """停止周期性点击"""
        if hasattr(self, '_click_stop_event'):
            self._click_stop_event.set()
            self.click_thread.join(timeout=1)
    @_check_init
    def release_all(self):
        """释放所有按压点"""
        for idx in range(10):
            self._press_up(idx)
        self.multitouch_process.stdin.write("c\n")
        self.multitouch_process.stdin.flush()

        # 添加存在性检查
        if hasattr(self, 'click_queue') and self.click_queue is not None:
            # logging.info(f"启动交错点击，队列容量: {self.click_queue.qsize()}")
            pass
        else:
            logging.info("未初始化点击队列")

    def _click_worker(self):
        """点击工作线程（带独立ID段）"""
        import threading
        current_id = 20  # 从ID 20开始避免冲突
        max_retries = 3  # 失败重试次数

        while not self._click_stop_event.is_set():
            try:
                if self.click_queue.empty():
                    time.sleep(0.1)  # 队列空时短暂等待
                    continue

                pos, wait_time = self.click_queue.get()
                logging.debug(f"开始点击操作: {pos} 等待时间: {wait_time}s")

                # 动态分配触点ID（范围20-44）
                for attempt in range(max_retries):
                    try:
                        # 按下->等待->抬起
                        self._press_down(current_id, pos[0], pos[1], 50)
                        time.sleep(0.05)  # 确保按下生效
                        self._press_up(current_id)
                        current_id = (current_id + 1) % 25 + 20  # 循环使用ID
                        break
                    except BrokenPipeError:
                        logging.warning(f"点击{pos}失败，重试{attempt + 1}/{max_retries}")
                        self._initialize()  # 重新初始化连接

                # 精确等待
                start = time.perf_counter()
                while (time.perf_counter() - start) < wait_time:
                    if self._click_stop_event.is_set():
                        return
                    time.sleep(max(0.01, wait_time / 100))

            except Exception as e:
                logging.error(f"点击线程异常: {str(e)}")
                traceback.print_exc()

    @_check_init
    def staggered_click(self,
                        click_sequence: list[tuple],
                        interval_map: dict[tuple, float],
                        base_interval: float = 0.5
                        ):
        """带队列循环填充的精确点击"""
        import itertools
        from queue import Queue

        self._click_stop_event = threading.Event()
        self.click_queue = Queue(maxsize=100)  # 限制队列大小防止内存溢出

        # 循环生成点击序列
        def _generate_sequence():
            while not self._click_stop_event.is_set():
                for pos in click_sequence:
                    if self._click_stop_event.is_set():
                        return
                    wait_time = interval_map.get(pos, base_interval)
                    self.click_queue.put((pos, wait_time))
                    logging.debug(f"填充点击队列: {pos} 间隔: {wait_time}s")

        # 启动填充线程
        self.fill_thread = threading.Thread(
            target=_generate_sequence,
            daemon=True,
            name="ClickSequenceGenerator"
        )
        self.fill_thread.start()

        # 启动点击工作线程
        self.click_thread = threading.Thread(
            target=self._click_worker,
            daemon=True,
            name="ClickWorker"
        )
        self.click_thread.start()

        # self.click_thread = threading.Thread(target=_click_worker, daemon=True)
        # self.click_thread.start()
