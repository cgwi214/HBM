
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import config, logging, click, swipe, match, page_pic, button_pic, popup_pic, sleep, click_relative, screenshot


class Organization(Task):
    def __init__(self, name="组织") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)


    def pray(self):
        logging.info("组织祈福")
        self.run_until(
            lambda: match(button_pic(ButtonName.BUTTON_ORGANIZATION_GRAY)),
            lambda: click_relative(button_pic(ButtonName.BUTTON_ORGANIZATION_GRAY), 0, 205,relative_ratio=False),
            sleeptime=3
        )
        if not self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match(page_pic(PageName.PAGE_ORGANIZATION_PRAY)),
        ):
            return

        if match(button_pic(ButtonName.BUTTON_ORGANIZATION_VIP)):
            click(button_pic(ButtonName.BUTTON_ORGANIZATION_VIP))
        elif config.userconfigdict['ORGAN_TYPE'] == "PAY":
            click(button_pic(ButtonName.BUTTON_ORGANIZATION_PAY))
        elif config.userconfigdict['ORGAN_TYPE'] == "GPAY":
            click(button_pic(ButtonName.BUTTON_ORGANIZATION_GPAY))
        elif config.userconfigdict['ORGAN_TYPE'] == "VPAY":
            click(button_pic(ButtonName.BUTTON_ORGANIZATION_VPAY))
        else:
            logging.error("没有找到祈福按钮")
            return

        for _ in range(3):
            click(Page.MAGICPOINT)

        if self.run_until(
            lambda : click(button_pic(ButtonName.BUTTON_ORGANIZATION_LEFT)),
            lambda : match(button_pic(ButtonName.BUTTON_ORGANIZATION_LEFT_SURE)),
            times=3
        ):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_ORGANIZATION_LEFT_SURE)),
                lambda: not match(button_pic(ButtonName.BUTTON_ORGANIZATION_LEFT_SURE))
            )
        else:
            logging.error("昨晚的组织奖励已领取或没有")

        for _ in range(3):
            click(Page.MAGICPOINT)

        if match(button_pic(ButtonName.BUTTON_ORGANIZATION_15)):
            click(button_pic(ButtonName.BUTTON_ORGANIZATION_15))
            click(Page.MAGICPOINT)
            click(Page.MAGICPOINT)
        if match(button_pic(ButtonName.BUTTON_ORGANIZATION_20)):
            click(button_pic(ButtonName.BUTTON_ORGANIZATION_20))
            click(Page.MAGICPOINT)
            click(Page.MAGICPOINT)
        if match(button_pic(ButtonName.BUTTON_ORGANIZATION_25)):
            click(button_pic(ButtonName.BUTTON_ORGANIZATION_25))
            click(Page.MAGICPOINT)
            click(Page.MAGICPOINT)

        for _ in range(2):
            click(Page.TOPLEFTBACK)

        self.back_to_home()



    def akaciqi(self):
        logging.info("追击晓组织")
        if not self.run_until(
                lambda: swipe((918,362), (572,363), 0.6),
                lambda: match(button_pic(ButtonName.BUTTON_ORGANIZATION_AKACIQI)),
        ):
            logging.warning("未找到晓组织活动按钮，返回主页")
            return False


        if not self.run_until(
                lambda: click_relative(button_pic(ButtonName.BUTTON_ORGANIZATION_AKACIQI), 0, 205,relative_ratio=False),
                lambda: match(page_pic(PageName.PAGE_ORGANIZATION_AKACIQI)),
                sleeptime=3
        ):
            return

        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ORGANIZATION_REWARD)),
            lambda: match(popup_pic(PopupName.POPUP_ORGANIZATION_REWARD))
        )
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ORGANIZATION_AWARD), sleeptime=1.5),
            lambda: not match(button_pic(ButtonName.BUTTON_ORGANIZATION_AWARD))
        )

        if match(button_pic(ButtonName.BUTTON_ORGANIZATION_ALL)):
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_ORGANIZATION_ALL), sleeptime=1.5),
                lambda: not match(button_pic(ButtonName.BUTTON_ORGANIZATION_ALL))
            )

        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT)

        if match(button_pic(ButtonName.BUTTON_ORGANIZATION_AWARD)):
            self.run_until(
                lambda: (click(button_pic(ButtonName.BUTTON_ORGANIZATION_AWARD), sleeptime=1.5),click(Page.MAGICPOINT, sleeptime=1.5)),
                lambda: not match(button_pic(ButtonName.BUTTON_ORGANIZATION_AWARD))
            )

        for _ in range(3):
            click(Page.MAGICPOINT)

        self.back_to_home()

    def into_organ(self):
        for _ in range(5):
            swipe((259, 356), (774, 352), 0.85)

        self._navigate_to_subpage(ButtonName.BUTTON_VILLAGE_ORGANIZATION, PageName.PAGE_ORGANIZATION)

        # self.run_until(
        #     lambda: click(button_pic(ButtonName.BUTTON_ORGANIZATION_ACTIVITY)),
        #     lambda: match(button_pic(ButtonName.BUTTON_ORGANIZATION_IN), threshold=0.95)
        # )

        switchres = self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ORGANIZATION_ACTIVITY)),
            lambda: match(button_pic(ButtonName.BUTTON_ORGANIZATION_IN), threshold=0.95),
            times=3
        )
        if not switchres:
            logging.error("切换到组织活动失败")
            return


    def on_run(self) -> None:

        self.into_organ()

        self.pray()

        self.into_organ()

        self.akaciqi()

        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)