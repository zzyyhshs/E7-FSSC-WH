# Author : 朱尧
# email: zhuy@yuanian.com, zzyyhshs@163.com
import base64
from time import sleep
import time

import os

from autoTestFrame.pyselenium import PySelenium
from config import globalparam
from public.pages.SubmitToBillPageConfig import SubmitToBillPageConfig
from PIL import Image
from functools import wraps


success = "SUCCESS   "
fail = "FAIL   "
HTML_IMG_TEMPLATE = """
    <a href="data:image/png;base64, {}">
    <img src="data:image/png;base64, {}" width="800px" height="500px"/>
    </a>
    <br></br>
"""


class MobileSelenium(PySelenium):
    def __init__(self, browser, logger=None, remoteAddress=None):
        super().__init__(browser, logger, remoteAddress)
        # self.driver.implicitly_wait(10)

    def jsClickElement(self, element):
        """
        针对IE浏览器点击元素无效或者错误
        :param element: 需要点击的元素
        :return: None
        """
        t1 = time.time()
        click_js = "arguments[0].click();"
        try:
            self.driver.execute_script(click_js, element)
            self.my_print(
                "{0} Use javascript [{1}] click element: {2}, Spend {3} seconds".format(success, click_js, element.text,
                                                                                        time.time() - t1))
        except Exception:
            self.my_print(
                "{0} Unable to use javascript [{1}] click element: {2}, Spend {3} seconds".format(fail, click_js,
                                                                                                  element.text,
                                                                                                  time.time() - t1))
            raise

    def browserRoll(self, element, css):
        """控制页面滚动到指定元素"""
        t1 = time.time()
        roll_js = "arguments[0].scrollIntoView();"
        try:
            self.driver.execute_script(roll_js, element)
            self.my_print(
                "{0} Use javascript [{1}] scroll to element: {2}, Spend {3} seconds".format(success, roll_js, css,
                                                                                            time.time() - t1))
        except Exception:
            self.my_print(
                "{0} Unable to use javascript [{1}] scroll to element: {2}, Spend {3} seconds".format(fail, roll_js,
                                                                                                      css,
                                                                                                      time.time() - t1))
            raise

    def click_Mob(self, xpath):
        """点击不到元素,滚动之后再点击一次"""
        self.my_print("点击元素[{0}]".format(xpath))
        ele = self.get_element(xpath)
        sleep(0.5)
        try:
            ele.click()
        except:
            self.browserRoll(ele, xpath)
            ele.click()

    def get_img(self, file_name):
        """
        截图
        :param file_name:图片名
        :return: 图片路径
        """
        path = globalparam.mobile_img_path + '\\' + file_name
        self.driver.save_screenshot(path)
        return path

    def join_img(self, main_path, second_path):
        """拼接图片"""
        base_img = Image.open(main_path)
        second_img = Image.open(second_path)
        base_img_w, base_img_h = base_img.size
        second_img_w, secong_img_h = second_img.size
        result = Image.new("RGB", (base_img_w, base_img_h + secong_img_h))
        result.paste(base_img, box=(0, 0))
        result.paste(second_img, box=(0, base_img_h))
        result.save(main_path)
        os.remove(second_path)

    def print_img(self):
        """截取图片打印到测试报告"""
        path = os.path.join(globalparam.mobile_img_path,
                            "图片路径_" + time.strftime("%Y-%m-%d_%H_%M_%S") + '.png')
        self.driver.get_screenshot_as_file(path)
        with open(path, 'rb') as file:
            data = file.read()
        os.remove(path)
        data = base64.b64encode(data).decode()
        self.my_print(HTML_IMG_TEMPLATE.format(data, data))


url = "http://192.168.64.11:9000/e7-fssc/pages/login.jsp"
"""移动端获取数据装饰器"""
def openSystem(func):  # 打开url
    def run(self, bills_name):
        self.driver.openSystem(url)
        self.driver.dr.max_window()
        self.driver.loginSystem("admin", "1")
        sleep(3)
        func(self, bills_name)
        self.driver.dr.quit()

    return run


def switchIframe_main(func):  # 切换iframe -> main
    @wraps(func)
    def fool(self, *args, **kwargs):
        self.driver.switch_to_iframe(SubmitToBillPageConfig.mainIframe)
        sleep(1)
        func(self, *args, **kwargs)
        self.driver.switch_to_parent_iframe()

    return fool


def switchIframe_formTree(func):  # 切换iframe -> formTree
    @wraps(func)
    def fool(self, *args, **kwargs):
        self.driver.switch_to_iframe(SubmitToBillPageConfig.formTreeIframe)
        # sleep(3)
        func(self, *args, **kwargs)
        self.driver.switch_to_parent_iframe()

    return fool


def switchIframe_formContent(func):  # 切换iframe -> formContent
    @wraps(func)
    def fool(self, *args, **kwargs):
        self.driver.switch_to_iframe(SubmitToBillPageConfig.formContentIframe)
        # sleep(3)
        func(self, *args, **kwargs)
        self.driver.switch_to_parent_iframe()

    return fool


def switchIframe_jd(func):  # 切换iframe -> jd
    @wraps(func)
    def fool(self, *args, **kwargs):
        self.driver.switch_to_iframe(SubmitToBillPageConfig.jdIframe)
        # sleep(3)
        func(self, *args, **kwargs)
        self.driver.switch_to_parent_iframe()

    return fool


def switchIframe_tasks(func):  # 切换iframe -> tasks
    @wraps(func)
    def fool(self, *args, **kwargs):
        self.driver.switch_to_iframe(SubmitToBillPageConfig.tasksIframe)
        # sleep(3)
        func(self, *args, **kwargs)
        self.driver.switch_to_parent_iframe()

    return fool


def switchIframe_center(func):  # 切换iframe -> center
    @wraps(func)
    def fool(self, *args, **kwargs):
        self.driver.switch_to_iframe(SubmitToBillPageConfig.centerFrame)
        # sleep(3)
        func(self, *args, **kwargs)
        self.driver.switch_to_parent_iframe()

    return fool


def switchIframe_No(func):  # 切换iframe -> No
    @wraps(func)
    def fool(self, *args, **kwargs):
        self.driver.switch_to_iframe(SubmitToBillPageConfig.iframeNo)
        # sleep(3)
        func(self, *args, **kwargs)
        self.driver.switch_to_parent_iframe()

    return fool


def switchIframe_No1(func):  # 切换iframe -> No1
    @wraps(func)
    def fool(self, *args, **kwargs):
        self.driver.switch_to_iframe(SubmitToBillPageConfig.iframeNo1)
        # sleep(3)
        func(self, *args, **kwargs)
        self.driver.switch_to_parent_iframe()

    return fool
