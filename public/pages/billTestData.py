from public.common import datainfo
from public.MobileScript import mobileDataInfo
from xlrd import xldate_as_tuple


class BillTestData(object):
    def __init__(self, testCaseFile, token=None):
        """
        :param testCaseFile: exl文件路径
        :param token: 区分移动端和pc端
        """
        if token == None:
            # 使用ID作为Dict的key
            self.itemIdList = datainfo.getColumnToList(testCaseFile, "billData", "itemId")
            self.itemName = datainfo.getColumnToDict(testCaseFile, "billData", "itemId", "itemName")
            self.itemInputType = datainfo.getColumnToDict(testCaseFile, "billData", "itemId", "itemType")
            self.itemCss = datainfo.getColumnToDict(testCaseFile, "billData", "itemId", "css")
            self.itemVerifyValue = datainfo.getColumnToDict(testCaseFile, "billData", "itemId", "verifyValue")
            self.itemInputValue = datainfo.getColumnToDict(testCaseFile, "billData", "itemId", "inputValue")
            self.handleUsers = datainfo.getColumnToDict(testCaseFile, "action", "serialNumber", "user")
            self.actions = datainfo.getColumnToDict(testCaseFile, "action", "serialNumber", "action")
        else:
            self.itemList = mobileDataInfo.read_xls(testCaseFile, "billData")
            self.actions = mobileDataInfo.read_xls(testCaseFile, "action")

    def judgeInputValue(self, nrows):
        if nrows[2] == "currency" and nrows[7]:
            # input_value = float(nrows[7])
            input_value = "%.2f" % nrows[7]
        elif nrows[2] == "date" and nrows[7]:
            if type(nrows[7]) == str:
                input_value = nrows[7]
            else:
                time_tup = xldate_as_tuple(nrows[7], 0)
                input_value = str(time_tup[0])
                for i in time_tup[1:3]:
                    if 0 < i < 10:
                        input_value = input_value + "-0" + str(i)
                    else:
                        input_value = input_value + "-" + str(i)
        elif nrows[2] != "currency" and type(nrows[7]) == float:
            input_value = int(nrows[7])
        else:
            input_value = str(nrows[7])
        return input_value

    def judgeVerifyValue(self, nrows):
        if nrows[2] == "currency" and nrows[9]:
            verify_value = "%.2f" % nrows[9]
        elif nrows[2] == "date" and nrows[9]:
            if type(nrows[9]) == str:
                verify_value = nrows[9]
            else:
                time_tup = xldate_as_tuple(nrows[9], 0)
                verify_value = str(time_tup[0])
                for i in time_tup[1:3]:
                    if 0 < i < 10:
                        verify_value = verify_value + "-0" + str(i)
                    else:
                        verify_value = verify_value + "-" + str(i)
        elif nrows[2] != "currency" and type(nrows[9]) == float:
            verify_value = int(nrows[9])
        else:
            verify_value = str(nrows[9]).strip()
        return verify_value

    @property
    def billInputData(self):
        i = 0
        while i < self.itemList.nrows:
            nrows = self.itemList.row_values(i)
            if i == 0:
                self.dict_key = nrows
            else:
                input_value = self.judgeInputValue(nrows)
                verify_value = self.judgeVerifyValue(nrows)
                data = {
                    self.dict_key[0]: nrows[0],
                    self.dict_key[1]: nrows[1],
                    self.dict_key[2]: nrows[2],
                    self.dict_key[3]: nrows[3],
                    self.dict_key[4]: nrows[4],
                    self.dict_key[5]: nrows[5],
                    self.dict_key[6]: int(nrows[6]),
                    self.dict_key[7]: input_value,
                    self.dict_key[8]: int(nrows[8]),
                    self.dict_key[9]: verify_value,
                }
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
                data = {
                    self.dict_key[0]: nrows[0],
                    self.dict_key[1]: nrows[1],
                    self.dict_key[2]: nrows[2],
                }
                yield data
            i += 1


if __name__ == '__main__':
    testCaseFile = "zq费用报销组\\1.1-zq日常费用申请单.xls"
    testCaseData = BillTestData(testCaseFile, 1)

    for i in testCaseData.billInputData:
        print("{}-{}-{}-{}".format(i['itemName'], i['itemType'], i['inputValue'], i['verifyValue']))
