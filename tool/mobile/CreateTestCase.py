# -*- coding:utf-8 -*-
__author__ = '朱尧'
import time
from public.MobileScript import mobileDataInfo
import os


class CaseTestClass(object):
    TESTCASETEMPLATE = """
# -*- coding=UTF-8 -*-
# Author: zhuyao
#   Date: {0}
# Modify the record:
from public.MobileScript.MobilePage import MobilePage
from public.common import mytest
from config import globalparam
import unittest
from public.pages.billTestData import BillTestData


class test_{1}(mytest.MyMobileTest):
    \"\"\"测试单据-{2}-{3}\"\"\""""
    TESTCASETEMPLATE2 = """
    @unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
    def test_{0}_{5}(self):
        \"\"\"测试单据-{2}-{3}-{5}\"\"\"
        # 准备测试数据
        bill_name = "{2}"
        fill_person = "{3}"
        approval_model = "{4}"
        test_case_file = "{1}\\\\{2}.xls"
        # 初始化测试对象
        fssc_test = MobilePage(self.dr, bill_name)
        test_case_data = BillTestData.instance(test_case_file, 1)
        # 打开系统
        fssc_test.openSystem_Mob(globalparam.mobile_sys_address)
        fssc_test.login_Mob(fill_person)
        fssc_test.intoFillBillPage()
        fssc_test.getBillNum()
        fssc_test.typeInputBillValue(test_case_data.billInputData)
        fssc_test.saveBill()
        verify_result = fssc_test.verifyBillValue(test_case_data.billInputData)
        self.assertFalse(verify_result, fssc_test.wrong_data)
        next_approve = fssc_test.submissionBill()
        fssc_test.logoutSystem_Mob(1)
        if approval_model == "Auto":
            while next_approve:
                next_approve = fssc_test.handleBillAuto(next_approve, test_case_data.billInputData)
"""

    def __init__(self, data_file):
        self.billList = mobileDataInfo.getAllDataList(data_file, "bill")
        self.billDataDict = {}

    def getUNm(self):
        inputValues = mobileDataInfo.getColumnToList("{}/{}.xls".format(self.billDataDict["billGroup"],
                                                                        self.billDataDict["billName"]),
                                                     "billData",
                                                     "inputValue")
        for value in inputValues:
            if isinstance(value, str) and "&" in value:
                return value.split("&").__len__()
        return 1

    def setTemplateStr(self):
        unm = self.getUNm()
        templatestr = self.TESTCASETEMPLATE.format(self.billDataDict["timeStr"],
                                                   self.billDataDict["billCode"],
                                                   self.billDataDict["billGroup"],
                                                   self.billDataDict["billName"])
        for i in range(unm):
            templatestr += self.TESTCASETEMPLATE2.format(self.billDataDict["billCode"],
                                                         self.billDataDict["billGroup"],
                                                         self.billDataDict["billName"],
                                                         self.billDataDict["fillPerson"],
                                                         self.billDataDict["approvalModel"],
                                                         i + 1)

        return templatestr

    def run(self):
        # 将billList的数据提取出来
        for bill_data in self.billList:
            if bill_data[0] == "billGroup":
                pass
            elif bill_data[0] != "AutoTestGroup" and bill_data[3] != "No":
                # 准备数据
                self.billDataDict["timeStr"] = time.strftime("%Y-%m-%d_%H_%M_%S")
                self.billDataDict["billGroup"] = bill_data[0]
                self.billDataDict["billName"] = bill_data[1]
                self.billDataDict["billCode"] = bill_data[2]
                self.billDataDict["fillPerson"] = bill_data[4]
                self.billDataDict["approvalModel"] = bill_data[5]
                # 创建
                self.createTestCase(self.setTemplateStr(), self.setFilePath())

    def setFilePath(self):
        billBroupDir = os.path.join(os.path.abspath('../..'), 'testcase', self.billDataDict["billGroup"].lower())
        # 使用billCode作为文件名称
        billFilePath = os.path.join(billBroupDir, "test_" + self.billDataDict["billCode"] + ".py")
        if os.path.exists(billBroupDir) is False:
            os.makedirs(billBroupDir)
        self.createTestCase("", os.path.join(billBroupDir, "__init__.py"))
        return billFilePath

    @classmethod
    def createTestCase(cls, templateStr, filePath):
        # if os.path.exists(filePath):
        #     if templateStr != "":
        #         print("测试用例已存在: %s" % filePath)
        # else:
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(templateStr.strip())
        if templateStr != "":
            print("测试用例已创建: %s" % filePath)


if __name__ == '__main__':
    a = CaseTestClass("allBaseData.xls")
    a.run()