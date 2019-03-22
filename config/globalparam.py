# coding=utf-8
import os
from public.common.readconfig import ReadConfig
# from public.common import caseinfo

# 读取配置文件
config_file_path = os.path.split(os.path.realpath(__file__))[0]  # os.path.split:当前模块的绝对路径
read_config = ReadConfig(os.path.join(config_file_path, 'config.ini'))  # 连接当前模块的绝对路径和ini配置文件

# 项目参数设置
prj_path = read_config.getValue('projectConfig', 'project_path')
# os.path.abspath('..')
# "D:\PycharmProjects\Auto_Test_TMS"

# #
# 日志路径
log_path = os.path.join(prj_path, 'report\\log')

# 截图文件路径
img_path = os.path.join(prj_path, 'report\\image')
# 移动端截图文件路径
mobile_img_path = os.path.join(prj_path, 'report\\mobile_image')

# 测试报告路径
report_path = os.path.join(prj_path, 'report\\testreport')

# report_path = os.path.join(prj_path, 'report\\testreport')

# 浏览器
browser_mobile = 'chrome'
# browser = 'phantomjs'  # 兼容性
browser = 'ie'
# browser = 'ff'  # 版本太低

# 测试数据路径
data_path = os.path.join(prj_path, 'data\pc')  # 项目路径+data文件夹
# 移动端测试数据路径
data_mobile_path = os.path.join(prj_path, "data\mobile")

# 用例执行模式(0：执行调试用例，1:执行所有level1用例，2：执行所有level2及以上用例，3：执行所有level3及以上用例，4：执行所有用例)
usecase_run_mode = 4

# 读取用例编号及级别
# casenumbers = caseinfo.get_usecasenumbers_dict('aaa.xlsx', 'Sheet1',2,3)

# 被测系统地址
# system_address = "http://192.168.64.11:9000/e7-fssc/pages/login.jsp "
system_address = "http://192.168.64.12:9000/pages/login.jsp"
mobile_sys_address = "http://192.168.48.115:8050/e7/#/login"

# system_address = 'http://172.16.100.38:9901/e7-fssc/pages/home.jsp'

# 凭证生成后是否推送，True为推送，False为不推送
vouchersPush = False
# vouchersPush = True
# 共享中心为自动派工模式，值为True，手工派工为False
automate = False
# 自动派工周期，自动派工时，脚本等待派工时间
automaticWorkCycle = 60
