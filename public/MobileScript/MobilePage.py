# Author : 朱尧
# email: zhuy@yuanian.com, zzyyhshs@163.com
from time import sleep
import time
import re
from CustomizationError import OwnError
from public.MobileScript import mobileDataInfo, mobileConfig
from public.common.basepage import Page
import traceback
from selenium.webdriver.support.select import Select


class MobilePage(Page):
    allUserDict = mobileDataInfo.getAllUsers("allBaseData.xls", "user", "name")

    def __init__(self, selenium_driver):
        super().__init__(selenium_driver)
        self.wrong_data = ""
        self.last_group_xpath = ""
        self.bill_num = ""
        self.img_path = ""

    def handleBillAuto(self, next_approve, billTestData):
        if next_approve:
            self.login_Mob(next_approve)
            sleep(3)
            self.click(mobileConfig.approve_for_xpath)
            sleep(3)
            verifyResult = self.verifyBillValue(billTestData)
            assert verifyResult == 0, self.wrong_data
            next_approve = self.submissionBill()
            self.logoutSystem_Mob()
            self.handleBillAuto(next_approve, billTestData)

    def filterVerifyData(self, test_data):
        # 1 判断test_data是哪个分组
        #   1.1 判断分组,滚动到分组,点击
        # 2 使用对应的xpath获取数据
        # 3 for ele in 获取到的数据:
        # 4 返回ele.text
        self.judgeBrowserRoll(test_data["field"], 1)
        if test_data["field"] == "主表区":
            elements = self.getElements(mobileConfig.primary_table)
        else:
            elements = self.getElements(mobileConfig.row_path)
        for element in elements:
            if test_data["itemName"] in element.text:
                return element.text.split("\n")[1]

    def logoutSystem_Mob(self, token=None):
        if token:
            sleep(3)
            self.click(mobileConfig.get_back_xpath)
        sleep(3)
        self.click(mobileConfig.my_for_xpath)
        sleep(3)
        self.click(mobileConfig.log_out_xpath)
        sleep(3)

    def getNextOneApprover(self):
        self.infoPrint("获取下一节点审批人")
        try:
            next_one_approver = self.dr.get_element(mobileConfig.next_one_approver_xpath).text
        except:
            next_one_approver = None
        sleep(3)
        return next_one_approver

    def submissionBill(self):
        if traceback.extract_stack()[-2][2] == "handleBillAuto":
            mission_xpath = mobileConfig.verify_pass
        else:
            mission_xpath = mobileConfig.mission_bill_xpath
        self.click(mission_xpath)
        sleep(3)
        approver = self.getNextOneApprover()
        self.click(mobileConfig.make_sure_xpath)
        sleep(3)
        self.assertEqual("提交成功", "提交失败", mobileConfig.pop_up_text)
        return approver

    def searchBill(self, bill_num):
        if traceback.extract_stack()[-3][2] == "handleBillAuto":
            search_xpath = mobileConfig.searchNameDSP
        else:
            search_xpath = mobileConfig.searchNameDCL
        # print(traceback.extract_stack()[-3][2])
        sleep(3)
        self.dr.clear_type(search_xpath, bill_num)
        sleep(3)
        self.click(mobileConfig.search_submit_xpath)
        sleep(2)
        self.click(mobileConfig.find_the_bill)
        sleep(1)

    def verifyBillValue(self, test_data):
        """
        验证数据
        :param bill_num: 单据编号
        :type test_data: <class 'generator'>
        """
        if traceback.extract_stack()[-2][2] == "handleBillAuto":
            self.getVerifyData = self.filterVerifyData
        else:
            self.getVerifyData = self.getVerifyText
        self.searchBill(self.bill_num)
        self.wrong_data = ""
        for verify_data in test_data:
            if verify_data["verifyValue"] and verify_data["verifyShow"]:
                sleep(1)
                self.judgeBrowserRoll(verify_data["field"], 1)
                actual_value = self.getVerifyData(verify_data)
                sleep(3)
                if verify_data["itemType"] == "currency":
                    self.judgeValue(float(actual_value), float(verify_data["verifyValue"]), verify_data["itemName"])
                else:
                    self.judgeValue(str(actual_value), str(verify_data["verifyValue"]), verify_data["itemName"])
        self.setScreenshot()  # 截图
        self.last_group_xpath = ""  # 初始化数据
        self.img_path = ""
        return len(self.wrong_data)

    def getVerifyText(self, verify_data):
        return self.dr.get_element(verify_data["css"]).get_attribute("value")

    def judgeValue(self, actual_value, expected_value, item_name):
        if actual_value == expected_value:
            self.infoPrint("[验证成功]{0}：【实际】{1} 【预期】{2}".format(item_name, actual_value, expected_value))
            return True
        else:
            self.wrong_data += "\n验证失败字段: {0}:【实际】{1} 【预期】{2}".format(item_name, actual_value, expected_value)
            self.infoPrint("[验证失败]{0}：【实际】{1} 【预期】{2}".format(item_name, actual_value, expected_value))
            return False

    def saveBill(self):
        self.click(mobileConfig.save_Btn_xpath)
        sleep(1)
        self.assertEqual("单据保存成功", "保存失败", mobileConfig.pop_up_text)

    def assertEqual(self, assert1, msg, xpath):
        assert2 = self.getText(xpath)
        self.assertionContain(assert2, assert1, msg)
        sleep(2)
        self.infoPrint(assert1)
        self.click(mobileConfig.pop_up_sure)

    def typeInputBillValue(self, billTestData, bill_name):
        """
        输入数据
        :param bill_name: 单据名
        :type billTestData: <class 'generator'>
        """
        for data in billTestData:
            if data["inputShow"] and data["inputValue"]:
                sleep(1)
                self.judgeBrowserRoll(data["field"])
                self.inputValue(data)
        self.setScreenshot()
        self.img_path = ""
        self.dr.click("xpath->//h1[text()='{}']".format(bill_name))

    def judgeBrowserRoll(self, group_name, token=None):
        if group_name == "主表区":
            return
        if token:
            xpath = "xpath->//label[text()='{}']".format(mobileConfig.group_field_dict[group_name])
        else:
            xpath = mobileConfig.Area_dict[group_name]
        if self.last_group_xpath != xpath:
            self.setScreenshot()
            group_element = self.getElement(xpath)
            self.dr.browserRoll(group_element, xpath)
            if group_name != "明细区":
                group_element.click()
                self.dr.browserRoll(group_element, xpath)
            self.last_group_xpath = xpath

    def setScreenshot(self):
        """截图, 拼接"""
        file_name = self.bill_num + "_" + time.strftime("%Y-%m-%d_%H_%M_%S") + '.png'
        img_path = self.dr.get_img(file_name)
        if self.img_path == "":
            self.img_path = img_path
        else:
            self.dr.join_img(self.img_path, img_path)

    def inputValue(self, data):
        if data["itemType"] == "select":
            self.selectInput(data["css"], data["itemName"], data["inputValue"])
        elif data["itemType"] == "date":
            self.dateInput(data["css"], data["itemName"], data["inputValue"])
        else:
            if data["itemName"] in ["申请单号", "合同编号", "发票号码", "单据编号"]:
                self.otherInput(data["css"], data["itemName"], data["inputValue"])
            elif data["itemName"] == "对方账户":
                self.selectInput(data["css"], data["itemName"], data["inputValue"])
            else:
                self.typeInput(data["css"], data["itemName"], data["inputValue"])

    def otherInput(self, css, column_name, value):
        # 不支持多选
        self.infoPrint("输入[{0}],值：{1}".format(column_name, value))
        try:
            self.dr.click_Mob(css)
        except Exception:
            raise OwnError.SelectError(column_name, css=css)
        sleep(2)
        if column_name == "发票号码":
            xpath = "xpath->//label[text()='{}']/../../../preceding-sibling::div[1]/input".format(value)
            sure_xpath = mobileConfig.select_sure3
        elif column_name == "合同编号":
            xpath = "xpath->//label[text()='{}']/../../preceding-sibling::label[1]/input".format(value)
            sure_xpath = mobileConfig.select_sure2
        else:
            xpath = "xpath->//label[text()='{}']/../../preceding-sibling::input[1]".format(value)
            sure_xpath = mobileConfig.select_sure
        try:
            select = Select(self.getElement("xpath->//select[@id='selectId']"))
        except:
            select = None
        if select and select.options:
            i = 0
            while i < len(select.options):
                select.select_by_index(i)
                try:
                    self.dr.click_Mob(xpath)
                    sleep(2)
                    self.click(sure_xpath)
                    return
                except:
                    i += 1
            raise OwnError.OtherError(column_name, value)
        else:
            try:
                self.dr.click_Mob(xpath)
                sleep(2)
                self.click(sure_xpath)
            except Exception:
                raise OwnError.OtherError(column_name, value)

    def dateInput(self, css, column_name, value):
        self.infoPrint("输入[{0}],值：{1}".format(column_name, value))
        try:
            self.dr.click_Mob(css)
        except Exception:
            raise OwnError.DateError(column_name, css=css)
        sleep(1)
        if value == "today":
            self.click("xpath->//td[text()='今天']")
        elif "-" in value:
            try:
                self.click("xpath->//td[@date='{}']".format(value))
            except Exception:
                raise OwnError.DateError(column_name, value)
        else:
            raise OwnError.DateError(column_name)

    def selectInput(self, css, column_name, value):
        self.infoPrint("输入[{0}],值：{1}".format(column_name, value))
        try:
            self.click(css)
        except Exception:
            raise OwnError.SelectError(column_name, css=css)
        sleep(1)
        self.dr.element_wait(mobileConfig.search_input_xpath, 10)
        sleep(1)
        if column_name == "受益人":
            beneficiary_list = re.findall(r"(.*?);", value)
            self.click("xpath->//div[@class='body-center-right']")
            sleep(1)
            for beneficiary in beneficiary_list:
                xpath = "xpath->//span[contains(text(), '{}')]/parent::li[@class='children-li']".format(beneficiary)
                try:
                    self.dr.click_Mob(xpath)
                except Exception:
                    raise OwnError.SelectError(column_name, value=beneficiary)
                sleep(0.5)
            self.click(mobileConfig.select_sure4)
        else:
            self.clearType(mobileConfig.search_input_xpath, value)
            sleep(2)
            self.click(mobileConfig.search_submit_xpath2)
            try:
                xpath = "xpath->//div[@class='scroll']/ul/li[@class='children-li'][2]"
                self.click(xpath)
            except Exception:
                raise OwnError.SelectError(column_name, value=value)

    def getBillNum(self):
        """获取单据编号"""
        self.infoPrint("获取单据编号")
        self.dr.element_wait(mobileConfig.bill_num_img_xpath, 10)
        sleep(1)
        self.click(mobileConfig.bill_num_img_xpath)
        sleep(1)
        bill_num = self.getText(mobileConfig.pop_up_text)
        self.click(mobileConfig.quit_confirm_xpath)
        if bill_num:
            self.bill_num = bill_num.split(":")[1]
        else:
            raise NameError("获取的单据编号为空")

    def intoFillBillPage(self, bill):
        self.infoPrint("进入申请页面")
        self.dr.click(mobileConfig.apply_for_xpath)
        sleep(2)
        try:
            self.dr.click_Mob("xpath->//div[text()='{}']".format(bill))
            sleep(2)
        except Exception:
            raise NameError("单据【{0}】在填单列表没有找到".format(bill))

    def login_Mob(self, user_name):
        self.infoPrint("用户【{0}】登陆系统".format(user_name))
        try:
            username = self.allUserDict[user_name]["username"]
            password = self.allUserDict[user_name]["password"]
        except Exception:
            raise OwnError.UserError(user_name)
        self.loginSystem_Mob(username, password)
        sleep(3)

    def loginSystem_Mob(self, userName, password):  # 登录系统
        self.infoPrint("使用用户[{0}]登陆系统：{0}".format(userName))
        self.inputUserName_Mob(userName)
        sleep(1)
        self.inputPassword_Mob(password)
        sleep(2)
        self.clickLoginButton_Mob()
        sleep(2)
        try:
            erro_ele = self.getElement(mobileConfig.ErrorId)
        except:
            erro_ele = None
            self.infoPrint("使用用户[{0}]登陆成功".format(userName))
        if erro_ele:
            raise OwnError.ButtonError(userName, erro_ele.text)

    def click(self, css):
        super().click(css)
        try:
            sleep(1)
            text = self.dr.get_element(mobileConfig.pop_up_text).text
        except:
            text = None
        if text:
            if "成功" in text or text.count("-") == 3:
                return
            raise OwnError.AlertError(text)
        else:
            pass

    def openSystem_Mob(self, system_address):  # 打开系统
        """打开TSP系统首页"""
        # system_address: url路径
        self.infoPrint("打开系统：{0}".format(system_address))
        self.dr.open(system_address)
        # 等待页面打开成功，如果打开不成功，尝试再打开一次
        try:
            self.dr.element_wait(mobileConfig.LoginButton, secs=10)
        except:
            self.dr.open(system_address)
        sleep(3)

    def inputUserName_Mob(self, user_name):  # 输入用户名
        self.typeInput(mobileConfig.UserName, "用户名", user_name)

    def inputPassword_Mob(self, pass_word):  # 输入密码
        self.typeInput(mobileConfig.UserPwd, "密码", pass_word)

    def clickLoginButton_Mob(self):  # 登录
        self.click(mobileConfig.LoginButton)

    def openManageForm(self):
        self.dr.infoPrint("系统管理/单据定义/单据定义")
        fromIndex = "home.pathGo('designer/manageForm.jsf?" + str(time.time()) + "',this)"
        self.dr.js(fromIndex)
        time.sleep(3)

    def openMobileFieldConfig(self):
        self.infoPrint("系统管理/单据定义/移动填单字段配置")
        fromIndex = "home.pathGo('form/mobileFieldConfig.jsf?" + str(time.time()) + "',this)"
        self.dr.js(fromIndex)
        time.sleep(3)

    def openMobileApprovalConfig(self):
        self.infoPrint("系统管理/单据定义/移动审批字段配置")
        fromIndex = "home.pathGo('form/mobileApprovalConfig.jsf?" + str(time.time()) + "',this)"
        self.dr.js(fromIndex)
        time.sleep(3)
