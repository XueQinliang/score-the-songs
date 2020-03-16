# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 00:08:28 2019

@author: Qinliang Xue
"""

from record import *
from play import *
from show_lrc_with_time import show_lrc_with_time
import threading
from Stop_Thread import stop_thread
import wave
import time

def t(sn,st):
    with open("../lrc/"+sn+".lrc","w") as f:
        stime = time.time()
        for i in st:
            a= input()
            print("[%f]"%(time.time()-stime),i)
            f.write("[%f]"%(time.time()-stime)+i+'\n')
#相信你只是怕伤害我不是骗我        
#我活了我爱了我都不管了心爱到疯了恨到算了就好了       
#突然好想你你会在哪里过的快乐或委屈    
#匆匆那年我们究竟说了几遍再见之后再拖延
#刮风这天我试过握着你手但偏偏雨渐渐大到我看你不见
#该配合你演出的我演视而不见在逼一个最爱你的人即兴表演
#总是学不会再聪明一点记得自我保护必要时候讲些善意谎言
#我爱谁跨不过从来也不觉得错
#说有什么不能说怕什么相信我不会哭我不会难过
#这是一首简单的小情歌唱着人们心肠的曲折
def play_record(songname):
    #歌名为指定要唱的歌曲，播放相应的伴奏
    musicpath = r"../wavbanzou/%s.wav" % songname
    #musicpath = r"D:\薛钦亮文件\SLP2019\bigprogram\学不会-林俊杰.wav"
    lrcpath = r"../lrc/%s.lrc" % songname
    voicepath = r"./test.wav"
    wf=wave.open(musicpath,'rb')
    #计算记录时长
    recordtime = wf.getnframes()/wf.getframerate()
    wf.close()
    #play_audio(musicpath)
    #record_audio(voicepath,recordtime)
    #并发
    #a = input("start:")
    p1 = threading.Thread(target = play_audio,args = (musicpath,)) #创建进程对象,并指定进程将来要执行的函数.
    p1.start()
    #t(songname,r"这是一首简单的小情歌唱着人们心肠的曲折")
    p2 = threading.Thread(target = record_audio,args = (voicepath,recordtime)) #创建进程对象,并指定进程将来要执行的函数.
    p2.start()
    #p3 = threading.Thread(target = show_lrc_with_time,args = (lrcpath,recordtime))
    #p3.start()
    
if __name__ == "__main__":
    play_record("6-演员-薛之谦")