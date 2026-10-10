
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import logging, config, click, swipe, match, page_pic, button_pic, popup_pic, sleep, find_in_area


class InAutoPVE(Task):
    def __init__(self, name="小队突袭") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def choose(self):
        if config.userconfigdict["AUTOPVE_BUY"]:
            if not find_in_area(popup_pic(PopupName.POPUP_APVE_BUY), ((465,641),(533,711))):
                self.run_until(
                    lambda: click((502, 678)),
                    lambda: find_in_area(popup_pic(PopupName.POPUP_APVE_BUY), ((465,641),(533,711))),
                )
            else:
                pass
        else:
            if find_in_area(popup_pic(PopupName.POPUP_APVE_BUY), ((465,641),(533,711))):
                self.run_until(
                    lambda: click((502, 678)),
                    lambda: not find_in_area(popup_pic(PopupName.POPUP_APVE_BUY), ((465,641),(533,711))),
                )
            else:
                pass

    def free(self):
        # 开始
        for i in range(2):
            if match(button_pic(ButtonName.BUTTON_APVE_START)):
                click(button_pic(ButtonName.BUTTON_APVE_START))
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_APVE_JUNP)),
                    lambda: not match(button_pic(ButtonName.BUTTON_APVE_JUNP), threshold=0.95),
                )
                sleep(50)
                self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match(page_pic(PageName.PAGE_APVE))
                )

            if match(button_pic(ButtonName.BUTTON_APVE_AUTO)):
                click(button_pic(ButtonName.BUTTON_APVE_AUTO))
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_APVE_JUNP)),
                    lambda: not match(button_pic(ButtonName.BUTTON_APVE_JUNP), threshold=0.95),
                )
                sleep(10)
                self.run_until(
                    lambda: click((106, 686), sleeptime=2),
                    lambda: match(page_pic(PageName.PAGE_APVE))
                )
            logging.info(f"第{i+1}次突袭完成")

    def on_run(self) -> None:

        for _ in range(5):
            swipe((259, 356), (774, 352), 0.85),

        self._navigate_to_subpage(ButtonName.BUTTON_VILLAGE_APVE, PageName.PAGE_APVE)

        self.choose()

        self.free()

        for _ in range(3):
            click(Page.MAGICPOINT, sleeptime=1.5)

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)