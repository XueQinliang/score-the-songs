# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 19:49:44 2019

@author: Nicole~
"""
'''
任务：
2. 需要判断是否是间奏，间奏可以不去匹配
3. midi提取出来的旋律，要找一个好的方式去匹配（确定评分函数）
4. 和真实的原唱去比较分数，让分数更合理一点
'''

'''
实现思路：
1. music21将midi转换成整数序列
2. DTW进行打分比对
******3. 尝试进行动态打分
'''

from music21 import *
import os
from dtw_music import dtw_distance
import numpy as np
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process



def GenerateTemplateMidiSequenceFiles():
    filelist=os.listdir(r'..\melody')
    print(filelist)
    #在每一个文件夹里的每一个文件，都要生成一个序列并且存下来
    for midfile in filelist:
#        midfile = str(i)+'\\'+str(file)
        s = converter.parse('..\melody\\'+midfile)
        fout = open('../template_sqnc/'+midfile+'.txt','w',encoding = 'utf-8')
        for nt in s.recurse():
            if 'Note' in nt.classes:
                fout.write(str(nt.pitch.midi)+',')
    
        fout.write('\n')
        fout.close()


def Midi2Sqnc(filepath):
    s = converter.parse(filepath)
    sqnc = []
    for nt in s.recurse():
        if 'Note' in nt.classes:
            sqnc.append(nt.pitch.midi)
    return sqnc


          
#def GetSqncDict():            
#    notesqnc = {}
#    filePath = '..\midisqnc'
#    for i,j,filelist in os.walk(filePath):
#        #跳过第一轮
#        if i == '..\midisqnc':
#            continue
#         #在每一个文件夹里的每一个文件，都要生成一个序列并且存下来
#    #    print(i, j, filelist)
#        for file in filelist:
#            fin = open(i+'/'+file, encoding = 'utf-8')
#            sqncstr = fin.readline()
#            sqnc = sqncstr[0:-2].split(',')
#            for l in range(len(sqnc)):
#                sqnc[l] = int(sqnc[l])
#            notesqnc.update({file[0:-8]:sqnc})
#            fin.close()
#    return notesqnc
#
##
def DtwScore(t_sqnc, q_sqnc):
    ## A noisy sine wave as query
    query = np.array(q_sqnc)
    print('query   : ',query)
    ## A cosine is for template; sin and cos are offset by 25 samples
    template = np.array(t_sqnc)
    print('template: ',template)
    
    ## Find the best match with the canonical recursion formula
    cost = dtw_distance(query, template)
    
#    score = ((12*len(t_sqnc)-cost)/len(t_sqnc))*(100/12)
    score = ((6*len(t_sqnc)-cost)/len(t_sqnc))*(100/6)
    print(cost,   score)
    return score

    

#def Whole_FuzzyMatchScore(t, q, notesqnc):
#    '''此算法无法解决八度整数倍的问题'''
#    #fuzz.ratio("this is a test", "this is a test!")
#    score = fuzz.partial_ratio(notesqnc[t],notesqnc[q])
#    print(score)
#    
#    #选择得分最高的文件
#    #choices = list(notesqnc_str.values())
#    #result_sqnc = (process.extract(notesqnc_str['lxk33'], choices, limit=2))[1][0]
#    #print([k for k,v in notesqnc_str.items() if v == result_sqnc])



def CoconutScore(t_file_txt, q_file_midi):
    '''首先把文件转成midi序列'''
    #查询文件
    q_sqnc = Midi2Sqnc(q_file_midi)
    fin = open(t_file_txt, encoding = 'utf-8')
    #模板文件
    t_sqnc = ((fin.readline())[0:-2]).split(',')
    for i in range(len(t_sqnc)):
        t_sqnc[i] = int(t_sqnc[i])   
    fin.close()
  
    '''针对整数序列，自定义评价标准'''
    '''
    预处理：
    统计八度差距，决定是否改变数据
    打分思路：由几部分加权组成
    1. 综合音高准确度0.25
    2. 音符总个数是否准确0.25
    3. 单音准确度0.5
    '''
#    print(notesqnc[t],'\n',notesqnc[q])
    #统计八度差距,并作八度调整
    avg_t = sum(t_sqnc)/len(t_sqnc)
    avg_q = sum(q_sqnc)/len(q_sqnc)
    print(avg_t,',',avg_q,avg_t - avg_q)
    if (avg_t - avg_q) >= 11:
        print("调高八度")
        #低n*八度处理
        if(avg_t - avg_q) >= 12:
            for i in range(len(q_sqnc)):
                q_sqnc[i] += 12*int((avg_t - avg_q)/12)
        else:
            for i in range(len(q_sqnc)):
                q_sqnc[i] += 12
        avg_q = sum(q_sqnc)/len(q_sqnc)
        
    elif (avg_q - avg_t) >= 11:
        print("调低八度")
        #高n*八度处理
        if(avg_q - avg_t) >= 12:
            for i in range(len(q_sqnc)):
                q_sqnc[i] -= 12*int((avg_t - avg_q)/12)
        else:
            for i in range(len(q_sqnc)):
                q_sqnc[i] -= 12
        avg_q = sum(q_sqnc)/len(q_sqnc)
        
    print(avg_t,',',avg_q)
            
    #综合音高准确度部分
    comprehensive_pitch_score = ((6 - abs(avg_t - avg_q))/6) * (100)
    print(comprehensive_pitch_score)
    #音符总个数
    notes_number_score = ((len(t_sqnc) - abs(len(t_sqnc) - len(q_sqnc))) / len(t_sqnc) )*100
    print(notes_number_score)
    
    #单音准确度
    #首先按确保template长度大于等于query长度
##    print(notesqnc[t],'\n',notesqnc[q])
#    if len(t_sqnc) - len(q_sqnc) > 0:
#        for i in range(abs(len(t_sqnc) - len(q_sqnc))):
#            q_sqnc.append(t_sqnc[i] - 11.9)
#            
##    print(notesqnc[t],'\n',notesqnc[q])
#    #接下来逐个计算分数
#    individual_pitch_score = 0
#    for i in range(len(t_sqnc)):
#        individual_pitch_score += ((12 - abs(t_sqnc[i] - q_sqnc[i]))/12) * (100)
#    individual_pitch_score /= len(t_sqnc)    
    individual_pitch_score = DtwScore(t_sqnc, q_sqnc)
    print(individual_pitch_score)
    
    #综合分数
    comprehensive_score = 0.25*comprehensive_pitch_score + \
        0.25*notes_number_score + 0.5*individual_pitch_score
    print('your comprehensive singing score is: ',comprehensive_score)
    
    return comprehensive_score

    
    

'''-----------------------------------------------'''
#GenerateMidiSequenceFiles()

#notesqnc_int = GetSqncDict()
#notesqnc_str = dict([(x,str(y)[1:-1]) for x,y in notesqnc_int.items()])
#Whole_DtwScore('xzq6','xql66',notesqnc_int)
#Whole_FuzzyMatchScore('lxk99','lxk9', notesqnc_str)
#CoconutScore('xzq6','lfy66', notesqnc_int)
#GenerateTemplateMidiSequenceFiles()

#CoconutScore('../template_sqnc/2.mid.txt', './test.mid')
'''-------------------------------------------------'''
#s = difflib.SequenceMatcher(None, '62', '69')
#simi = s.ratio()
