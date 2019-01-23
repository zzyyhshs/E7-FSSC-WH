__author__ = ""
__version__ = "0.8.2"
# coding=utf-8
# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from public.common.log import Log

success = "SUCCESS   "
fail = "FAIL   "
#logger = Log()

class PySelenium(object):
    """
        pyselenium framework for the main class, the original
    selenium provided by the method of the two packaging,
    making it easier to use.
    """
    Browser = ""
    def __init__(self, browser,logger =None,remoteAddress=None):
        """
        remote consle：
        dr = PySelenium('RChrome','127.0.0.1:8080')
        """
        t1 = time.time()
        dc = {'platform': 'ANY', 'browserName': 'chrome', 'version': '', 'javascriptEnabled': True}
        dr = None
        print(browser)
        self.Browser = browser
        if logger is None:
            self.logger = Log()
        else:
            self.logger = logger
        if remoteAddress is None:
            if browser == "firefox" or browser == "ff":
                dr = webdriver.Firefox()
            elif browser == "chrome" or browser == "Chrome":
                dr = webdriver.Chrome()
            elif browser == "internet explorer" or browser == "ie":
                dr = webdriver.Ie()
            elif browser == "opera":
                dr = webdriver.Opera()
            elif browser == "phantomjs":
                dr = webdriver.PhantomJS(r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe")
            elif browser == "edge":
                dr = webdriver.Edge()
        else:
            if browser == "RChrome":
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
            elif browser == "RIE":
                dc['browserName'] = 'internet explorer'
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
            elif browser == "RFirefox":
                dc['browserName'] = 'firefox'
                dc['marionette'] = False
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
        try:
            self.driver = dr
            self.my_print("{0} Start a new browser: {1}, Spend {2} seconds".format(success,browser,time.time()-t1))
        except Exception:
            raise NameError("Not found {0} browser,You can enter 'ie','ff',"
                            "'chrome','RChrome','RIe' or 'RFirefox'.".format( browser))

    def my_print(self,msg):#日志输出
        self.logger.info(msg)

    def element_wait(self, css, secs=10):#寻找元素是否存在
        """
        Waiting for an element to display.

        Usage:
        driver.element_wait("id->kw",10)
        """
        if "->" not in css:
            raise NameError("定位语法错误,缺少 '->'.")

        by = css.split("->")[0].strip()
        value = css.split("->")[1].strip()
        messages = 'Element: {0} not found in {1} seconds.'.format(css, secs)

        if by == "id":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.ID, value)), messages)
        elif by == "name":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.NAME, value)), messages)
        elif by == "class":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)), messages)
        elif by == "link_text":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)), messages)
        elif by == "xpath":
            # WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.XPATH, value)), messages)
            WebDriverWait(self.driver, secs, 3).until(EC.presence_of_element_located((By.XPATH, value)), messages)
        elif by == "css":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)),messages)
        else:
            raise NameError("请输入正确的定位元素：'id','name','class','link_text','xpaht','css'.")

    def get_element(self, css):#定位元素，并返回
        """
        Judge element positioning way, and returns the element.

        Usage:
        driver.get_element('id->kw')
        """
        if "->" not in css:
            raise NameError("定位语法错误,缺少'->'.")

        by = css.split("->")[0].strip()
        value = css.split("->")[1].strip()

        if by == "id":
            element = self.driver.find_element_by_id(value)
        elif by == "name":
            element = self.driver.find_element_by_name(value)
        elif by == "class":
            element = self.driver.find_element_by_class_name(value)
        elif by == "link_text":
            element = self.driver.find_element_by_link_text(value)
        elif by == "xpath":
            element = self.driver.find_element_by_xpath(value)
        elif by == "css":
            element = self.driver.find_element_by_css_selector(value)
        else:
            raise NameError("请输入正确的定位元素：'id','name','class','link_text','xpaht','css'.")
        return element

    def get_elements(self,css):#定位一组元素
        """
        Judge element positioning way, and returns the element.

        Usage:
        driver.get_elements('id->kw')
        """
        if "->" not in css:
            raise NameError("定位语法错误，缺少‘->’.")
        by = css.split("->")[0].strip()
        value = css.split("->")[1].strip()
        if by == "id":
            elements = self.driver.find_elements_by_id(value)
        elif by == "name":
            elements = self.driver.find_elements_by_name(value)
        elif by == "class":
            elements = self.driver.find_elements_by_class_name(value)
        elif by == "link_text":
            elements = self.driver.find_elements_by_link_text(value)
        elif by == "xpath":
            elements = self.driver.find_elements_by_xpath(value)
        elif by == "css":
            elements = self.driver.find_elements_by_css_selector(value)
        else:
            raise NameError("请输入正确的定位元素：'id','name','class','link_text','xpaht','css'.")
        return elements

    def isElementExist(self, css):#判断元素是否是否存在
        """
         判断一个元素是否存在.
         存在返回True，不存在返回false

         Usage:
                driver.isElementExist('id->kw')
        """
        flag = True
        if "->" not in css:
            raise NameError("定位语法错误,缺少 '->'.")
        by = css.split("->")[0].strip()
        value = css.split("->")[1].strip()
        try:
            if by == "id":
                element = self.driver.find_element_by_id(value)
                return flag
            elif by == "name":
                element = self.driver.find_element_by_name(value)
                return flag
            elif by == "class":
                element = self.driver.find_element_by_class_name(value)
                return flag
            elif by == "link_text":
                element = self.driver.find_element_by_link_text(value)
                return flag
            elif by == "xpath":
                element = self.driver.find_element_by_xpath(value)
                return flag
            elif by == "css":
                element = self.driver.find_element_by_css_selector(value)
                return flag
            else:
                raise NameError("请输入正确的定位元素：'id','name','class','link_text','xpaht','css'.")
        except:
            flag = False
            return flag

    def open(self, url):#打开系统
        """
        open url.

        Usage:
        driver.open("https://www.baidu.com")
        """
        t1 = time.time()
        try:
            self.driver.get(url)
            self.my_print("{0} Navigated to {1}, Spend {2} seconds".format(success,url,time.time()-t1))
        except Exception:
            self.my_print("{0} Unable to load {1}, Spend {2} seconds".format(fail, url, time.time() - t1))
            raise

    def max_window(self):#最大化
        """
        Set browser window maximized.

        Usage:
        driver.max_window()
        """
        t1 = time.time()
        self.driver.maximize_window()
        self.my_print("{0} Set browser window maximized, Spend {1} seconds".format(success, time.time() - t1))

    def set_window(self, wide, high):#设置浏览器的宽高
        """
        Set browser window wide and high.

        Usage:
        driver.set_window(wide,high)
        """
        t1 = time.time()
        self.driver.set_window_size(wide, high)
        self.my_print("{0} Set browser window wide: {1},high: {2}, Spend {3} seconds".format(success,
            wide,high,time.time() - t1))

    def type(self, css, text):#定位元素并输入text
        """
        Operation input box.

        Usage:
        driver.type("id->kw","selenium")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.send_keys(text)
            self.my_print("{0} Typed element: <{1}> content: {2}, Spend {3} seconds".format(success,
                css,text,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to type element: <{1}> content: {2}, Spend {3} seconds".format(fail,
                css, text, time.time() - t1))
            raise

    def clear_type(self, css, text):#定位元素，清空，输入text
        """
        Clear and input element.

        Usage:
        driver.clear_type("id->kw","selenium")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            time.sleep(1)
            #el.click()
            el.clear()
            el.send_keys(text)
            self.my_print("{0} Clear and type element: <{1}> content: {2}, Spend {3} seconds".format(success,
                css, text,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to clear and type element: <{1}> content: {2}, Spend {3} seconds".format(fail,
                css, text,time.time() - t1))
            raise

    def click(self, css):#点击
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.click()
            self.my_print("{0} Clicked element: <{1}>, Spend {2} seconds".format(success,css,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def js_click(self, css):  # 点击js
        """
        Input a css selecter,use javascript click element.

        Usage:
        driver.js_click('#buttonid')
        """
        t1 = time.time()
        js_str = "arguments[0].click();"  # "$('{0}').click()".format(css)
        try:
            self.element_wait(css)
            ele = self.get_element(css)
            self.driver.execute_script(js_str, ele)
            self.my_print("{0} Use javascript [{1}] click element: {2}, Spend {3} seconds".format(success,
                js_str, css,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to use javascript [{1}] click element: {2}, Spend {3} seconds".format(fail,
                js_str,css, time.time() - t1))
            raise

    def clickByOffset(self,xoffset=0,yoffset=0):#点击坐标
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.click("id->kw")
        """
        t1 = time.time()
        try:
            ActionChains(self.driver).move_by_offset(xoffset,yoffset).click().perform()
            self.my_print("{0} Clicked Blank: <{1}>, Spend {2} seconds".format(success,str(xoffset)+","+str(yoffset),time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to click Blank: <{1}>, Spend {2} seconds".format(fail, str(xoffset)+","+str(yoffset), time.time() - t1))
            raise

    def click_by_element(self,element):  # 参数为元素，直接点击
        t1 = time.time()
        try:
            element.click()
            self.my_print("{0} Clicked element: <{1}>, Spend {2} seconds".format(success,element.get_attribute("class"),time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to click element: <{1}>, Spend {2} seconds".format(fail,element.get_attribute("class"), time.time() - t1))
            raise

    def right_click(self, css):  # 右击
        """
        Right click element.

        Usage:
        driver.right_click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).context_click(el).perform()
            self.my_print("{0} Right click element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to right click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def move_to_element(self, css):  # 移动到指定元素
        """
        Mouse over the element.

        Usage:
        driver.move_to_element("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).move_to_element(el).perform()
            self.my_print("{0} Move to element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} unable move to element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def move_to_element_by_element(self, element):  # 参数为元素，直接移动到元素处
        """
        Mouse over the element.

        Usage:
        driver.move_to_element("id->kw")
        """
        t1 = time.time()
        try:
            ActionChains(self.driver).move_to_element(element).perform()
            self.my_print("{0} Move to element: <{1}>, Spend {2} seconds".format(success, element.get_attribute("class"), time.time() - t1))
        except Exception:
            self.my_print("{0} unable move to element: <{1}>, Spend {2} seconds".format(fail, element.get_attribute("class"), time.time() - t1))
            raise

    def double_click(self, css):  # 双击
        """
        Double click element.

        Usage:
        driver.double_click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).double_click(el).perform()
            self.my_print("{0} Double click element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to double click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def drag_and_drop(self, el_css, ta_css):  # 将鼠标从el_cs拖拽至ta_css处
        """
        Drags an element a certain distance and then drops it.

        Usage:
        driver.drag_and_drop("id->kw","id->su")
        """
        t1 = time.time()
        try:
            self.element_wait(el_css)
            element = self.get_element(el_css)
            self.element_wait(ta_css)
            target = self.get_element(ta_css)
            ActionChains(driver).drag_and_drop(element, target).perform()
            self.my_print("{0} Drag and drop element: <{1}> to element: <{2}>, Spend {3} seconds".format(success,
                el_css,ta_css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to drag and drop element: <{1}> to element: <{2}>, Spend {3} seconds".format(fail,
                el_css, ta_css, time.time() - t1))
            raise

    def click_text(self, text):  # 点击带链接文本
        """
        Click the element by the link text

        Usage:
        driver.click_text("新闻")
        """
        t1 = time.time()
        try:
            self.driver.find_element_by_link_text(text).click()
            # self.driver.find_element_by_partial_link_text(text).click()
            self.my_print("{0} Click by text content: {1}, Spend {2} seconds".format(success, text,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to Click by text content: {1}, Spend {2} seconds".format(fail, text, time.time() - t1))
            raise

    def close(self):  # 关闭浏览器
        """
        Simulates the user clicking the "close" button in the titlebar of a popup
        window or tab.

        Usage:
        driver.close()
        """
        t1 = time.time()
        self.driver.close()
        self.my_print("{0} Closed current window, Spend {1} seconds".format(success, time.time() - t1))

    def quit(self):  # 退出浏览器
        """
        Quit the driver and close all the windows.

        Usage:
        driver.quit()
        """
        t1 = time.time()
        self.driver.quit()
        self.my_print("{0} Closed all window and quit the driver, Spend {1} seconds".format(success, time.time() - t1))

    def submit(self, css):  # 提交
        """
        Submit the specified form.

        Usage:
        driver.submit("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.submit()
            self.my_print("{0} Submit form args element: <{1}>, Spend {2} seconds".format(success,css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to submit form args element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def F5(self):  # 刷新
        """
        Refresh the current page.

        Usage:
        driver.F5()
        """
        t1 = time
        self.driver.refresh()
        self.my_print("{0} Refresh the current page, Spend {1} seconds".format(success, time.time() - t1))

    def js(self, script):  # 执行js
        """
        Execute JavaScript scripts.

        Usage:
        driver.js("window.scrollTo(200,1000);")
        """
        t1 = time.time()
        try:
            self.driver.execute_script(script)
            self.my_print("{0} Execute javascript scripts: {1}, Spend {2} seconds".format(success,script, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to execute javascript scripts: {1}, Spend {2} seconds".format(fail,
                script, time.time() - t1))
            raise

    def get_attribute(self, css, attribute):  # 获取元素指定的属性
        """
        Gets the value of an element attribute.

        Usage:
        driver.get_attribute("id->su","href")
        """
        t1 = time.time()
        try:
            el = self.get_element(css)
            attr = el.get_attribute(attribute)
            self.my_print("{0} Get attribute element: <{1}>,attribute: {2}, Spend {3} seconds".format(success,
                css,attribute,time.time()-t1))
            return attr
        except Exception:
            self.my_print("{0} Unable to get attribute element: <{1}>,attribute: {2}, Spend {3} seconds".format(fail,
                css, attribute,time.time() - t1))
            raise

    def get_text(self, css):  # 获取指定元素的文本
        """
        Get element text information.

        Usage:
        driver.get_text("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            text = self.get_element(css).text
            self.my_print("{0} Get element text element: <{1}>, Spend {2} seconds".format(success,css,time.time()-t1))
            return text
        except Exception:
            self.my_print("{0} Unable to get element text element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def get_title(self):  # 获取浏览器的title
        """
        Get window title.

        Usage:
        driver.get_title()
        """

        t1 = time.time()
        title = self.driver.title
        self.my_print("{0} Get current window title, Spend {1} seconds".format(success, time.time() - t1))
        return title

    def get_url(self):  # 获取页面的url
        """
        Get the URL address of the current page.

        Usage:
        driver.get_url()
        """
        t1 = time.time()
        url = self.driver.current_url
        self.my_print("{0} Get current window url, Spend {1} seconds".format(success, time.time() - t1))
        return url

    def wait(self, secs):  # 显示等待implicitly_wait
        """
        Implicitly wait.All elements on the page.

        Usage:
        driver.wait(10)
        """
        t1 = time.time()
        self.driver.implicitly_wait(secs)
        self.my_print("{0} Set wait all element display in {1} seconds, Spend {2} seconds".format(success,
            secs,time.time() - t1))

    def blockUIWait(self):
        WebDriverWait(self.driver,10).until(EC.invisibility_of_element_located((By.CLASS_NAME,"blockUI blockOverlay")))
        # 判断蒙版是否可存在

    def clickable(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//input[@itemtext='科目']")))
        # 判断某个元素中是否可见并且是可以点击的
        # .ElementToBeClick(WebElement element) --->WebElement

    def accept_alert(self):  # 点击弹框的确定按钮
        """
        Accept warning box.

        Usage:
        driver.accept_alert()
        """
        t1 = time.time()
        self.driver.switch_to.alert.accept()
        # self.driver.switch_to_alert().accept()
        self.my_print("{0} Accept warning box, Spend {1} seconds".format(success, time.time() - t1))

    def dismiss_alert(self):# 点击弹框的取消按钮
        """
        Dismisses the alert available.

        Usage:
        driver.dismiss_alert()
        """
        t1 = time.time()
        self.driver.switch_to.alert.dismiss()
        self.my_print("{0} Dismisses the alert available, Spend {1} seconds".format(success, time.time() - t1))

    def switch_to_frame(self,css):#跳入iframe
        """
        Switch to the specified frame.

        Usage:
        driver.switch_to_frame("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            iframe_el = self.get_element(css)
            self.driver.switch_to.frame(iframe_el)
            self.my_print("{0} Switch to frame element: <{1}>, Spend {2} seconds".format(success,css,time.time()-t1))
        except Exception:
            self.my_print("{0} Unable switch to frame element: <{1}>, Spend {2} seconds".format(fail,css,time.time()-t1))
            raise

    def switch_to_frame_out(self):#跳出iframe
        """
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        Usage:
        driver.switch_to_frame_out()
        """
        t1 = time.time()
        self.driver.switch_to.default_content()
        self.my_print("{0} Switch to frame out, Spend {1} seconds".format(success, time.time() - t1))

    def switch_to_parent_iframe(self):
        t1 = time.time()
        self.driver.switch_to.parent_frame()
        self.my_print("{0} Switch to frame out, Spend {1} seconds".format(success, time.time() - t1))

    def open_new_window(self, css):#打开一个新窗口，句柄
        """
        Open the new window and switch the handle to the newly opened window.

        Usage:
        driver.open_new_window("id->kw")
        """
        t1 = time.time()
        try:
            original_windows = self.driver.current_window_handle
            el = self.get_element(css)
            el.click()
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != original_windows:
                    self.driver.switch_to.window(handle)
            self.my_print("{0} Click element: <{1}> open a new window and swich into, Spend {2} seconds".format(success,
                css,time.time() - t1))
        except Exception:
            self.my_print("{0} Click element: <{1}> open a new window and swich into, Spend {2} seconds".format(fail,
                css,time.time() - t1))
            raise

    def element_exist(self, css):#元素是否存在
        """
        judge element is exist,The return result is true or false.

        Usage:
        driver.element_exist("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            self.my_print("{0} Element: <{1}> is exist, Spend {2} seconds".format(success,css, time.time() - t1))
            return True
        except TimeoutException:
            self.my_print("{0} Element: <{1}> is not exist, Spend {2} seconds".format(fail, css, time.time() - t1))
            return False

    def take_screenshot(self, file_path):#截图
        """
        Get the current window screenshot.

        Usage:
        driver.take_screenshot('c:/test.png')
        """
        t1 = time.time()
        try:
            self.driver.get_screenshot_as_file(file_path)
            self.my_print("{0} Get the current window screenshot,path: {1}, Spend {2} seconds".format(success,
                file_path, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to get the current window screenshot,path: {1}, Spend {2} seconds".format(fail,
                file_path,time.time() - t1))
            raise

    def into_new_window(self):#
        """
        Into the new window.

        Usage:
        dirver.into_new_window()
        """
        t1 = time.time()
        try:
            all_handle = self.driver.window_handles
            flag = 0
            while len(all_handle) < 2:
                time.sleep(1)
                all_handle = self.driver.window_handles
                flag += 1
                if flag == 5:
                    break
            self.driver.switch_to.window(all_handle[-1])
            self.my_print("{0} Switch to the new window,new window's url: {1}, Spend {2} seconds".format(success,
                self.driver.current_url,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable switch to the new window, Spend {1} seconds".format(fail, time.time() - t1))
            raise

    def type_and_enter(self, css, text, secs=0.5):#输入文本框，并且按enter键
        """
        Operation input box. 1、input message,sleep 0.5s;2、input ENTER.

        Usage:
        driver.type_css_keys('id->kw','beck')
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            ele = self.get_element(css)
            ele.send_keys(text)
            time.sleep(secs)
            ele.send_keys(Keys.ENTER)
            self.my_print("{0} Element <{1}> type content: {2},and sleep {3} seconds,input ENTER key, Spend {4} seconds".format(
                success,css,text,secs,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable element <{1}> type content: {2},and sleep {3} seconds,input ENTER key, Spend {4} seconds".
                format(fail, css, text, secs, time.time() - t1))
            raise

    @property
    def origin_driver(self):#返回driver
        """
        Return the original driver,Can use webdriver API.

        Usage:
        driver.origin_driver
        """
        return self.driver



if __name__ == '__main__':
    driver = PySelenium("chrome",logger="")
