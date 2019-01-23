#coding=utf-8
__author__ = '崔畅'
class BasePageConfig(object):
    UserName = "xpath->//input[@id='usernameInput']"
    UserPwd = "xpath->//input[@id='passwordInput']"
    LoginButton = "xpath->//div[@id='submitButton']"

    # 当前用户
    currentUser = "xpath->//div[@id='divwra']/div[2]/a"
    mainIframe = "xpath->//iframe[@id='main']"
    formTreeIframe = "xpath->//iframe[@id='formTree']"
    formContentIframe = "xpath->//iframe[@id='formContent']"
    jdIframe = "xpath->//iframe[@id='jd_iframe']"

    # 单据定义，中间单据列表iframe
    centerFrame = "xpath->//iframe[@id='centerFrame']"

    # iframe无id和name
    iframeNo = "xpath->//div[@id='tabs']/div/iframe"
    iframeNo1 = "xpath->//div[@id='tabs']/div[4]/iframe"

    # 下拉框的文本输入框&查找按钮
    searchInput = "id->searchInput"
    searchSubmit = "xpath->//input[@value='查找']"

    #单据关联弹出框
    searchText = "id->billNumber"
    searchButton = "id->showMainBu"
    plusSign = "xpath->//input[@value='+'][1]"
    allSelect = "id->allselect"
    sureButton = "css->input[class='button_new'][value=' 确定 ']"
    #

    FirstMenuList = "xpath->//div[@id='menu']/ul/li"#一级
    # menu ="a/span"#一级的文本定位
    # children = "div/ul"
    # second_menu = "li"
    # second_children = "li/div/ul"
    # 查询按钮
    searchCX = "xpath->//input[@value='查询']"
    # 确定（弹框里的确定按钮）
    sure = "xpath->//input[@value='确定']"
    cancel = "xpath->//input[@value='取消']"
    # 单据提交审批时
    # 提交审批
    flowSubmit = "id->flow_submit"
    # 确定提交
    btnSubmit = "id->btnSubmit"
    # 确定（弹框里的确定按钮）
    js = 'parent.closeMsgPanel("true");'
    # 返回
    back = "id->form_back"

    # 我的单据提取单据编号
    documentNum = "xpath->//div[@id='billTable']/div/div[2]/table/tbody/tr/td[4]/a"

    # 注销
    logout = "id->loginOut"

    # 高级查询
    seniorInquire = "xpath->//label[@id='show_text']"

    # 查询单据编号
    formNoSearch = "id->formNo"

    # ...按钮
    formShowButton = "id->form_show_button"

    # 退回button
    backButton = "id->flow_reject"

    # 弹框信息
    msgContentId = "id->msgContentId"

if __name__=='__main__':
    config = BasePageConfig()
    #print(config.logo)