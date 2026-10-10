 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class CollectMails(Task):
    def __init__(self, name="邮件") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
    
    def on_run(self) -> None:
        if not self.run_until(
            lambda: click((62,283)),
            lambda: Page.is_page(PageName.PAGE_MAIL),
            sleeptime=3
        ):
            # 如果没到邮箱界面，返回主页
            return

        if not match(button_pic(ButtonName.BUTTON_ONE_COLLECT)):
            # 收取邮箱
            click((465,623))
        else:
            click(button_pic(ButtonName.BUTTON_ONE_COLLECT))
        
        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)