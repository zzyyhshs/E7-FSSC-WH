# -*- coding=UTF-8 -*-
# Author: zhuyao
#   Date: {0}
# Modify the record:
from public.MobileScript.MobilePage import MobilePage
from public.common import mytest
from config import globalparam
import unittest
from public.pages.billTestData import BillTestData


class test_1(mytest.MyMobileTest):
    """测试单据-{2}-{3}"""

    @unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
    def test_0_5(self):
        """测试单据-{2}-{3}-{5}"""
        # 初始化测试对象
        fsscTest = MobilePage(self.dr)
        # 准备测试数据
        billName = "1.2-zq费用报销单（无申请)"
        fillPerson = "测试一号"
        approvalModel = "Auto"
        testCaseFile = "zq费用报销组\\1.2-zq费用报销单（无申请).xls"
        testCaseData = BillTestData.instance(testCaseFile, 1)
        # 打开系统
        fsscTest.openSystem_Mob(globalparam.mobile_sys_address)
        fsscTest.login_Mob(fillPerson)
        fsscTest.intoFillBillPage(billName)
        fsscTest.getBillNum()
        fsscTest.typeInputBillValue(testCaseData.billInputData, billName)
        fsscTest.saveBill()
        verifyResult = fsscTest.verifyBillValue(testCaseData.billInputData)
        self.assertFalse(verifyResult, fsscTest.wrong_data)
        nextApprove = fsscTest.submissionBill(billName)
        fsscTest.logoutSystem_Mob(1)
        if approvalModel == "Auto":
            fsscTest.handleBillAuto(nextApprove, testCaseData.billInputData, billName)


if __name__ == '__main__':
    unittest.main