import math
import time
import threading
from typing import List, Optional
from .game_control import GameControl
from yolo.utils.objects import Detect_Object


class HeroAgent:
    def __init__(self, control: GameControl):
        self.control = control
        self.attack_distance = 100  # 攻击触发距离
        self.dodge_distance = 50  # 闪避触发距离
        self.hero_pos: Optional[tuple] = None  # (x, y)
        self.current_target: Optional[Detect_Object] = None

    def _get_hero_position(self, objects: List[Detect_Object]) -> Optional[tuple]:
        """从检测结果中获取Hero坐标"""
        for obj in objects:
            if obj.label == 0:
                # 计算中心点坐标
                return (
                    int(obj.rect.x + obj.rect.w / 2),
                    int(obj.rect.y + obj.rect.h / 2)
                )
        return None

    def select_target(self, objects: List[Detect_Object]) -> Optional[Detect_Object]:
        """动态优先级选择目标（每帧更新）"""
        # 实时获取Hero坐标
        self.hero_pos = self._get_hero_position(objects)
        if not self.hero_pos:
            return None

        valid_objects = []
        for obj in objects:
            # 只保留两种怪物类型
            if obj.label in (2, 3):
                dx = obj.rect.x - self.hero_pos[0]
                dy = obj.rect.y - self.hero_pos[1]
                distance = math.hypot(dx, dy)
                valid_objects.append((obj, distance))

        # 按新优先级排序：类型优先 > 距离次之
        priority_order = {3: 0, 2: 1}
        valid_objects.sort(key=lambda x: (
            priority_order[x[0].label],  # 先按类型优先级
            x[1]  # 再按距离排序
        ))

        return valid_objects[0][0] if valid_objects else None

    def calculate_angle(self, target_pos: tuple) -> float:
        """计算目标相对于Hero的角度"""
        dx = target_pos[0] - self.hero_pos[0]
        dy = self.hero_pos[1] - target_pos[1]  # Y轴向下
        return math.degrees(math.atan2(dy, dx)) % 360

    def move_towards(self, target_pos: tuple, duration: float = 0.1):
        """向目标方向移动（持续更新）"""
        angle = self.calculate_angle(target_pos)
        self.control.move(angle, duration)

    def execute_attack(self, target_pos: tuple):
        """执行攻击序列（带位置更新）"""

        # def _attack_sequence():
        self.control.skill2()
        time.sleep(3)
        self.control.skill1()
        time.sleep(1.8)
        self.control.attack()
        time.sleep(0.01)
        self.control.skill3()
        time.sleep(1)
        self.control.attack()
        # threading.Thread(target=_attack_sequence).start()


    def should_dodge(self, target_pos: tuple) -> bool:
        """判断是否需要闪避"""
        dx = target_pos[0] - self.hero_pos[0]
        dy = target_pos[1] - self.hero_pos[1]
        distance = math.hypot(dx, dy)
        return distance < self.dodge_distance

    def update(self, objects: List[Detect_Object]):
        """每帧更新逻辑"""
        try:
            # 获取最新目标
            target = self.select_target(objects)
            if not target or not self.hero_pos:
                # 无目标时停止移动或执行巡逻
                self.control.move(0, 0)  # 停止移动
                self.current_target = None
                return

            target_pos = (target.rect.x, target.rect.y)

            # 躲避逻辑优先
            if self.should_dodge(target_pos):
                self.control.dodge(t=0.5)  # 长按闪避0.5秒
                return

            # 持续移动（每0.1秒更新方向）
            self.move_towards(target_pos)

            # 判断攻击条件
            dx = target_pos[0] - self.hero_pos[0]
            dy = target_pos[1] - self.hero_pos[1]
            if math.hypot(dx, dy) <= self.attack_distance:
                self.execute_attack(target_pos)
        except Exception as e:
            print(f"Action update error: {str(e)}")
            self.current_target = None