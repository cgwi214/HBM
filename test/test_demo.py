import sys
from modules.utils.log_utils import logging
from modules.configs.MyConfig import config
if len(sys.argv) > 1:
    configname = sys.argv[1]
    config.parse_user_config(configname)
    print("读取指定的config文件: "+configname)
else:
    configname = "config.json"
    config.parse_user_config(configname)
    print("读取默认config文件: "+configname)


import time
import statistics
from typing import Tuple
from modules.utils import click, swipe, screenshot, get_screenshot_cv_data, button_pic
from modules.utils.adb_utils import click_on_screen, swipe_on_screen
from modules.utils.image_processing import match_pattern
from DATA.assets.ButtonName import ButtonName

def measure_click_latency(test_times: int = 10) -> float:
    """
    测量点击操作的平均响应时间（单位：秒）
    使用魔法点作为测试坐标
    """
    click_durations = []
    test_pos = (750, 718)  # 使用魔法点或固定测试坐标

    for _ in range(test_times):
        screenshot()  # 确保每次操作前有最新截图
        start_time = time.perf_counter()
        click_on_screen(test_pos[0], test_pos[1])
        end_time = time.perf_counter()
        click_durations.append(end_time - start_time)
        time.sleep(0.5)  # 防止连续操作干扰

    return statistics.mean(click_durations)


def measure_swipe_latency(test_times: int = 10) -> float:
    """
    测量滑动操作的平均响应时间（单位：秒）
    使用固定起止坐标测试
    """
    swipe_durations = []
    from_pos = (500, 500)
    to_pos = (600, 600)

    for _ in range(test_times):
        screenshot()
        start_time = time.perf_counter()
        swipe_on_screen(from_pos[0], from_pos[1], to_pos[0], to_pos[1], 300)
        end_time = time.perf_counter()
        swipe_durations.append(end_time - start_time)
        time.sleep(0.5)

    return statistics.mean(swipe_durations)


def test_match_pattern_speed():
    """
    统计match_pattern处理截图的耗时特性（单位：秒）
    返回（总耗时，平均耗时）
    """
    # 截取一次截图并获取数据
    screenshot()
    cv_data = get_screenshot_cv_data()
    if cv_data is None:
        raise RuntimeError("截图失败，无法获取截图数据")

    # 使用一个固定的模板图片（示例：登录按钮）
    template = button_pic(ButtonName.BUTTON_LOGIN)

    total_time = 0
    test_cycles = 100

    for _ in range(test_cycles):
        start = time.perf_counter()
        # 调用匹配函数，传入已缓存的截图数据
        result = match_pattern(sourcepic_mat=cv_data, patternpic=template, threshold=0.9)
        end = time.perf_counter()
        total_time += (end - start)

    avg_time = total_time / test_cycles
    print(f"匹配耗时统计：")
    print(f"- 总次数: {test_cycles}")
    print(f"- 总耗时: {total_time:.3f} 秒")
    print(f"- 平均耗时: {avg_time * 1000:.2f} 毫秒/次")


# 使用示例
if __name__ == "__main__":
    print(f"点击平均延迟: {measure_click_latency():.3f}s")
    print(f"滑动平均延迟: {measure_swipe_latency():.3f}s")
    test_match_pattern_speed()