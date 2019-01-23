__author__ = '崔畅'
from public.common import datainfo
from time import strftime
import os
def createPage(dataFile,modularName,scriptAuthor="cuichang"):
    parameterList = datainfo.getAllDataList(dataFile, modularName)
    #del parameterList[0]#去掉第一行表头数据
    createTime = strftime("%Y-%m-%d_%H_%M_%S")
    fileHeadInfo = "#coding=UTF-8\n" \
            "# Author: " + scriptAuthor + "\n" \
            "#   Date: " + createTime + "\n" \
            "# Modify the record:\n"
    fileHeadImport = "from time import sleep\n" \
                     "from public.common.basepage import Page\n" \
                     "from selenium.webdriver.support.select import Select\n" \
                    "from public.pages.Tool."+modularName+"Config import "+modularName+"Config\n"
    fileTestFunction = "from config import globalparam\n" \
                        "from autoTestFrame.pyselenium import PySelenium\n" \
                        "if __name__ == '__main__':\n" \
                        "\tdr = PySelenium(\"chrome\")\n" \
                        "\tsleep(4)\n" \
                        "\tdr.max_window()\n" \
                        "\tfsscTest = "+modularName+"(dr)\n" \
                        "\tfsscTest.openSystem(globalparam.system_address)\n" \
                        "\tfsscTest.loginSystem(\"autotest001\",\"1\")\n"
    filePath = os.path.split(os.path.realpath(__file__))[0]
    # 使用billCode作为文件名称
    pageFillPath = os.path.join(filePath, modularName + ".py")
    configFillPath = os.path.join(filePath, modularName + "Config.py")
    if os.path.exists(pageFillPath) is False:
        file = open(pageFillPath, 'w', encoding='utf-8')
        file.write(fileHeadInfo)
        file.write(fileHeadImport)
        # 使用billCode作为类名
        file.write("class " + modularName + "(Page):\n")
        for parameter in parameterList:
            if parameter[3] == "click":
                function = "\tdef click"+parameter[2].title()+"(self):#点击元素--"+parameter[5]+"\n" \
                           "\t\tself.click("+modularName+"Config."+parameter[2]+")\n" \
                            "\t\tsleep(1)\n"
            elif parameter[3] == "input":
                function = "\tdef input" + parameter[2].title() + "(self,value):#选择元素--"+parameter[5]+"\n" \
                            "\t\tself.typeInput("+modularName+"Config."+parameter[2]+",\""+parameter[5]+"\",value)\n" \
                            "\t\tsleep(1)\n"
            elif parameter[3] == "select":
                function = "\tdef select" + parameter[2].title() + "(self,value):#选择元素--"+parameter[5]+"\n" \
                            "\t\tself.select("+modularName+"Config."+parameter[2]+",\""+parameter[5]+"\",value)\n" \
                            "\t\tsleep(1)\n"
            elif parameter[3] == "date":
                function = "\tdef input" + parameter[2].title() + "(self,value):#选择元素--"+parameter[5]+"\n" \
                            "\t\tself.dateInput("+modularName+"Config."+parameter[2]+",\""+parameter[5]+"\",value)\n" \
                            "\t\tsleep(1)\n"
            elif parameter[3] == "selectInput":
                function = "\tdef input" + parameter[2].title() + "(self,value):#选择元素--"+parameter[5]+"\n" \
                            "\t\tself.selectInput("+modularName+"Config."+parameter[2]+",\""+parameter[5]+"\",value)\n" \
                            "\t\tsleep(1)\n"
            else:
                function = "\t#暂无定义" + str(parameter)
            file.write(function + "\n")
        file.write(fileTestFunction)
        file.close()
    if os.path.exists(configFillPath) is False:  # 如果用例文件不存在，则创建文件
        file = open(configFillPath, 'w', encoding='utf-8')
        file.write(fileHeadInfo)
        file.write("class "+modularName+"Config(object):\n")
        # 使用billCode作为类名
        for parameter in parameterList:
            file.write("\t#" + parameter[5] +"\n")
            file.write("\t"+parameter[2]+" = \""+parameter[4]+"\"\n")
        file.close()



if __name__ == '__main__':
    createPage("allPage.xls","PaymentInfo")

