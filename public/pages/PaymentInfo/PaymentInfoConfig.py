# coding=UTF-8
# Author: cuichang
#   Date: 2018-08-21_14_25_40
# Modify the record:


class PaymentInfoConfig(object):
    # 功能说明
    parameter = "css"
    # 审批状态
    status = "xpath->//select[@id='status']"
    # 单据编号
    billNumber = "xpath->//input[@id='billNumber']"
    # 核算公司
    accountingCompany = "xpath->//input[@id='accountingCompany']"
    # 付款方式
    settlementMethod = "xpath->//input[@id='settlementMethod']"
    # 开始日期
    needPaymentDateBegin = "xpath->//input[@id='needPaymentDateBegin']"
    # 结束日期
    needPaymentDateEnd = "xpath->//input[@id='needPaymentDateEnd']"
    # 付款对象
    company = "xpath->//input[@id='company']"
    # 付款公司
    paymentCompany = "xpath->//input[@id='paymentCompany']"
    # 查询
    query = "xpath->//input[@value='查询']"
    # 重置
    reset = "xpath->//input[@value='重置']"
    # 变更
    change = "xpath->//input[@value='变更']"
    # 拆分
    split = "xpath->//input[@value='拆分']"
    # 变更审批人
    changeApprover = "xpath->//input[@value='变更审批人']"
    # 变更复审人
    changeSecondApprover = "xpath->//input[@value='变更复审人']"
    # 派工
    dispatch = "xpath->//input[@value='派工']"
    # 冻结
    freezing = "xpath->//input[@value='冻结']"
    # 沟通
    communicate = "xpath->//input[@value='沟通']"
    # 导入
    importResult = "xpath->//input[@value='导入']"
    # 导出
    export = "xpath->//input[@value='导出']"
    # 通过
    passResult = "xpath->//input[@value='通过']"
    # 制证
    vouchercreate = "xpath->//input[@value='制证']"
    # 凭证预览
    voucherview = "xpath->//input[@value='凭证预览']"
    # 付款
    pay = "xpath->//input[@value='付款']"
    # 退回
    back = "xpath->//input[@value='退回']"
