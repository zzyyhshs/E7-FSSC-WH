# -*- coding:utf-8 -*-
import base64
import time

from config import globalparam
import os


class BillsNameError(Exception):
    """自定义异常类"""

    def __init__(self, name):
        self.name = "请确认当前单据组名是否正确: %s" % name

    def __str__(self):
        return self.name


class PageError(Exception):
    def __init__(self, key, value=None, css=None):
        self.key = key
        self.value = value
        self.css = css

    def __str__(self):
        return "未找到该元素: 【{}: {}】".format(self.key, self.css)


class AlertError(PageError):
    def __str__(self):
        return self.key


class UserError(PageError):
    def __str__(self):
        return "为获取到用户: {}; 请在: data_mobile/allBaseData.xls中添加用户".format(self.key)


class ButtonError(PageError):
    def __str__(self):
        return "账号: {};【登录失败: {}】".format(self.key, self.value)


class DateError(PageError):
    def __str__(self):
        if self.css:
            super().__str__()
        elif self.value:
            if self.key == "创建日期":
                return "字段:【单据创建日期】无法修改"
            return "未获取到当前日期: 【{}: {}】".format(self.key, self.value)
        else:
            return "日期格式错误:【{}】日期格式应为: 2019-01-01(年-月-日)".format(self.key)


class SelectError(PageError):
    def __str__(self):
        if self.css:
            super().__str__()
        elif self.value:
            return "未获取到值:【{}: {}】".format(self.key, self.value)
        else:
            return "未知错误"


class OtherError(PageError):
    def __str__(self):
        return "错误字段: 【{}：未获取到编号为{}的单据】".format(self.key, self.value)


class DataError(PageError):
    def __str__(self):
        return "错误字段:【{}: {}】".format(self.key, self.value)