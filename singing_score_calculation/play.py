# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 21:59:03 2019

@author: QinLiang Xue
"""

import pyaudio
import wave
import pygame
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

def play_audio(playfile):
    print("playing……")
    print(playfile)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load(playfile)
    pygame.mixer.music.play()

def play_audio2(playfile):
    #这些包好像并发不太稳定，我就用了两个包来搞
    print("playing……")
    print(playfile)
    chunk=1024  #2014kb
    wf=wave.open(playfile,'rb')
    p=pyaudio.PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),
                  channels=wf.getnchannels(),
                  rate=wf.getframerate(),output=True)
    data = wf.readframes(chunk)  # 读取数据
    while data != b'':  # 播放  
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()   # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio
    wf.close()

if __name__ == "__main__":
    play_audio(r"../wavbanzou/5-晴天-周杰伦.wav")
    
    