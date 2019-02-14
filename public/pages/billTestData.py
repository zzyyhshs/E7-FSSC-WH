import threading

from public.common import datainfo
from public.MobileScript import mobileDataInfo
from xlrd import xldate_as_tuple


class BillTestData(object):
    _instance_lock = threading.Lock()
    _instance = {}

    def __init__(self, testCaseFile, token=None):
        """
        :param testCaseFile: exl文件路径
        :param token: 区分移动端和pc端
        """
        self.path = testCaseFile
        if token is None:
            # 使用ID作为Dict的key
            self.itemIdList = datainfo.getColumnToList(self.path, "billData", "itemId")
            self.itemName = datainfo.getColumnToDict(self.path, "billData", "itemId", "itemName")
            self.itemInputType = datainfo.getColumnToDict(self.path, "billData", "itemId", "itemType")
            self.itemCss = datainfo.getColumnToDict(self.path, "billData", "itemId", "css")
            self.itemVerifyValue = datainfo.getColumnToDict(self.path, "billData", "itemId", "verifyValue")
            self.itemInputValue = datainfo.getColumnToDict(self.path, "billData", "itemId", "inputValue")
            self.handleUsers = datainfo.getColumnToDict(self.path, "action", "serialNumber", "user")
            self.actions = datainfo.getColumnToDict(self.path, "action", "serialNumber", "action")
        else:
            self.itemList = mobileDataInfo.read_xls(self.path, "billData")
            self.actions = mobileDataInfo.read_xls(self.path, "action")

    def judgeValue(self, itemtype, value):
        if isinstance(value, str) and "&" in value:
            value = value.split("&")[self._instance[self.path][1]]
        if itemtype == "currency" and value:
            return "%.2f" % float(value)
        elif itemtype == "date" and value:
            return self.getDate(value)
        elif itemtype != "currency" and type(value) == float:
            return int(value)
        else:
            return str(value).strip()

    def getDate(self, date):
        if not isinstance(date, str):
            time_tup = xldate_as_tuple(date, 0)
            date = str(time_tup[0])
            for i in time_tup[1:3]:
                if 0 < i < 10:
                    date = date + "-0" + str(i)
                else:
                    date = date + "-" + str(i)
        return date

    @property
    def billInputData(self):
        i = 0
        while i < self.itemList.nrows:
            nrows = self.itemList.row_values(i)
            if i == 0:
                self.dict_key = nrows
            else:
                nrows[6] = int(nrows[6])
                nrows[7] = self.judgeValue(nrows[2], nrows[7])
                nrows[8] = int(nrows[8])
                nrows[9] = self.judgeValue(nrows[2], nrows[9])
                data = dict(zip(self.dict_key, nrows))
                yield data
            i += 1

    @property
    def billAction(self):
        i = 0
        while i < self.actions.nrows:
            nrows = self.actions.row_values(i)
            if i == 0:
                self.dict_key = nrows
            else:
                data = dict(zip(self.dict_key, nrows))
                yield data
            i += 1

    @classmethod
    def instance(cls, testCaseFile, token=None):
        if testCaseFile not in BillTestData._instance:
            with BillTestData._instance_lock:
                if testCaseFile not in BillTestData._instance:
                    BillTestData._instance[testCaseFile] = [BillTestData(testCaseFile, token), 0]
        else:
            BillTestData._instance[testCaseFile][1] += 1
        return BillTestData._instance[testCaseFile][0]


if __name__ == '__main__':
    testCaseFile = "zq费用报销组\\1.1-zq日常费用申请单.xls"
    testCaseData = BillTestData.instance(testCaseFile, 1)

    for i in testCaseData.billInputData:
        print("{}-{}-{}-{}".format(i['itemName'], i['itemType'], i['inputValue'], i['verifyValue']))
    print("*" * 50)
    testCaseFile = "zq费用报销组\\1.2-zq费用报销单（无申请).xls"
    testCaseData = BillTestData.instance(testCaseFile, 1)

    for i in testCaseData.billInputData:
        print("{}-{}-{}-{}".format(i['itemName'], i['itemType'], i['inputValue'], i['verifyValue']))

    print("*" * 50)
    testCaseFile = "zq费用报销组\\1.1-zq日常费用申请单.xls"
    testCaseData = BillTestData.instance(testCaseFile, 1)

    for i in testCaseData.billInputData:
        print("{}-{}-{}-{}".format(i['itemName'], i['itemType'], i['inputValue'], i['verifyValue']))
