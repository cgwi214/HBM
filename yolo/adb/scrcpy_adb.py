from adbutils import adb
import scrcpy
import cv2
import time
import threading
from threading import Lock
from yolo.utils.yolov5 import YoloV5s

class ScrcpyADB:
    def __init__(self):
        devices = adb.device_list()
        client =scrcpy.Client(device=devices[0])
        self.last_screen = None
        #You can also pass an ABlient instance to it
        adb.connect("127.0.0.1:5555")
        print(devices, client)
        client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)
        client.start(threaded=True)
        self.client = client
        self.yolo = YoloV5s(target_size=640,
                            prob_threshold=0.25,
                            nms_threshold=0.45,
                            num_threads=4,
                            use_gpu=True)
        self.detected_objects = []
        self.lock = Lock()  # 线程锁

    def on_frame(self, frame: cv2.Mat):
        if frame is not None:
            self.last_screen = frame
            # 启动新线程处理检测
            threading.Thread(target=self._async_detect, args=(frame,)).start()
            # try:
            #     result = self.yolo(frame)
            #     for obj in result:
            #         color = (0, 255, 0)  # 绿
            #         if obj.label == 0:
            #             color = (255, 0, 0)
            #         elif obj.label == 2:
            #             color = (0, 0, 255)
            #
            #
            #         cv2.rectangle(frame,
            #                     (int(obj.rect.x), int(obj.rect.y)),
            #                     (int(obj.rect.x + obj.rect.w), int(obj.rect.y + + obj.rect.h)),
            #                     color, 2
            #                      )
            #
            #         print(obj)
            #
            # except Exception as e:
            #     print(e)

            cv2.imshow('frame',frame)
            cv2.waitKey(1)

    def _async_detect(self, frame):
        try:
            result = self.yolo(frame)
            with self.lock:
                self.detected_objects = result
        except Exception as e:
            print(e)

    def touch_start(self, x: int or float, y: int or float):
        self.client.control.touch(int(x),int(y),scrcpy.ACTION_DOWN)

    def touch_move(self,x: int or float, y: int or float):
        self.client.control.touch(int(x),int(y),scrcpy.ACTION_MOVE)

    def touch_end(self,x: int or float, y: int or float):
        self.client.control.touch(int(x),int(y),scrcpy.ACTION_UP)

    def tap(self, x: int or float, y: int or float):
        self.touch_start(x, y)
        time.sleep(0.01)
        self.touch_end(x, y)


if __name__ == '__main__':
    sadb = ScrcpyADB()
    time.sleep(1)