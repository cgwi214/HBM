 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import config, click, swipe, match, page_pic, button_pic, popup_pic, sleep, logging
from modules.AllTask.InShop.ShopCoin import ShopCoin
from modules.AllTask.InShop.ShopVIP import ShopVIP
from modules.AllTask.InShop.OrganItems import OrganItems
class InShop(Task):
    def __init__(self, name="商店") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)

    def shop_organ(self):  # 进入组织商店
        if match(button_pic(ButtonName.BUTTON_STORE_C_D)):  # 组织商店
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_STORE_C_D), threshold=0.95),
                lambda: match(button_pic(ButtonName.BUTTON_STORE_C_D_ON), threshold=0.95)
            )
        elif match(button_pic(ButtonName.BUTTON_STORE_C)):  # 玩法商店
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_STORE_C)),
                lambda: match(button_pic(ButtonName.BUTTON_STORE_C_ON))
            )
        else:
            swipe((108, 488), (111, 233), 0.6)


    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((1215,253)),
            lambda: Page.is_page(PageName.PAGE_STORE),
            sleeptime=3
        ):
            # 如果没到商城界面，返回主页
            return

        if config.userconfigdict["SHOP_VIP_SWITCH"]:
            ShopVIP().run()

        if config.userconfigdict["SHOP_VIP_FREE"]:
            ShopCoin().run()

        if config.userconfigdict["SHOP_ORGAN_SWITCH"]:
            self.run_until(self.shop_organ,
                           lambda: match(button_pic(ButtonName.BUTTON_STORE_C_D_A_ON))
                           )
            OrganItems().run()







        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)