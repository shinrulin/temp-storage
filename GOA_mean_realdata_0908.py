
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


def arr_apend(channel):
        array=[]
        for r in channel:
            
            array.append(float(r))
        return array
    
    
def select(channel,array,mean):
    array=[i for i in array if not(i>mean)]
    # a=array[0][0]
    # b=channel.index(array.pop())
    # b=array[0][-1]
    # a=channel.index(array.index[0])
    # print(a)
    return array

if __name__ == '__main__':
    
    # 開啟 CSV 檔案
    with open('Tek002_ALL.csv', newline='') as csvfile:
    
      # 讀取 CSV 檔案內容
      rows = csv.reader(csvfile)
      df=pd.read_csv(csvfile) 
      df=df.drop(0)
      # df=df.drop([1,2,3,4,5,6,7,8,9,10,11],axis=0,inplace=True)
      df=df.dropna(axis=0,how='any')
      
      
    # #去雜訊
    d = 1
    df['CH4'] = df['CH4'].rolling(d).mean()
    df['CH3'] = df['CH3'].rolling(d).mean()
    df['CH2']= df['CH2'].rolling(d).mean()
    df['CH1'] = df['CH1'].rolling(d).mean()
    df['CH1']=pd.to_numeric(df['CH1'],downcast='float')
    df['CH2']=pd.to_numeric(df['CH2'],downcast='float')
    df['CH3']=pd.to_numeric(df['CH3'],downcast='float')
    df['CH4']=pd.to_numeric(df['CH4'],downcast='float')
    
    # #將CSV資訊放入List中
    CH1=arr_apend(df['CH1'])
    CH2=arr_apend(df['CH2'])
    CH3=arr_apend(df['CH3'])    
    CH4=arr_apend(df['CH4'])    

    # #求均值
    mean1=np.mean(CH1)
    mean2=np.mean(CH2)
    mean3=np.mean(CH3)
    mean4=np.mean(CH4)
    array1=CH1
    array2=CH2
    array3=CH3
    array4=CH4
    # print("mean:   ",mean1)
    
    #均值以下的數值存進array中
    array1=select(CH1,array1,mean1)
    array2=select(CH2,array2,mean2)
    array3=select(CH3,array3,mean3)
    array4=select(CH4,array4,mean4) 
    
    # print(array4)
    
    # #找出對應的時間點a.b
    # a=array1.index(array2[0])
    # b=array1.index(array2[-1])    
    
    # xpt = df['x-axis'][a-1:b]
    # print("time1:   ",df['x-axis'][a-1])
    # print("time2:   ",df['x-axis'][b])
    # t1=float(df['x-axis'][a-1])
    # t2=float(df['x-axis'][b])
    # print("Period:   ",t2-t1)#一個週期的時間
    
    # #找出振幅大小進行判斷
    # min_amp1=min(array2)
    # min_amp=heapq.nsmallest(10,array2)
    # min_amp=np.mean(min_amp)
    
    # Max_amp1=max(array1)
    # Max_amp=heapq.nlargest(100,array1)
    # Max_amp=np.mean(Max_amp)
    
    # print("AVG min ",min_amp)
    # print("AVG Max ",Max_amp)
    # print("AVG AMP",Max_amp-min_amp)
    # print("Total min",min_amp1)
    # print("Total Max ",Max_amp1)
    # print("Total AMP",Max_amp1-min_amp1)
    
    # #製圖
    # plt.xticks([])
    plt.yticks([])
    plt.plot(array4) 
    plt.show() #顯示繪製的圖形
    
    
        