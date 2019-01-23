#、coding=UTF-8
# Author: hsy
#   Date: 2018-08-06_13_16_52
# Modify the record:
from public.common import mytest
from public.pages import SubmitToBillPage
from time import strftime
from config import globalparam
import unittest
from public.common import publicfunction
from public.pages.billTestData import BillTestData
import os
class test_FYBX(mytest.MyTest):
	"""测试单据-费用报销内置组"""
	@unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
	def test_FYBX_01(self):
		"""测试单据-费用报销内置组-自动填单模式"""
		fybx_path = os.path.join(globalparam.data_path,'autotestgroup')
		#初始化测试对象
		fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
		for parent,dirnames,filenames in os.walk(fybx_path):
			for file in filenames:
				testCaseFile = os.path.join('autotestgroup\\',file)
				fillPerson = "填单用户001"
				approvalModel = "Auto"
				billName = os.path.splitext(str(file))[0]
				testCaseData = BillTestData(testCaseFile)
				# 打开系统
				fsscTest.openSystem(globalparam.system_address)
				fsscTest.login(fillPerson)
				fsscTest.intoFillBillPage(billName)
				billNum = fsscTest.getBillNum()
				publicfunction.get_img(self.dr, billNum + "_" + strftime('%Y-%m-%d_%H_%M_%S') + ".jpg")
				fsscTest.typeInputBillValue(testCaseData)
				publicfunction.get_img(self.dr, billNum + "_" + strftime('%Y-%m-%d_%H_%M_%S') + ".jpg")
				fsscTest.saveBill()
				fsscTest.switchToContentIframe()
				verifyResult = fsscTest.verifyBillValue(testCaseData)
				fsscTest.switch_to_iframe_out()
				self.assertTrue(verifyResult["verifyResult"], verifyResult["verifyMsg"])
				publicfunction.get_img(self.dr, billNum + "_" + strftime('%Y-%m-%d_%H_%M_%S') + ".jpg")
				nextApproveList = fsscTest.submissionBill()
				fsscTest.logoutSystem()
				if approvalModel == "Auto":
					fsscTest.handleBillAuto(nextApproveList, billNum, testCaseData)
				elif approvalModel == "Manual":
					fsscTest.handleBillManual(billNum, testCaseData)
