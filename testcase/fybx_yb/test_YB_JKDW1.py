#coding=UTF-8
# Author: hsy
#   Date: 2018-08-10_17_10_52
# Modify the record:
from public.common import mytest
from public.pages import SubmitToBillPage
from time import strftime
from config import globalparam
import unittest
from public.common import publicfunction
from public.pages.billTestData import BillTestData
class test_YB_JKDW1(mytest.MyTest):
	"""测试单据-费用报销组（原币）-13.05-借款单-无申请"""
	@unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
	def test_YB_JKDW1_01(self):
		"""测试单据-费用报销组（原币）-13.05-借款单-无申请-本位币人民币"""
		#初始化测试对象
		fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
		#准备测试数据
		billName = "13.05-借款单-无申请"
		fillPerson = "填单用户001"
		approvalModel = "Auto"
		testCaseFile = "费用报销组（原币）\\13.05-借款单-无申请-01.xls"
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

	@unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
	def test_YB_JKDW1_02(self):
		"""测试单据-费用报销组（原币）-13.05-借款单-无申请-本位币美元"""
		# 初始化测试对象
		fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
		# 准备测试数据
		billName = "13.05-借款单-无申请"
		fillPerson = "填单用户007"
		approvalModel = "Auto"
		testCaseFile = "费用报销组（原币）\\13.05-借款单-无申请-02.xls"
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