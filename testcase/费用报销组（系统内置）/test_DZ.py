# coding=UTF-8
# Author: cuichang
#   Date: 2018-12-21_09_32_22
# Modify the record:
from public.common import mytest
from public.pages import SubmitToBillPage
from time import strftime
from config import globalparam
import unittest
from public.common import publicfunction
from public.pages.billTestData import BillTestData


class test_DZ(mytest.MyTest):
    """测试单据-费用报销组（系统内置）-1.2-日常费用申请单"""
    @unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
    def test_BXDW_01(self):
        """测试单据-费用报销组（系统内置）-1.2-日常费用申请单_Auto模式"""
        #初始化测试对象
        fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
        #准备测试数据
        billName = "1.2-日常费用申请单"
        fillPerson = "填单用户001"
        approvalModel = "Auto"
        testCaseFile = "费用报销组（系统内置）\\1.2-日常费用申请单.xls"
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