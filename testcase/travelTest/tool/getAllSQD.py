from public.common import pyselenium
from config import globalparam
from time import sleep
from public.pages.SubmitToBillPage import SubmitToBillPage
from public.common import datainfo
import time
if __name__ == '__main__':
    recordList = datainfo.getAllDataList("travelTest\\allTravelBillRecord.xls","allRecord")
    dr = pyselenium.PySelenium(globalparam.browser)
    sleep(4)
    dr.max_window()
    fsscTest = SubmitToBillPage(dr)
    fillPerson = "张一"
    date = "2018-06-26"
    #打开系统，使用指定用户登陆系统
    fsscTest.openSystem(globalparam.system_address)
    fsscTest.login(fillPerson)
    #打开单据
    # 进入待办任务
    fsscTest.dr.js("home.pathGo('form/myFormList.jsp?" + str(time.time()) + "',this)")
    fsscTest.switch_to_iframe("xpath->//iframe[@id='main']")
    # 高级查询
    fsscTest.dr.element_wait("xpath->//label[@id='show_text']")
    fsscTest.click("xpath->//label[@id='show_text']")
    # 输入单据类型
    fsscTest.click("id->formName")
    sleep(1)
    fsscTest.clearType("id->searchSupportInput", "1.11-差旅申请单")
    # 查询
    sleep(1)
    fsscTest.click("id->find")
    # 选中
    sleep(1)
    fsscTest.click("xpath->//span[contains(text(),'1.11-差旅申请单')]")
    sleep(1)
    fsscTest.click("xpath->//button[contains(text(),'确定')]")
    sleep(1)
    fsscTest.dateInput("id->billBeginT","起始时间",date)
    sleep(1)
    fsscTest.dateInput("id->billEndT", "结束时间时间", date)
    sleep(1)
    # 查询
    fsscTest.click("xpath->//input[@value='查询']")
    sleep(4)
    xpath = ""
    numElements = fsscTest.dr.get_elements("xpath->//table[@id='tbl']/tbody/tr/td[4]/a")
    amountElements = fsscTest.dr.get_elements("xpath->//table[@id='tbl']/tbody/tr/td[6]")
    dateElements = fsscTest.dr.get_elements("xpath->//table[@id='tbl']/tbody/tr/td[10]")
    stateElements = fsscTest.dr.get_elements("xpath->//table[@id='tbl']/tbody/tr/td[11]")
    nodeElements = fsscTest.dr.get_elements("xpath->//table[@id='tbl']/tbody/tr/td[12]")
    for num,amount,date,state,node in zip(numElements,amountElements,dateElements,stateElements,nodeElements):
        record = [num.text,amount.text,date.text,state.text,node.text]
        print(record)
        if record in recordList:
            continue
        else:
            recordList.append(record)
    #给单据输入数据
    datainfo.createFile("travelTest\\allTravelBillRecord.xls", ["allBill"], [recordList])
    #fsscTest.dr.quit()