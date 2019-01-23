#coding=UTF-8
# Author: hsy
#   Date: 2018-08-06_15_45_52
# Modify the record:
from public.common import mytest
from public.pages import SubmitToBillPage
from time import strftime
from config import globalparam
import unittest
from public.common import publicfunction
from public.pages.billTestData import BillTestData
class test_DBZ_HKD1(mytest.MyTest):
	"""测试单据-费用报销组（多币种）-8.07-还款单"""
	@unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
	def test_DBZ_HKD1_01(self):
		"""测试单据-AutoTestGroup-8.07-还款单-本位币人民币-币种一致"""
		#初始化测试对象
		fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
		#准备测试数据
		billName = "8.07-还款单"
		fillPerson = "填单用户001"
		approvalModel = "Auto"
		testCaseFile = "费用报销组（多币种）\\8.07-还款单-01.xls"
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
	def test_DBZ_BXDW1_02(self):
		"""测试单据-费用报销组（多币种）-8.03-报销单-无申请-本位币为人民币-币种不一致"""
		# 初始化测试对象
		fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
		# 准备测试数据
		billName = "8.03-报销单-无申请"
		fillPerson = "填单用户001"
		approvalModel = "Auto"
		testCaseFile = "费用报销组（多币种）\\8.03-报销单-无申请-02.xls"
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
		fsscTest.clickBillSubmit()
		fsscTest.windowAssertContain("币种必须一致", "币种未校验成功")
		fsscTest.logoutSystem()

	@unittest.skipUnless(globalparam.usecase_run_mode >= 1, "")
	def test_DBZ_HKD1_03(self):
		"""测试单据-AutoTestGroup-8.07-还款单-本位币美元-币种一致"""
		#初始化测试对象
		fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
		#准备测试数据
		billName = "8.07-还款单"
		fillPerson = "填单用户007"
		approvalModel = "Auto"
		testCaseFile = "费用报销组（多币种）\\8.07-还款单-03.xls"
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
	def test_DBZ_BXDW1_04(self):
		"""测试单据-费用报销组（多币种）-8.03-报销单-无申请-本位币为美元-币种不一致"""
		# 初始化测试对象
		fsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)
		# 准备测试数据
		billName = "8.03-报销单-无申请"
		fillPerson = "填单用户007"
		approvalModel = "Auto"
		testCaseFile = "费用报销组（多币种）\\8.03-报销单-无申请-04.xls"
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
		fsscTest.clickBillSubmit()
		fsscTest.windowAssertContain("币种必须一致", "币种未校验成功")
		fsscTest.logoutSystem()