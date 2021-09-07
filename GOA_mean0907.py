
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

if __name__ == '__main__':
    
    # 開啟 CSV 檔案
    with open('scope_419_0827.csv', newline='') as csvfile:
    
      # 讀取 CSV 檔案內容
      rows = csv.reader(csvfile)
      df=pd.read_csv(csvfile) 
      df=df.drop(0)
      # df=df.drop([1,2,3,4,5,6,7,8,9,10,11])
      # df=df.drop(df.index[1:11],inplace=True)
      df=df.dropna(axis=0,how='any')
      
      
    #去雜訊
    d = 1
    df['4'] = df['4'].rolling(d).mean()
    # df['3'] = df['CH2'].rolling(d).mean()
    df['2']= df['2'].rolling(d).mean()
    df['1'] = df['1'].rolling(d).mean()
    df['1']=pd.to_numeric(df['1'],downcast='float')
    
    #將CSV資訊放入List中
    array1=[]
    for r in df['1']:
        array1.append(float(r))
    #求均值
    mean=np.mean(array1)
    array2=array1
    print(mean)
    #均值以下的數值存進array2中
    array2=[i for i in array2 if not(i>mean)]         
    print(array2)
    #找出對應的時間點a.b
    a=array1.index(array2[0])
    b=array1.index(array2[-1])
    
    
    xpt = df['x-axis'][a-1:b]
    print("time1:   ",df['x-axis'][a-1])
    print("time2:   ",df['x-axis'][b])
    t1=float(df['x-axis'][a-1])
    t2=float(df['x-axis'][b])
    print("Period:   ",t2-t1)#一個週期的時間
    
    #找出振幅大小進行判斷
    min_amp=min(array2)
    Max_amp=max(array1)
    print("SHOOOOOOOW",min_amp,Max_amp,Max_amp-min_amp)
    plt.xticks([])
    plt.yticks([])
    plt.plot(xpt,array2) 
    
    plt.show() #顯示繪製的圖形