 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, logging, config

class ShopVIP(Task):
    def __init__(self, name="特权商店"):
        super().__init__(name)

    # 列坐标与购买按钮映射（硬编码版）
    COLUMN_BUTTONS = {
        365: (310, 549),
        628: (574, 549),
        890: (842, 549),
        1156: (1104, 549)
    }
     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_STORE)

    def _find_nearest_column(self, x):
        """找最近列"""
        return min(self.COLUMN_BUTTONS.keys(), key=lambda k: abs(k - x))

    def _handle_purchase_popup(self):
        """弹窗处理"""
        return self.run_until(
            lambda: (click(button_pic(ButtonName.BUTTON_STORE_B_B_A_COMFIRM), sleeptime=1),click(Page.MAGICPOINT, sleeptime=1)),
            lambda: not match(popup_pic(PopupName.POPUP_STORE_TIE)),
            times=2  # 减少重试次数
        )

    def _ap_ticket(self):
        found, (x, y), _ = match(popup_pic(PopupName.POPUP_SUIPIAN), returnpos=True)
        if not found:
            logging.error("未找到商品碎片！")
            return

        # 找到最近列按钮
        btn_pos = self.COLUMN_BUTTONS[self._find_nearest_column(x)]

        # 根据配置点击购买
        for _ in range(config.userconfigdict.get("AP_TICKET_BUY_TIMES")):
            click(btn_pos)
            if not self._handle_purchase_popup():
                break
            sleep(0.5)  # 缩短等待时间

    def shopin(self):
        if match(button_pic(ButtonName.BUTTON_STORE_B_B)):# 特权商店
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
        
        self.run_until(self.shopin,
                       lambda: match(button_pic(ButtonName.BUTTON_STORE_B_B_A_ON))
                       )

        if config.userconfigdict["SHOP_VIP_AP"]:
            self._ap_ticket()


     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_STORE)