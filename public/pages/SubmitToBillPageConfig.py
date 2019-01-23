import time
class SubmitToBillPageConfig(object):
    fromIndex = "home.pathGo('form/formIndex.jsf?"+str(time.time())+"',this)"
    mainIframe = "xpath->//iframe[@id='main']"
    formTreeIframe = "xpath->//iframe[@id='formTree']"
    formContentIframe = "xpath->//iframe[@id='formContent']"
    jdIframe = "xpath->//iframe[@id='jd_iframe']"
    tasksIframe = "xpath->//iframe[@id='tasks']"
    # iframe无id和name
    iframeNo = "xpath->//div[@id='tabs']/div/iframe"
    iframeNo1 = "xpath->//div[@id='tabs']/div[4]/iframe"

    #单据定义，中间单据列表iframe
    centerFrame = "xpath->//iframe[@id='centerFrame']"

    # 提交审批按钮
    billSubmit = "xpath->//input[@id='flow_submit']"
    #单据制证按钮
    formAuthCertBtn = "xpath->//input[@id='form_authCertBtn' and @style='display: inline-block; cursor: pointer;']"
    # 确定提交
    processSubmit = "xpath->//input[@id='btnSubmit']"
    #保存单据按钮 = ""
    billSave = "xpath->//input[@id='form_save']"
    #account = "xpath->//input[@itemtext='科目']"

    # 我的单据提取单据编号
    documentNum = "xpath->//div[@id='billTable']/div/div[2]/table/tbody/tr/td[4]/a"

    billNum = "xpath->//td[@itemid='1000000000001956']"

    nextApprover="xpath->//div[@id ='actorListDiv']/ul/li[3]"

    endNode= "xpath->//div[@id ='actorListDiv']/div"

    # 高级查询
    seniorInquire = "xpath->//label[@id='show_text']"

    # 查询单据编号
    formNoSearch = "id->formNo"

    # 查询按钮
    searchCX = "xpath->//input[@value='查询']"

    # 提交审批
    flowSubmit = "id->flow_submit"
    # 确定提交
    btnSubmit = "id->btnSubmit"

    # 弹框信息
    msgContentId = "id->msgContentId"
    # 确定（弹框里的确定按钮）
    sure = "xpath->//input[@value='确定']"
    okBtn = "xpath->//input[@id='okBtn']"