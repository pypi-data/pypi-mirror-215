from tkinter import *
from tkinter import ttk
import pyautogui as pagui
import pyperclip
from PIL import Image, ImageTk
from PyQt5 import QtWidgets, uic
import time
import os
import datetime
import sys
if(sys.version[:1] == "3"):
    import _thread as thread
else:
    import thread 

class Page:
    def __init__(self):
        self.root
        self.wid
        self.hei
        self.can
        self.time
        
    def get_img(self):
        self.impath = '1.jpg'
        self.err = 1
        self.btnerr = 1
        try:
            img = Image.open(self.impath).resize((self.wid,self.hei))
            self.im = ImageTk.PhotoImage(img)
        except FileNotFoundError as e:
            print('请在文件目录添加1.jpg的背景图片!')
            self.err = 0
    def gettime(self):
        time = datetime.datetime
        endtime = time.today().strftime('%Y%m%d')
        self.time = endtime

    def setbg(self):
        #设置背景图片
        if self.err == 1:
            self.can = Canvas(self.root, width = self.wid, height = self.hei, bg='white')
            self.can.create_image(self.wid/2,self.hei/2,image = self.im)    #图片中心点位置
            self.can.grid(column=0,row=0)

    def getwinsize(self, root):
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
    
    def win_init(self, title=None, iconimg=None):
        self.get_img()
        self.setbg()
        self.getwinsize(self.root)
        screen_width = (self.screen_width - self.wid)/2
        screen_height = (self.screen_height - self.hei)/2
        try:
            if os.path.splitext(iconimg)[1] == '.png':
                png_image = Image.open(iconimg)
                 # 将图像转换为 ICO 格式
                png_image.save(os.path.splitext(iconimg)[0] + '.ico')
                iconimg = os.path.splitext(iconimg)[0] + '.ico'
           
            self.root.iconbitmap(iconimg)
        except:
            print('icon.ico not found')
        self.root.geometry(f'{self.wid}x{self.hei}+{int(screen_width)}+{int(screen_height)}')
        self.root.resizable(FALSE, FALSE)
        if title is not None:
            self.root.title(title)
        self.root.configure(bg='#BEEDC7')

class AutoWxGui(object):
    def __init__(self, mine = '文件传输助手'):
        self.mine = mine
        for tt in pagui.getWindowsWithTitle('微信'):
            if tt.title == '微信':
                self.wxwin = tt  
        self.width, self.height = pagui.size()
        self.midwid = (self.width-self.wxwin.width)/2
        self.midhei = (self.height-self.wxwin.height)/2
        print(self.wxwin)
        print("屏幕分辨率：",self.width, self.height)
        print("屏幕中心点:",self.midwid, self.midhei)

    def getWxPath(self):
        if os.path.exists('wechat_path.txt'):
            with open('wechat_path.txt', 'r') as f:
                wxpath = f.read()
                print(wxpath)
        else:
            root_dir = 'C:\\'  # 从根目录开始搜索，可以根据需要更改
            wechat_paths = []
            # 遍历文件系统 路径,文件夹名字,文件名
            for root, dirs, files in os.walk(root_dir):
                # print(root, dirs, files)
                for file in files:
                    if file.lower() == 'wechat.exe':
                        wechat_paths.append(os.path.join(root, file))
            # 打印找到的微信路径
            for wechat_path in wechat_paths:
                print(wechat_path)
            wxpath = '"' + wechat_paths[0].replace('\\', '/') + '"'
            with open('wechat_path.txt', 'w', encoding='utf-8') as f:
                f.write(''.join(wxpath))
        return wxpath

    def open_wechat(self):
        # wxpath = self.getWxPath()
        # pagui.hotkey('win', 'r')
        # pagui.typewrite('cmd')
        # pagui.press('enter')
        # pagui.press('enter')
        # time.sleep(1)
        # self.typewrite(wxpath)
        # pagui.press('enter')
        # time.sleep(1)  # 等待微信应用程序打开
        # pagui.moveTo(self.wxwin.left + 10, self.wxwin.top + 10)
        # pagui.dragTo(self.midwid, self.midhei,duration=0.5)
        # self.close_app("C:\\")
        pagui.keyDown('ctrl')
        pagui.keyDown('alt')
        pagui.press('w')
        pagui.keyUp('ctrl')
        pagui.keyUp('alt')
    
    def close_app(self, name):
        app = pagui.getWindowsWithTitle(name)[0]
        print('close ', app)
        pagui.click(app.left + 10, app.top + 10)
        time.sleep(0.5)
        pagui.hotkey('alt', 'f4')
        time.sleep(0.5)
        pagui.click(self.midwid+10, self.midhei+10)
        time.sleep(0.5)

    def typewrite(self, text):
        pyperclip.copy(text)
        pagui.keyDown('ctrl')
        pagui.press('v')
        pagui.keyUp('ctrl')
        # 添加适当的延迟，确保文本输入完全
        time.sleep(0.5)

    def search_chat(self, keyword):
        print('in search_chat')
        pagui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        self.typewrite(keyword)
        pagui.press('enter')
        print('search_chat finished')

    def send_msg(self, msg):
        pagui.hotkey('ctrl', 'a')
        time.sleep(1)
        self.typewrite(msg)
        pagui.press('enter')

    def msg_alarm(self, info):
        self.search_chat(self.mine)
        self.send_msg(info)

class MyQtApp(QtWidgets.QMainWindow):
    def __init__(self, UiFileName):
        self.app = QtWidgets.QApplication(sys.argv)
        super(MyQtApp, self).__init__()

        # 加载UI文件
        uic.loadUi(UiFileName, self)
        
        # 连接信号槽
        # self.startbut.clicked.connect(self.button_clicked)
        # self.stopbut.clicked.connect(self.close)
        self.show()

    # 按钮点击事件的槽函数
    def close(self):
        self.app.quit()
