 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, logging

class ShopCoin(Task):
    def __init__(self, name="商店领铜币") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_STORE)



    def free(self): # 白嫖铜币
        if match(button_pic(ButtonName.BUTTON_STORE_B_B_C_REWARD)):# 铜币领取
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_STORE_B_B_C_REWARD)),
                lambda: not match(button_pic(ButtonName.BUTTON_STORE_B_B_C_REWARD))
            )
        elif match(button_pic(ButtonName.BUTTON_STORE_B_B_C)):# 特权积分
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_STORE_B_B_C)),
                lambda: match(button_pic(ButtonName.BUTTON_STORE_B_B_C_ON))
            )
        elif match(button_pic(ButtonName.BUTTON_STORE_B_B)):# 特权商店
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_STORE_B_B),threshold=0.95),
                lambda: match(button_pic(ButtonName.BUTTON_STORE_B_B_ON),threshold=0.95)
            )
        elif match(button_pic(ButtonName.BUTTON_STORE_B)):# 商店
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_STORE_B)),
                lambda: match(button_pic(ButtonName.BUTTON_STORE_B_ON))
            )






    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((1215,253)),
            lambda: Page.is_page(PageName.PAGE_STORE),
            sleeptime=3
        ):
            # 如果没到商城界面，返回主页
            return
        
        self.run_until(self.free,
                       lambda: match(popup_pic(PopupName.POPUP_STORE_B_B_C_REWARD))
                       )
        logging.info("铜币已领取")

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_STORE)