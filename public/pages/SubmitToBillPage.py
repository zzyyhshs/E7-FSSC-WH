__author__ = '崔畅'
import datetime
import time
import random
from public.common import basepage
from config import globalparam
from time import sleep
from public.pages.SubmitToBillPageConfig import SubmitToBillPageConfig
from public.common import datainfo
from public.common import publicfunction
from time import strftime
from selenium.webdriver.support.select import Select
import re
class SubmitToBillPage(basepage.Page):
    #加载所有用户列表数据
    allUserDict = datainfo.getAllUsers("allBaseData.xls", "user", "name")

    def login(self,userName):
        self.infoPrint("用户【{0}】登陆系统".format(userName))
        self.loginSystem(self.allUserDict[userName]["username"], self.allUserDict[userName]["password"])
        sleep(3)

    #点击单据提交审批按钮，并处理可能的弹出框，比如借款未还提示
    def clickFlowSubmit(self):
        self.infoPrint("点击单据提交审批按钮")
        self.switchToIframeNo()
        self.click(SubmitToBillPageConfig.flowSubmit)
        try:
        #self.switch_to_iframe_out()
            self.dr.accept_alert()
            self.infoPrint("存在借款未还")
        #self.switchToIframeNo()
        except:
             self.infoPrint("正常审批")
        sleep(2)
        self.switch_to_iframe_out()

        # 点击单据提交审批按钮，并处理可能的弹出框，比如借款未还提示

    def clickBillSubmit(self):
        self.switchToContentIframe()
        sleep(1)
        self.click(SubmitToBillPageConfig.billSubmit)
        sleep(1)
        self.switch_to_iframe_out()

    def intoFillBillPage(self,billName):
        self.infoPrint("进入我的菜单-填写单据")
        # home.pathGo('dimension/dimensionTypeManagerNew.jsf?4.625020662136949',this)
        self.dr.js("home.pathGo('form/formIndex.jsf?" + str(time.time()) + "',this)")
        sleep(3)
        if billName is not None and billName!="":
            self.infoPrint("填写单据-" + billName)
            #进入主iframe
            self.switch_to_iframe(SubmitToBillPageConfig.mainIframe)
            #进入单据树iframe
            self.switch_to_iframe(SubmitToBillPageConfig.formTreeIframe)
            sleep(2)
            #点击单据名称，打开单据填单页
            self.click("xpath->//a[contains(text(),'"+billName+"')]")
            sleep(3)
            self.switch_to_iframe_out()
        else:
            raise NameError("单据【{0}】在填单列表没有找到".format(billName))

     # 进入待办任务单据界面，打开对应的单据
    def intoHandleBillPage(self,billNum):
        self.infoPrint("进入我的菜单-待办任务")
        self.dr.js("home.pathGo('flow/newTaskList.jsp?" + str(time.time()) + "',this)")
        sleep(3)
        self.infoPrint("待办任务模块搜索单据："+billNum)
        self.switchToIframeNo()
        # 高级查询
        self.click(SubmitToBillPageConfig.seniorInquire)
        # 输入编号
        self.clearType(SubmitToBillPageConfig.formNoSearch, billNum)
        sleep(2)
        # 查询
        self.click(SubmitToBillPageConfig.searchCX)
        sleep(4)
        # 点击编码打开单据
        self.click("xpath->//a[text()='"+billNum+"']")
        # self.dr.click_text(billNum)
        self.switch_to_iframe_out()
        sleep(3)

    #e7 单据输入数据
    def typeInputBillValue(self,billTestData):
        itemIdList     = billTestData.itemIdList
        itemInputType  = billTestData.itemInputType
        itemCss        = billTestData.itemCss
        itemInputValue = billTestData.itemInputValue
        self.infoPrint("输入单据数据")
        #跳转iframe
        self.switchToContentIframe()
        #输入数据
        self.inputDataBase(itemIdList,itemInputType,itemCss,itemInputValue)
        sleep(1)
        #点击单据Logo，保证所有联动运行
        self.dr.click("xpath->//td[@itemvarname='CompanyLogo' and @itemid='1000000000002002']/img")
        sleep(1)
        # 跳出iframe
        self.switch_to_iframe_out()

    #e7验证单据数据，仅验证数据，不跳转iframe
    def verifyBillValue(self,billTestData):
        itemList = billTestData.itemIdList
        itemName = billTestData.itemName
        itemInputType = billTestData.itemInputType
        itemCss = billTestData.itemCss
        itemVerifyValue = billTestData.itemVerifyValue
        #输入数据
        returnResult = dict()
        verifyResult = True
        verifyMsg = "数据错误的字段：\n"
        for item in itemList:
            if itemVerifyValue[item] != "":
                itemValue = self.dr.get_element(itemCss[item]).get_attribute('value')
                verifyValue = itemVerifyValue[item]
                if itemInputType[item] == "currency":
                    #去除首部的币种符号以及千分位的逗号
                    itemValue = float(re.sub("^[^0-9]*","",itemValue).replace(",",""))
                    verifyValue = float(verifyValue)
                if itemInputType[item] == "date":
                    if verifyValue == "today":
                        verifyValue = str(datetime.datetime.now().date())
                if itemValue != verifyValue:
                    self.infoPrint("[验证失败]{0}：【实际】{1}【预期】{2}".format(itemName[item], itemValue, verifyValue))
                    verifyResult = False
                    verifyMsg += "{0}：【实际】{1} 【预期】{2}\n".format(itemName[item],itemValue,verifyValue)
                else:
                    self.infoPrint("[验证成功]{0}：【实际】{1} 【预期】{2}".format(itemName[item], itemValue, verifyValue))
                sleep(0.2)
        if verifyResult is True:
            self.infoPrint("单据上所有数据验证通过！")
        else:
            self.infoPrint("单据上存在数据验证不通过！")
        returnResult["verifyResult"] = verifyResult
        returnResult["verifyMsg"] = verifyMsg
        return returnResult

    def submissionBill(self):
        self.switchToContentIframe()
        sleep(1)
        self.click(SubmitToBillPageConfig.billSubmit)
        sleep(1)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        nextApproveList = self.getNextApproveList()
        sleep(1)
        self.click(SubmitToBillPageConfig.processSubmit)
        self.switch_to_iframe_out()
        sleep(2)
        self.windowAssertEqual("提交成功", "提交失败")
        return nextApproveList

    def getNextApproveList(self):
        # noinspection PyBroadException
        self.infoPrint("开始获取下一步审批人")
        nextApproveList = []
        self.dr.element_wait("xpath->//div[@id ='actorListDiv']", secs=5)
        elements = self.dr.get_elements("xpath->//div[@id ='actorListDiv']/ul/li[3]")
        for element in elements:
            nextApprove = element.text
            nextApproveList.append(nextApprove)
        if len(nextApproveList) == 0:
            actor = self.getText("xpath->//div[@id ='actorListDiv']/div")
            nextApproveList.append(actor)
        self.infoPrint("下一步审批人"+str(nextApproveList))
        return nextApproveList

    def saveBill(self):
        self.infoPrint("保存单据")
        self.switchToContentIframe()
        self.click(SubmitToBillPageConfig.billSave)
        sleep(1)
        self.switch_to_iframe_out()
        self.windowAssertEqual("单据保存成功！", "保存失败")


    def getBillNum(self):#单据上获取单据编号
        self.infoPrint("开始获取单据编号")
        self.switchToContentIframe()
        billNums = self.dr.get_elements("xpath->//input[@itemvarname='BillNumber' and @itemid='1000000000001955']")
        billNum = billNums[0].get_attribute("value")
        # element = self.dr.get_element("xpath->//td[@itemid='1000000000001956']/img")
        # billNum = element.get_attribute("src")
        # start = billNum.find("=")+1
        # end = billNum.find("&")
        # billNum = billNum[start:end]
        self.infoPrint("单据编号：{0}".format(billNum))
        self.switch_to_iframe_out()
        if billNum == "":
            publicfunction.get_img(self.dr, strftime('%Y-%m-%d_%H_%M_%S') + "_" + "单据编号为空" + ".jpg")
            raise NameError("获取的单据编号为空")
        return billNum

    #E7,传入用户登陆信息&单据编号，完成单据审批,返回下一步审批人
    #需要处理多个人会签的情况
    def handleBillAuto(self,nextApproveList,billNum,testCaseData):
        hasNextApprove = True
        while hasNextApprove:
            self.infoPrint("自动审批单据，审批人列表：{0},单据编号：{1}".format(str(nextApproveList), billNum))
            nextApproveList = self.approvalBillAuto(nextApproveList, billNum, testCaseData)
            if len(nextApproveList) == 0:
                hasNextApprove = False

    def approvalBillAuto(self,approveList,billNum,testCaseData):
        if approveList[0] == "待派工":
            nextApproveList = self.dispatchedWorkersAuto(approveList[0],billNum)
            return nextApproveList
        if approveList[0] == "结束节点":
            return []
        nextApproveList = list()
        for i in range(0, len(approveList)):
            # 登陆系统
            self.openSystem(globalparam.system_address)
            self.infoPrint("切换登陆成功")
            self.login(approveList[i])
            self.intoHandleBillPage(billNum)
            sleep(3)
            self.switchToIframeNo()
            sleep(1)
            verifyResult = self.verifyBillValue(testCaseData)
            sleep(1)
            if verifyResult["verifyResult"] is False:
                raise Exception(verifyResult["verifyMsg"])
            self.switch_to_iframe_out()
            #判断是否需要制证
            if self.hasMakingVoucherBtn():
                self.makingVouchers()
            self.switch_to_iframe_out()
            sleep(1)
            # 点击提交审批按钮
            self.clickFlowSubmit()
            self.switchToJdIframe()
            # 获取下一轮审批人列表，如果提交成功则结束当前审批轮次，提示有会签则不结束
            #if i + 1 == len(approveList):
            nextApproveList = self.getNextApproveList()
            sleep(1)
            self.click(SubmitToBillPageConfig.btnSubmit)
            sleep(3)
            self.switch_to_iframe_out()
            # self.windowAssertContain("成功", "提交审批失败")
            # sleep(1)
            self.switchToJdIframe()
            sleep(1)
            assertMsg = self.getText(SubmitToBillPageConfig.msgContentId)
            self.infoPrint("弹出框信息：" + assertMsg)
            if assertMsg == "提交成功":#单据提交成功，说明如果是会签模式，会签结束了
                self.click(SubmitToBillPageConfig.sure)
                sleep(1)
                self.switch_to_iframe_out()
                self.logoutSystem()
                return nextApproveList
            elif  "成功提交当前任务！" in assertMsg:# 成功提交当前任务！但流程需要等演示用户6处理完成之后，才能进入下一环节
                self.click(SubmitToBillPageConfig.sure)
            else:
                publicfunction.get_img(self.dr, strftime('%Y-%m-%d_%H_%M_%S') + ".jpg")
                raise Exception("提交报错，错误信息：" + assertMsg)
            self.switch_to_iframe_out()
            sleep(2)
            self.logoutSystem()
        return nextApproveList

    #E7手动模式下审批单据
    def handleBillManual(self,billNum,testCaseData):
        handleUsers = testCaseData.handleUsers
        actions = testCaseData.actions
        for i in range(0,len(handleUsers)):
            #serialNumber从1开始，key需要加1
            user = handleUsers[str(i+1)]
            action = actions[str(i+1)]
            temp = action.split(":")
            self.infoPrint("手工模式：user【{0}】，action【{1}】".format(user,action))
            if user =="" or action =="":
                self.infoPrint("user或者action为空，自动跳过")
                continue
            if action == "填单":
                self.infoPrint("单据填写，跳过")
                continue
            elif "提交审批" == action:#退回重新提交
                self.approvalBillManual(user, billNum, testCaseData, action)
            elif "派工" == action:
                # 默认派工给下一步审批人
                handleUsers[str(i+2)]=self.dispatchedWorkersManual(user,billNum,handleUsers[str(i+2)])
            elif "审批" in temp:#审批:派工
                self.approvalBillManual(user,billNum,testCaseData,action)
            elif "退回" in action:
                self.returnBill(user,billNum,action)
            elif "制证" == action:
                self.login(handleUsers[str(i + 1)])
                self.intoHandleBillPage(billNum)
                self.makingVouchers()
                self.logoutSystem()
            elif "自动审批" == action:
                self.handleBillAuto([user],billNum,testCaseData)
            else:
                raise Exception("操作名称错误")

    def returnBill(self,approve,billNum,action):
        actionDataList = action.split(":")
        if len(actionDataList) == 1:
            actionDataList.append("开始节点")
            actionDataList.append("逐级审批")
        if actionDataList[2]=="逐级审批":
            actionDataList[2] = "reject-stepby"
        else:
            actionDataList[2] = "reject-direct"
        self.login(approve)
        self.intoHandleBillPage(billNum)
        sleep(3)
        self.switchToIframeNo()
        #点击退回按钮
        self.click("id->flow_reject")
        sleep(1)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        #退回流程节点，默认开始节点
        targetState = self.dr.get_element("xpath->//select[@id='targetStateSelector']")
        Select(targetState).select_by_value(actionDataList[1])
        sleep(1)
        #在提交类型，默认逐级审批，直送至我
        rejectResult = self.dr.get_element("xpath->//select[@id='rejectResultSelector']")
        Select(rejectResult).select_by_value(actionDataList[2])
        sleep(1)
        self.clearType("id->rejectCommentsInput","自动化测试退回")
        sleep(1)
        self.click("xpath->//input[@value='确定']")
        sleep(1)
        self.windowAssertEqual("退回成功","退回失败")
        sleep(1)
        self.logoutSystem()


    def approvalBillManual(self,approve,billNum,testCaseData,action):
        #登陆系统
        self.openSystem(globalparam.system_address)
        self.login(approve)
        self.intoHandleBillPage(billNum)
        sleep(3)
        self.switchToIframeNo()
        verifyResult = self.verifyBillValue(testCaseData)
        if verifyResult["verifyResult"] is False:
            raise Exception(verifyResult["verifyMsg"])
        self.switch_to_iframe_out()
        if "制证" in action:
            self.makingVouchers()
        # 点击提交审批按钮
        self.clickFlowSubmit()
        sleep(3)
        self.switchToJdIframe()
        sleep(1)
        self.click(SubmitToBillPageConfig.btnSubmit)
        self.switch_to_iframe_out()
        sleep(2)
        self.switchToJdIframe()
        sleep(1)
        assertMsg = self.getText(SubmitToBillPageConfig.msgContentId)
        self.infoPrint("弹出框信息：" + assertMsg)
        if assertMsg == "提交成功" or "成功提交当前任务！" in assertMsg:
            self.click(SubmitToBillPageConfig.sure)
            # 成功提交当前任务！但流程需要等演示用户6处理完成之后，才能进入下一环节
        else:
            raise Exception("提交报错，错误信息：" + assertMsg)
        self.switch_to_iframe_out()
        sleep(2)
        self.logoutSystem()

    #手工模式派工
    def dispatchedWorkersManual(self,approve,billNum,accountant):
        # 登陆系统
        self.login(approve)
        #如果系统是自动派工模式，则等待系统派工后，获取单据当前申请人
        if globalparam.automate is True:
            sleep(globalparam.automaticWorkCycle)
            return self.getNowApprove(billNum)[1]
        self.dr.js("home.pathGo('shareCenter/center-todo-tasks.jsp?" + str(time.time()) + "',this)")
        sleep(3)
        self.switchToIframeNo()
        # 高级查询
        self.click(SubmitToBillPageConfig.seniorInquire)
        sleep(1)
        # 输入编号
        self.clearType(SubmitToBillPageConfig.formNoSearch, billNum)
        sleep(1)
        # 查询
        self.click(SubmitToBillPageConfig.searchCX)
        sleep(1)
        self.click("id->tbl_tr_0_cb")
        sleep(1)
        self.click("xpath->//input[@value='批量派工']")
        sleep(1)
        self.switch_to_iframe_out()
        self.windowAssertEqual("确认批量派工吗?", "派工失败！")
        sleep(2)
        #li[@class='x-tree-node']/div/a/span
        self.switchToJdIframe()
        sleep(1)
        accountantName = ""
        #如果没有传入派工会计名称，则自动派给第一个会计，并返回派工会计姓名
        if accountant == "":
            accountantElement = self.dr.get_element("xpath->//span[@unselectable='on' and contains(text(),'能力值')][1]")
            accountantName = accountantElement.text
            self.infoPrint("单据{0}派工给：{1}".format(billNum, accountantName))
            end = accountantName.find("【")
            accountantName = accountantName[0:end]
            self.click("xpath->//span[@unselectable='on' and contains(text(),'能力值')][1]")
        else:
            accountantElements = self.dr.get_elements("xpath->//span[@unselectable='on' and contains(text(),'能力值')]")
            for accountantElement in accountantElements:
                accountantName = accountantElement.text
                self.infoPrint("单据{0}派工给：{1}".format(billNum, accountantName))
                end = accountantName.find("【")
                accountantName= accountantName[0:end]
                if accountantName == accountant:
                    self.click("xpath->//span[@unselectable='on' and contains(text(),'"+accountantName+"')]")
                    break
        self.switch_to_iframe_out()
        self.windowAssertEqual("手动批量派工成功", "派工失败")
        self.logoutSystem()
        return accountantName

        # 自动模式-派工
    def dispatchedWorkersAuto(self, approve, billNum):
        # 登陆系统
        self.login(approve)
        if globalparam.automate is True:
            sleep(globalparam.automaticWorkCycle)
            return self.getNowApprove(billNum)
        self.infoPrint("进入共享任务管理模块")
        self.dr.js("home.pathGo('shareCenter/center-todo-tasks.jsp?" + str(time.time()) + "',this)")
        sleep(3)
        self.switchToIframeNo()
        # 高级查询
        self.click(SubmitToBillPageConfig.seniorInquire)
        sleep(1)
        # 输入编号
        self.clearType(SubmitToBillPageConfig.formNoSearch, billNum)
        sleep(1)
        # 查询
        self.click(SubmitToBillPageConfig.searchCX)
        sleep(1)
        self.switch_to_iframe_out()
        needRepeat = True
        accountingName = ""
        num = -1
        while needRepeat:
            result = self.arrangeAccountant(billNum,num)
            accountingName = result["accountantName"]
            num = result["num"]
            self.switchToJdIframe()
            alertMsg = self.getText("id->msgContentId")
            self.infoPrint(alertMsg)
            expectMsg1 = "["+billNum+"]共享审批人重复"
            expectMsg2 = "手动批量派工成功"
            if alertMsg == expectMsg1:
                self.click("id->closeBtn")
            elif alertMsg == expectMsg2:
                needRepeat = False
                self.infoPrint("共享审批人未重复！")
            self.switch_to_iframe_out()
        self.windowAssertEqual("手动批量派工成功", "派工失败")
        self.logoutSystem()
        return [accountingName]

    def arrangeAccountant(self,billNum,num):
        self.switchToIframeNo()
        # 如果找不到待派工单据，继续等待5秒
        try:
            self.dr.element_wait("id->tbl_tr_0_cb", 5)
        except:
            self.dr.element_wait("id->tbl_tr_0_cb", 5)
        self.switch_to_iframe_out()
        self.switchToIframeNo()
        self.click("id->tbl_tr_0_cb")
        sleep(1)
        self.click("xpath->//input[@value='批量派工']")
        sleep(1)
        self.switch_to_iframe_out()
        self.windowAssertEqual("确认批量派工吗?", "派工失败！")
        sleep(2)
        # li[@class='x-tree-node']/div/a/span
        self.switchToJdIframe()
        sleep(1)
        # 随机派给一个会计，并返回派工会计姓名
        accountantElements = self.dr.get_elements("xpath->//span[@unselectable='on' and contains(text(),'能力值')]")
        if num == -1:
            num = random.randint(0, len(accountantElements)-1)
        elif len(accountantElements) <= 1:
            raise NameError("产品配置错误，初审复审会计组人员重复")
        elif num == 0:
            num += 1
        elif num >= 1:
            num -= 1
        accountantName = accountantElements[num].text
        self.infoPrint("单据{0}派工给：{1}".format(billNum, accountantName))
        end = accountantName.find("【")
        accountantName = accountantName[0:end]
        accountantElements[num].click()
        #self.click("xpath->//span[@unselectable='on' and contains(text(),'能力值')][" + str(num + 1) + "]")
        self.switch_to_iframe_out()
        result = {"accountantName":accountantName,"num":num}
        self.infoPrint(str(result))
        return result

    def makingVouchers(self):
        self.switchToIframeNo()
        #点击生成凭证按钮
        self.click(SubmitToBillPageConfig.formAuthCertBtn)
        sleep(1)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        #点击确认按钮
        self.click(SubmitToBillPageConfig.okBtn)
        self.switch_to_iframe_out()
        sleep(1)
        #等待凭证生成成功，给出结果
        self.dr.element_wait("xpath->//div[@id='info']",10)
        makingVoucherResult = self.dr.get_element("xpath->//div[@id='info']").text
        #loanBalanceResult = self.dr.get_element("xpath->//div[@id='info']/label/span").text
        self.infoPrint(makingVoucherResult)
        if "生成凭证成功!" not in makingVoucherResult :
            self.infoPrint(makingVoucherResult)
            raise Exception("凭证生成失败")
        if "借贷平衡" not in makingVoucherResult:
            self.infoPrint("凭证借贷不平衡："+makingVoucherResult)
            raise Exception("凭证借贷不平衡，请检查凭证配置！")
        sleep(1)
        self.click("xpath->//img[@id='deleteImg']")
        sleep(1)
        #
        if globalparam.vouchersPush is True:
            self.infoPrint("凭证自动推送")
            self.windowAssertEqual("是否推送", "凭证生成失败")
            sleep(5)
            self.windowAssertEqual("凭证生成并推送成功!", "凭证推送失败")
            sleep(2)
        elif globalparam.vouchersPush is False:
            self.infoPrint("凭证不推送")
            self.windowCancelEqual("是否推送", "凭证生成失败")



    def hasMakingVoucherBtn(self):
        self.switchToIframeNo()
        try:
            self.dr.element_wait(SubmitToBillPageConfig.formAuthCertBtn, 1)
            self.infoPrint("找到凭证生成按钮，执行生成凭证流程！")
            self.switch_to_iframe_out()
            return True
        except:
            self.infoPrint("该流程节点不需要生成凭证，没有找到按钮！")
            self.switch_to_iframe_out()
            return False

    def getNowApprove(self,billNum):
        self.infoPrint("进入查询管理-系统单据模块")
        self.dr.js("home.pathGo('queryAnlay/querySysFormList.jsp?" + str(time.time()) + "',this)")
        sleep(1)
        self.switch_to_iframe(SubmitToBillPageConfig.mainIframe)
        #输入单据编号
        self.clearType(SubmitToBillPageConfig.formNoSearch, billNum)
        sleep(1)
        #点击查询
        self.click(SubmitToBillPageConfig.searchCX)
        sleep(1)
        self.click("xpath->//a[text()='查看流程']")
        sleep(1)
        self.switch_to_iframe_out()
        self.switch_to_iframe(SubmitToBillPageConfig.jdIframe)
        self.switch_to_iframe(SubmitToBillPageConfig.tasksIframe)
        elements = self.dr.get_elements("xpath->//li[@class='list-content2']/div[1]")
        approveList= list()
        for element in elements:
            approve = element.text
            self.infoPrint("当前的审批人：{0}".format(approve))
            approveList.append(approve)
        sleep(1)
        self.switch_to_parent_iframe()
        self.click("xpath->//input[@value='关闭']")
        sleep(1)
        self.switch_to_iframe_out()
        self.logoutSystem()
        return approveList

from autoTestFrame import pyselenium
from config import globalparam
if __name__ == '__main__':
    dr = pyselenium.PySelenium(globalparam.browser)
    sleep(4)
    dr.max_window()
    fsscTest = SubmitToBillPage(dr)
    fsscTest.openSystem(globalparam.system_address)
    #name=fsscTest.dispatchedWorkers("填单用户006","AUTOBXDWSQ1-180529-000064","")
    #print(name)
    # 登陆系统
    # fsscTest.login("填单用户006")
    name = fsscTest.dispatchedWorkersAuto("填单用户006","AUTOBXDWSQ1-180702-000039")
    print(name)
    self.intoModular("我的菜单/待办任务")
    fsscTest.intoHandleBillPage("")
    fsscTest.makingVouchers()
    # 点击提交审批按钮
    fsscTest.switchToIframeNo()
    fsscTest.click(SubmitToBillPageConfig.flowSubmit)
    fsscTest.switch_to_iframe_out()
    fsscTest.getNowApprove("AUTOFYSQD1-180531-000080")
