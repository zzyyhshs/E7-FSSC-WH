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
        # 准备测试数据
        bill_name = "1.2-zq费用报销单（无申请)"
        fill_person = "测试一号"
        approval_model = "Auto"
        test_case_file = "zq费用报销组\\1.2-zq费用报销单（无申请).xls"
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


if __name__ == '__main__':
    unittest.main