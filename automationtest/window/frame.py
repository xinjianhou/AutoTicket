#!/usr/bin/python3
# coding=utf-8

import wx
import wx.adv
from utils.DBUtil import DBUtil
from utils.StationUtil import Station
import os
from datetime import datetime


class MyFrame(wx.Frame):

    def __init__(self, parent, id):
        self.message = ""
        self.frame= wx.Frame.__init__(self, parent, id, '自助购票', size=(800, 700))
        panel = wx.Panel(self)
        title_font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        info_font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        panel.BackgroundColour = 'Yellow'

        self.bt_confirm = wx.Button(panel, label='确定')
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
        self.bt_cancel = wx.Button(panel, label='清除')
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)
        # 创建文本，左对齐
        self.title = wx.StaticText(panel, label="请输入用户名和密码")
        self.title.SetFont(title_font)
        self.label_user = wx.StaticText(panel, label="用户名:")
        self.text_user = wx.TextCtrl(panel, style=wx.TE_RICH2)
        # self.text_user.SetDefaultStyle(wx.TextAttr(wx.YELLOW))
        self.label_pwd = wx.StaticText(panel, label="密   码:")
        self.text_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)

        self.sub_title = wx.StaticText(panel, label="请输入订票信息")
        self.title.SetFont(title_font)
        self.label_ori = wx.StaticText(panel, label="始发站:")
        self.text_ori = wx.TextCtrl(panel, style=wx.TE_RICH2)
        # self.text_user.SetDefaultStyle(wx.TextAttr(wx.YELLOW))
        self.label_des = wx.StaticText(panel, label="目的地:")
        self.text_des = wx.TextCtrl(panel, style=wx.TE_RICH)
        self.label_date = wx.StaticText(panel, label="出发日期:")
        self.text_date = wx.TextCtrl(panel, style=wx.TE_RICH)
        self.text_date.SetValue(datetime.now().strftime('%Y-%m-%d'))
        # 添加容器，容器中控件按横向并排排列
        hsizer_user = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_user.Add(self.label_user, proportion=0, flag=wx.ALL, border=5)
        hsizer_user.Add(self.text_user, proportion=1, flag=wx.ALL, border=5)
        # hsizer_pwd = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_user.Add(self.label_pwd, proportion=0, flag=wx.ALL, border=5)
        hsizer_user.Add(self.text_password, proportion=1, flag=wx.ALL, border=5)

        hsizer_ticket = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_ticket.Add(self.label_ori, proportion=0, flag=wx.ALL, border=5)
        hsizer_ticket.Add(self.text_ori, proportion=1, flag=wx.ALL, border=5)

        hsizer_ticket.Add(self.label_des, proportion=0, flag=wx.ALL, border=5)
        hsizer_ticket.Add(self.text_des, proportion=1, flag=wx.ALL, border=5)

        hsizer_ticket.Add(self.label_date, proportion=0, flag=wx.ALL, border=5)
        hsizer_ticket.Add(self.text_date, proportion=1, flag=wx.ALL, border=5)

        hsizer_button = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_button.Add(self.bt_confirm, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        hsizer_button.Add(self.bt_cancel, proportion=0, flag=wx.ALIGN_CENTER, border=5)

        self.statictext = wx.StaticText(panel, label='发车时间：')
        list1 = ['00:00-06:00', '06:00-12:00', "12:00-18:00", "18:00-24:00"]
        self.ch1 = wx.ComboBox(panel, -1, value='00:00-24:00', choices=list1)
        # 添加事件处理
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox, self.ch1)

        hsizer_ticket.Add(self.statictext, proportion=0, flag=wx.ALL, border=5)
        hsizer_ticket.Add(self.ch1, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE, border=5)

        # 添加容器，容器中控件按纵向并排排列
        vsizer_all = wx.BoxSizer(wx.VERTICAL)
        vsizer_all.Add(self.title, proportion=0, flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER,
                       border=15)
        vsizer_all.Add(hsizer_user, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(self.sub_title, proportion=0, flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER,
                       border=15)
        vsizer_all.Add(hsizer_ticket, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(hsizer_button, proportion=0, flag=wx.ALIGN_CENTER | wx.TOP, border=15)
        panel.SetSizer(vsizer_all)

    def on_combobox(self, event):
        print("选择{0}".format(event.GetString()))

    def on_choice(self, event):
        print("选择{0}".format(event.GetString()))

    def OnclickSubmit(self, event):
        station = Station()
        db = DBUtil()
        """ 点击确定按钮，执行方法 """

        if (os.path.exists(station.dirPath + "result.txt")):
            pass
        else:
            station.send_request()

        username = self.text_user.GetValue()  # 获取输入的用户名
        password = self.text_password.GetValue()  # 获取输入的密码
        if username == "" or password == "":  # 判断用户名或密码是否为空
            wx.MessageBox('用户名或密码不能为空')
        # elif username == 'admin' and password == '123456':  # 用户名和密码正确
        #     self.message = '登录成功'
        # else:
        #     self.message = '用户名和密码不匹配'  # 用户名或密码错误
        # 弹出提示框
        else:
            DBUtil.setUser(db, username, password)

        origin = self.text_ori.GetValue()
        destination = self.text_des.GetValue()
        travel_date = self.text_date.GetValue()
        if self.ch1.GetValue()=='00:00-06:00':
            travel_time = '00000600'
        elif self.ch1.GetValue()=='06:00-12:00':
            travel_time = '06001200'
        elif self.ch1.GetValue() == '12:00-18:00':
            travel_time = '12001800'
        elif self.ch1.GetValue() == '18:00-24:00':
            travel_time = '18002400'
        else:
            travel_time = '00002400'

        if origin == "" or destination == "":
            wx.MessageBox('请输入订票信息')
            return False
        elif None == station.get_station(origin) or None == station.get_station(destination):
            wx.MessageBox('请输入正确的城市名称')
            return False
        else:
            try:
                datetime.strptime(travel_date, '%Y-%m-%d')
            except ValueError as error:
                wx.MessageBox('请输入正确正确的日期 像2019-12-01')
                return False
            DBUtil.setTiket(db, station.get_station(origin), station.get_station(destination), travel_date, travel_time)
        if db.count() > 5:
            self.Close(True)

    def OnclickCancel(self, event):  # 没有event点击取消会报错
        """ 点击取消按钮，执行方法 """
        self.text_user.SetValue("")  # 清空输入的用户名
        self.text_password.SetValue("")  # 清空输入的密码

# if __name__ == '__main__':
#     app = wx.App()  # 初始化
#     frame = MyFrame(parent=None, id=-1)  # 实例MyFrame类，并传递参数
#     frame.Show()  # 显示窗口
#     app.MainLoop()
