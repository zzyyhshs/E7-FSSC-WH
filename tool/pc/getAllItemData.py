__author__ = '崔畅'
import os
from public.common import datainfo
import xlrd
from config import globalparam
def getTrueType(displayType,dataType):
    #type = ["input","textarea","currency","date","pop","select"]
    displayType = int(displayType)
    dataType = int(dataType)
    print(str(displayType)+"_"+str(dataType))
    if dataType == 4 or dataType == 6:
        return "date"
    if displayType == 4:
        return "textarea"
    if displayType == 5:
        return "pop"
    if displayType == 7:
        return "currency"
    if displayType == 2:
        return "select"
    if dataType == 2:
        return "currency"
    if displayType == 1:
        return "input"
    if displayType == 3:
        return ""


if __name__=='__main__':
    """ 自动生成xpath """
    itemDataFill = "item.xls"
    project = ""
    itemBillType = datainfo.getColumnToDict(itemDataFill,"itemBillType","itemBillType","areaName")
    # itemBillType = {itemBillType : areaName}
    itemDisplayType = datainfo.getColumnToDict(itemDataFill, "itemDisplayType", "value", "trueType")
    # itemDisplayType = {value : trueType}
    itemDataType = datainfo.getColumnToDict(itemDataFill, "itemDataType", "value", "trueType")
    dataHead = ["field", "itemName", "itemType", "itemId","itemVarName","css","inputValue","verifyValue"]
    dataFilePath = os.path.join(globalparam.data_path, itemDataFill)
    xls1 = xlrd.open_workbook(dataFilePath)
    table = xls1.sheet_by_name("allItem")
    allItemData = list()
    allItemData.append(dataHead)
    for i in range(1,table.nrows):
        item = list()
        print(table.row_values(i))
        try:
            item.append(itemBillType[table.row_values(i)[1]])
        except Exception as e:
            print(e)
        item.append(table.row_values(i)[4])
        trueType = getTrueType(table.row_values(i)[2],table.row_values(i)[3])
        item.append(trueType)
        item.append(table.row_values(i)[0])
        item.append(table.row_values(i)[5])
        if item[2] == "input" or item[2] == "pop" or item[2] == "currency" or item[2] == "date":
            item.append("xpath->//input[@itemvarname='{0}' and @itemid='{1}']".format(table.row_values(i)[5],table.row_values(i)[0]))
        elif item[2] == "select":
            item.append("xpath->//input[@itemvarname='{0}{1}' and @itemid='{2}']".format(table.row_values(i)[5],"_label",table.row_values(i)[0]))
        elif item[2] == "textarea":
            item.append("xpath->//textarea[@itemvarname='{0}' and @itemid='{1}']".format(table.row_values(i)[5],table.row_values(i)[0]))
        print(item)
        allItemData.append(item)
    datainfo.createFile("allItemData"+project+".xls",["billData"],[allItemData])