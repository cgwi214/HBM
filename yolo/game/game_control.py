import time

from typing import Tuple

from yolo.adb.scrcpy_adb import ScrcpyADB
import math

class GameControl:
    def __init__(self, adb: ScrcpyADB):
        self.adb = adb

    def calc_mov_point(self, angle: float) -> Tuple[int, int]:
        rx, ry = (220,550)
        r = 80

        x = rx + r * math.cos(angle * math.pi / 180)
        y = ry - r * math.sin(angle * math.pi / 180)
        return int(x), int(y)

    def move(self, angle: float, t: float):
        # 计算轮盘x，y坐标
        x, y = self.calc_mov_point(angle)
        self.adb.touch_start(x, y)
        time.sleep(t)
        self.adb.touch_end(x, y)

    def attack(self, t: float =0.01):
        x, y = (1110, 565)
        self.adb.touch_start(x, y)
        time.sleep(4)
        self.adb.touch_end(x, y)

    def skill1(self, t: float =0.01):
        x, y = (1000, 630)
        self.adb.touch_start(x, y)
        time.sleep(2)
        self.adb.touch_end(x, y)

    def skill2(self, t: float =0.01):
        x, y = (1010, 480)
        self.adb.touch_start(x, y)
        time.sleep(4)
        self.adb.touch_end(x, y)

    def skill3(self, t: float =0.01):
        x, y = (1130, 430)
        self.adb.touch_start(x, y)
        time.sleep(t)
        self.adb.touch_end(x, y)

    def item1(self, t: float =0.01):
        x, y = (1130, 290)
        self.adb.touch_start(x, y)
        time.sleep(t)
        self.adb.touch_end(x, y)

    def dodge(self, t: float =0.5):
        x, y = (860, 620)
        self.adb.touch_start(x, y)
        time.sleep(t)
        self.adb.touch_end(x, y)

if __name__ == '__main__':
    ctl = GameControl(ScrcpyADB())
    # ctl.move(45, 5)
    # ctl.attack()
    # ctl.move(180, 5)
    # ctl.skill1()
    # ctl.move(270, 5)
    # ctl.skill2()
    # ctl.move(0, 5)
    # ctl.skill3()
    # ctl.move(90, 5)
    # ctl.item1()
    # ctl.move(45, 5)
    ctl.dodge()
