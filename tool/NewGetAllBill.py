# -*- coding:utf-8 -*-
from public.common import basepage
from autoTestFrame import pyselenium
from public.common import datainfo
from config import globalparam
from time import sleep
import time
from public.pages.SubmitToBillPageConfig import SubmitToBillPageConfig


class CreatAllBillXls(basepage.Page):
    xpath = "xpath->//table[@class='rich-tree-node']/tbody/tr"
    bill_type_js = "home.pathGo('designer/manageForm.jsf?" + str(time.time()) + "',this)"
    bill_type_sheet_xpath = "xpath->//td[@id='tab2_lbl']"

    def __init__(self, data):
        self.dr = pyselenium.PySelenium(data["browser"])
        self.username = data["username"]
        self.password = data["password"]
        self.allBill_list = [["billGroup","billName"],]
        self.xls_name = data["xls_name"]
        self.element_text = ""

    def openLoginSystem(self):
        self.openSystem(globalparam.system_address)
        self.dr.max_window()
        self.loginSystem(self.username, self.password)

    def filterElement(self, BillGroupList):
        for i in range(0, len(BillGroupList)):
            # print(BillGroupList[i].text)#find_element(By.XPATH,"td[3]").
            billGroupName = BillGroupList[i].text
            if "日常费用" not in billGroupName:
                continue
            # 点击单据组
            # fsscTest.dr.click_by_element(billGroup)
            self.click("xpath->//table[@class='rich-tree-node'][" + str(i + 1) + "]/tbody/tr")
            # sleep(3)
            sleep(1)
            # 切换iframe
            self.switch_to_iframe(SubmitToBillPageConfig.centerFrame)
            # 切换到单据定义页签
            self.click(CreatAllBillXls.bill_type_sheet_xpath)
            bills = self.dr.get_elements(CreatAllBillXls.xpath)
            # sleep(5)
            sleep(1)
            for j in range(0, len(bills)):
                billName = bills[j].text
                bill = [billGroupName, billName]
                self.allBill_list.append(bill)
                # fsscTest.click("xpath->//table[@class='rich-tree-node'][" + str(j + 1) + "]/tbody/tr")
                sleep(1)
                # fsscTest.click("xpath->//div[@id='budgetMenu:panel1_body']/table/tbody/tr/td[2]")
            self.switch_to_parent_iframe()
            # break  #调试只循环一次

    def createXls(self):
        datainfo.createFile(self.xls_name, ["allBill"], [self.allBill_list])

    def run(self):
        # 打开浏览器
        # 登录admin账号
        self.openLoginSystem()
        # 进入"系统管理/单据定义/单据定义"
        self.dr.js(CreatAllBillXls.bill_type_js)
        self.infoPrint("系统管理/单据定义/单据定义")
        sleep(3)
        # 获取所有单据组名称
        self.switch_to_iframe(SubmitToBillPageConfig.mainIframe)
        BillGroupList = self.dr.get_elements(CreatAllBillXls.xpath)
        # 判断单据组名称是否包含"日常费用"字符,如果有点击
        # 点击单据定义页签,获取所有billdata
        self.filterElement(BillGroupList)
        # 退出系统 关闭浏览器
        self.switch_to_iframe_out()
        self.dr.quit()
        # 创建xls文件, 文件名"allBill_HT.xls", sheet名"allBill",
        self.createXls()

if __name__ == '__main__':
    data = {
        "browser": "ie",
        "username": "admin",
        "password": "1",
        "xls_name": "allBill_HT.xls"
    }
    a = CreatAllBillXls(data)
    a.run()