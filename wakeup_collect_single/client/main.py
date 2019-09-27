#! /usr/bin/python
# coding=utf-8

import wx

import threading
import time
import datetime
import random
import struct
import os, sys
import iplist
import socket
import  requests
import logging


from ping_alive import ping_all,my_scan_port
import mycsv

g_local_debug = False
g_debug_only_one = False

all_machines_in_lan = []
machines_open_80_port = []
g_local_ip = ""
g_ipaddr_one = ""
g_ipaddr_three = ""
g_ipaddr_five = ""
g_recording = False
g_recorder_set_ok = False

g_recorder_id = ""
g_recorder_name = ""
g_recorder_age = ""
g_recorder_gender = ""
g_recorder_province = ""
g_recorder_time = ""

g_down_finish_one = False
g_down_finish_three = False
g_down_finish_five = False
g_cur_target_dir = "./"

MAX_WIDTH=1000
MAX_HEIGHT = 600
#logging.basicConfig(filename="./1.log", filemode='w', format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s", level=logging.DEBUG)

g_info_file = "./info.csv"

if not os.path.exists(g_info_file):
    mycsv.create_csv(g_info_file)

if not os.path.exists("./audio_files"):
    os.makedirs("./audio_files")


def start_record_thread(ip_addr):
    target = "http://{}/cgi-bin/index.sh".format(ip_addr)
    r = requests.get(url=target)

def download_audio_file(ip_addr):
    global g_recorder_id, g_recorder_name, g_recorder_age, g_recorder_gender, g_recorder_province
    global  g_ipaddr_one, g_ipaddr_three, g_ipaddr_five
    global  g_recording, g_cur_target_dir
    global g_down_finish_one, g_down_finish_three, g_down_finish_five

    target = "http://{}/cgi-bin/output/{}.pcm".format(ip_addr, g_recorder_id)
    # print(target)
    filename="{}.pcm".format(g_recorder_id)
    try:
        r = requests.get(url=target, stream=False)
        local_file = ""
        if ip_addr == g_ipaddr_one:
            local_file = "{}/1m/{}".format(g_cur_target_dir,filename)
        if ip_addr == g_ipaddr_three:
            local_file = "{}/3m/{}".format(g_cur_target_dir,filename)
        if ip_addr == g_ipaddr_five:
            local_file = "{}/5m/{}".format(g_cur_target_dir,filename)
        f = open(local_file, "wb")
        f.write(r.content)
        f.close()
    except:
        logging.error('download {} fail'.format(target))

class MainWindow(wx.Frame):
    def __init__(self):
        self.initGlobalData()

        wx.Frame.__init__(
            self, None, title='DOSS语料采集工具', size=(MAX_WIDTH, MAX_HEIGHT))
        self.SetMaxSize((MAX_WIDTH,MAX_HEIGHT))
        self.ui_main()
        self.Show(True)

    def __del__(self):
        pass

    def initGlobalData(self):
        pass


    def ui_main(self):
        panel = wx.Panel(self)
        color = panel.GetBackgroundColour()
        self.SetBackgroundColour(color)

        layout_main = wx.BoxSizer(wx.VERTICAL)
        layout_upper = self.ui_upper()

        layout_top = self.ui_top()
        layout_middle = self.ui_middle()
        layout_bottom = self.ui_bottom()
        layout_status_bar = self.ui_status_bar()
        layout_main.Add(layout_upper, 0, wx.EXPAND | wx.ALL, 4)
        layout_main.Add(layout_top, 0, wx.EXPAND | wx.ALL, 4)
        layout_main.Add(layout_middle, 0, wx.EXPAND | wx.ALL, 4)
        layout_main.Add(layout_bottom, 0, wx.EXPAND | wx.ALL, 4)
        layout_main.Add(layout_status_bar, 0, wx.EXPAND | wx.ALL, 4)
        global g_local_ip
        # g_local_ip = get_host_ip()
        g_local_ip = socket.gethostbyname(socket.gethostname())
        self.statusText.SetValue("本机ip地址：{}".format(g_local_ip))

        self.SetSizer(layout_main)

        # self.updateInfo()
    def ui_upper(self):
        layout_upper = wx.BoxSizer(wx.HORIZONTAL)
        layout_upper.AddSpacer(50)
        self.btnDetect = wx.Button(self, wx.NewId(), '发现设备')
        self.Bind(wx.EVT_BUTTON, self.onBtnDetect, self.btnDetect)
        layout_upper.Add(self.btnDetect, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        labelHint = wx.StaticText(self, label="这一步比较耗时，执行时界面会无响应只需要执行一次，请耐心等待")
        layout_upper.Add(labelHint, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_upper.AddSpacer(50)
        return layout_upper

    def ui_middle(self):
        ip_1m = "192.168.31.154"
        ip_3m = "192.168.31.149"
        ip_5m = "192.168.31.61"
        layout_middle = wx.BoxSizer(wx.VERTICAL)

        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1_title = wx.StaticText(self, label="1m机器：")

        self.row1_status = wx.StaticText(self, label="    离线")
        self.row1_ipaddr = wx.TextCtrl(self, value=ip_1m)

        row1.Add(row1_title, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        row1.Add(self.row1_status, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        row1.Add(self.row1_ipaddr, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_middle.Add(row1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_middle.AddSpacer(32)

        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2_title = wx.StaticText(self, label="3m机器：")

        self.row2_status = wx.StaticText(self, label="    离线")
        self.row2_ipaddr = wx.TextCtrl(self, value=ip_3m)
        row2.Add(row2_title, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        row2.Add(self.row2_status, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        row2.Add(self.row2_ipaddr, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        layout_middle.Add(row2, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        layout_middle.AddSpacer(32)

        row3 = wx.BoxSizer(wx.HORIZONTAL)
        row3_title = wx.StaticText(self, label="5m机器：")

        self.row3_status = wx.StaticText(self, label="    离线")
        self.row3_ipaddr = wx.TextCtrl(self,value=ip_5m)
        row3.Add(row3_title, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        row3.Add(self.row3_status, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        row3.Add(self.row3_ipaddr, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        layout_middle.Add(row3, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        layout_middle.AddSpacer(50)

        return layout_middle

    def ui_top(self):
        ITEM_SPACE=10
        layout_top = wx.BoxSizer(wx.HORIZONTAL)

        labelId = wx.StaticText(self, label='录音者ID：')

        self.recorder_id = wx.TextCtrl(self, value="001")
        layout_top.Add(labelId, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.Add(self.recorder_id, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        # self.choice_port_sel.SetSelection(self.port_no)
        layout_top.AddSpacer(ITEM_SPACE)

        labelName = wx.StaticText(self, label='名字：')
        self.recorder_name = wx.TextCtrl(self, value="张三")
        layout_top.Add(labelName, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.Add(self.recorder_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        # self.choice_port_sel.SetSelection(self.port_no)
        layout_top.AddSpacer(ITEM_SPACE)

        labelRecorderAge = wx.StaticText(self, label='年龄：')
        self.recorder_age = wx.TextCtrl(self,value="28")
        layout_top.Add(labelRecorderAge, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.Add(self.recorder_age, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.AddSpacer(ITEM_SPACE)

        labelRecorderGender = wx.StaticText(self, label='性别：')
        self.recorder_gender = wx.TextCtrl(self, value="1")
        layout_top.Add(labelRecorderGender, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.Add(self.recorder_gender, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.AddSpacer(ITEM_SPACE)

        labelRecorderProvince = wx.StaticText(self, label="省份：")
        self.recorder_province = wx.TextCtrl(self, value="hunan")
        layout_top.Add(labelRecorderProvince, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.Add(self.recorder_province, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.AddSpacer(ITEM_SPACE)

        # labelRecorderTime = wx.StaticText(self, label="时长：")
        # self.recorder_time = wx.TextCtrl(self, value="5")
        # layout_top.Add(labelRecorderTime, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        # layout_top.Add(self.recorder_time, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        # layout_top.AddSpacer(ITEM_SPACE)

        self.btnFillInfo = wx.Button(self, wx.NewId(), '填入信息')
        self.Bind(wx.EVT_BUTTON, self.onBtnFillInfo, self.btnFillInfo)
        layout_top.Add(self.btnFillInfo, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        layout_top.AddSpacer(50)

        return layout_top

    def ui_bottom(self):
        layout_bottom = wx.BoxSizer(wx.HORIZONTAL)
        self.btnStartRecord = wx.Button(self, wx.NewId(), '开始测试')
        layout_bottom.Add(self.btnStartRecord, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.btnDownload = wx.Button(self, wx.NewId(), '停止录音并下载文件到电脑，然后手动拷贝手机文件到电脑目录下')
        layout_bottom.Add(self.btnDownload, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.Bind(wx.EVT_BUTTON, self.onStartRecord, self.btnStartRecord)
        self.Bind(wx.EVT_BUTTON, self.onBtnDownload, self.btnDownload)
        return layout_bottom

    def onBtnDownload(self, event):
        # 现在修改逻辑为：先停止录音，再下载文件，再删除文件，三步走。
        # 如何下载？
        # 先下载1m的，再是3m，再是5m。
        # 三台机器的，用3个线程来下载
        global  g_ipaddr_one, g_ipaddr_three, g_ipaddr_five
        global  g_recording
        if  g_ipaddr_one == "" or  g_ipaddr_three == "" or g_ipaddr_five == "" :
            self.statusText.SetValue("必须所有机器上线才能尝试下载文件")
            return
        #
        if not g_recording:
            self.statusText.SetValue("当前并没有在录音")
            return
        # 停止录音
        # 方式是通过发送命令给板端，
        target = "http://{}/cgi-bin/stop_record.sh".format(g_ipaddr_one)
        requests.get(url=target)
        target = "http://{}/cgi-bin/stop_record.sh".format(g_ipaddr_three)
        requests.get(url=target)
        target = "http://{}/cgi-bin/stop_record.sh".format(g_ipaddr_five)
        requests.get(url=target)
        self.statusText.SetValue("已经停止录音，开始下载文件")
        g_recording = False
        global  g_down_finish_one, g_down_finish_three, g_down_finish_five
        g_down_finish_one = False
        g_down_finish_three= False
        g_down_finish_five = False
        t1 = threading.Thread(target=download_audio_file, args=(g_ipaddr_one,))
        t2 = threading.Thread(target=download_audio_file, args=(g_ipaddr_three,))
        t3 = threading.Thread(target=download_audio_file, args=(g_ipaddr_five,))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()

        self.statusText.SetValue("下载文成，正在自动删除板端的录音文件")
        # 这个也做一个脚本
        try:
            target = "http://{}/cgi-bin/delete_audio.sh".format(g_ipaddr_one)
            r = requests.get(url=target)
            target = "http://{}/cgi-bin/delete_audio.sh".format(g_ipaddr_three)
            r = requests.get(url=target)
            target = "http://{}/cgi-bin/delete_audio.sh".format(g_ipaddr_five)
            r = requests.get(url=target)
        except:
            self.statusText.SetValue("删除失败，下次再删除，删除只是为了避免设备端flash被占满")
            return
        self.statusText.SetValue("删除板端文件完成，请手动拷贝手机上的文件到对应目录下。")


    def onStartRecord(self, event):
        global  g_ipaddr_one, g_ipaddr_three, g_ipaddr_five
        global  g_recording
        if  g_ipaddr_one == "" or  g_ipaddr_three == "" or g_ipaddr_five == "" :
            self.statusText.SetValue("必须所有机器上线才能开始测试")
            return
        if g_recording:
            self.statusText.SetValue("正在录音，请等待录音完成")
            return


        # 同时给3台机器发送http://ip/record.sh
        t1 = threading.Thread(target=start_record_thread, args=(g_ipaddr_one,))
        t2 = threading.Thread(target=start_record_thread, args=(g_ipaddr_three,))
        t3 = threading.Thread(target=start_record_thread, args=(g_ipaddr_five,))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        g_recording = True

    def onBtnDetect(self,event):
        self.statusText.SetValue("正在发现设备，请耐心等待，不要关闭窗口。")

        # 然后根据本机ip所在网段，把所有alive的ip拿到。
        # all_machines_in_lan =  ping_all(g_local_ip)
        # self.statusText.SetValue("局域网扫描完成，所有活跃IP为：".format(all_machines_in_lan))
        # print("get all ip ok")
        # print(all_machines_in_lan)
        # global machines_open_80_port
        # # 还必须先扫描端口，端口80打开的才进行连接测试。
        # for ip_addr in all_machines_in_lan:
        #     if my_scan_port(ip_addr, 80):
        #         machines_open_80_port.append(ip_addr)

        # if len(machines_open_80_port)==0:
        #     self.statusText.SetValue("没有找到打开了80端口的机器")
        #     return

        global g_ipaddr_one, g_ipaddr_three, g_ipaddr_five
        g_ipaddr_one = ""
        g_ipaddr_three = ""
        g_ipaddr_five = ""

        # 检查3个ip地址是否都已经填写了。
        if self.row1_ipaddr.GetValue().strip()=="" or  self.row2_ipaddr.GetValue().strip()=="" or self.row3_ipaddr.GetValue().strip()=="":
            self.statusText.SetValue("请正确填写ip地址")
            return
        ip_addr = self.row1_ipaddr.GetValue()
        target_url = "http://{}/cgi-bin/machine_name.sh".format(ip_addr)
        resp = requests.get(target_url)
        print(resp.text)
        if resp.text.find('one')==0:
            g_ipaddr_one = ip_addr
        else:
            self.statusText.SetValue("1m机器异常")
            return

        ip_addr = self.row2_ipaddr.GetValue()
        target_url = "http://{}/cgi-bin/machine_name.sh".format(ip_addr)
        resp = requests.get(target_url)
        print(resp.text)
        if resp.text.find('three')==0:
            g_ipaddr_three= ip_addr
        else:
            self.statusText.SetValue("3m机器异常")
            return
        ip_addr = self.row3_ipaddr.GetValue()
        target_url = "http://{}/cgi-bin/machine_name.sh".format(ip_addr)
        resp = requests.get(target_url)
        print(resp.text)
        if resp.text.find('five')==0:
            g_ipaddr_five = ip_addr
        else:
            self.statusText.SetValue("5m机器异常")
            return

        self.statusText.SetValue("所有设备都已经上线了")
        # 把ip地址展示到ui界面上，并且把状态设置为上线。
        if g_ipaddr_one:
            self.row1_status.SetLabel(" 在线 ")
        if g_ipaddr_three:
            self.row2_status.SetLabel(" 在线 ")
        if g_ipaddr_five:
            self.row3_status.SetLabel(" 在线 ")

    def ui_status_bar(self):
        status_bar = wx.BoxSizer(wx.VERTICAL)
        hintLabel = wx.StaticText(self, label="""
            说明：
            录音者ID：001,3位，不足的高位补零。
            性别：男的写1，女的写0。
            省份：写全拼，全部小写。例如湖南写：hunan。
            时长：默认时长是5秒。如果觉得太短，可以进行调整。
        """)
        status_bar.Add(hintLabel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.statusText = wx.TextCtrl(self, value="" , style = wx.BORDER_SIMPLE | wx.TE_MULTILINE | wx.HSCROLL, size=(MAX_WIDTH,200))
        status_bar.Add(self.statusText, 0, wx.ALIGN_LEFT, 0)
        return status_bar
    def onBtnFillInfo(self, event):
        global g_ipaddr_one, g_ipaddr_three, g_ipaddr_five
        global  g_recording
        global  g_recorder_set_ok
        global  g_local_debug
        g_recorder_set_ok = False
        if not g_local_debug:
            if  g_ipaddr_one == "" or  g_ipaddr_three == "" or g_ipaddr_five == "" :
                self.statusText.SetValue("必须所有机器上线才能设置信息")
                return
        if g_recording:
            self.statusText.SetValue("正在录音，请等待录音完成")
            return
        # 检查设置内容
        if self.recorder_id.GetValue().strip() == "":
            self.statusText.SetValue("id不能为空")
            return
        if self.recorder_age.GetValue().strip() == "":
            self.statusText.SetValue("年龄不能为空")
            return
        if self.recorder_gender.GetValue().strip() == "":
            self.statusText.SetValue("性别不能为空")
            return
        if self.recorder_province.GetValue().strip() == "":
            self.statusText.SetValue("省份不能为空")
            return
        # if self.recorder_time.GetValue().strip() == "":
        #     self.statusText.SetValue("时长不能为空")
        #     return
        id = self.recorder_id.GetValue().strip()
        name = self.recorder_name.GetValue().strip()
        age = self.recorder_age.GetValue().strip()
        gender = self.recorder_gender.GetValue().strip()
        province = self.recorder_province.GetValue().strip()
        # time_len = self.recorder_time.GetValue().strip()
        time_len = "5"
        global g_recorder_id, g_recorder_name, g_recorder_age, g_recorder_gender, g_recorder_province, g_recorder_time
        g_recorder_id = id
        g_recorder_name = name
        g_recorder_age = age
        g_recorder_gender = gender
        g_recorder_province = province
        g_recorder_time = time
        self.statusText.SetValue("")
        try:
            if not g_local_debug:
                pattern="http://{}"  + "/cgi-bin/set_recorder.sh?id=" + id + "&age=" + age + "&gender=" + gender + "&province=" + province + "&time=" + time_len
                url = pattern.format(g_ipaddr_one)
                r = requests.get(url=url)
                url=pattern.format(g_ipaddr_three)
                r = requests.get(url=url)
                url=pattern.format(g_ipaddr_five)
                r = requests.get(url=url)
                g_recorder_set_ok = True
            # 把信息保存到csv文件里
            global g_info_file
            mycsv.append_csv(g_info_file, [id, name, age, gender, province])
            self.statusText.SetValue("设置信息成功")
            # 开始录音时，需要创建对应的目录。
            #
            """
            目录结构示例：
            001_1_28_hunan
                1m
                    001.pcm
                3m
                    001.pcm
                5m
                    001.pcm
                mobile
                    *.pcm
                    *.txt
            """

            global g_cur_target_dir
            top_dir = "./audio_files/{}_{}_{}_{}".format(g_recorder_id, g_recorder_gender, g_recorder_age, g_recorder_province)
            g_cur_target_dir = top_dir

            if not os.path.exists(top_dir):
                os.makedirs(top_dir)
            if not os.path.exists("{}/1m".format(top_dir)):
                os.makedirs("{}/1m".format(top_dir))
            if not os.path.exists("{}/3m".format(top_dir)):
                os.makedirs("{}/3m".format(top_dir))
            if not os.path.exists("{}/5m".format(top_dir)):
                os.makedirs("{}/5m".format(top_dir))
            if not os.path.exists("{}/mobile".format(top_dir)):
                os.makedirs("{}/mobile".format(top_dir))
        except:
            self.statusText.SetValue("设置信息出错了，请重试一下")


class RecordToolApp(wx.App):
    def OnInit(self):
        frame = MainWindow()
        return True


app = RecordToolApp()
app.MainLoop()
