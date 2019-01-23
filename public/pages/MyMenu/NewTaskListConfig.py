#coding=UTF-8
# Author: cuichang
#   Date: 2018-08-10_17_53_48
# Modify the record:
class NewTaskListConfig(object):
	#功能说明
	parameter = "css"
	#待办任务
	link_a1 = "xpath->//a[@id='_link-a1']"
	#抄送任务
	link_a2 = "xpath->//a[@id='_link-a2']"
	#高级查询
	show_text = "xpath->//label[@id='show_text']"
	#任务状态
	taskStatus = "xpath->//select[@id='taskStatus']"
	#起始创建时间
	billBeginT = "xpath->//input[@id='billBeginT']"
	#结束创建时间
	billEndT = "xpath->//input[@id='billEndT']"
	#单据编号
	formNo = "xpath->//input[@id='formNo']"
	#单据名称
	formInput = "xpath->//input[@id='formInput']"
	#预算科目
	dim = "xpath->//input[@id='dim']"
	#申请人
	applicant = "xpath->//input[@id='applicant']"
	#申请标题
	billtitle = "xpath->//input[@id='billtitle']"
	#经办部门
	deptSelectorName = "xpath->//input[@id='deptSelectorName']"
	#最小单据金额
	beginM = "xpath->//input[@id='beginM']"
	#最大单据金额
	endM = "xpath->//input[@id='endM']"
	#审批类型
	approvalType = "xpath->//select[@id='approvalType']"
	#单据状态
	formStatus = "xpath->//select[@id='approvalType']"
	#核算公式
	companyCode = "xpath->//input[@id='companyCode']"
	#流程环节
	activityName = "xpath->//input[@id='activityName']"
	#查询
	searchCX = "xpath->//input[@value='查询']"
	#批量审批
	batch_approval = "xpath->//input[@id='batch_approval']"
	#批量打印
	batch_print = "xpath->//input[@value='批量打印']"
	#重置
	reset_search = "xpath->//input[@value='重置']"
