# -*- coding:utf-8 -*-
import time
from public.common import datainfo
import os


class CaseTestClass(object):
    TESTCASETEMPLATE = """
# coding=UTF-8
# Author: cuichang
#   Date: {0}
# Modify the record:
from public.common import mytest
from public.pages import SubmitToBillPage
from time import strftime
from config import globalparam
import unittest
from public.common import publicfunction
from public.pages.billTestData import BillTestData


class test_{1}(mytest.MyTest):
    \"\"\"测试单据-{2}-{3}\"\"\"
    @unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
    def test_BXDW_01(self):
        \"\"\"测试单据-{2}-{3}_{5}模式\"\"\"
        #初始化测试对象
        fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
        #准备测试数据
        billName = "{3}"
        fillPerson = "{4}"
        approvalModel = "{5}"
        testCaseFile = "{2}\\\\{3}.xls"
        testCaseData = BillTestData(testCaseFile)
        #打开系统
        fsscTest.openSystem(globalparam.system_address)
        fsscTest.login(fillPerson)
        fsscTest.intoFillBillPage(billName)
        billNum = fsscTest.getBillNum()
        publicfunction.get_img(self.dr,billNum+"_"+strftime('%Y-%m-%d_%H_%M_%S')+".jpg")
        fsscTest.typeInputBillValue(billNum,testCaseData)
        publicfunction.get_img(self.dr,billNum+"_"+strftime('%Y-%m-%d_%H_%M_%S')+".jpg")
        fsscTest.saveBill(billNum)
        fsscTest.switchToContentIframe()
        verifyResult = fsscTest.verifyBillValue(billNum,testCaseData)
        fsscTest.switch_to_iframe_out()
        self.assertTrue(verifyResult["verifyResult"],verifyResult["verifyMsg"])
        publicfunction.get_img(self.dr,billNum+"_"+strftime('%Y-%m-%d_%H_%M_%S')+".jpg")
        nextApproveList = fsscTest.submissionBill(billNum)
        fsscTest.logoutSystem()
        if approvalModel == "Auto":
            fsscTest.handleBillAuto(nextApproveList, billNum, testCaseData)
        elif approvalModel == "Manual":
            fsscTest.handleBillManual(billNum, testCaseData)
        """

    def __init__(self, data_file):
        self.billList = datainfo.getAllDataList(data_file, "bill")
        self.billDataDict = {
            "timeStr": "",
            "billGroup": "",
            "billName": "",
            "billCode": "",
            "fillPerson": "",
            "approvalModel": "",
        }

    def setTemplateStr(self):
        templateStr = CaseTestClass.TESTCASETEMPLATE.format(self.billDataDict["timeStr"],
                                                            self.billDataDict["billCode"],
                                                            self.billDataDict["billGroup"],
                                                            self.billDataDict["billName"],
                                                            self.billDataDict["fillPerson"],
                                                            self.billDataDict["approvalModel"])
        return templateStr

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
                CaseTestClass.createTestCase(self.setTemplateStr(), self.setFilePath())

    def setFilePath(self):
        billBroupDir = os.path.join(os.path.abspath('..'), 'testcase', self.billDataDict["billGroup"].lower())
        # 使用billCode作为文件名称
        billFilePath = os.path.join(billBroupDir, "test_" + self.billDataDict["billCode"] + ".py")
        if os.path.exists(billBroupDir) is False:
            os.makedirs(billBroupDir)
        CaseTestClass.createTestCase("", os.path.join(billBroupDir, "__init__.py"))
        return billFilePath

    @classmethod
    def createTestCase(cls, templateStr, filePath):
        if os.path.exists(filePath):
            if templateStr != "":
                print("测试用例已存在: %s" % filePath)
        else:
            with open(filePath, "w", encoding="utf-8") as f:
                f.write(templateStr.strip())
            if templateStr != "":
                print("测试用例已创建: %s" % filePath)


if __name__ == '__main__':
    a = CaseTestClass("allBaseData.xls")
    a.run()