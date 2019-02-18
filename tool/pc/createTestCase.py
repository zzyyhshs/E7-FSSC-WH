__author__ = '崔畅'
from public.common import datainfo
from time import strftime
import time
import os
def createTestCase(dataFile,scriptAuthor="cuichang"):
    """
    生成 .py文件 测试用例
    :param dataFile:
    :param scriptAuthor:
    :return:
    """
    billList = datainfo.getAllDataList(dataFile, "bill")
    createTime = strftime("%Y-%m-%d_%H_%M_%S")
    fileHeadInfo = "#coding=UTF-8\n" \
            "# Author: " + scriptAuthor + "\n" \
            "#   Date: " + createTime + "\n" \
            "# Modify the record:\n"
    fileHeadImport = "from public.common import mytest\n" \
                     "from public.pages import SubmitToBillPage\n" \
                     "from time import strftime\n" \
                     "from config import globalparam\n" \
                     "import unittest\n" \
                     "from public.common import publicfunction\n" \
                     "from public.pages.billTestData import BillTestData\n"
    for bill in billList:  # 如果bill[0] == "billGroup" or bill[3] == "No"则不创建用例
        if bill[0]=="billGroup":
            continue
        if bill[3] == "No":
            continue
        billBroupDir = os.path.join(os.path.abspath('../..'), 'testcase',bill[0].lower())
        #使用billCode作为文件名称
        billFilePath = os.path.join(billBroupDir,"test_"+bill[2]+".py")
        if os.path.exists(billBroupDir) is False:
            os.makedirs(billBroupDir)
            file = open(os.path.join(billBroupDir, "__init__.py"), 'w')
            file.close()
        if os.path.exists(billFilePath) is False:#如果用例文件不存在，则创建文件
            file = open(billFilePath,'w',encoding = 'utf-8')
            file.write(fileHeadInfo)
            file.write(fileHeadImport)
            #使用billCode作为类名
            file.write("class {0}(mytest.MyTest):\n".format("test_"+bill[2]))
            file.write("\t\"\"\"测试单据-"+bill[0]+"-"+bill[1]+"\"\"\"\n")
            file.write("\t@unittest.skipUnless(globalparam.usecase_run_mode >= 1, \"\")\n"
                       "\tdef test_{0}_01(self):\n".format(bill[2]))
            file.write("\t\t\"\"\"测试单据-"+bill[0]+"-"+bill[1]+"_"+bill[5]+"模式"+"\"\"\"\n"
                "\t\t#初始化测试对象\n"
                "\t\tfsscTest = SubmitToBillPage.SubmitToBillPage(self.dr)\n"
                "\t\t#准备测试数据\n"
              #  "\t\tbillGroup = \""+bill[0]+"\"\n"
                "\t\tbillName = \""+bill[1]+"\"\n"
                "\t\tfillPerson = \""+bill[4]+"\"\n"
                "\t\tapprovalModel = \""+bill[5]+"\"\n"
                "\t\ttestCaseFile = \""+bill[0]+"\\"+bill[1]+".xls\"\n"
                "\t\ttestCaseData = BillTestData(testCaseFile)\n"
                "\t\t#打开系统\n"
                "\t\tfsscTest.openSystem(globalparam.system_address)\n"
                "\t\tfsscTest.login(fillPerson)\n"
                "\t\tfsscTest.intoFillBillPage(billName)\n"
                "\t\tbillNum = fsscTest.getBillNum()\n"
                "\t\tpublicfunction.get_img(self.dr,billNum+\"_\"+strftime('%Y-%m-%d_%H_%M_%S')+\".jpg\")\n"
                "\t\tfsscTest.typeInputBillValue(billNum,testCaseData)\n"
                "\t\tpublicfunction.get_img(self.dr,billNum+\"_\"+strftime('%Y-%m-%d_%H_%M_%S')+\".jpg\")\n"
                "\t\tfsscTest.saveBill(billNum)\n"
                "\t\tfsscTest.switchToContentIframe()\n"
                "\t\tverifyResult = fsscTest.verifyBillValue(billNum,testCaseData)\n"
                "\t\tfsscTest.switch_to_iframe_out()\n"
                "\t\tself.assertTrue(verifyResult[\"verifyResult\"],verifyResult[\"verifyMsg\"])\n"
                "\t\tpublicfunction.get_img(self.dr,billNum+\"_\"+strftime('%Y-%m-%d_%H_%M_%S')+\".jpg\")\n"
                "\t\tnextApproveList = fsscTest.submissionBill(billNum)\n"
                "\t\tfsscTest.logoutSystem()\n"
                "\t\tif approvalModel == \"Auto\":\n"
                "\t\t\tfsscTest.handleBillAuto(nextApproveList, billNum, testCaseData)\n"
                "\t\telif approvalModel == \"Manual\":\n"
                "\t\t\tfsscTest.handleBillManual(billNum, testCaseData)\n")
            file.close()

if __name__ == '__main__':
    createTestCase("allBaseData.xls")
