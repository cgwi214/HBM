from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InShop.BuyItems import BuyItems
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config


class OrganItems(Task):
    def __init__(self, name="组织商店") -> None:
        super().__init__(name)

    def pre_condition(self) -> bool:
        # 有要购买的物品或者要购买所有物品
        return (Page.is_page(PageName.PAGE_STORE) and config.userconfigdict["SHOP_ORGAN"] and
                len(config.userconfigdict["SHOP_ORGAN"]) > 0) or config.userconfigdict["SHOP_ORGAN_BUYALL"]

    def on_run(self) -> None:
        logging.info("开始组织商店购买")
        # 执行购买任务
        BuyItems(
            buyitems=config.userconfigdict['SHOP_ORGAN'],
            buyall=config.userconfigdict["SHOP_ORGAN_BUYALL"]
        ).run()

        # 返回主页
        self.back_to_home()


def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_STORE)