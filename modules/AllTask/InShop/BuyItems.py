from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName
from DATA.assets.ItemName import ITEM_MAP

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config
import numpy as np


class BuyItems(Task):
    def __init__(self, buyitems, buyall = False, name="购买商品") -> None:
        super().__init__(name)
        self.buyitems = buyitems
        self.buyall = buyall

    COLUMN_X = {
        1: 365,
        2: 625,
        3: 885,
        4: 1150,
    }
    # 行坐标定义（两行）
    ROW_Y = {
        1: 342,
        2: 595
    }
    SWIPE_START_X = 1000  # 右侧起始点x坐标
    SWIPE_END_X = 200  # 左侧结束点x坐标
    SWIPE_Y = 500  # 滑动操作的y坐标

    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_STORE)


    def handle_popup(self):
        """处理购买弹窗流程"""
        # 点击"最多"按钮
        max_btn = self.run_until(
            lambda: match(button_pic(ButtonName.BUTTON_STORE_MAX)),
            lambda: click(button_pic(ButtonName.BUTTON_STORE_MAX)),
            times=3
        )
        if not max_btn:
            logging.warn("未找到最多按钮")

        # 点击购买确认
        confirm_res = self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_STORE_BUY)),
            lambda: not match(popup_pic(PopupName.POPUP_STORE_BUY)),
            times=3
        )
        if not confirm_res:
            logging.error("购买确认失败")
            return False
        return True

    def swipe_to_column(self, target_col):
        """滑动到目标列"""
        if target_col <= 4:
            return  # 前四列无需滑动

        # 计算需要滑动的次数（每滑动一次显示两列）
        swipe_times = (target_col - 3) // 2
        logging.info(f"需要横向滑动{swipe_times}次到达第{target_col}列")

        for _ in range(swipe_times):
            swipe(
                (self.SWIPE_START_X, self.SWIPE_Y),
                (self.SWIPE_END_X, self.SWIPE_Y),
                0.5
            )
            sleep(1)  # 滑动后等待界面稳定

    def buy_single_item(self, col, row):
        """购买单个商品"""
        item_name = ITEM_MAP.get((col, row), f"未知商品({col},{row})")
        logging.info(f"尝试购买商品：{item_name}")

        # 滑动到目标列
        self.swipe_to_column(col)

        # 计算点击坐标
        # if col <= 4:
        #     click_x = self.COLUMN_X[col]
        # else:
        #     # 动态计算滑动后的列位置（每滑动一次显示两列）
        #     visible_col = 4 + (col - 4) % 2
        #     click_x = self.COLUMN_X[visible_col]
        #
        # click_y = self.ROW_Y[row]

        column_mapping = {5: 2, 6: 3, 7: 4}
        visible_col = column_mapping.get(col, col)  # 前4列保持原值
        click_x = self.COLUMN_X[visible_col]
        click_y = self.ROW_Y[row]

        # 点击商品
        click_res = self.run_until(
            lambda: click((click_x, click_y)),
            lambda: match(popup_pic(PopupName.POPUP_STORE_BUY)),
            times=3
        )
        if not click_res:
            logging.warn(f"{item_name}商品点击失败或已购买")
            return False

        logging.info(f"成功购买：{item_name}")
        # 处理弹窗
        return self.handle_popup()

    def on_run(self) -> None:
        if self.buyall:
            logging.warn("执行一键购买所有商品")
            # 需要购买的所有商品坐标（按列排序，减少滑动次数）
            all_items = sorted(
                [(col, row) for col, row in ITEM_MAP.keys()],
                key=lambda x: x[0]  # 按列号排序
            )

            # 记录已成功购买的商品
            success_buy = []
            current_col = 1  # 当前所在的列

            for col, row in all_items:
                item_name = ITEM_MAP[(col, row)]
                try:
                    # 智能滑动：只在需要时滑动
                    if col > current_col:
                        self.swipe_to_column(col)
                        current_col = col  # 更新当前列
                        sleep(1)  # 滑动后等待界面稳定

                    # 计算点击坐标（适配滑动后的列映射）
                    if col <= 4:
                        click_x = self.COLUMN_X[col]
                    else:
                        # 滑动后列映射规则：5→2, 6→3, 7→4
                        mapped_col = {5: 2, 6: 3, 7: 4}.get(col, 2)
                        click_x = self.COLUMN_X[mapped_col]

                    click_y = self.ROW_Y[row]

                    # 点击商品并处理弹窗
                    if self.buy_single_item(col, row):
                        success_buy.append(item_name)
                        sleep(1.5)  # 增加购买间隔确保稳定性
                    else:
                        logging.warn(f"{item_name} 可能已售罄或购买失败")

                except Exception as e:
                    logging.error(f"购买{item_name}时发生异常: {str(e)}")
                    self.back_to_home()  # 异常后返回安全位置
                    current_col = 1  # 重置列位置

            logging.info(f"一键购买完成，成功购买{len(success_buy)}件商品: {', '.join(success_buy)}")
            return

        total_buy = 0
        for item in self.buyitems:
            if not item['enabled']:
                continue

            col = item['col']
            row = item['row']

            if col < 1 or col > 7:
                logging.error(f"无效列号{col}")
                continue
            if row not in [1, 2]:
                logging.error(f"无效行号{row}")
                continue

            if self.buy_single_item(col, row):
                total_buy += 1
                sleep(1)  # 购买间隔

        if total_buy == 0:
            logging.info("没有需要购买的商品")

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_STORE)