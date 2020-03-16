# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 10:33:03 2019

@author: Qinliang Xue
"""

import time
import re

def load_lrc(lrc_path):
    lrclist = []
    with open(lrc_path) as f:
        for info in f.readlines():
            t = re.findall(r"\[(.*?)\]",info)[0]
            if not '.' in t:
                continue
            lyric = re.findall(r"\[.*\](.*)",info)[0]
            second = float(t)
            lrclist.append((second,lyric))
    return lrclist

def show_lrc_with_time(lrc_path, record_second):
    #length是歌曲的时长秒数
    time_start = time.time()
    lrclist = load_lrc(lrc_path)
    line = 0
    while True:
        if line >= len(lrclist):
            break
        nowtime = time.time() - time_start
        if nowtime > record_second:
            break
        if nowtime < lrclist[line][0]:
            pass
            #print(nowtime,lrclist[line][1])
        else:
            print(nowtime,lrclist[line][1])
            line += 1

if __name__ == '__main__':
    show_lrc_with_time(r"../lrc/2-崇拜-梁静茹.lrc",300)
            
        
        
        
#load_lrc(r"C:\Users\HP\Desktop\yuanchang\学不会.lrc")