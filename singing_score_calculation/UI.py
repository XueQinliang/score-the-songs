# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:09:24 2019

@author: 李方怡
"""
import tkinter as tk
from mp3towav import easymp3towav
from sqc_comparison import CoconutScore
from play_record import *
from show_lrc_with_time import *
import pygame
import threading
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import time

class MyDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        top = self.top
        tk.Label(top, text="Value").pack()
        self.e = tk.Entry(top)
        self.e.pack(padx=5)
        b = tk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
    def ok(self):
        print("value is", self.e.get())
        self.top.destroy()

class Dialog(tk.Toplevel):
    def __init__(self, parent, text, title, colour):
        self.top = tk.Toplevel.__init__(self, parent)
        self.colour = colour
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack()
        tk.Label(body, text=text,
                 font=('Comic Sans MS',20),fg=colour).pack()
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+600,
                                  parent.winfo_rooty()+300))
        self.initial_focus.focus_set()
        self.wait_window(self)
    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = tk.Frame(self)
        w = tk.Button(box, text="OK", width=8, command=self.ok, default=tk.ACTIVE,
                      font=('Comic Sans MS',12), fg='white' ,bg=self.colour)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        #w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        #w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        #self.bind("<Escape>", self.cancel)
        box.pack()
    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()
    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
    #
    # command hooks
    def validate(self):
        return 1 # override
    def apply(self):
        pass # override

var = 'test.mid'
wavvar = 'test.wav'
playing = False
# 第1步，实例化object，建立窗口window
window = tk.Tk()
window.resizable(0,0)
window.wm_state('zoomed') #默认最大化
#插入背景图片
im = Image.open('timg1.jpg')#'C:\\Users\\李方怡\\Desktop\\SLP\\timg1.jpg'
img = ImageTk.PhotoImage(im.resize((1550,900),Image.ANTIALIAS))
imLabel = tk.Label(window,image=img).pack()
#建立输出文本框
scroll = tk.Scrollbar()
lrc = tk.Text(window, font=('Comic Sans MS',30), fg='white',bg='BlueViolet')
scroll.pack(side=tk.RIGHT,fill=tk.Y) # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
lrc.pack(side=tk.LEFT,fill=tk.Y) # 将文本框填充进wuya窗口的左侧，
# 将滚动条与文本框关联
scroll.config(command=lrc.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
lrc.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框
lrc.place(rely=0.7,relx=0.3, relwidth=0.4, relheight=0.15)

txt = tk.Text(window, font=('Comic Sans MS',20), fg='white',bg='BlueViolet')
txt.place(rely=0.85,relx=0.3, relwidth=0.4, relheight=0.05)
# 第2步，给窗口的可视化起名字
window.title('音准检测')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('1550x900')  # 这里的乘是小x
################设置上传音频文件的控件###############################
# 第5步，定义点击upload file时触发的函数i
def upload_file(): # 在鼠标焦点处插入输入内容
    global var
    global wavvar
    global window
    uppath = filedialog.askopenfilename()
    if uppath == r'':
        return
    wavvar = uppath
    #tk.messagebox.showinfo(title='hi',message='so this is a msgbox')
    var = wavvar#var就会得到选择的文件
    filename = var.split('/')[-1]
    if filename[-3:] == 'wav':
        pass
    elif filename[-3:] == 'mp3':
        easymp3towav(var)
        var = var[:-3] + "wav"
        wavvar = var
    else:
        Dialog(window,"   Not supported file format!   ","Some Error", "Crimson")
        return
    window.update()
    Dialog(window,"    Upload Successfully    ","Upload Info", "orange")
    midiname = filename[:-3] + "mid"
    if not os.path.exists("../melody/"+midiname) or midiname == 'test.wav':
        os.popen("wav2midi.exe "+var)
        var = var.replace('/','\\')
        while not os.path.exists(var[:-3]+"mid"):
            #等待转换完毕
            pass
        #tk.messagebox.askquestion(title='Success', message='Recording has completed')
        os.popen("move "+var[:-3]+"mid"+" ../melody/")
    var = "../melody/"+midiname
    print(var) #var现在为wav转成的mid文件的相对路径

def dynamic_show_lrc(lrc_path):
    lrclist = load_lrc(lrc_path)
    time_start = time.time()
    line = 0
    window.update()
    lrc.mark_set("insert", "%d.%d" % (1, 0))
    while True:
        if line >= len(lrclist):
            break
        nowtime = time.time() - time_start
        if nowtime > 20:
            break
        if nowtime < lrclist[line][0]:
            pass
        else:
            print(nowtime,lrclist[line][1])
            lrc.delete(lrc.index('insert'),)
            lrc.insert(tk.INSERT,lrclist[line][1],'color')
            window.update()
            line += 1
    lrc.mark_set("insert", "%d.%d" % (1, 0))
    
def Play_record():
    songname = ''
    try:
        songname = lb.get(lb.curselection())
    except:
        Dialog(window,"   Please Choose one song!   ","Some Error", "Crimson")
        return
    print(songname)
    play_record(songname)
    lrc_path = "../lrc/"+songname+".lrc"
    lrc.delete(0.0,tk.END)
    lrclist = load_lrc(lrc_path)
    for i in lrclist:
        lrc.insert(tk.END, i[1])
    dynamic_show_lrc(lrc_path)
    window.update()
    d = Dialog(window,"    Record Successfully    ","Record Info", "orange")
    global var
    var = "test.mid"
    global wavvar
    wavvar = "test.wav"
    print(var)
    
def listen_source():
    songname = ''
    try:
        songname = lb.get(lb.curselection())
    except:
        Dialog(window,"   Please Choose a song!   ","Some Error", "Crimson")
        return
    play_audio(r"../wavsong/%s.wav"%songname)
    lrc_path = "../lrc/"+songname+".lrc"
    lrc.delete(0.0,tk.END)
    lrclist = load_lrc(lrc_path)
    for i in lrclist:
        lrc.insert(tk.END, i[1])
    dynamic_show_lrc(lrc_path)
    
def listen_me():
    global wavvar
    songname = ''
    try:
        songname = lb.get(lb.curselection())
    except:
        Dialog(window,"   Which song do you sing?   ","Some Error", "Crimson")
        return
    musicpath = r"../wavbanzou/%s.wav" % songname
    voicepath = wavvar
    if voicepath == '':
        Dialog(window,"   You haven't sung yet!   ","Some Error", "Crimson")
        return
    t1 = threading.Thread(target = play_audio, args = (musicpath,))
    t2 = threading.Thread(target = play_audio2, args = (voicepath,))
    t1.start()
    t2.start()
    lrc_path = "../lrc/"+songname+".lrc"
    lrc.delete(0.0,tk.END)
    lrclist = load_lrc(lrc_path)
    for i in lrclist:
        lrc.insert(tk.END, i[1])
    dynamic_show_lrc(lrc_path)
# 第6步，创建并放置按钮触发上传音频文件的事件
# 第6步，创建并放置按钮触发上传音频文件的事件
    
def save_me():
    global wavvar
    savepath = filedialog.asksaveasfilename(filetypes=[("WAV",".wav")],defaultextension=True).replace('/','\\')
    os.popen("copy "+wavvar+" "+savepath)
    print("copy "+wavvar+" "+savepath)
    
b1 = tk.Button(window, text='upload file', font=('Comic Sans MS',36), width=10,
               height=1, command=upload_file, fg='white',bg='#22C9C9')
b1.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.1)

b2 = tk.Button(window, text='record now', font=('Comic Sans MS',36), width=10,
               height=1, command=Play_record, fg='white',bg='#22C9C9')
b2.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.1)

b3 = tk.Button(window, text='listen me', font=('Comic Sans MS',36), width=10,
               height=1, command=listen_me, fg='white',bg='#FF4081')
b3.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)

b4 = tk.Button(window, text='save me', font=('Comic Sans MS',36), width=10,
               height=1, command=save_me, fg='white',bg='#22C9C9')
b4.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.1)

b5 = tk.Button(window, text='listen source', font=('Comic Sans MS',36), width=10,
               height=1, command=listen_source, fg='white',bg='#FF4081')
b5.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)
################设置选择歌曲的控件###############################
# 第7步,创建一个方法用于按钮的点击事件
def print_selection():
    #这里要获取value的相对路径
    value = ''
    try:
        value = lb.get(lb.curselection())   # 获取当前选中的文本
    except:
        Dialog(window,"   Please Choose one song!   ","Some Error", "Crimson")
    print(value)
    #把value中的曲号提取出来
    songnumber = value.split('-')[0]
    t_sqnc = '../template_sqnc/'+songnumber+'.mid.txt'
#    notesqnc_int = GetSqncDict()
    score = CoconutScore(t_sqnc, var)
    txt.delete(0.0,tk.END)
    txt.insert(tk.END, score)

    
# 第8步，创建一个按钮并放置，点击按钮调用print_selection函数
b6 = tk.Button(window, text='Get your score', font=('Comic Sans MS',36), width=15, 
               height=2, command=print_selection, fg='white',bg='BlueViolet')
b6.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.1)

# 第9步，创建Listbox并为其添加内容
lb = tk.Listbox(window,font=('微软雅黑',18),fg='DeepSkyBlue')  #创建Listbox，将var2的值赋给Listbox
list_items = ['1-开始懂了-孙燕姿',
             '2-崇拜-梁静茹',
             '3-突然好想你-徐佳莹',
             '4-匆匆那年-王菲',
             '5-晴天-周杰伦',
             '6-演员-薛之谦',
             '7-学不会-林俊杰',
             '8-身骑白马-徐佳莹',
             '9-我很快乐-刘惜君',
             '10-小情歌-苏打绿']#定义listbox中的选项
def Printlrc(event):
    print("in")
    print(lb.curselection())
    lrcname = lb.get(lb.curselection())
    if lrc.index('insert') == '1.0':#只有在光标位于开头的时候替换歌词，不然认为别的歌曲正在放
        pass
    else:
        return
    lrc.delete(0.0,tk.END)
    lrc.tag_configure('color', foreground='Goldenrod', 
                        font=('Comic Sans MS',30))
    lrc_path = "../lrc/"+lrcname+".lrc"
    lrclist = load_lrc(lrc_path)
    for i in lrclist:
        lrc.insert(tk.END, i[1])
    lrc.mark_set("insert", "%d.%d" % (1, 0))
    
        
lb.bind('<ButtonRelease-1>',Printlrc)
for item in list_items:
    lb.insert('end',item)# 从最后一个位置开始加入值

lb.place(relx=0.60, rely=0.1, relwidth=0.3, relheight=0.4)


################设置画布美化界面###############################
# 第4步，在图形界面上创建 500 * 200 大小的画布并放置各种元素
#canvas = tk.Canvas(window, background='white', height=300, width=300)
# 说明图片位置，并导入图片到画布上
#image_file = tk.PhotoImage(file=r'C:\Users\李方怡\Desktop\SLP\timg1~1.gif')
# image = Image.open(r'C:\Users\李方怡\Desktop\SLP\timg.jpg')  
# im = ImageTk.PhotoImage(image)  
#image = canvas.create_image(250, 100, anchor='nw',image=image_file)
# 第10步，主窗口循环显示
window.mainloop()

