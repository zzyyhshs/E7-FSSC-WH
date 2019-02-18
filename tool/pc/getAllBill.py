__author__ = '崔畅'
from public.common import basepage
from autoTestFrame import pyselenium
from public.common import datainfo
from config import globalparam
from time import sleep
import time
from public.pages.SubmitToBillPageConfig import SubmitToBillPageConfig
class CreateBillData(basepage.Page):
    def getBillData(self):
        self.alertAccept()

if __name__ == '__main__':
    #获取单据字段数据模板文件内容，字典，key = filed+itemName
    #billList = datainfo.getAllData("allBaseData.xlsx","bill")
    dr = pyselenium.PySelenium("ie")
    # sleep(4)
    sleep(1)
    dr.max_window()
    fsscTest = CreateBillData(dr)
    fsscTest.openSystem(globalparam.system_address)
    fsscTest.loginSystem("admin","1")
    #fsscTest.intoModular("系统管理/单据定义/单据定义")
    fsscTest.infoPrint("系统管理/单据定义/单据定义")
    fromIndex =  "home.pathGo('designer/manageForm.jsf?" + str(time.time()) + "',this)"
    fsscTest.dr.js(fromIndex)
    # sleep(5)
    sleep(1)
    #切换iframe
    fsscTest.switch_to_iframe(SubmitToBillPageConfig.mainIframe)
    #获取所有单据组名称
    xpath = "xpath->//table[@class='rich-tree-node']/tbody/tr"
    BillGroupList  = fsscTest.dr.get_elements(xpath)
    allBill = list()
    allBill.append(["billGroup","billName"])
    #循环所有单据组
    for i in range(0,len(BillGroupList)):
        #print(BillGroupList[i].text)#find_element(By.XPATH,"td[3]").
        billGroupName = BillGroupList[i].text
        if "日常费用" not in billGroupName:
            continue
        #点击单据组
        #fsscTest.dr.click_by_element(billGroup)
        fsscTest.click("xpath->//table[@class='rich-tree-node']["+str(i+1)+"]/tbody/tr")
        # sleep(3)
        sleep(1)
        # 切换iframe
        fsscTest.switch_to_iframe(SubmitToBillPageConfig.centerFrame)
        #切换到单据定义页签
        vouchers = "xpath->//td[@id='tab2_lbl']"
        fsscTest.click(vouchers)
        bills = fsscTest.dr.get_elements(xpath)
        # sleep(5)
        sleep(1)
        for j in range(0, len(bills)):
            billName = bills[j].text
            bill = [billGroupName,billName]
            allBill.append(bill)
            #fsscTest.click("xpath->//table[@class='rich-tree-node'][" + str(j + 1) + "]/tbody/tr")
            sleep(1)
            #fsscTest.click("xpath->//div[@id='budgetMenu:panel1_body']/table/tbody/tr/td[2]")
        fsscTest.switch_to_parent_iframe()
        #break  #调试只循环一次
    fsscTest.switch_to_iframe_out()
    fsscTest.dr.quit()
    datainfo.createFile("allBill_HT.xls", ["allBill"], [allBill])
