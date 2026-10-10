# 针对于单个HBM任务实例的工具方法，默认截图内容为当前HBM任务实例的模拟器截图
import json
from typing import Tuple, Union
from .adb_utils import *
from .image_processing import *
from .subprocess_helper import *
from .notification import *
from .data_utils import *
from .hbm_exceptions import *

from modules.utils.log_utils import logging
import time
from modules.configs.MyConfig import config


def get_config_time_after_click():
    return config.userconfigdict['TIME_AFTER_CLICK']

def get_config_screenshot_name():
    return config.userconfigdict['SCREENSHOT_NAME']

def get_config_pic_path():
    return config.userconfigdict['PIC_PATH']

def get_screenshot_cv_data():
    """
    获取截图的内容数据，当图片截图出错时，返回的内容是None
    """
    if config.userconfigdict["SCREENSHOT_METHOD"] == "pipe":
        return config.sessiondict["SCREENSHOT_DATA"]
    else:
        return cv2.imread(get_config_screenshot_name())

def click(item:Union[str, Tuple[float, float]], sleeptime = -1, threshold=0.9) -> bool:
    """
    点击图片的位置（x, y）或中心（由str给出）

    这个动作在点击之后会休眠一段时间
    """
    # 检查元素是否为str类型
    if isinstance(item, str):
        matchRes = match(item, returnpos=True, threshold=threshold)
        if matchRes[0]:
            click_on_screen(matchRes[1][0], matchRes[1][1])
            if(sleeptime!=-1):
                time.sleep(sleeptime)
            else:
                time.sleep(get_config_time_after_click())
            return True
        else:
            logging.warning("无法匹配模板图像: {} ".format(item))
            return False
    else:
        click_on_screen(item[0], item[1])
        if(sleeptime!=-1):
            time.sleep(sleeptime)
        else:
            time.sleep(get_config_time_after_click())
        return True

def swipe(item:Union[str, Tuple[float, float]], toitem: Union[str, Tuple[float, float]], durationtime = 0.3, sleeptime = -1) -> bool:
    """
    将位置（x, y）或图片的中心滑动到一个位置或图片
    """
    frompos = None
    topos = None
    # 检查元素是否为str类型
    if isinstance(item, str):
        (res, pos) = match_pattern(sourcepic_mat=get_screenshot_cv_data() ,patternpic=item)
        if res:
            frompos = (pos[0], pos[1])
    else:
        frompos = (item[0], item[1])
    if isinstance(toitem, str):
        (res, pos) = match_pattern(sourcepic_mat=get_screenshot_cv_data(), patternpic=toitem)
        if res:
            topos = (pos[0], pos[1])
    else:
        topos = (toitem[0], toitem[1])
    if(frompos and topos):
        swipe_on_screen(frompos[0], frompos[1], topos[0], topos[1], durationtime*1000)
        if sleeptime == -1:
            sleep(get_config_time_after_click())
        else:
            sleep(sleeptime)
        return True
    else:
        logging.warning("Cannot find the target pattern {} and {} when try to swipe".format(item, toitem))
        return False

def match(imgurl:str, threshold:float = 0.9, returnpos = False, rotate_trans=False) -> Union[
    bool, Tuple[bool, Tuple[float, float], float]]:
    """
    任务：给定一个模式图片url匹配它

    只有光线变化时，匹配结果才会有细微的差别

    如果returnpos为真，Return[是否找到模式，（模式的x，模式的y），最大匹配值]
    其他:返回布尔值
    """
    # 检查元素是否为str类型
    if returnpos:
        return match_pattern(get_screenshot_cv_data(),imgurl, threshold=threshold, auto_rotate_if_trans=rotate_trans)
    else:
        return match_pattern(get_screenshot_cv_data(),imgurl, threshold=threshold, auto_rotate_if_trans=rotate_trans)[0]

def ocr_area(frompixel, topixel, multi_lines = False) -> Tuple[str, float]:
    """
    OCR屏幕截图中给定矩形区域中的区域
    """
    lowerpixel = (min(frompixel[0], topixel[0]), min(frompixel[1], topixel[1]))
    highterpixel = (max(frompixel[0], topixel[0]), max(frompixel[1], topixel[1]))
    ocr_result = ocr_pic_area(get_screenshot_cv_data(), lowerpixel[0], lowerpixel[1], highterpixel[0], highterpixel[1], multi_lines=multi_lines)
    return ocr_result

def ocr_area_0(frompixel, topixel) -> bool:
    """
    OCR给定矩形区域中的数字是否为0，如果长度为>1则返回False
    """
    lowerpixel = (min(frompixel[0], topixel[0]), min(frompixel[1], topixel[1]))
    highterpixel = (max(frompixel[0], topixel[0]), max(frompixel[1], topixel[1]))
    res_str = ocr_pic_area(get_screenshot_cv_data(), lowerpixel[0], lowerpixel[1], highterpixel[0], highterpixel[1])[0]
    res_str = res_str.strip()
    allpossibles = ["0", "O", "o", "Q", "０"]
    # 如果长度为1，就判断它是不是0
    if len(res_str) == 1:
        if res_str[0] in allpossibles:
            return True
    return False

def match_pixel(xy, color, printit = False):
    """
    匹配像素是否为给定颜色
    """
    sc_mat_data = get_screenshot_cv_data()
    return match_pixel_color_range(sc_mat_data, xy[0], xy[1], color[0], color[1], printit=printit)

def page_pic(picname):
    """
    给定页面的图片名称，得到图片的路径
    """
    # get_config_pic_path() + "/PAGE" + f"/{picname}.png"
    return os.path.join(get_config_pic_path(), "PAGE", f"{picname}.png")

def button_pic(buttonname):
    """
    给定按钮的图片名称，得到图片的路径
    """
    # get_config_pic_path() + "/BUTTON" + f"/{buttonname}.png"
    return os.path.join(get_config_pic_path(), "BUTTON", f"{buttonname}.png")

def popup_pic(popupname):
    """
    给定弹窗的图片名称，得到图片的路径
    """
    # get_config_pic_path() + "/POPUP" + f"/{popupname}.png"
    return os.path.join(get_config_pic_path(), "POPUP", f"{popupname}.png")



def sleep(seconds:float):

    time.sleep(seconds)

def screenshot(output_png = False):
    """
    截图
    """
    # start = time.time()
    screen_shot_to_global(output_png = output_png)
    # end = time.time()
    # 输出截图耗时小数点后两位
    # logging.debug("截图耗时{:.2f}秒".format(end-start))

def check_connect():
    # 检查当前python目录下是否有screenshot.png文件，如果有就删除
    if os.path.exists(get_config_screenshot_name()):
        logging.info(f"删除{get_config_screenshot_name()}")
        os.remove(get_config_screenshot_name())
    connect_to_device()
    # 尝试截图
    screenshot()
    time.sleep(1)
    sc_data = get_screenshot_cv_data()
    if sc_data is not None:
        logging.info("adb与模拟器连接正常")
        # 检查图片长和宽
        wm_height = sc_data.shape[0]
        wm_width = sc_data.shape[1]
        # 第一维度是高，第二维度是宽
        if wm_height == 720 and wm_width == 1280:
            logging.info("图片分辨率为1280*720")
            dpi_res = get_dpi()
            logging.info(f"DPI: {dpi_res}")
            if "240" not in dpi_res:
                logging.warn("请设置模拟器dpi为240")
                set_dpi(240)
                return False
            return True
        elif wm_height == 1280 and wm_width == 720:
            logging.warn("图片分辨率为720*1280，可能是模拟器设置错误，也可能是模拟器bug")
            logging.warn("继续运行，但是可能会出现问题，请确保模拟器分辨率为1280*720")
            dpi_res = get_dpi()
            logging.info(f"DPI: {dpi_res}")
            if "240" not in dpi_res:
                logging.warn("请设置模拟器dpi为240")
                set_dpi(240)
                return False
            return True
        else:
            logging.error("图片分辨率不为1280*720，请设置模拟器分辨率为1280*720（当前{}*{}）".format(wm_width, wm_height))
            raise Exception("图片分辨率不为1280*720，请设置模拟器分辨率为1280*720（当前{}*{}）".format(wm_width, wm_height))
    logging.error("adb与模拟器连接失败")
    logging.warn("请检查adb与模拟器连接端口号是否正确")
    if "127.0.0.1" in getNewestSeialNumber():
        logging.warn("请确保关闭模拟器网络桥接")
    return False


# def multi_click_until(
#     click_positions: list,
#     stop_condition: callable,
#     interval: float = 0,
#     max_duration: float = 299.0,
#     use_multitouch: bool = False,
#     sleeptime: float = None  # 新增参数
# ) -> bool:
#     """
#     多位置连续点击直到满足停止条件或超时
#
#     Args:
#         click_positions: 点击位置列表，格式 [(x1,y1), (x2,y2)...]
#         stop_condition: 停止条件函数，返回bool
#         interval: 点击间隔（秒）
#         max_duration: 最长持续时间（秒）
#         use_multitouch: 是否使用multiTouch高性能点击
#         sleeptime: 操作结束后等待时间（秒），None时使用config配置
#     """
#     start_time = time.time()
#     attempt_count = 0
#     clicker = MultiTouchUtils() if use_multitouch else None
#
#     # 根据项目配置获取默认等待时间
#     if sleeptime is None:
#         sleeptime = get_config_time_after_click()  # 来自__init__.py
#
#     try:
#         if clicker:
#             clicker.load_config(config)
#
#         while time.time() - start_time < max_duration:
#             attempt_count += 1
#             logging.debug(f"点击循环 #{attempt_count} 已用时间：{time.time() - start_time:.1f}s")
#
#             # 执行批量点击（保持原有逻辑）
#             for pos in click_positions:
#                 try:
#                     # 动态计算剩余时间
#                     remaining = max_duration - (time.time() - start_time)
#                     if remaining <= 0:
#                         break
#
#                     # 执行点击（缩短最后一次点击的等待时间）
#                     actual_delay = min(interval, remaining * 0.8)
#
#                     if clicker:
#                         clicker.click(*pos)
#                     else:
#                         click_on_screen(*pos)
#
#                     sleep(actual_delay)
#
#                 except Exception as e:
#                     logging.error(f"点击{pos}失败: {str(e)}")
#                     traceback.print_exc()
#
#             # 检查停止条件
#             if stop_condition():
#                 logging.info("战斗结束")
#                 break  # 不直接return，为了执行后续等待
#
#             # 动态调整间隔（最后10%时间加速检测）
#             time_left = max_duration - (time.time() - start_time)
#             adjusted_interval = interval * (0.5 if time_left < max_duration * 0.1 else 1.0)
#             sleep(max(0.1, adjusted_interval))
#
#         else:  # while...else结构处理超时
#             logging.warning(f"超过最大持续时间{max_duration}s仍未满足条件")
#             return False
#
#     finally:
#         # 无论是否满足条件都执行等待
#         if sleeptime and sleeptime > 0:
#             logging.debug(f"执行结束等待 {sleeptime}s")
#             sleep(sleeptime)
#
#     return True

# def multi_click_until(
#     click_positions: list,
#     stop_condition: callable,
#     interval: float = 0,
#     max_duration: float = 299.0,
#     use_multitouch: bool = True,  # 默认启用多点触控
#     sleeptime: float = None
# ) -> bool:
#     """优化版：使用多点触控实现真正同步点击"""
#     start_time = time.time()
#     attempt_count = 0
#     clicker = MultiTouchUtils() if use_multitouch else None
#
#     if sleeptime is None:
#         sleeptime = get_config_time_after_click()
#
#     try:
#         if clicker:
#             clicker.load_config(config)
#
#         while time.time() - start_time < max_duration:
#             attempt_count += 1
#             logging.debug(f"多点触控循环 #{attempt_count} 已用时间：{time.time() - start_time:.1f}s")
#
#             # 批量点击逻辑
#             if use_multitouch and clicker:
#                 # 使用MultiTouchUtils实现真正同步点击
#                 for idx, pos in enumerate(click_positions):
#                     clicker._press_down(idx, pos[0], pos[1], 100)
#                 clicker.multitouch_process.stdin.write("c\n")  # 提交所有按压
#                 clicker.multitouch_process.stdin.flush()
#                 sleep(0.05)  # 极短按压保持时间
#                 for idx in range(len(click_positions)):
#                     clicker._press_up(idx)
#             else:
#                 # 使用ADB命令实现伪同步（依赖设备支持）
#                 pointers = " ".join([f"-d {x} {y} 0" for (x, y) in click_positions])
#                 subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(),
#                               "shell", f"input multitouch {len(click_positions)} {pointers} --duration 50"])
#
#             # 检查停止条件
#             if stop_condition():
#                 logging.info("操作终止条件满足")
#                 break
#
#             # 动态间隔控制
#             remaining_time = max_duration - (time.time() - start_time)
#             adjusted_interval = interval * (0.3 if remaining_time < max_duration * 0.2 else 1.0)
#             sleep(max(0.05, adjusted_interval))  # 最小间隔50ms
#
#     except Exception as e:
#         logging.error(f"多点触控异常: {str(e)}")
#         return False
#
#     finally:
#         if sleeptime and sleeptime > 0:
#             sleep(sleeptime)
#
#     return True


# def multi_press_until(
#         press_positions: list[tuple],
#         stop_condition: callable,
#         check_interval: float = 10,
#         max_duration: float = 60.0,
#         use_multitouch: bool = True,
#         sleeptime: float = None
# ) -> bool:
#     """
#     同时长按多个坐标点，直到满足停止条件或超时
#
#     Args:
#         press_positions: 长按坐标列表，格式 [(x1,y1), (x2,y2)...]
#         stop_condition: 停止条件函数，返回 bool
#         check_interval: 条件检查间隔（秒）
#         max_duration: 最大持续时间（秒）
#         use_multitouch: 是否使用多点触控工具
#         sleeptime: 结束后等待时间（秒）
#     """
#     start_time = time.time()
#     mt = MultiTouchUtils() if use_multitouch else None
#     success = False
#
#     try:
#         if mt:
#             mt.load_config(config)
#             mt.press_and_hold(press_positions)
#             logging.info(f"开始同时长按 {len(press_positions)} 个坐标点")
#
#         while time.time() - start_time < max_duration:
#             # 检查停止条件
#             if stop_condition():
#                 success = True
#                 break
#             time.sleep(check_interval)
#
#         else:  # 超时处理
#             logging.warning(f"超过最大持续时间 {max_duration}s 未满足条件")
#
#     except Exception as e:
#         logging.error(f"长按过程中发生异常: {str(e)}")
#         traceback.print_exc()
#     finally:
#         if mt:
#             mt.release_all()
#             logging.info("已释放所有长按坐标点")
#         # 最终等待
#         final_sleeptime = sleeptime if sleeptime is not None else get_config_time_after_click()
#         if final_sleeptime > 0:
#             sleep(final_sleeptime)
#
#     return success


def multi_press_until(
        press_positions: list[tuple],
        stop_condition: callable,
        check_interval: float = 10,
        max_duration: float = 60.0,
        use_multitouch: bool = True,
        sleeptime: float = None
) -> bool:
    start_time = time.time()
    mt = MultiTouchUtils() if use_multitouch else None
    success = False

    try:
        if mt:
            mt.load_config(config)
            mt.press_and_hold(press_positions)
            # logging.info(f"开始同时长按 {len(press_positions)} 个坐标点")

            # ==== 新增逻辑：显式初始化 click_queue（类似 advanced_hybrid_operation）====
            from queue import Queue
            mt.click_queue = Queue(maxsize=100)  # 强制初始化队列

        while time.time() - start_time < max_duration:
            if stop_condition():
                success = True
                break
            time.sleep(check_interval)

    except Exception as e:
        logging.error(f"长按过程中发生异常: {str(e)}")
        traceback.print_exc()
    finally:
        if mt:
            # ==== 修改 release_all 逻辑，避免访问未初始化的 click_queue ====
            if hasattr(mt, 'click_queue') and mt.click_queue is not None:
                # logging.info(f"队列容量: {mt.click_queue.qsize()}")
                logging.info("使用队列")
            else:
                _ = logging.info("未使用队列")
            mt.release_all()

        # 最终等待
        final_sleeptime = sleeptime if sleeptime is not None else get_config_time_after_click()
        if final_sleeptime > 0:
            sleep(final_sleeptime)

    return success


def advanced_hybrid_operation(
        hold_positions: list[tuple],  # 长按坐标列表
        click_sequence: list[tuple],  # 点击顺序队列
        interval_map: dict[tuple, float],  # 坐标:点击后等待时间
        stop_condition: callable,  # 停止条件
        max_duration: float = 310.0,  # 最大持续时间
        base_interval: float = 16,  # 默认间隔
        check_interval: float = 30,  # 条件检查精度
        use_multitouch: bool = True,
        sleeptime: float = None  # 新增参数：结束后等待时间
) -> bool:
    """
    高级组合操作：
    1. 持续长按hold_positions
    2. 按click_sequence顺序点击，每个点击后等待interval_map定义的时间
    3. 循环执行点击序列直到条件满足
    4. 停止后等待sleeptime秒（None时使用配置默认值）
    """
    mt = MultiTouchUtils() if use_multitouch else None
    success = False
    start_time = time.time()

    try:
        if mt:
            mt.load_config(config)
            # 长按启动
            mt.press_and_hold(hold_positions)
            # 启动精确点击序列
            mt.staggered_click(click_sequence, interval_map, base_interval)

        # 监控循环
        while time.time() - start_time < max_duration:
            if stop_condition():
                success = True
                break
            # 动态调整检查间隔
            elapsed = time.time() - start_time
            if elapsed > max_duration * 0.9:
                check_interval = max(0.05, check_interval * 0.5)
            time.sleep(check_interval)

        else:
            logging.warning(f"操作超时 ({max_duration}s)")

    except Exception as e:
        logging.error(f"操作异常: {str(e)}")
        traceback.print_exc()
    finally:
        if mt:
            mt._click_stop_event.set()
            mt.release_all()
            if mt.click_thread.is_alive():
                mt.click_thread.join(timeout=1)

        # 新增sleeptime处理
        final_sleeptime = sleeptime if sleeptime is not None else get_config_time_after_click()
        if final_sleeptime > 0:
            logging.debug(f"执行结束等待 {final_sleeptime}s")
            sleep(final_sleeptime)

    return success


def click_relative(
        img_pattern: str,
        offset_x: float,
        offset_y: float,
        threshold: float = 0.9,
        sleeptime: float = -1,
        relative_ratio: bool = True
) -> bool:
    """
    基于图像匹配的坐标进行相对点击

    Args:
        img_pattern: 要匹配的图片路径/名称
        offset_x: X轴偏移量（比例或像素）
        offset_y: Y轴偏移量（比例或像素）
        threshold: 匹配阈值(0-1)
        sleeptime: 点击后等待时间(秒)，-1使用配置时间
        relative_ratio: 是否使用比例偏移模式

    Returns:
        bool: 是否点击成功
    """
    # 获取匹配结果
    match_res = match(img_pattern, threshold=threshold, returnpos=True)
    if not match_res[0]:
        #logging.warning(f"图片匹配失败: {img_pattern}")
        return False

    # 计算实际坐标
    base_x, base_y = match_res[1]
    img_h, img_w = cv2.imread(img_pattern).shape[:2]

    if relative_ratio:
        target_x = base_x + offset_x * img_w
        target_y = base_y + offset_y * img_h
    else:
        target_x = base_x + offset_x
        target_y = base_y + offset_y

    # 执行点击
    click_success = click((target_x, target_y))

    # 处理等待时间
    if sleeptime == -1:
        # 使用__init__.py中的配置获取方法
        final_sleeptime = get_config_time_after_click()
    else:
        final_sleeptime = max(0, sleeptime)

    sleep(final_sleeptime)

    return click_success


def find_in_area(
        template_path: str,
        search_area: Tuple[Tuple[int, int], Tuple[int, int]],
        threshold: float = 0.9
) -> bool:
    """
    在指定区域内查找模板图片

    Args:
        template_path: 模板路径
        search_area: 搜索区域 ((x1,y1), (x2,y2))
        threshold: 匹配阈值

    Returns:
        bool: 是否找到模板
    """
    # 获取屏幕截图数据
    screenshot()
    screenshot_mat = get_screenshot_cv_data()
    if screenshot_mat is None:
        logging.debug("屏幕截图数据无效")
        return False

    # 解包搜索区域坐标
    (x1, y1), (x2, y2) = search_area

    try:
        # 提取ROI区域
        roi_img = screenshot_mat[y1:y2, x1:x2]
    except Exception as e:
        logging.debug(f"区域截取失败: {str(e)}")
        return False

    # 调用核心匹配逻辑
    matched, _, _ = match_pattern(
        sourcepic_mat=roi_img,
        patternpic=template_path,
        threshold=threshold
    )

    return matched


def click_in_area(
        template_path: str,
        search_area: Tuple[Tuple[int, int], Tuple[int, int]],
        threshold: float = 0.9,
        sleeptime: float = -1
) -> bool:
    """
    在指定区域内查找模板图片并点击中心点

    Args:
        template_path: 模板图片路径
        search_area: 搜索区域 ((x1,y1), (x2,y2))
        threshold: 匹配阈值
        sleeptime: 点击后等待时间

    Returns:
        bool: 是否找到并点击成功
    """
    # 获取全屏截图
    screenshot()
    screenshot_mat = get_screenshot_cv_data()
    if screenshot_mat is None:
        #logging.error("无法获取屏幕截图")
        return False

    # 提取搜索区域ROI
    (x1, y1), (x2, y2) = search_area
    roi_img = screenshot_mat[y1:y2, x1:x2]

    # 区域匹配
    matched, (local_x, local_y), _ = match_pattern(
        sourcepic_mat=roi_img,
        patternpic=template_path,
        threshold=threshold
    )

    if sleeptime == -1:
        # 使用__init__.py中的配置获取方法
        final_sleeptime = get_config_time_after_click()
    else:
        final_sleeptime = max(0, sleeptime)

    if matched:
        # 转换坐标到全局
        global_x = x1 + local_x
        global_y = y1 + local_y
        #logging.info(f"在区域{search_area}中找到模板，点击坐标 ({global_x}, {global_y})")
        return click((global_x, global_y), final_sleeptime)

    #logging.warning(f"未在区域{search_area}中找到模板 {template_path}")