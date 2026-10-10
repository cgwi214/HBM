from yolo.adb.scrcpy_adb import ScrcpyADB
from yolo.game.game_control import GameControl
from yolo.game.game_action import HeroAgent
import time

def main():
    adb = ScrcpyADB()
    control = GameControl(adb)
    agent = HeroAgent(control)

    while True:
        try:
            # 强制处理当前帧（即使与上一帧相同）
            if adb.last_screen is not None:
                with adb.lock:
                    # 直接调用YOLO检测最新帧
                    detected_objects = adb.yolo(adb.last_screen)
                agent.update(detected_objects)
            time.sleep(0.05)
        except Exception as e:
            print(f"Main loop error: {e}")

if __name__ == "__main__":
    main()
