__author__ = 'Muyinghui'

#from public.common import datainfo
from autoTestFrame import pyselenium
from public.common import basepage
from time import sleep
import time
from config import globalparam
from public.common.basePageConfig import BasePageConfig
#from selenium import webdriver
from  selenium.webdriver.support.select import Select
from public.MobileScript import mobileDataInfo
import os

 #切割区域文本信息文字
def TextCutexx(Cute_text):
     #切割文本信息字段
     drop_text = Cute_text[0:-4]
     #如果是切割信息是表,就拼接区
     if "表" in drop_text:
         drop_text = drop_text[0:-1] + "区"
     return drop_text

#获取数据方法
# if __name__ == '__main__':
#          bill_grounp = "zq费用报销组"
#          bill_name = "1.1-zq日常费用申请单_(FYSQD)"
def ObtainData(bill_grounp,bill_name):
        # bill_dict = {
        #     "主表区-字段1": [0,1],
        #     "主表区-字段2": [1,1],
        # }

        # #获取单据所有字段文件数据列表
        # billItemData = datainfo.getAllDataDict("allItemData_HT.xls","billData")
        # #定义列表对象
        # billList = datainfo.getAllDataList("allBill_HT.xls","allBill")

    #定义数据字段数据列表
    field_Data = {}
    #定义对象
    dr = pyselenium.PySelenium("ie")
    sleep(2)
    #浏览器最大化
    dr.max_window()
    #所有页面的基类
    MTestPage = basepage.Page(dr)
    sleep(2)
    #输入测试环境地址
    MTestPage.openSystem(globalparam.system_address)
    #输入账号密码
    MTestPage.loginSystem("admin", "1")

    ####************************************************************************************
    #进入系统  移动填单字段配置
    MTestPage.infoPrint("系统管理/单据定义/移动填单字段配置")
    #移动填单字段配置xpath
    fromIndex ="home.pathGo('form/mobileFieldConfig.jsf?" + str(time.time()) + "',this)"
    MTestPage.dr.js(fromIndex)
    sleep(2)
    # switch_to_iframe切换表单
    MTestPage.switch_to_iframe(BasePageConfig.mainIframe)
    #点击单据组"可以传任何一个单据组"
    useSelect = "xpath->//div[@title='{}']/img".format(bill_grounp)
    # BXZ = MTestPage.getElement(useSelect)
    # BXZ.click()
    #*****
    MTestPage.clickIE(useSelect)
    sleep(1)
    #选择表单
    DSingle = "xpath->//div[@title='{}']".format(bill_name)
    # SQD =MTestPage.getElement(DSingle)
    # SQD.click()
    MTestPage.clickIE(DSingle)
    sleep(1)
    #**判断  是否启用移动填单是否勾选  是,生成xls. 否,不生成.
    #获取勾选框xpath
    mobileBill = "xpath->//input[@id='mobileBill']"
    mob = MTestPage.getElement(mobileBill)

    if mob.is_selected():
        #获取下拉框区域xpath
        XLK = "xpath->//select[@id='billfieldtype']"
        xlk1 =MTestPage.getElement(XLK)
        a = Select(xlk1)
        #根据option索引来定位下拉选项主表区/明细区
        # a.select_by_index(0)
        #循环下拉区域
        i = 0
        while i < len(a.options):
            a.select_by_index(i)
            #**判断是否启动移动区域,勾选生成文件,否,获取移动区域xpath
            mobileBillFieldCheck = "xpath->//input[@id='mobileBillFieldCheck']"
            mobFC = MTestPage.getElement(mobileBillFieldCheck)
            #判断区域字段是否可见
            if mobFC.is_selected():
                #***获取下拉文本信息
                drop_text = a.options[i].text####
                #对文本信息文字切割    引用丰富TextCutexx
                Cute_text =TextCutexx(drop_text)
                     # So = "xpath->//input[@id='itemdisplay']"
                     # ZDso = MTestPage.getElement(So)
                     #获取移动审批所有字段的元素xpath,返回一个字段元素列表
                     # ZdName = "xpath->//tr[@id='hiddenTr']"
                     # ZD1 = MTestPage.getElements(ZdName)
                Ziduan_Xpath= "xpath->//tr[@id='hiddenTr'and @name='cloneTr']"
                Zid_elementlist = MTestPage.getElements(Ziduan_Xpath)

                #循环遍历区域字段元素
                for ZD_element in Zid_elementlist:
                    #获取字段名称   #*****通过字段元素定位xpath
                    ZidName = ZD_element.find_element_by_xpath("td[2]/input").get_attribute("value")
                    #通过元素获取子元素
                    Zi_element = ZD_element.find_element_by_xpath("td[4]/input")

                    #判断判断填单字段元素(hiddenTr)是否可见
                    if Zi_element.is_selected():
                        inputShow = 1
                    else:
                        inputShow = 0
                    #拼接key *********下拉文本信息,字段名称
                    Zid_key = "{}-{}".format(Cute_text,ZidName)
                    #打印字段键
                    print(Zid_key)
                    field_Data[Zid_key] = [inputShow]
            i += 1

    #默认恢复页面,再进入移动审批菜单
    #MTestPage.switch_to.default_content()
    MTestPage.dr.driver.switch_to.default_content()

    # ### """获取移动审批字段"""********************************************************************
    # 移动填单字段配置xpath
    fromIndex = "home.pathGo('form/mobileApprovalConfig.jsf?" + str(time.time()) + "',this)"
    MTestPage.dr.js(fromIndex)
    sleep(2)
    # switch_to_iframe切换表单
    MTestPage.switch_to_iframe(BasePageConfig.mainIframe)
    # 点击单据组
    useSelect = "xpath->//div[@title='{}']/img".format(bill_grounp)
    # BXZ = MTestPage.getElement(useSelect)
    # BXZ.click()
    #******点击元素
    MTestPage.click(useSelect)
    sleep(1)
    # 选择表单
    DSingle = "xpath->//div[@title='{}']".format(bill_name)
    # SQD = MTestPage.getElement(DSingle)
    # SQD.click()
    #点击元素
    MTestPage.click(DSingle)
    sleep(1)
    # **判断  是否启用移动填单是否勾选  是,生成xls. 否,不生成.
    # 获取勾选框xpath
    mobileBill = "xpath->//input[@id='mobileBill']"
    mob = MTestPage.getElement(mobileBill)

    if mob.is_selected():
        # 获取下拉框区域xpath
        XLK = "xpath->//select[@id='billfieldtype']"
        xlk1 = MTestPage.getElement(XLK)
        a = Select(xlk1)
        # 根据option索引来定位下拉选项主表区/明细区
        # a.select_by_index(0)
        # 循环下拉区域
        i = 0
        while i < len(a.options):
            a.select_by_index(i)
            # **判断是否启动移动区域,勾选生成文件,否,获取移动区域xpath
            mobileBillFieldCheck = "xpath->//input[@id='mobileBillFieldCheck']"
            mobFC = MTestPage.getElement(mobileBillFieldCheck)
            # 判断区域字段是否可见
            if mobFC.is_selected():
                # ***获取下拉文本信息
                drop_text = a.options[i].text  ####
                # 对文本信息文字切割    引用方法extCutexx
                Cute_text = TextCutexx(drop_text)
                #获取所有字段xpath
                Ziduan_Xpath = "xpath->//tr[@id='hiddenTr'and @name='cloneTr']"
                #获取字段元素
                Zid_elementlist = MTestPage.getElements(Ziduan_Xpath)

                # 循环遍历区域字段元素
                for ZD_element in Zid_elementlist:
                    # 获取字段名称   #*****通过字段元素定位xpath
                    ZidName = ZD_element.find_element_by_xpath("td[3]/input").get_attribute("value")
                    # 通过元素获取子元素
                    Zi_element = ZD_element.find_element_by_xpath("td[4]/input")

                    # 判断判断填单字段元素()是否显示
                    if Zi_element.is_selected():
                        inputShow = 1
                    else:
                        inputShow = 0

                    # 拼接key *********下拉文本信息(区域),字段名称
                    Zid_key = "{}-{}".format(Cute_text, ZidName)
                    # 打印字段键
                    print(Zid_key)
                    #字段数据的key*********
                    field_Data[Zid_key].append(inputShow)
            i += 1
    #关闭浏览器
    MTestPage.dr.driver.quit()
    #*******返回字段数据
    return field_Data

    #***创建表单Excel文件**************************************************************************
def CreatFormFile(fieldData,bill_name,bill_grounp):
    #单据名称和编码从分隔符split***********split("_", 1)[0]以下划线为分割两部分
    bill_name = bill_name.split("_", 1)[0]
    # bill_name = bill_name.split()[0]
    #生成数据列表
    dataHeadlist = [["field", "itemName", "itemType", "itemId", "itemVarName", "css","inputShow", "inputValue", "verifyShow","verifyValue"]]
    #读取allItemData.xls文件
    Read_ExceFile = mobileDataInfo.getAllDataDict("allItemData.xls","billData")
    for field in fieldData:
        #获取第一张表字段的数据
        fieldinfo1 = Read_ExceFile[field]
        ##获取第二张表字段的数据
        fieldinfo2 = fieldData[field]
        #开始组装数据(dataHead_list生成的数据列表)Excel列表显示顺序
        dataHeadlist.append([fieldinfo1[0],fieldinfo1[1],fieldinfo1[2],fieldinfo1[3],fieldinfo1[4],fieldinfo1[5],
                             fieldinfo2[0],"",
                             fieldinfo2[1],""])
    #单据组/单据路径
    path = bill_grounp +"\\" + bill_name + ".xls"
    #存放路径
    file_path= os.path.join(globalparam.data_mobile_path,path)
    mobileDataInfo.createFile(file_path,["billData"],[dataHeadlist])
    #打印创建文件
    print("创建Excel文件:" + file_path)

if __name__ == '__main__':
    bill_grounp = "zq费用报销组"
    bill_name = "1.1-zq日常费用申请单_(FYSQD)"
    #获取数据方法ObtainData
    fieldData = ObtainData(bill_grounp,bill_name)
    #调用创建文件方法
    CreatFormFile(fieldData,bill_name,bill_grounp)























