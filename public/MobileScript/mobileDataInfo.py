# coding=utf-8
__author__ = '崔畅'
import codecs
import os
import xlrd
import xlwt
from config import globalparam

testDataPath = os.path.join(globalparam.data_mobile_path, "testdata")
# pagedata_path = os.path.join(globalparam.data_path,"pagedata")
test_path = globalparam.data_mobile_path


# fileName = globalparam.fileName
def get_xls_to_dict(fileName,
                    sheetName):  # 文件名，sheet名，列名   输出：[{'列名行[0]':'第2行[0]','列名行[1]':'第2行[1]'....},{'列名行[0]':'第3行[0]','列名行[1]':'第3行[1]'}.....]
    """                                               xlsx:a b c     输出：[{a:1,b:2,c:3},{a:4,b:5,c"6}]
                                                           1 2 3
                                                           4 5 6
    读取excel表结果为dict
    第一行为字典的key，下面的为值
    return [{'title':'1','user':'root'},{'title':'2','user':'xiaoshitou'}]
    """
    dataResult = list()
    result = list()
    dataFilePath = os.path.join(test_path, fileName)
    xls1 = xlrd.open_workbook(dataFilePath)
    table = xls1.sheet_by_name(sheetName)
    for i in range(0, table.nrows):
        dataResult.append(table.row_values(i))  # dataresult={[第1行[0]，第1行[1].....],[第2行[0],第2行[1]...]}
    # 将list转化成dict
    for i in range(1, len(dataResult)):  # len(dataresult)：数组的元素个数，
        temp = dict(zip(dataResult[0],
                        dataResult[i]))  # dict（zip(list1,list2)）--> [{list1[0]:list2[0]},{list1[1]:list2[1]}......]
        # if temp["casenumber"]==useCaseNumber:#temp[key]
        # print(temp)
        result.append(temp)
    # print(len(result))   print(res["casenumber"])
    return result  # result=temp=[{list1[0]:list2[0]},{list1[1]:list2[1]}......]


def get_xls_to_list(fileName, sheetname, keyValue):  # xlsx a b c    输出：[[1,2,3],[4,5,6]]
    #                                                               1 2 3
    """                                                         4 5 6
    读取excel表包含指定值的一行数据
    第一行为字典的key，下面的为值
    return [{'title':'1','user':'root'},{'title':'2','user':'xiaoshitou'}]
	"""
    dataFilePath = os.path.join(test_path, fileName)
    dataResult = []
    xls1 = xlrd.open_workbook(dataFilePath)
    table = xls1.sheet_by_name(sheetname)
    for i in range(0, table.nrows):
        if keyValue in table.row_values(i):
            table.row_values(i).remove(keyValue)

            # print(table.row_values(i))
            def fun1(s): return s if s != '' else None

            dataResult.append(list(filter(fun1, table.row_values(i))))
            break
        # print(dataresult)
        # print(len(dataresult))
    return dataResult


def getAllUsers(fileName, sheetName, keyColumn):
    dataFilePath = os.path.join(test_path, fileName)
    dataResult = []
    result = {}
    xls1 = xlrd.open_workbook(dataFilePath)
    table = xls1.sheet_by_name(sheetName)
    for i in range(0, table.nrows):  # [0,1,2,....,99]
        dataResult.append(table.row_values(i))  # dataresult={[第1行[0]，第1行[1].....],[第2行[0],第2行[1]...]}
    for i in range(1, len(dataResult)):  # len(dataresult)：数组的元素个数，
        temp = dict(zip(dataResult[0], dataResult[i]))
        result[temp[keyColumn]] = temp
    return result


def get_url_data(title):
    """
    读取txt文件，转化成dict;读取url和导航栏的对应关系
    将txt转化成一个字典:下单=>/admin/order/index
    {'title1':'url1','下单':'/admin/order/index'}
    """
    name = 'urlsource.txt'
    txtPath = os.path.join(testDataPath, name)
    with codecs.open(txtPath, 'r', encoding='utf-8') as f:
        txtContent = f.readlines()
    txtDict = dict([txt.strip().replace('\ufeff', '').split('=>') for txt in txtContent])
    return txtDict[title]


def getColumnToList(fileName, sheetName, keyColumn):  # 返回某列的所有数据
    """
    读取excel表，返回一个list,只是返回第一列的值
    return [1,2,3,4,5]
    """
    dataFilePath = os.path.join(test_path, fileName)
    excel = xlrd.open_workbook(dataFilePath)
    table = excel.sheet_by_name(sheetName)
    columnNumber = -1
    for i in range(0, table.ncols):
        if keyColumn == table.row_values(0)[i]:
            columnNumber = i
            break
    if columnNumber is -1:
        raise NameError("获取数据错误，指定的列名不正确")
    result = [table.row_values(i)[columnNumber].strip() for i in range(1, table.nrows)]
    return result


def getColumnToDict(fileName, sheetName, keyColumn, valueColumn):
    """
    :param fileName: xls文件名
    :param sheetName: xls页面名
    :param keyColumn: xls页面第一行的值, dict的key
    :param valueColumn: xls页面第一行的值, dict的value
    :return: 读取excel表，返回一个字典
    """
    try:
        dataFilePath = os.path.join(test_path, fileName)
        excel = xlrd.open_workbook(dataFilePath)
        table = excel.sheet_by_name(sheetName)
        keyNumber = 1
        valueNumber = 1
        for i in range(0, table.ncols):
            if keyColumn == table.row_values(0)[i]:
                keyNumber = i
            if valueColumn == table.row_values(0)[i]:
                valueNumber = i
        if keyNumber == -1 or valueNumber == -1:
            raise NameError("获取数据错误，指定的列名不正确")
        result = {}
        for i in range(1, table.nrows):
            columnKey = table.row_values(i)[keyNumber]
            columnValue = table.row_values(i)[valueNumber]
            result[columnKey] = columnValue
    except Exception:
        result = {}
    return result


def createFile(file_path, sheetnameList, datasList):
    # fileFullPath = os.path.join(test_path, fileName)
    file = xlwt.Workbook()
    # file =  xlwt.open_workbook(fileFullPath, formatting_info=True)
    for sheetname, datas in zip(sheetnameList, datasList):
        sheet = file.add_sheet(sheetname)
        for row in range(0, len(datas)):
            for col in range(0, len(datas[row])):
                sheet.write(row, col, datas[row][col])
    file.save(file_path)


# E7,获取单据所有字段文件数据，以第一个列+第二列为Key的dict，每行字段数据为list
def getAllDataDict(fileName, sheetname):
    """
    :param fileName: xls表路径
    :param sheetname: 页面名
    :return: ｛key = str(一个列+第二列) : values = list[每一行的所有数据]｝
    """
    dataresult = {}
    try:
        dataFilepath = os.path.join(test_path, fileName)
        xls1 = xlrd.open_workbook(dataFilepath)
        table = xls1.sheet_by_name(sheetname)
        for i in range(0, table.nrows):
            dataresult[str(table.row_values(i)[0]) + "-" + str(table.row_values(i)[1])] = table.row_values(i)
    except Exception:
        return dataresult
    return dataresult


def getAllDataList(fileName, sheetName):
    dataResult = list()
    try:
        dataFilepath = os.path.join(test_path, fileName)
        xls1 = xlrd.open_workbook(dataFilepath)
        table = xls1.sheet_by_name(sheetName)
        for i in range(0, table.nrows):
            dataResult.append(table.row_values(i))
    except:
        return dataResult
    return dataResult


def zbzIduan():
    filed = getColumnToDict("ziduan.xlsx", "Sheet2", "ITEMBILLTYPE", "AREANAME")
    trueType = getColumnToDict("ziduan.xlsx", "Sheet3", "value", "trueType")
    dataHead = ["field", "itemName", "itemType", "itemId", "itemVarName", "css", "verifyValue", "inputValue"]
    dataFilePath = os.path.join(test_path, "ziduan.xlsx")
    xls1 = xlrd.open_workbook(dataFilePath)
    table = xls1.sheet_by_name("Sheet1")
    allItemData = list()
    allItemData.append(dataHead)
    for i in range(1, table.nrows):
        item = list()
        # print(table.row_values(i))
        item.append(filed[table.row_values(i)[1]])
        item.append(table.row_values(i)[3])
        item.append(trueType[table.row_values(i)[2]])
        item.append(table.row_values(i)[0])
        item.append(table.row_values(i)[4])
        if item[2] == "input" or item[2] == "pop" or item[2] == "currency":
            item.append("xpath->//input[@itemvarname='{0}']".format(table.row_values(i)[4]))
        elif item[2] == "select":
            item.append("xpath->//input[@itemvarname='{0}{1}']".format(table.row_values(i)[4], "_label"))
        allItemData.append(item)
    createFile("all.xlsx", "billData", allItemData)


def read_xls(file, sheet):
    dataFilePath = os.path.join(test_path, file)
    data = xlrd.open_workbook(dataFilePath)
    table = data.sheet_by_name(sheet)
    return table


