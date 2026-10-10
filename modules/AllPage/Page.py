import logging

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep
from modules.configs.MyConfig import config



class Page:
    CENTER = (1280 / 2, 720 / 2)
    """
    屏幕中央
    """
    MAGICPOINT = (750, 718)
    """
    Magicpoint是不包含任何可激活物品的点
    """
    TOPLEFTBACK = (1250, 30)
    """
    大多数情况下，可关闭的全屏幕弹窗在右上角
    """
    TOPLEFT = ((1100, 0), (1280, 90))
    fight_click = [(1135, 160), (1136, 281)]
    """
    点击战斗按钮
    """
    fight_press = [
         (1135, 431), (996, 379), (896, 525), (1002, 492), (998, 610), (859, 615), (1114, 547)
    ]
    """
    长按战斗按钮
    """
    COLOR_BUTTON_YELLOW = ((216, 180, 64), (255, 255, 200))
    COLOR_BUTTON_GRAY = ((50, 55, 55), (175, 160, 150))

    # 父类
    def __init__(self, pagename) -> None:
        self.name = pagename
        self.topages = dict()

    def is_this_page(self) -> bool:
        """
        确定当前截图是否是这一页面
        
        return: 如果是这一页面，返回True，否则返回False
        """
        return match(page_pic(self.name))

    @staticmethod
    def is_page(pagename) -> bool:
        """
        确定当前截图是否是指定页面
        
        Parameters
        ----------
        pagename: 
            PageName下的页面名
        
        Return
        ------
        如果是指定页面，返回True，否则返回False
        """
        return match(page_pic(pagename))
