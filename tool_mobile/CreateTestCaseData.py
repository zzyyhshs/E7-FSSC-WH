__author__ = '朱尧'
import copy
import os
import time

from selenium.webdriver.support.select import Select

from CustomizationError import OwnError
from config import globalparam
from public.MobileScript import Instrument, mobileDataInfo, mobileConfig
from public.MobileScript.Instrument import MobileSelenium
from public.MobileScript.MobilePage import MobilePage


class DataFilter(object):

    def __init__(self, selenium_driver, xls_name="allItemData.xls"):
        """
        self.bill_dict = {
                            '1.1-zq日常费用申请单':{
                                "主表区-字段1": [0,1],
                                "主表区-字段2": [1,1],
                                ...
                                                },
                            '1.2-zq费用报销单（无申请)':{
                                "主表区-字段1": [0,1],
                                ...
                                                    },
                            ...
                        }
                """
        self.driver = MobilePage(selenium_driver)
        self.allItemData = mobileDataInfo.getAllDataDict(xls_name, "billData")
        self.account_book_list = []
        self.account_book = None
        self.bill_dict = {}
        self.field_dict = {}
        self.file_path = ""

    def judgeClick(self, element, son_xpath=None):
        """
        :param element: 要点击的元素 or 要点击元素的父元素
        :param son_xpath:
        :return: None
        """
        if son_xpath:
            element = element.find_element_by_xpath(son_xpath)
        if self.driver.dr.Browser in ["internet explorer", "ie", "RIE"]:
            self.driver.dr.jsClickElement(element)
        else:
            element.click()
        time.sleep(3)

    def judgeChecked(self, css, element=None):
        """判断元素是否勾选"""
        if element:
            return element.is_selected()
        return self.driver.getElement(css).is_selected()

    def judgeExist(self, name):
        """判断单据组是否存在"""
        for account_book in self.account_book_list:
            if name == account_book.get_attribute("title"):
                return account_book
        return False

    def judgeField(self, field):
        """判断字段是否存在"""
        if field == "单据Logo":
            return True
        for i in self.field_dict:
            old_field = i.split("-", 1)[1]
            if field == old_field:
                return True
        return False

    def judgeText(self, group_text):
        """规避移动填单和移动审批字段分组不一致"""
        text = group_text[0:-4]
        if "表" in text:
            text = text[0:-1] + "区"
        if text == "行程老区":
            return "商旅原行程区"
        elif text == "行程区":
            return "商旅行程区"
        else:
            return text

    def getTotalAccountBook(self):
        """获取单据组列表"""
        # if self.account_book_list == []:
        self.account_book_list = self.driver.getElements(mobileConfig.mobile_xpath)

    def getTotalBill(self):
        """获取单据列表"""
        self.judgeClick(self.account_book, "img")
        return self.driver.getElements(mobileConfig.mobile_bill_xpath)

    def getTotalField(self):
        """获取字段列表"""
        return self.driver.getElements(mobileConfig.field_xpath)

    def addBillData(self):
        self.judgeClick(self.account_book, "img")
        for bill in self.bill_dict:
            css = "xpath->//span[text()='{}']".format(bill)
            element = self.driver.getElement(css)
            self.judgeClick(element)
            select = Select(self.driver.getElement(mobileConfig.select_xpath))
            i = 0
            while i < len(select.options):
                select.select_by_index(i)
                group_text = select.all_selected_options[0].text
                time.sleep(1)
                if self.judgeChecked(mobileConfig.check_field_set_xpath):
                    for element in self.getTotalField():
                        input_element = element.find_element_by_xpath("td[3]/input")
                        group_flied = group_text[0:-4] + "-" + input_element.get_attribute('value')
                        if self.judgeChecked("", element.find_element_by_xpath("td[4]/input")):
                            show = 1
                        else:
                            show = 0
                        if group_flied in self.bill_dict[bill]:
                            self.bill_dict[bill][group_flied][1] = show
                        else:
                            self.bill_dict[bill][group_flied] = [0, show]
                i += 1

    @Instrument.switchIframe_main
    def setAccountBook(self, account_book_name, token=None):
        # 校验单据组,创建单据组文件夹
        self.getTotalAccountBook()
        self.account_book = self.judgeExist(account_book_name)
        if self.account_book:
            if token is None:
                self.file_path = self.createFile(account_book_name)
                self.setBill()
            else:
                self.addBillData()
        else:
            raise OwnError.BillsNameError(account_book_name)

    def setBill(self):
        present_bill_list = self.getTotalBill()
        for bill in present_bill_list:
            self.judgeClick(bill)
            if self.judgeChecked(mobileConfig.check_bill_xpath):
                select = Select(self.driver.getElement(mobileConfig.select_xpath))
                i = 0
                while i < len(select.options):
                    select.select_by_index(i)
                    time.sleep(1)
                    if self.judgeChecked(mobileConfig.check_field_set_xpath):
                        group_text = self.judgeText(select.all_selected_options[0].text)
                        self.setField(group_text)
                    i += 1
                self.bill_dict[bill.text] = self.field_dict
                self.field_dict = {}

    def setField(self, group_text):
        total_field = self.getTotalField()
        for field in total_field:
            input_element = field.find_element_by_xpath("td[2]/input")
            if self.judgeField(input_element.get_attribute('value')):
                show = 0
            else:
                if self.judgeChecked("", field.find_element_by_xpath("td[4]/input")):
                    show = 1
                else:
                    show = 0
            # self.field_dict[input_element.get_attribute('value') + "-" + text[0:-4]] = [show]
            self.field_dict[group_text + "-" + input_element.get_attribute('value')] = [show, 0]

    def createExcel(self):
        # [field, itemName, itemType, itemId, itemVarName, css, inputShow, inputValue, verifyShow,verifyValue]
        for bill_name in self.bill_dict:
            new_bill_name = bill_name.split("_")[0]
            file_path = os.path.join(self.file_path, new_bill_name+".xls")
            result = copy.deepcopy(mobileConfig.result)
            action = mobileConfig.action
            allItemData = copy.deepcopy(self.allItemData)
            for field in self.bill_dict[bill_name]:
                field_info = self.bill_dict[bill_name][field]
                # if field_info[0] == field_info[1] == 0:  # 当输入与展示都为0时不创建
                #     pass
                # else:
                if field in allItemData:
                    allItemData[field].insert(-2, field_info[0])
                    allItemData[field].insert(-1, field_info[1])
                    result.append(allItemData[field])
                else:
                    # try:
                    field1, itemName = field.split("-", 1)
                    result.append([field1, itemName, "", "", "", "", field_info[0], "", field_info[1], ""])
                    # except:
                    #     print("错误数据: " + field)

            self.driver.infoPrint("创建Excel文件: %s" % file_path)
            mobileDataInfo.createFile(file_path, ["billData", "action"], [result, action])

    @Instrument.openSystem
    def run(self, account_book):
        # for name in account_books:
        # 1. 进入移动填单字段配置
        self.driver.openMobileFieldConfig()
        # 1.1 校验单据组,获取单据名及字段信息
        self.setAccountBook(account_book)
        # 2. 进入移动审批字段配置
        self.driver.openMobileApprovalConfig()
        # 2.1 补充字段信息
        self.setAccountBook(account_book, 1)
        # 3. 读取allItemData.xls文件数据
        # 4. 生成excel文件
        self.createExcel()

    def createFile(self, file_name):
        file_path = os.path.join(globalparam.data_mobile_path, file_name)
        if os.path.exists(file_path) is False:
            os.makedirs(file_path)
            self.driver.infoPrint("创建文件夹: %s" % file_path)
        return file_path


# @tomorrow.threads(3)
def main(name):
    star_time = time.time()
    dr = MobileSelenium("ie")
    a = DataFilter(dr)
    a.run(name)
    print(time.time() - star_time)


if __name__ == '__main__':
    # AccountBooks_name = ["zq费用报销组", "合同组（系统内置）", "商旅商城"]
    # AccountBooks_name = ["商旅组-行程版本"]
    # AccountBooks_name = ["Hsy-Test"]
    AccountBooks_name = ["zq费用报销组"]
    for AccountBook in AccountBooks_name:
        main(AccountBook)