from public.common import basepage
from time import sleep
from public.common import datainfo
import datetime
import random
class TraverPage(basepage.Page):
    #打开单据填单页面
    allUserDict = datainfo.getAllUsers("allBaseData.xlsx", "user", "name")
    def inputHotel(self,num,nightCount):
        hasPassenger = True
        while True:
            self.switchToContentIframe()
            if num==1:
                self.click("xpath->//input[@itemvarname='hotelname'][1]")
            else:
                if hasPassenger:
                    self.click("xpath->//img[@areatype='hotel']")
                sleep(1)
                elements = self.dr.get_elements("xpath->//input[@itemvarname='hotelname']")
                elements[num-1].click()
            self.switch_to_iframe_out()
            self.switchToJdIframe()
            self.dr.element_wait("xpath->//input[@id='start-date']", 20)
            sleep(5)
            passenger = self.dr.get_element("id->passenger").get_attribute('value')
            self.infoPrint("出行人："+passenger)
            if passenger !="":
                break
            else:
                self.switch_to_iframe_out()
                self.click("xpath->//img[@id='jd_dialog_m_h_r']")
                hasPassenger = False
                sleep(2)
        dataTime = datetime.datetime.now()
        year = dataTime.year
        month = dataTime.month
        day = dataTime.day
        sleep(1)
        self.clearType("id->citySelect", "上海")
        sleep(2)
        self.clearType("id->start-date", str(year) + "-" + str(month) + "-" + str(day+num))
        sleep(1)
        self.clearType("id->end-date", str(year) + "-" + str(month) + "-" + str(day+num+nightCount))
        sleep(1)
        self.click("xpath->//div[contains(text(),'国内酒店查询')]")
        sleep(1)
        self.clearType("id->keywords","7天连锁酒店")
        sleep(1)
        self.click("xpath->//button[contains(text(),'查询酒店')]")
        sleep(1)
        try:
            self.dr.element_wait("xpath->//span[contains(text(),'查看详情')][1]", 20)
        except:
            self.click("xpath->//button[contains(text(),'查询酒店')]")
            self.dr.element_wait("xpath->//span[contains(text(),'查看详情')][1]", 20)
        sleep(1)
        self.click("xpath->//span[contains(text(),'查看详情')][1]")
        sleep(1)
        try:
            alert = self.dr.switch_to_alert()
            self.infoPrint(alert.text)
            alert.accept()
            sleep(2)
            self.click("xpath->//button[contains(text(),'查询酒店')]")
            self.dr.element_wait("xpath->//span[contains(text(),'查看详情')][1]", 20)
            sleep(1)
            self.click("xpath->//span[contains(text(),'查看详情')][1]")
            sleep(1)
        except:
            self.infoPrint("正常")
        #找寻公司统付的酒店，尝试一次
        try:
            self.dr.element_wait("xpath->//div[contains(text(),'公司统付')][1]", 20)
        except:
            self.click("xpath->//button[contains(text(),'查询酒店')]")
            self.dr.element_wait("xpath->//span[contains(text(),'查看详情')][1]", 20)
            sleep(1)
            self.click("xpath->//span[contains(text(),'查看详情')][1]")
            sleep(1)
            self.dr.element_wait("xpath->//div[contains(text(),'公司统付')][1]", 20)
        sleep(1)
        self.click("xpath->//div[contains(text(),'公司统付')][1]")
        sleep(1)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        self.dr.element_wait("xpath->//button[contains(text(),'预订')][1]", 30)
        sleep(1)
        self.click("xpath->//button[contains(text(),'预订')][1]")
        sleep(1)
        self.switch_to_iframe_out()

    def inputFlight(self,num,flightType,person):
        recordList = datainfo.getAllDataList("allFlightRecord.xls","allRecord")
        self.switchToContentIframe()
        if num == 1:
            self.click("xpath->//input[@itemvarname='flightno'][1]")
        else:
            self.click("xpath->//img[@areatype='flight']")
            sleep(1)
            elements = self.dr.get_elements("xpath->//input[@itemvarname='flightno']")
            elements[num-1].click()
        sleep(2)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        self.dr.element_wait("xpath->//input[@id='setInCity']", 30)
        sleep(5)
        setInCity = ""
        setOutCity = ""
        if flightType == 1:
            setInCity = "上海"
            setOutCity = "海口"
        elif flightType == 2:
            setInCity = "郑州"
            setOutCity = "沈阳"
        elif flightType == 3:
            setInCity = "长沙"
            setOutCity = "哈尔滨"
        self.dr.element_wait("xpath->//button[contains(text(),'查询机票')]", 30)
        self.clearType("id->setInCity",setInCity)
        sleep(1)
        self.clearType("id->setOutCity",setOutCity)
        sleep(1)
        self.click("xpath->//input[@placeholder='请选择出发日期']")
        sleep(1)
        self.dr.element_wait("xpath->//td[@class='day']",10)
        dayElements = self.dr.get_elements("xpath->//td[@class='day']")
        delayDay = random.randint(0, len(dayElements)-1)
        dataTime = datetime.datetime.now()
        year = dataTime.year
        month = dataTime.month
        day = dataTime.day
        dayChoose = int(dayElements[delayDay].text)
        dayElements[delayDay].click()
        if day > dayChoose:
            month+=1
        bookingTime = str(year) + "-" + str(month) + "-" + str(dayChoose)
        sleep(1)
        self.click("xpath->//button[contains(text(),'查询机票')]")
        self.dr.element_wait("xpath->//button[@class='select_btn'][1]", 60)
        sleep(1)
        self.click("xpath->//label[contains(text(),'显示所有航班')]")
        sleep(2)
        chooseButtons = self.dr.get_elements("xpath->//button[@class='select_btn']")
        sleep(1)
        #flightElements =self.dr.get_elements("xpath->//div[@class='flight_no']/span")
        print(len(chooseButtons))
        isFixed = False
        for chooseButton in chooseButtons:
            flight = chooseButton.get_attribute('data-flightno')
            record = [person, flight, bookingTime, str(flightType)]
            index = chooseButtons.index(chooseButton) + 1
            if record in recordList:
                continue
            else:
                recordList.append(record)
            sleep(1)
            self.dr.click_by_element(chooseButton)
            sleep(2)
            #//*[@id="flightList"]/div[1]/div[2]/div[2]/div[2]/button
            #//*[@id="flightList"]/div[3]/div[2]/div[2]/div[2]/button
            #//*[@id="flightList"]/div[1]/div[2]/div[2]/div[3]/div/strong
            #//*[@id="flightList"]/div[3]/div[2]/div[2]/div[3]/div/strong
            fixedElements = self.dr.get_elements("xpath->//div[@id='flightList']/div["+str(index)+"]/div[2]/div/div[2]/button")
            priceElements = self.dr.get_elements("xpath->//div[@id='flightList']/div["+str(index)+"]/div[2]/div/div[3]/div/strong")
            print(len(fixedElements))
            print(len(priceElements))
            for fixedElement,priceElement in zip(fixedElements,priceElements):
                price = float(priceElement.text)
                if flightType == 1 and 740<=price<=1440:
                    self.dr.click_by_element(fixedElement)
                    isFixed = True
                    break
                if flightType == 2 and price < 740:
                    self.dr.click_by_element(fixedElement)
                    isFixed = True
                    break
                if flightType == 3 and price > 1440:
                    self.dr.click_by_element(fixedElement)
                    isFixed = True
                    break
            if isFixed:
                break
        sleep(2)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        self.dr.element_wait("xpath->//button[contains(text(),'提交审批')][1]", 30)
        sleep(1)
        self.click("xpath->//button[contains(text(),'提交审批')][1]")
        sleep(5)
        self.switch_to_iframe_out()
        datainfo.createFile("allFlightRecord.xls",["allRecord"],[recordList])

    def inputTrain(self,num,seatType,person):
        recordList = datainfo.getAllDataList("allTrainRecord.xls","allRecord")
        self.switchToContentIframe()
        if num == 1:
            self.click("xpath->//input[@itemvarname='trainno'][1]")
        else:
            self.click("xpath->//img[@areatype='train']")
            sleep(1)
            elements = self.dr.get_elements("xpath->//input[@itemvarname='trainno']")
            elements[num-1].click()
        sleep(1)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        self.click("xpath->//input[@value='确认']")
        sleep(1)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        self.dr.element_wait("xpath->//input[@id='fromCity']", 30)
        self.clearType("id->fromCity", "长沙南")
        sleep(1)
        self.clearType("id->toCity","广州南")
        sleep(1)
        dataTime = datetime.datetime.now()
        year = dataTime.year
        month = dataTime.month
        day = dataTime.day
        bookingDate = str(year) + "-" + str(month) + "-" + str(day+num)
        self.clearType("xpath->//input[@name='startDate']",bookingDate)
        sleep(1)
        self.click("xpath->//div[contains(text(),'出发城市')]")
        sleep(1)
        self.click("xpath->//span[@id='start-search']")
        sleep(1)
        self.dr.element_wait("xpath->//span[@class='buy buynow'][1]", 60)
        self.click("xpath->//img[@src='/ie8/images/checkbox-unchecked.png']")
        sleep(1)
        buyNowElements = self.dr.get_elements("xpath->//span[@class='buy buynow']")
        print(len(buyNowElements))
        for element in buyNowElements:
            trainNo = element.get_attribute("trainno")
            seatTypeNow = element.get_attribute("seattype")
            record = [person,trainNo,bookingDate]
            if record in recordList:
                continue
            if seatTypeNow == seatType:
                self.dr.click_by_element(element)
                recordList.append(record)
                break
            sleep(0.1)
        sleep(1)
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        self.dr.element_wait("xpath->//span[contains(text(),'"+person+"')]",60)
        self.click("xpath->//span[contains(text(),'提交审批')]")
        sleep(5)
        self.switch_to_iframe_out()
        datainfo.createFile("allTrainRecord.xls", ["allRecord"], [recordList])
        self.switchToContentIframe()
        self.clearType("xpath->//input[@itemvarname='outstandardmemo' and @areatype='scroll_train_b']["+str(num)+"]","超标说明")
        sleep(2)
        self.switch_to_iframe_out()