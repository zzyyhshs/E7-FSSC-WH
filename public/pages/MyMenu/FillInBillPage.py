from public.common import basepage
import time
from public.pages.MyMenu.FillInBillPageConfig import FillInBillPageConfig
class FillInBillPage(basepage.Page):
    def intoModular(self):
        self.infoPrint("进入我的菜单-填写单据")
        self.dr.js("home.pathGo('form/formIndex.jsf?" + str(time.time()) + "',this)")



