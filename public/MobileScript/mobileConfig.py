# coding=utf-8
"""PC配置页面xpath"""
# 单据组xpath
mobile_xpath = "xpath->//li[@class='bbit-tree-node']/div"
# 单据xpath
mobile_bill_xpath = "xpath->//ul[@class='bbit-tree-node-ct']/li/div/span[2]"
# 单据配置勾选框
check_bill_xpath = "xpath->//*[@id='mobileBill']"
# 所有字段
field_xpath = "xpath->//tr[@id='hiddenTr' and @name='cloneTr']"
# 下拉框
select_xpath = "xpath->//*[@id='billfieldtype']"
# 所有字段勾选框
check_field_xpath = field_xpath + "/td[3]/input"
# 是否启用字段组勾选框
check_field_set_xpath = "xpath->//*[@id='mobileBillFieldCheck']"


"""exl文件表头 and 默认数据"""
result = [["field", "itemName", "itemType", "itemId", "itemVarName", "css", "inputShow", "inputValue", "verifyShow", "verifyValue"]]
action = [["serialNumber", "user", "action"], ["1", "张一", "填单"], ["2", "张二", "审批"]]


"""移动端xpath"""
UserName = "id->loginNameInput"
UserPwd = "id->passwordInput"
LoginButton = "xpath->//div[@class='scroll']/button"
ErrorId = "xpath->//div[@class='erroID']"

apply_for_xpath = "xpath->//a[@class='titleName tab-item' and @title='申请']"
my_for_xpath = "xpath->//a[@class='titleName tab-item' and @title='我的']"
approve_for_xpath = "xpath->//a[@class='titleName tab-item' and @title='审批']"

# 滚动条
scroll = "xpath->//div[@class='scroll-bar-indicator scroll-bar-fade-out']"

bill_num_img_xpath = "xpath->//div[@class='line-css']/img[2]"
bill_num_xpath = "xpath->//div[@class='popup-body']/span"
quit_confirm_xpath = "xpath->//div[@class='popup-buttons']/button"

search_input_xpath = "xpath->//input[@placeholder='关键词']"
search_input_xpath2 = "xpath->//label[@class='item-input-wrapper']/input[@placeholder='关键词']"
search_submit_xpath = "xpath->//input[@class='searchBtnSize']"
search_submit_xpath2 = "xpath->//input[@class='search-icon']"
search_submit_xpath3 = "xpath->//button[@class='button button-clear ng-binding']"
select_sure = "xpath->//a[@class='main-theme h1TitleCss button button-clear ng-binding']"
select_sure2 = "xpath->//a[@class='h1TitleCss button btnColor ng-binding'][2]"
select_sure3 = "xpath->//a[@class='button button-bill-sure ng-binding']"
select_sure4 = "xpath->//span[@class='treeModel-operate ng-binding'][2]"

"""填单分组xpath"""
# ShowHideMX = "xpath->//div[@id='AreaShowHideMX']"  # 明细
# ShowHideCX = "xpath->//div[@id='AreaShowHideCX']"  # 冲销
# ShowHideHT = "xpath->//div[@id='AreaShowHideHT']"  # 合同
# ShowHideFK = "xpath->//div[@id='AreaShowHideFK']"  # 支付
# ShowHideHK = "xpath->//div[@id='AreaShowHideHK']"  # 还款
# ShowHideXC = "xpath->//div[@id='AreaShowHideXC']"  # 行程
# ShowHideOT = "xpath->//div[@id='AreaShowHideOT']"  # 原行程

Area_dict = {
    "明细区": "xpath->//div[@id='AreaShowHideMX']",
    "冲销区": "xpath->//div[@id='AreaShowHideCX']",
    "合同区": "xpath->//div[@id='AreaShowHideHT']",
    "付款区": "xpath->//div[@id='AreaShowHideFK']",
    "还款区": "xpath->//div[@id='AreaShowHideHK']",
    "商旅行程区": "xpath->//div[@id='AreaShowHideXC']",
    "商旅原行程区": "xpath->//div[@id='AreaShowHideOT']",
}

"""单据保存"""
save_Btn_xpath = "xpath->//button[@id='saveBtn']"

pop_up_text = "xpath->//div[@class='popup-body']/child::*"  # 弹框文本
pop_up_sure = "xpath->//button[@class='button ng-binding button-positive']"  # 弹框确定

"""查找单据"""
searchNameDCL = "xpath->//input[@id='searchNameDCL']"  # 待审批
searchNameDSP = "xpath->//input[@id='searchNameDSP']"  # 待处理
searchNameSP = "xpath->//input[@id='searchNameSP']"  # 审批
searchNameYWC = "xpath->//input[@id='searchNameYWC']"  # 已完成
find_the_bill = "xpath->//div[@class='cardOne col-90'][1]"  # 查找到的单据

"""提交单据"""
mission_bill_xpath = "xpath->//a[@class='button button-submit ng-binding']"
next_one_approver_xpath = "xpath->//div[@class='person ng-binding']"
make_sure_xpath = "xpath->//a[@class='button btn-sure space_4 ng-binding']"

"""退出系统"""
get_back_xpath = "xpath->//*[@class='titleColor bar bar-header disable-user-behavior has-tabs-top']/button"
log_out_xpath = "xpath->//div[@class='label_left sign_out ng-binding']"

"""审批通过 or 驳回"""
# verify_pass = "xpath->//a[@id='flowGround']"
verify_pass = "xpath->//a[@class='button btn-sure space_4 ng-binding']"
# verify_back = "xpath->//a[@id='sendBack']"
verify_back = "xpath->//a[@class='button btn-cancel space_4 ng-binding']"

"""审批账号所有字段"""
row_path = "xpath->//div[@class='row']"  # 其他区域
primary_table = "xpath->//div[@class='stripeTop']"  # 主表区
group_by_xpath = "xpath->//div[@class='blue-color']"

group_field_dict = {
    "明细区": "明细信息",
    "冲销区": "冲销区",
    "付款区": "支付信息",
    "合同区": "合同区",
    # "还款区": "还款区",
    # "商旅行程区": "行程信息",
    # "商旅原行程区": "原行程信息",
}