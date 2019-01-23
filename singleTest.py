from autoTestFrame import pyselenium
from config import globalparam
from time import sleep
from public.pages.SubmitToBillPage import SubmitToBillPage
from public.pages.billTestData import BillTestData
if __name__ == '__main__':
    dr = pyselenium.PySelenium(globalparam.browser)
    sleep(4)
    dr.max_window()
    fsscTest = SubmitToBillPage(dr)
    billName = "8.01-事项申请单"
    fillPerson = "填单用户001"
    approvalModel = "Manual"
    testCaseFile = "AutoTestGroup\\8.01-事项申请单-01.xls"
    testCaseData = BillTestData(testCaseFile)
    #fillPerson = testCaseData.handleUsers["1"]
    #打开系统，使用指定用户登陆系统
    fsscTest.openSystem(globalparam.system_address)
    fsscTest.login(fillPerson)
    #打开单据
    fsscTest.intoFillBillPage(billName)
    # 获取单据编号
    billNum = fsscTest.getBillNum()
    #给单据输入数据
    fsscTest.typeInputBillValue(testCaseData)
    sleep(1)
    fsscTest.saveBill()
    sleep(2)
    # 跳转iframe
    fsscTest.switchToContentIframe()
    #验证单据数据
    verifyResult = fsscTest.verifyBillValue(testCaseData)
    fsscTest.switch_to_iframe_out()
    sleep(1)
    if verifyResult["verifyResult"] is False:
        raise Exception(verifyResult["verifyMsg"])
    #fsscTest.assertTrue(verifyResult["verifyResult"], verifyResult["verifyMsg"])
    #提交单据，同时获取下一步审批人
    nextApproveList = fsscTest.submissionBill()
    fsscTest.logoutSystem()
    if approvalModel == "Auto":
        fsscTest.handleBillAuto(nextApproveList, billNum, testCaseData)
    elif approvalModel == "Manual":
        fsscTest.handleBillManual(billNum, testCaseData)
    fsscTest.dr.quit()