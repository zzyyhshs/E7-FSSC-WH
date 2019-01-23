# coding=UTF-8
# Author: cuichang
#   Date: 2018-08-14_17_48_45
# Modify the record:

from selenium.webdriver.support.select import Select
from public.common.basepage import Page
from public.pages.MyMenu.NewTaskListConfig import NewTaskListConfig
from time import sleep


class NewTaskList(Page):
    def openTaskByNum(self, billNum):
        self.intoModular()
        self.infoPrint("待办任务模块搜索单据：" + billNum)
        self.switchToIframeNo()
        # 高级查询
        self.clickShow_Text()
        # 输入编号
        self.inputFormno(billNum)
        # 查询
        self.clickSearchcx()
        # 点击编码打开单据
        self.click("xpath->//a[text()='" + billNum + "']")
        # self.dr.click_text(billNum)
        self.switch_to_iframe_out()
        sleep(3)

    def intoModular(self):
        self.intoModularByPath("我的菜单-待办任务", "home.pathGo('flow/newTaskList.jsp?")
        sleep(3)

    def clickLink_A1(self):  # 点击元素--待办任务
        self.click(NewTaskListConfig.link_a1)
        sleep(1)

    def clickLink_A2(self):  # 点击元素--抄送任务
        self.click(NewTaskListConfig.link_a2)
        sleep(1)

    def clickShow_Text(self):  # 点击元素--高级查询
        self.click(NewTaskListConfig.show_text)
        sleep(1)

    def slectTaskstatus(self, value):  # 选择元素--任务状态
        taskStatus = self.dr.get_element(NewTaskListConfig.taskStatus)
        Select(taskStatus).select_by_value(value)
        sleep(1)

    def inputBillbegint(self, value):  # 选择元素--起始创建时间
        self.dateInput(NewTaskListConfig.billBeginT, "起始创建时间", value)
        sleep(1)

    def inputBillendt(self, value):  # 选择元素--结束创建时间
        self.dateInput(NewTaskListConfig.billEndT, "结束创建时间", value)
        sleep(1)

    def inputFormno(self, value):  # 选择元素--单据编号
        self.typeInput(NewTaskListConfig.formNo, "单据编号", value)
        sleep(1)

    def inputForminput(self, value):  # 选择元素--单据名称
        self.selectInput(NewTaskListConfig.formInput, "单据名称", value)
        sleep(1)

    def inputDim(self, value):  # 选择元素--预算科目
        self.selectInput(NewTaskListConfig.dim, "预算科目", value)
        sleep(1)

    def inputApplicant(self, value):  # 选择元素--申请人
        self.typeInput(NewTaskListConfig.applicant, "申请人", value)
        sleep(1)

    def inputBilltitle(self, value):  # 选择元素--申请标题
        self.typeInput(NewTaskListConfig.billtitle, "申请标题", value)
        sleep(1)

    def inputDeptselectorname(self, value):  # 选择元素--经办部门
        self.selectInput(NewTaskListConfig.deptSelectorName, "经办部门", value)
        sleep(1)

    def inputBeginm(self, value):  # 选择元素--最小单据金额
        self.typeInput(NewTaskListConfig.beginM, "最小单据金额", value)
        sleep(1)

    def inputEndm(self, value):  # 选择元素--最大单据金额
        self.typeInput(NewTaskListConfig.endM, "最大单据金额", value)
        sleep(1)

    def slectApprovaltype(self, value):  # 选择元素--审批类型
        approvalType = self.dr.get_element(NewTaskListConfig.approvalType)
        Select(approvalType).select_by_value(value)
        sleep(1)

    def slectFormstatus(self, value):  # 选择元素--单据状态
        formStatus = self.dr.get_element(NewTaskListConfig.formStatus)
        Select(formStatus).select_by_value(value)
        sleep(1)

    def inputCompanycode(self, value):  # 选择元素--核算公式
        self.selectInput(NewTaskListConfig.companyCode, "核算公式", value)
        sleep(1)

    def inputActivityname(self, value):  # 选择元素--流程环节
        self.typeInput(NewTaskListConfig.activityName, "流程环节", value)
        sleep(1)

    def clickSearchcx(self):  # 点击元素--查询
        self.click(NewTaskListConfig.searchCX)
        sleep(1)

    def clickBatch_Approval(self):  # 点击元素--批量审批
        self.click(NewTaskListConfig.batch_approval)
        sleep(1)

    def clickBatch_Print(self):  # 点击元素--批量打印
        self.click(NewTaskListConfig.batch_print)
        sleep(1)

    def clickReset_Search(self):  # 点击元素--重置
        self.click(NewTaskListConfig.reset_search)
        sleep(1)


from config import globalparam
from autoTestFrame.pyselenium import PySelenium

if __name__ == '__main__':
    dr = PySelenium("chrome")
    sleep(4)
    dr.max_window()
    fsscTest = NewTaskList(dr)
    fsscTest.openSystem(globalparam.system_address)
    fsscTest.loginSystem("autotest001", "1")
    fsscTest.openTaskByNum("JKDYYB-180813-000176")
