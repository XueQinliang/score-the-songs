# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 21:54:01 2019

@author: Qinliang Xue
"""
import pyaudio
import wave
import os

CHUNK = 1024  # 每个缓冲区的帧数
FORMAT = pyaudio.paInt16  # 采样位数
CHANNELS = 1  # 单声道
RATE = 44100  # 采样频率

def record_audio(wave_out_path, record_second):
    """ 录音功能 """
    print("recording……")
    print(wave_out_path)
    p = pyaudio.PyAudio()  # 实例化对象
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # 打开流，传入响应参数
    wf = wave.open(wave_out_path, 'wb')  # 打开 wav 文件。
    wf.setnchannels(CHANNELS)  # 声道设置
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
    wf.setframerate(RATE)  # 采样频率设置

    for _ in range(0, int(RATE * record_second / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)  # 写入数据
    stream.stop_stream()  # 关闭流
    stream.close()
    p.terminate()
    wf.close()
    os.popen("wav2midi.exe %s" % wave_out_path)
    #exit(0)
if __name__ == "__main__":
    record_audio(r"./test.wav",5)
    
  