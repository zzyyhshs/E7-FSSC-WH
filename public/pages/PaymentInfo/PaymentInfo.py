# coding=UTF-8
# Author: cuichang
#   Date: 2018-08-21_14_26_11
# Modify the record:
from time import sleep
from public.common.basepage import Page
from public.pages.PaymentInfo.PaymentInfoConfig import PaymentInfoConfig


class PaymentInfo(Page):
    def dispatchByBillNumber(self, billNumber, accountant):
        self.intoPaymentInfoManagement()
        self.switchToMainIframe()
        self.selectStatus("待派工")
        self.inputBillnumber(billNumber)
        self.clickQuery()
        self.chonseFirstPaymentInfo()
        self.clickDispatch()
        self.switch_to_iframe_out()
        self.switchToJdIframe()
        accountantName = ""
        # 如果没有传入派工会计名称，则自动派给第一个会计，并返回派工会计姓名
        accountantElements = self.dr.get_elements("xpath->//span[@unselectable='on' and contains(text(),'能力值')]")
        for accountantElement in accountantElements:
            accountantName = accountantElement.text
            end = accountantName.find("【")
            accountantName = accountantName[0:end]
            if accountant == "":
                self.infoPrint("单据{0}派工给：{1}".format(billNumber, accountantName))
                self.click("xpath->//span[@unselectable='on' and contains(text(),'" + accountantName + "')]")
                break
            elif accountantName == accountant:
                self.infoPrint("单据{0}派工给：{1}".format(billNumber, accountantName))
                self.click("xpath->//span[@unselectable='on' and contains(text(),'" + accountantName + "')]")
                break
        self.windowAssertEqual("派工成功", "派工失败")
        print(accountantName)

    def chonseFirstPaymentInfo(self):  # 在列表中选择第一个支付建议
        self.click("id->tbl_tr_0_cb")
        sleep(1)

    def intoPaymentInfoManagement(self):
        self.intoModularByPath("资金管理-资金任务管理", "home.pathGo('payment/paymentInfo.jsp?type=admin&")
        sleep(3)

    def intoPaymentInfoApproval(self):
        self.intoModularByPath("资金管理-资金审批", "home.pathGo('payment/paymentInfo.jsp?type=1&")
        sleep(3)

    def intoPaymentInfoPayment(self):
        self.intoModularByPath("资金管理-资金付款", "home.pathGo('payment/paymentInfo.jsp?type=2&")
        sleep(3)

    def selectStatus(self, value):  # 选择元素--审批状态
        if value == "":
            status = ""
        elif value == "待派工":
            status = "0"
        elif value == "待审批":
            status = "1"
        elif value == "待付款":
            status = "2"
        elif value == "付款中":
            status = "3"
        elif value == "付款成功":
            status = "4"
        elif value == "付款失败":
            status = "5"
        elif value == "已冻结":
            status = "6"
        elif value == "变更中":
            status = "7"
        elif value == "已退回":
            status = "8"
        elif value == "已作废":
            status = "9"
        elif value == "沟通中":
            status = "10"
        else:
            status = ""
        self.select(PaymentInfoConfig.status, "审批状态", status)
        sleep(1)

    def inputBillnumber(self, value):  # 选择元素--单据编号
        self.typeInput(PaymentInfoConfig.billNumber, "单据编号", value)
        sleep(1)

    def inputAccountingcompany(self, value):  # 选择元素--核算公司
        self.selectInput(PaymentInfoConfig.accountingCompany, "核算公司", value)
        sleep(1)

    def inputSettlementmethod(self, value):  # 选择元素--付款方式
        self.selectInput(PaymentInfoConfig.settlementMethod, "付款方式", value)
        sleep(1)

    def inputNeedpaymentdatebegin(self, value):  # 选择元素--开始日期
        self.dateInput(PaymentInfoConfig.needPaymentDateBegin, "开始日期", value)
        sleep(1)

    def inputNeedpaymentdateend(self, value):  # 选择元素--结束日期
        self.dateInput(PaymentInfoConfig.needPaymentDateEnd, "结束日期", value)
        sleep(1)

    def inputCompany(self, value):  # 选择元素--付款对象
        self.selectInput(PaymentInfoConfig.company, "付款对象", value)
        sleep(1)

    def inputPaymentcompany(self, value):  # 选择元素--付款公司
        self.selectInput(PaymentInfoConfig.paymentCompany, "付款公司", value)
        sleep(1)

    def clickQuery(self):  # 点击元素--查询
        self.click(PaymentInfoConfig.query)
        sleep(1)

    def clickReset(self):  # 点击元素--重置
        self.click(PaymentInfoConfig.reset)
        sleep(1)

    def clickChange(self):  # 点击元素--变更
        self.click(PaymentInfoConfig.change)
        sleep(1)

    def clickSplit(self):  # 点击元素--拆分
        self.click(PaymentInfoConfig.split)
        sleep(1)

    def clickChangeapprover(self):  # 点击元素--变更审批人
        self.click(PaymentInfoConfig.changeApprover)
        sleep(1)

    def clickChangesecondapprover(self):  # 点击元素--变更复审人
        self.click(PaymentInfoConfig.changeSecondApprover)
        sleep(1)

    def clickDispatch(self):  # 点击元素--派工
        self.click(PaymentInfoConfig.dispatch)
        sleep(1)

    def clickFreezing(self):  # 点击元素--冻结
        self.click(PaymentInfoConfig.freezing)
        sleep(1)

    def clickCommunicate(self):  # 点击元素--沟通
        self.click(PaymentInfoConfig.communicate)
        sleep(1)

    def clickImport(self):  # 点击元素--导入
        self.click(PaymentInfoConfig.importResult)
        sleep(1)

    def clickExport(self):  # 点击元素--导出
        self.click(PaymentInfoConfig.export)
        sleep(1)

    def clickPass(self):  # 点击元素--通过
        self.click(PaymentInfoConfig.passResult)
        sleep(1)

    def clickVouchercreate(self):  # 点击元素--制证
        self.click(PaymentInfoConfig.vouchercreate)
        sleep(1)

    def clickVoucherview(self):  # 点击元素--凭证预览
        self.click(PaymentInfoConfig.voucherview)
        sleep(1)

    def clickPay(self):  # 点击元素--付款
        self.click(PaymentInfoConfig.pay)
        sleep(1)

    def clickBack(self):  # 点击元素--退回
        self.click(PaymentInfoConfig.back)
        sleep(1)


from config import globalparam
from autoTestFrame.pyselenium import PySelenium

if __name__ == '__main__':
    dr = PySelenium("chrome")
    sleep(4)
    dr.max_window()
    fsscTest = PaymentInfo(dr)
    fsscTest.openSystem(globalparam.system_address)
    fsscTest.loginSystem("autotest025", "1")
    fsscTest.intoPaymentInfoManagement()
    sleep(3)
    fsscTest.dispatchByBillNumber("JKDYYB-180820-000044", "")
# fsscTest.switchToMainIframe()
# fsscTest.slectStatus("待付款")
# fsscTest.clickQuery()
# fsscTest.intoPaymentInfoApproval()
# sleep(3)
# fsscTest.intoPaymentInfoPayment()
