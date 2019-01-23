from public.common import pyselenium
from config import globalparam
from time import sleep
from public.pages.SubmitToBillPage import SubmitToBillPage
import datetime
if __name__ == '__main__':
    dr = pyselenium.PySelenium(globalparam.browser)
    sleep(4)
    dr.max_window()
    fsscTest = SubmitToBillPage(dr)
    billGroup = "费用报销组（系统内置）"
    billName = "1.11-差旅申请单"
    approvalModel = "Auto"
    fillPerson = "张一"
    #打开系统，使用指定用户登陆系统
    fsscTest.openSystem(globalparam.system_address)
    fsscTest.login(fillPerson)
    #打开单据
    fsscTest.intoFillBillPage(billName)

    #给单据输入数据
    fsscTest.inputTrain(1,"二等座",fillPerson)
    fsscTest.inputTrain(2, "特等座", fillPerson)
    #保存单据
    fsscTest.saveBill()
    sleep(2)
    # 获取单据编号
    billNum = fsscTest.getBillNum()
    #提交单据，同时获取下一步审批人
    nextApproveList = fsscTest.submissionBill()
    fsscTest.logoutSystem()

    #z2审批通过
    fsscTest.login("张二")
    fsscTest.intoHandleBillPage(billNum)
    sleep(3)
    # 点击提交审批按钮
    fsscTest.switchToIframeNo()
    fsscTest.click("id->flow_submit")
    sleep(2)
    fsscTest.switch_to_iframe_out()

    fsscTest.switchToJdIframe()
    fsscTest.click("id->btnSubmit")
    sleep(3)
    fsscTest.switch_to_iframe_out()
    fsscTest.windowAssertContain("提交成功", "提交审批失败")
    fsscTest.dr.quit()