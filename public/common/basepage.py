#coding=utf-8
__author__ = '崔畅'
from public.common.basePageConfig import BasePageConfig
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import re
from public.common import publicfunction
from time import strftime
import time
class Page(object):#所有页面类的基类
    """
    This is a base page class for Page Object.
    """
    def __init__(self, selenium_driver):#初始化driver
        self.dr = selenium_driver

    def openSystem(self,system_address):#打开系统
        """打开TSP系统首页"""
        # system_address: url路径
        self.infoPrint("打开系统：{0}".format(system_address))
        self.dr.open(system_address)
        #等待页面打开成功，如果打开不成功，尝试再打开一次
        try:
           self.dr.element_wait(BasePageConfig.LoginButton ,secs=10)
        except:
           self.dr.open(system_address)
        sleep(3)

    def loginSystem(self,userName,password):#登录系统
        self.infoPrint("使用用户[{0}]登陆系统：{0}".format(userName))
        self.inputUserName(userName)
        sleep(1)
        self.inputPassword(password)
        sleep(1)
        self.clickLoginButton()
        try:
            #等待用户名，确认登陆成功
            self.dr.element_wait(BasePageConfig.currentUser,secs=10)
        except:
            raise

    def intoModularByPath(self,modular,Path):
        self.infoPrint("进入模块"+modular)
        self.dr.js(Path + str(time.time()) + "',this)")

    def inputUserName(self,userName):#输入用户名
        self.typeInput(BasePageConfig.UserName, "用户名", userName)
    def inputPassword(self,password):#输入密码
        self.typeInput(BasePageConfig.UserPwd, "密码", password)
    def clickLoginButton(self):#
        self.click(BasePageConfig.LoginButton)

    def logoutSystem(self):#退出系统
        try:
            self.infoPrint("退出系统")
            #self.click("xpath->//a[@class=' c_fff']")
            sleep(1)
            self.click(BasePageConfig.logout)
            sleep(2)
            self.windowAssertEqual("是否退出平台系统？", "注销失败")
            sleep(1)
            self.dr.element_wait(BasePageConfig.LoginButton,secs=10)
        except:
            publicfunction.get_img(self.dr, strftime('%Y-%m-%d_%H_%M_%S') + "_退出系统操作.jpg")
            raise


    def typeInput(self,css,columnName,columnValue):#css,列名，列值
        self.infoPrint("输入[{0}],值：{1}".format(columnName,columnValue))
        if columnValue == "":
            self.dr.clear_type(css,"a")
            self.dr.get_element(css).send_keys(Keys.BACK_SPACE)
        else:
            self.dr.clear_type(css,str(columnValue))#输入数据

    def uploadfile(self,css,colunmName,columnValue):
        self.infoPrint("输入[{0}],值：{1}".format(colunmName,columnValue))
        # element =self.dr.get_element(css)
        # self.dr.driver.execute_script("arguments[0].scrollIntoView();", element)
        # sleep(1)
        if columnValue !="":
            self.dr.get_element(css).send_keys(columnValue)

    ###E7-单据输入下拉数据
    def selectInput(self,css,columnName,data):
        self.infoPrint("输入[{0}],值：{1}".format(columnName, data))
        # 点击
        self.click(css)
        # 输入
        self.dr.element_wait(BasePageConfig.searchInput,10)
        sleep(1)
        self.clearType(BasePageConfig.searchInput, data)
        # 查询
        sleep(1)
        self.click(BasePageConfig.searchSubmit)
        # 选中
        sleep(1)
        self.click("xpath->//span[contains(text(),'"+data+"')]")

    def dateInput(self,css,columnName,data):
        self.infoPrint("输入[{0}],值：{1}".format(columnName, data))
        # if "today" == data:
        #     self.infoPrint("输入当天日期：{0}")
        #     dataTime = datetime.datetime.now()
        #     year = dataTime.year
        #     month = dataTime.month
        #     day = dataTime.day
        #     data = str(year) + "-" + str(month) + "-" + str(day)
        #     self.infoPrint("输入当天日期：{0}".format(data))
        # 点击
        self.click(css)
        sleep(1)
        # 选中
        self.switch_to_iframe("xpath->//iframe[@id='__calendarIframe']")
        if data == "today":
            self.click("id->selectTodayButton")
            sleep(0.5)
        else:
            date = data.split("-")
            year = date[0]
            #去掉首部的0
            mouth = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date[1])
            day = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date[2])
            yearElement = self.dr.get_element("xpath->//select[@id='yearSelect']")
            Select(yearElement).select_by_value(year)
            sleep(0.5)
            mouthElement= self.dr.get_element("xpath->//select[@id='monthSelect']")
            Select(mouthElement).select_by_value(str(int(mouth)-1))
            sleep(0.5)
            self.click("xpath->//td[text()='"+str(int(day))+"']")
            sleep(0.5)
            self.click("id->sureButton")
            sleep(0.5)
        self.switch_to_parent_iframe()

    def popInput(self,css,columnName,data):
        #如果希望自动选择第一个单据，填入auto
        self.infoPrint("{0}选择关联单据：{1}".format(columnName, data))
        # 点击
        self.click(css)
        sleep(1)
        self.switch_to_iframe_out()
        self.dr.wait(10)
        sleep(5)
        self.switch_to_iframe(BasePageConfig.jdIframe)
        if data.lower() =="auto":
            self.infoPrint("自动关联选择第一条单据")
        else:
            self.clearType(BasePageConfig.searchText,data)
            sleep(1)
            self.click(BasePageConfig.searchButton)
            sleep(5)
        self.click(BasePageConfig.plusSign)
        sleep(1)
        self.click(BasePageConfig.allSelect)
        sleep(1)
        self.click(BasePageConfig.sureButton)
        sleep(1)
        self.switch_to_iframe_out()
        self.switchToContentIframe()

    def inputDataBase(self,idList,inputType,css,data):
        for columnId in idList:
            if data[columnId]!="":
                if inputType[columnId]=="input":#输入框
                    self.typeInput(css[columnId],columnId,data[columnId])
                elif inputType[columnId] == "textarea":  # 多行文本
                    self.typeInput(css[columnId], columnId, data[columnId])
                elif inputType[columnId]== "select":#单选
                    self.selectInput(css[columnId],columnId,data[columnId])
                elif inputType[columnId]== "currency":#货币型，跟input一样
                    self.typeInput(css[columnId], columnId, data[columnId])
                elif inputType[columnId] == "pop":
                    self.popInput(css[columnId],columnId,data[columnId])
                elif inputType[columnId] == "date":
                    self.dateInput(css[columnId],columnId,data[columnId])
                sleep(1)

    def getURL(self):
        """返回页面URL"""
        return self.dr.get_url()

    def getTitle(self):
        """返回该页面的title"""
        return self.dr.get_title()

    def getText(self,css):
        #返回当前元素的文本内容
        return self.dr.get_text(css)
    #-----------------------------------------------


    ###
    # #功能说明：E7系统进入任意模块方法
    # #参数说明：模块路径名称，连接符“/”，例如：商城商旅/我的订单
    # def intoModular(self,modularPath):
    #     areas = modularPath.split("/")
    #     self.infoPrint("进入系统模块：{0}".format(modularPath))
    #     parent = None
    #     elements = self.dr.get_elements(BasePageConfig.FirstMenuList)
    #     for element in elements:
    #         menuText = element.find_element(By.XPATH,"a/span").text#一级文本
    #         #self.infoPrint(menuText)
    #         if menuText == areas[0]:
    #             parent = element.find_element(By.XPATH,"div/ul")
    #             areas.remove(menuText)
    #             self.dr.move_to_element_by_element(element)
    #             #self.dr.click_by_element(element)
    #             self.infoPrint("找到顶级目录：{0}".format(areas[0]))
    #             break
    #         elif menuText == "更多":
    #             parent = element.find_element(By.XPATH,"div/ul")
    #             self.dr.move_to_element_by_element(element)
    #             #self.dr.click_by_element(element)
    #             self.infoPrint("找到顶级目录：{0}".format(areas[0]))
    #             break
    #     sleep(1)
    #     #遍历功能路径，每一级找到后点击一次，同时更新父子元素
    #     for i in range(0, len(areas)):
    #     #for area in areas:
    #         area =  areas[i]
    #         parents = parent.find_elements(By.XPATH, "li")
    #         for parent in parents:
    #             parentText = parent.find_element(By.XPATH, "a/span")
    #             if area == parentText.text:
    #                 self.infoPrint("找到模块路径：{0}".format(area))
    #                 self.dr.move_to_element_by_element(parentText)
    #                 self.dr.click_by_element(parentText)
    #                 if i+1 < len(areas):
    #                     parent = parent.find_element(By.XPATH, "div/ul")
    #                 sleep(2)
    #                 break
    #     sleep(3)

    #点击操作，规避IE浏览器直接点击无效的问题
    def click(self,css):
        self.infoPrint("点击元素[{0}]".format(css))
        if self.dr.Browser is "ie":
            self.dr.js_click(css)  #使用js操作点击操作
        else:
            self.dr.click(css)

    def clickIE(self,css):
        self.infoPrint("点击元素[{0}]".format(css))
        self.dr.js_click(css)

    def click_normal(self,css):
        self.infoPrint("点击元素[{0}]".format(css))
        self.dr.click(css)

    def switch_to_iframe(self, css: object) -> object:
        self.dr.switch_to_frame(css)

    def switch_to_iframe_out(self):
        self.dr.switch_to_frame_out()

    def switch_to_parent_iframe(self):
        self.dr.switch_to_parent_iframe()

    def switchMainIframe(self):
        self.switch_to_iframe(BasePageConfig.mainIframe)

    def switchToContentIframe(self):
        self.switch_to_iframe(BasePageConfig.mainIframe)
        sleep(1)
        self.switch_to_iframe(BasePageConfig.formContentIframe)
        sleep(1)

    def switchToIframeNo(self):
        self.switch_to_iframe(BasePageConfig.mainIframe)
        sleep(1)
        self.switch_to_iframe(BasePageConfig.iframeNo)
        sleep(1)

    def switchToJdIframe(self):
        self.switch_to_iframe(BasePageConfig.jdIframe)
        sleep(1)


    def clearType(self,css,value):
        self.dr.clear_type(css,value)

    def alertAccept(self):
        self.dr.accept_alert()

    def getAttribute(self,css,realAttribute):
        return self.dr.get_attribute(css,realAttribute)

    def getElement(self,css):
        return self.dr.get_element(css)

    def getElements(self,css):
        return self.dr.get_elements(css)

    def infoPrint(self,msg):
        self.dr.my_print(msg)

    """断言相等"""
    def assertionEqual(self,assert1,assert2,msg):
        try:
            assert assert1 == assert2
            self.infoPrint("Assertion test pass")
        except Exception as e:
            self.infoPrint(msg + str(e))
            raise

    """断言相等"""

    def assertionContain(self, assert1, assert2, msg):
        try:
            assert assert2 in assert1
            self.infoPrint("Assertion test pass")
        except Exception as e:
            self.infoPrint(msg + str(e))
            raise

    """弹框有断言：assert2，msg"""
    def windowAssertEqual(self,assert2,msg):
        self.switch_to_iframe(BasePageConfig.jdIframe)
        sleep(1)
        assert1 = self.getText(BasePageConfig.msgContentId)
        self.infoPrint("assert1："+assert1)
        self.assertionEqual(assert1,assert2,msg)
        sleep(1)
        self.click(BasePageConfig.sure)
        sleep(1)
        self.switch_to_iframe_out()

    """弹框有断言，assert1，2，msg"""
    def windowAssertContain(self,assert2,msg):
        self.switch_to_iframe(BasePageConfig.jdIframe)
        sleep(1)
        assert1 = self.getText(BasePageConfig.msgContentId)
        self.infoPrint("assert1：" + assert1)
        self.assertionContain(assert1, assert2, msg)
        sleep(1)
        self.click(BasePageConfig.sure)
        self.switch_to_iframe_out()

    """弹框无断言"""
    def windowAcceptNotAssert(self):
        self.switch_to_iframe(BasePageConfig.jdIframe)
        sleep(2)
        self.click(BasePageConfig.sure)
        self.switch_to_iframe_out()
        sleep(2)

    def windowCancelEqual(self,assert2,msg):
        self.switch_to_iframe(BasePageConfig.jdIframe)
        sleep(1)
        assert1 = self.getText(BasePageConfig.msgContentId)
        self.infoPrint("assert1：" + assert1)
        self.assertionEqual(assert1, assert2, msg)
        sleep(1)
        self.click(BasePageConfig.cancel)
        sleep(1)
        self.switch_to_iframe_out()

