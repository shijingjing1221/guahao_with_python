#!/usr/bin/python
# -*- coding: UTF8 -*-

"""
A simple selenium test example written by python
"""


import unittest
import re
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json

import sys
defaultencoding = 'utf8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
        print sys.getdefaultencoding()
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(10)
        f = open("Settings.json") 
        self.settings = json.load(f)
        self.wait_default_second = self.settings['wait_default_second']

    # def test_print_setting(self):
    #     print "================"
    #     print self.settings['name'].decode("utf-8")

    def tearDown(self):
        """Stop web driver"""
        # self.driver.quit()

    # def loadSettings(self):
    #     f = open("Settings.json") 
    #     settings = json.load(f)
    #     return settings
 

    def waitAndClickByXpath(self, xpath):
         driver = self.driver
         WebDriverWait(driver, self.wait_default_second).until(
            lambda driver: driver.find_element_by_xpath(xpath))
         el = driver.find_element_by_xpath(xpath)
         el.click()

    def waitAndClickLastByXpath(self, xpath):
         driver = self.driver
         WebDriverWait(driver, self.wait_default_second).until(
            lambda driver: driver.find_elements_by_xpath(xpath))
         elements = driver.find_elements_by_xpath(xpath)
         length = len(elements)
         el = elements[length - 1]
         el.click()
    
    def waitAndClickByCss(self, selector):
         driver = self.driver
         WebDriverWait(driver, self.wait_default_second).until(
            lambda driver: self.driver.find_element_by_css_selector(selector))
         el = self.driver.find_element_by_css_selector(selector)
         el.click()

    def waitAndClickSelectByCss(self, selector, value):
        driver = self.driver
        WebDriverWait(driver, self.wait_default_second).until(
            lambda driver: self.driver.find_element_by_css_selector(selector))
        driver.find_element_by_css_selector(selector).find_element_by_xpath("//option[@value='" +value+ "']").click()


    def waitAndSendKey(self, selector, sendKeysValue):
         driver = self.driver 
         WebDriverWait(driver, self.wait_default_second).until(
            lambda driver: self.driver.find_elements_by_css_selector(selector))
         el = self.driver.find_elements_by_css_selector(selector)[0]
         el.send_keys(sendKeysValue)
        #   elem.send_keys(Keys.RETURN)


    def waitAndSendKeyWithChinese(self, selector, sendKeysValue):
         driver = self.driver 
         WebDriverWait(driver, self.wait_default_second).until(
            lambda driver: self.driver.find_elements_by_css_selector(selector))
         el = self.driver.find_elements_by_css_selector(selector)[0]
         el.send_keys(sendKeysValue.decode("utf-8"))
        #   elem.send_keys(Keys.RETURN)

    def waitAndClickByLinkText(self, link_text):
        driver = self.driver 
        WebDriverWait(driver, self.wait_default_second).until(
            lambda driver: self.driver.find_element_by_link_text(link_text.decode("utf-8")))
        el = driver.find_element_by_link_text(link_text.decode("utf-8"))
        el.click()



    def test_guahao(self):
        login_phone = self.settings['login_phone']
        login_pass = self.settings['login_pass']
        hospital =  self.settings['hospital'].decode("utf-8")
        department =  self.settings['department'].decode("utf-8")
        url="http://www.114yygh.com/index.htm"
        self.driver.get(url)  

        self.waitAndClickByCss("#bdtj1")
        self.waitAndSendKey("#mobileNo", login_phone)
        self.waitAndClickByCss("#login_1")
        self.waitAndClickByCss("#pwd_login")
        self.waitAndSendKey("#pwd", login_pass)
        self.waitAndClickByCss("#loginStep2_pwd")
        self.waitAndSendKeyWithChinese("#words", hospital)
        self.waitAndClickByCss(".searchBox input:nth-child(3)")
        self.waitAndClickByLinkText(hospital)
        self.waitAndClickByLinkText(department)

        #等待今天放号码
        youhao_xpath='//span[text()="有号"]'.decode("utf-8")
        #driver.find_elements_by_xpath(xpath)
        #self.waitAndClickByXpath()
        youhao_loaded=False
        refresh_count=0
        while youhao_loaded==False:
            try:
                refresh_count = refresh_count + 1
                WebDriverWait(self.driver, self.wait_default_second).until(
                     lambda driver: self.driver.find_element_by_xpath(youhao_xpath))
                youhao_el = self.driver.find_element_by_xpath(youhao_xpath)
                youhao_el.click()
                youhao_loaded = True

            except:
                self.driver.refresh()
                time.sleep(10)
                print "%d times refresh" %(refresh_count)
            finally:
                print "finally"


        self.waitAndClickLastByXpath('//div[@id="ksorder_djgh_doctor"]//a[text()="预约挂号"]'.decode("utf-8"))
        self.waitAndClickSelectByCss('#Rese_db_dl_idselect', '1')
        self.waitAndClickByCss("#send_sms_code_btn")
        time.sleep(5)
        self.driver.switch_to_alert().accept();
        #self.driver.switch_to_window();
        
        #等待输入验证码
        founded = False
        while founded == False:
            sms_el = self.driver.find_element_by_css_selector("#sms_code")
            if sms_el:
                sms_code = sms_el.get_attribute('value')
                if len(sms_code) == 6:
                    founded = True
        #点击预约按钮
        self.waitAndClickByCss("#Rese_db_qryy_btn_v1")

        # self.waitAndClickByXpath('//span[text()="有号"]'.decode("utf-8"))

  
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    unittest.TextTestRunner(verbosity=2).run(suite)
