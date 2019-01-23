#coding=utf-8
__author__ = '崔畅'
import os
import xlrd
from config import globalparam

def get_usecasenumbers_dict(xlsname, sheetname,key,value):#key、value为数值型
	"""
	读取excel表任意两列，结果为dict
	参数说明：
	xlsname：文件名
	sheetname：sheet页
	key：keys所在的列
	value：values所在的列
	return {'casenumber1':1,casenumber2':2}
	"""
	data_path = globalparam.data_path#项目路径+data
	datapath = os.path.join(data_path, xlsname)#项目路径+data+文件名
	excel = xlrd.open_workbook(datapath)
	table = excel.sheet_by_name(sheetname)
	#table.row_value(i):获取列名行的值（col.value(i)）。
	# .strip():删除字符串两边的空格
	#table.nrows:获取行数（table.ncols）
	cases = [table.row_values(i)[key].strip() for i in range(1,table.nrows)]#？？？？？？？？？
	levels = [int(table.row_values(i)[value]) for i in range(1,table.nrows)]#？？？？？？？？？？
	#将list转化成dict
	result =dict(zip(cases,levels))#zip(keys,values):将两个列表合并为字典
	return result


if __name__=='__main__':
	res = get_usecasenumbers_dict('aaa.xlsx','Sheet1',2,3)
	for case,level in res:
		print(case + " : " + str(level))


