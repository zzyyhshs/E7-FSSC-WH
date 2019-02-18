__author__ = '崔畅'
from public.common import basepage
from autoTestFrame import pyselenium
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from public.common import datainfo
from config import globalparam
from time import sleep
import time
import os
from public.common.basePageConfig import BasePageConfig

def billInList(groupName,name,listBill):
    for bill in listBill:
        if groupName == bill[0] and name == bill[1]:
            return True
    return False

def billGroupInList(groupName,listBill):
    for bill in listBill:
        if groupName == bill[0]:
            return True
    return False

if __name__ == '__main__':
    #获取单据字段数据模板文件内容，字典，key = filed+itemName
    # billAllItemData = datainfo.getAllDataDict("allItemData_HT.xls","billData")
    billAllItemData = datainfo.getAllDataDict("allItemData_HT.xls","billData")
    billList = datainfo.getAllDataList("allBill_HT.xls","allBill")
    dr = pyselenium.PySelenium("ie")
    sleep(4)
    dr.max_window()
    fsscTest = basepage.Page(dr)
    fsscTest.openSystem(globalparam.system_address)
    fsscTest.loginSystem("admin","1")
    #fsscTest.intoModular("系统管理/单据定义/单据定义")
    fsscTest.infoPrint("系统管理/单据定义/单据定义")
    fromIndex =  "home.pathGo('designer/manageForm.jsf?" + str(time.time()) + "',this)"
    fsscTest.dr.js(fromIndex)
    sleep(5)
    #切换iframe
    fsscTest.switch_to_iframe(BasePageConfig.mainIframe)
    #获取所有单据组名称
    xpath = "xpath->//table[@class='rich-tree-node']/tbody/tr"
    BillGroupList  = fsscTest.dr.get_elements(xpath)
    useSelect =  "xpath->//select[@id='form2:dragFlag']"
    #循环所有单据组
    for i in range(0,len(BillGroupList)):
        billGroupName = BillGroupList[i].text
        if billGroupInList(billGroupName,billList) is False:  # 判断单据组是否在xls文件如果不在返回False
            continue
        billGroupDir = os.path.join(globalparam.data_path, billGroupName.lower())
        if os.path.exists(billGroupDir) is False:  # 判断文件是否存在
            os.makedirs(billGroupDir)  # 如果文件不存在则创建
        #点击单据组
        #fsscTest.dr.click_by_element(billGroup)
        fsscTest.click("xpath->//table[@class='rich-tree-node']["+str(i+1)+"]/tbody/tr")
        sleep(3)
        # 切换iframe
        fsscTest.switch_to_iframe(BasePageConfig.centerFrame)
        #切换到单据定义页签
        vouchers = "xpath->//td[@id='tab2_lbl']"
        fsscTest.click(vouchers)
        bills = fsscTest.dr.get_elements(xpath)
        sleep(5)
        for j in range(0, len(bills)):
            billName = bills[j].text
            if billInList(billGroupName,billName,billList) is False:
                continue
            billDataFilePath = os.path.join(billGroupName,billName+".xls")
            # bill = [billGroupName,billName]
            # allBill.append(bill)
            fsscTest.infoPrint("创建单据[{0}]数据文件[{1}]".format(billName,billDataFilePath))
            billNowData  = datainfo.getAllDataDict(billDataFilePath,"billData")  # 获取数据,如果该路径没有该文件则 得到{}
            #单据数据缓存{二维数组}
            datas = []
            dataHead = ["field","itemName","itemType","itemId","itemVarName","css","inputValue","verifyValue"]
            datas.append(dataHead)
            fsscTest.click("xpath->//table[@class='rich-tree-node'][" + str(j + 1) + "]/tbody/tr")
            sleep(4)
            #筛选已用字段
            selectElement = fsscTest.dr.get_element(useSelect)
            # Select(selectElement).select_by_index(0)
            # sleep(5)
            # Select(selectElement).select_by_index(1)  # 定位下拉框第一个元素
            # sleep(5)
            #获取每个区域根节点元素
            fieldList = fsscTest.dr.get_elements("xpath->//div[@class='rich-panelbar rich-panelbar-interior']")
            fieldTitleList = fsscTest.dr.get_elements("xpath->//div[@class='rich-panelbar rich-panelbar-interior']/div[1]")
            for k in range(0,len(fieldList)):
                field = fieldTitleList[k].text
                if field is None or field == "":
                    field = "主表区"
                fsscTest.click("xpath->//div[@class='rich-panelbar rich-panelbar-interior'][" + str(k + 1) + "]/div[2]")
                sleep(1)
                intemNameList = fieldList[k].find_elements(By.XPATH, "div/table/tbody/tr/td/table/tbody/tr/td[2]/div")  # 字段名
                intemTypeList = fieldList[k].find_elements(By.XPATH, "div/table/tbody/tr/td/table/tbody/tr/td[3]/div")  # 字段类型
                for l in range(0,len(intemNameList)):
                    # print("\t\t"+intemNameList[l].text)
                    itemName = intemNameList[l].text
                    itemType = intemTypeList[l].text
                    #如何当前已包含该字段，这加入该字段，如果没有取全量字段的值，如果没有现场组装值
                    key = field+itemName
                    if key in billNowData.keys() :
                        #考虑基础数据文件更新后，需要更新单据数据文件场景，替换"field","itemName","itemType","itemId","itemVarName","css"
                        try:
                            temp = billAllItemData[key]
                        except Exception as ret:
                            print(ret)
                        temp[6] = billNowData[key][6]
                        temp[7] = billNowData[key][7]
                        datas.append(temp)
                    elif key in billAllItemData.keys():
                        datas.append(billAllItemData[key])
                    else:
                        if itemType == "单行文本型" :
                            itemType = "input" #也可能是date，pop
                        elif itemType == "多行文本":
                            itemType = "textarea"
                        elif itemType == "货币型":#数据校验时，货币型数据特殊处理
                            itemType = "currency"
                        elif itemType == "下拉型":
                            itemType = "select"
                        else:
                            itemType = ""
                        item = list()
                        item.append(field)
                        item.append(itemName)
                        item.append(itemType)
                        datas.append(item)
            actionList = list()
            actionList = datainfo.getAllDataList(billDataFilePath, "action")
            if len(actionList) == 0:
                actionList = [["serialNumber","user","action"],["1","张一","填单"],["2","张二","审批"]]
            datainfo.createFile(billDataFilePath,["billData","action"],[datas,actionList])
            #break  #调试只循环一次
        sleep(1)
        fsscTest.switch_to_parent_iframe()
        #break  #调试只循环一次
    fsscTest.switch_to_iframe_out()
    fsscTest.dr.quit()
