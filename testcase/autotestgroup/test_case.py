from selenium import webdriver
from public.common import mytest
from public.pages import SubmitToBillPage
from time import strftime
from config import globalparam
import unittest
from public.common import publicfunction
from public.pages.billTestData import BillTestData
class test_case(mytest.MyTest):
	@unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
	def test_case_01(self):
		#初始化测试对象
		fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
		#准备测试数据
		billName = "8.03-报销单-无申请"
		fillPerson\
			= "填单用户001"
		approvalModel = "Auto"
		testCaseFile = "费用报销组（多币种）\8.03-报销单-无申请.xls"
		testCaseData = BillTestData(testCaseFile)
		#打开系统
		fsscTest.openSystem(globalparam.system_address)
		fsscTest.login(fillPerson)
		fsscTest.intoFillBillPage(billName)
		billNum = fsscTest.getBillNum()
		publicfunction.get_img(self.dr,billNum+"_"+strftime('%Y-%m-%d_%H_%M_%S')+".jpg")
		fsscTest.typeInputBillValue(testCaseData)
		publicfunction.get_img(self.dr, billNum + "_" + strftime('%Y-%m-%d_%H_%M_%S') + ".jpg")
		fsscTest.saveBill()
		fsscTest.clickBillSubmit()
		try:
			msg = fsscTest.windowGetText()
			if fsscTest.decContain(msg, "币种必须一致"):
				fsscTest.logoutSystem()
		except NosuchElement as e:
			fsscTest.switchToContentIframe()
			verifyResult = fsscTest.verifyBillValue(testCaseData)
			fsscTest.switch_to_iframe_out()
			self.assertTrue(verifyResult["verifyResult"],verifyResult["verifyMsg"])
			publicfunction.get_img(self.dr, billNum + "_" + strftime('%Y-%m-%d_%H_%M_%S') + ".jpg")
			nextApproveList = fsscTest.submissionBill()
			fsscTest.logoutSystem()
			if approvalModel == "Auto":
				fsscTest.handleBillAuto(nextApproveList, billNum, testCaseData)
			elif approvalModel == "Manual":
				fsscTest.handleBillManual(billNum, testCaseData)
# fsscTest.windowAssertContain("币种必须一致","币种一致")