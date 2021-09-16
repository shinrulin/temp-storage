
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 08:52:34 2021

@author: USER
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import numba
import collections
from scipy.interpolate import interp1d
from scipy.signal import find_peaks
import csv
import heapq
from collections import Counter

def preprocess(channel):
    d=1
    channel = channel.rolling(d).mean()#去雜訊
    channel = arr_apend(channel) #將CSV資訊放入List中    
    return channel

def arr_apend(channel):
        array=[]
        for r in channel:
            
            array.append(float(r))
        return array
    

def select(Time,channel,th):
    Time_select=[]
    Max_amp=heapq.nlargest(9000,channel)
    Max_avg=np.mean(Max_amp)
    range1=Max_avg*0.95 
    range2=Max_avg*1.05 
    # print("mean",Max_avg,range1,range2)

    for i,j in zip(channel,Time):
        # print(i,j) # 電壓跟時間
        if i> range1 and i<range2:
            Time_select.append(j)
    # print(Time_select)
    for a,b in zip(Time_select,Time_select[1:]):
        
        # print(Time_select)
        if (b-a)>(th*0.95) and (b-a)<(th*1.8): #+80% -5%
            # print("T1: ",a,"T2: ",b,"Low Period: ",b-a)
            # print("區間正常")
            return [a,b,b-a]        

def amp(channel):
    Max_amp=heapq.nlargest(9000,channel)
    min_amp=heapq.nsmallest(5, channel)
    Max_amp=np.mean(Max_amp)
    min_amp=np.mean(min_amp)
    amp=Max_amp-min_amp
    # print("max",Max_amp,"min",min_amp,"Ampltude: ",amp)
    if amp>12*0.95 and amp<12*1.05: #+5% -5%
        # print("振幅正常")
        return amp
        
def find_t3(channel):
    min_v=min(channel)
    for i,j in zip(channel,Time):
    # print(i,j) # 電壓跟時間
        if i==min_v:
            # print("T3",j)
            return j
        
def find_t3t4(channel,Time,low_th):
    low_time=[]
    r1=low_th*0.97
    r2=low_th*1.03
    for i,j in zip(channel,Time):
    # print(i,j) # 電壓跟時間
        if i> r2 and i<r1:
            low_time.append(j)
            # print("t3",j)
    # print("T3 T4",low_time[0],low_time[-1])
    return low_time

def falling(channel,time,a,b):

    # print(a,b)
    for i,j in zip(time,channel):
        if i==a:
            v1=j
       
        if i==b:
            v2=j

    v_10=v1-(v1-v2)*0.1
    v_90=v1-(v1-v2)*0.9
    print(v_10,v_90)
    fall=[]
    for m,n in zip(channel,time):
        # print(m,n) # 電壓跟時間
        if m<=v_10 and m>=v_90 and n>=a and n<=b:
            fall.append(n)
            # print(m,n)
    # print(fall)
    print(fall[0],fall[-1],fall[-1]-fall[0])
    return fall    
     
      
        
        

if __name__ == '__main__':
    
    # 開啟 CSV 檔案
    with open('scope_519.csv', newline='') as csvfile:
    
      # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        df=pd.read_csv(csvfile) 
        df=df.drop(0)
        df=df.dropna(axis=0,how='any')
        # df=df.drop(df.index[1])
    
    #前處理     
    Time=arr_apend(df['x-axis'])
    CH1=preprocess(df['S1'])
    CH2=preprocess(df['S2'])
    CH3=preprocess(df['EM1'])    
    CH4=preprocess(df['EM2'])    

    #篩選出Low週期
    CH1_t1t2=select(Time,CH1,0.000008)#0.0000145
    # print("CH1:   ",CH1_t1t2)
    CH2_t1t2=select(Time,CH2,0.000043)#0.00004705
    # print("CH2:   ",CH2_t1t2)
    CH3_t1t2=select(Time,CH3,0.000008)#0.000014
    # print("CH3:   ",CH3_t1t2)
    CH4_t1t2=select(Time,CH4,0.000043)#0.0000475
    # print("CH4:   ",CH4_t1t2)
    
    #判斷S1 EM1的t3
    CH1_t3=find_t3(CH1) #S1
    CH3_t3=find_t3(CH3) #EM1
    
    #判斷S2 EM2的t3 t4
    CH2_t3t4=find_t3t4(CH2,Time,-6)
    CH4_t3t4=find_t3t4(CH4, Time,-6)
    
    #判斷falling
    CH1_fall=falling(CH1,Time,CH1_t1t2[0],CH1_t3)
    CH2_fall=falling(CH2,Time,CH2_t1t2[0],CH2_t3t4[0])
    CH3_fall=falling(CH3,Time,CH3_t1t2[0],CH3_t3)
    CH4_fall=falling(CH4,Time,CH4_t1t2[0],CH4_t3t4[0])

      
    #判斷振幅
    amp(CH1)
    amp(CH2)
    amp(CH3)
    amp(CH4)
    
    #製圖
    plt.plot(Time,CH2) 
    
    #Show出t1t2在訊號上的位置
    plt.annotate(s="t1", xy=(CH2_t1t2[0],6.1), xytext=(-0.0001,1), color='r',arrowprops=dict(arrowstyle='->',connectionstyle='arc3',color='c'))
    plt.annotate(s="t2", xy=(CH2_t1t2[-1],6), xytext=(0.0001,1), color='r',arrowprops=dict(arrowstyle='->',connectionstyle='arc3',color='c'))
    
    #Show出t3t4的位置
    # plt.annotate(s="t3", xy=(CH3_t3,-7.2), xytext=(-0.0001,-4), color='r',arrowprops=dict(arrowstyle='->',connectionstyle='arc3',color='c'))
    
    plt.annotate(s="t3", xy=(CH2_t3t4[0],-6.1), xytext=(-0.0001,-4), color='r',arrowprops=dict(arrowstyle='->',connectionstyle='arc3',color='c'))
    plt.annotate(s="t4", xy=(CH2_t3t4[-1],-6.4), xytext=(0.0001,-4), color='r',arrowprops=dict(arrowstyle='->',connectionstyle='arc3',color='c'))
   
    # plt.savefig('CH4_falling_1w.png')
    
    plt.show() #顯示繪製的圖形
    
    
        