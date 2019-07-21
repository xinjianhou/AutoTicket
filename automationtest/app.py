#!/usr/bin/python3
# coding=utf-8

import time
from utils.DBUtil import DBUtil
from window.frame import MyFrame
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import base64
import requests
import re
import wx



class Automation():

    def __init__(self):

        self.coordinate = [[-40, -13], [-13, -13], [13, -13], [40, -13], [-40, 13], [-13, 13], [13, 13], [40, 13]]

        self.img_element = None
        self.result = None
        self.db = DBUtil()
    def login(self):

        browser_str = self.db.getBrowser()
        if browser_str == 'IE':
            self.browser = webdriver.Ie()
        elif browser_str == 'SAFARI':
            self.browser = webdriver.Safari()
        else:
            self.browser = webdriver.Chrome()

        # self.browser.set_window_size(1200, 900)
        self.browser.maximize_window()
        # self.browser.set_window_size()
        self.browser.get(self.db.getURL())

        time.sleep(2)
        self.browser.find_element_by_xpath('//a[@data-href="resources/login.html" and @name="g_href"]').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('login-hd-account').click()
        time.sleep(2)
        self.browser.find_element_by_id('J-userName').send_keys(self.db.getUserName())
        self.browser.find_element_by_id('J-password').send_keys(self.db.getPassword())

    def getVerifyImage(self):
        try:

            img_element = WebDriverWait(self.browser, 100).until(
                EC.presence_of_element_located((By.ID, "J-loginImg"))
            )

        except Exception as e:
            print(u"网络开小差,请稍后尝试" +str(e))
        base64_str = img_element.get_attribute("src").split(",")[-1]
        imgdata = base64.b64decode(base64_str)
        with open('verify.jpg', 'wb') as file:
            file.write(imgdata)

        self.img_element = img_element

    def getVerifyResult(self):

        url = "http://littlebigluo.qicp.net:47720/"
        response = requests.request("POST", url, data={"type": "1"}, files={'pic_xxfile': open('verify.jpg', 'rb')})
        result = []
        print(response.text)
        for i in re.findall("<B>(.*)</B>", response.text)[0].split(" "):
            result.append(int(i) - 1)
        self.result = result
        print(result)

    def moveAndClick(self):
        try:
            action = ActionChains(self.browser)

            for i in self.result:
                action.move_to_element(self.img_element).move_by_offset(self.coordinate[i][0],
                                                                        self.coordinate[i][1]).click()

            action.perform()

        except Exception as e:
            print('error occurs' + str(e))

    def submit(self):
        self.browser.find_element_by_id("J-login").click()

    def queryTicket(self):
        query_url = "https://kyfw.12306.cn/otn/leftTicket/init"
        self.browser.get(query_url)
        self.browser.execute_script("document.getElementById('fromStation').removeAttribute('type')")
        fromStation = self.browser.find_element_by_id("fromStation")
        fromStation.send_keys(self.db.getOrigin())
        self.browser.execute_script("document.getElementById('toStation').removeAttribute('type')")
        toStation = self.browser.find_element_by_id("toStation") 
        toStation.send_keys(self.db.getDes())
        self.browser.execute_script("document.getElementById('train_date').removeAttribute('readonly')")
        trainDate = self.browser.find_element_by_id("train_date")
        trainDate.clear()
        trainDate.send_keys(self.db.getDate())
        # if self.is_student:
        #     self.browser.find_element_by_id("sf2").click()
        # self.browser.find_element_by_id('avail_ticket').click()
        # self.browser.find_element_by_id('cc_start_time').send_keys('06001200')
        time.sleep(1)
        self.browser.find_element_by_id("query_ticket").click()


    def ticketOrder(self):
        # self.browser.find_element_by_id('avail_ticket').click()
        trains = self.browser.find_elements_by_class_name("number")
        self.browser.execute_script("document.getElementById('avail_ticket').checked")
        for i, item in enumerate(trains):
            print(item)
            print("【{}】{}".format(i, item.text))
        num = input("请输入预定车次编号：")
        print(num)
        self.browser.find_elements_by_class_name("btn72")[int(num)].click()
        ul = WebDriverWait(self.browser, 100).until(
            EC.presence_of_element_located((By.ID, "normal_passenger_id"))
        )
        time.sleep(1)
        lis = ul.find_elements_by_tag_name("li")
        for i, item in enumerate(lis):
            print("【{}】{}".format(i, item.find_elements_by_tag_name("label")[0].text))
        num = input("请输入购票人编号：")
        buy_num = int(num)
        lis[int(num)].find_elements_by_tag_name('input')[0].click()
        if self.is_student:
            self.browser.find_element_by_id("dialog_xsertcj_ok").click()
        else:
            self.browser.find_element_by_id("dialog_xsertcj_cancel").click()

        seatType = self.browser.find_element_by_id("seatType_1")

        for i, item in enumerate(self.type):
            print("【{}】{}".format(i, item))
        num = input("请输入座位类型：")
        code = self.type_code[int(num)]
        print("=======余票查询=======")
        count = 1
        flag = False
        while 1:
            print("第{}次查询".format(count))
            count += 1
            for i, item in enumerate(seatType.find_elements_by_tag_name("option")):
                if item.get_attribute("value") is code:
                    flag = True
                    item.click()
                    break;
            if flag:
                break;
            self.browser.back()
            time.sleep(1)
            self.browser.forward()
            # ================================================
            ul = WebDriverWait(self.browser, 100).until(
                EC.presence_of_element_located((By.ID, "normal_passenger_id"))
            )
            time.sleep(1.5)
            lis = ul.find_elements_by_tag_name("li")
            lis[buy_num].find_elements_by_tag_name('input')[0].click()
            if self.is_student:
                self.browser.find_element_by_id("dialog_xsertcj_ok").click()
            else:
                self.browser.find_element_by_id("dialog_xsertcj_cancel").click()
            seatType = self.browser.find_element_by_id("seatType_1")
        # ================================================

        self.browser.find_element_by_id("submitOrder_id").click()
        if code is "M" or code is "0":
            num = input("请输入座位编号：")
            for i, item in enumerate(self.position):
                print("【{}】{}".format(i, item))
            num = input("请输入座位编号：")
            id = "1" + self.position[int(num)]
            self.browser.find_element_by_id(id).click()
        time.sleep(1)
        isorder = input("已有余票,是否预订(【0】取消 【1】预定):")
        if int(isorder):
            self.browser.find_element_by_id("qr_submit_id").click()
            print("预定成功，请及时付款")
        else:
            print("Bye~")

    def buy_ticket(self):
        self.browser.execute_script("document.getElementById('avail_ticket').checked = true")

    def __call__(self, *args, **kwargs):
        app = wx.App()  # 初始化
        frame = MyFrame(parent=None, id=-1)  # 实例MyFrame类，并传递参数
        frame.Show()  # 显示窗口
        app.MainLoop()
        #time.sleep()
        if self.db.count() < 5:
            exit(1)
        self.login()

        self.getVerifyImage()
        # time.sleep(1)
        self.getVerifyResult()
        # time.sleep(1)
        self.moveAndClick()
        time.sleep(1)
        self.submit()
        time.sleep(3)
        self.queryTicket()
        time.sleep(1)
        self.buy_ticket()
        # self.ticketOrder()
        time.sleep(1000)


Automation()()
