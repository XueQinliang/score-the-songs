# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 23:55:39 2019

@author: 薛钦亮
"""

from pydub import AudioSegment

def easymp3towav(path):    
    sound = AudioSegment.from_mp3(path)
    filename = path[:-3] + "wav"
    sound.export(filename, format="wav")

def mp3towav(filename,inputdir='./',outputdir='./'):
    if inputdir[-1] != '/':
        inputdir += '/'
    if outputdir[-1] != '/':
        outputdir += '/'
    sound = AudioSegment.from_mp3(inputdir + filename)
    filename = filename[:-3] + "wav"
    sound.export(outputdir + filename, format="wav")
    
if __name__ == "__main__":
    import argparse
    import os
    import re
    #设置参数
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inputdir", required=True, type=str, help="dirpath to the input the mp3 files")
    ap.add_argument("-o", "--outputdir", required=True, type=str, help="dirpath to output wav files")
    args = vars(ap.parse_args())
    inputdir = args['inputdir']
    outputdir = args['outputdir']
    if not os.path.exists(inputdir):
        print("WARNING:the input dirpath may not exist")
        os.mkdir(inputdir)
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    for i in os.listdir(inputdir):
        if re.search("mp3$",i):
            mp3towav(i,inputdir,outputdir)
            print(i,"from mp3 to wav successfully")
    
