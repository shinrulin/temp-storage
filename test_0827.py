
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

def main():
    # fileName="scope_419_0827.csv"
    # df=pd.read_csv(fileName) 
    # df=df.drop(0)
    # df=df.dropna(axis=0,how='any')
    
    # x=df['1'].max()
    
    # 開啟 CSV 檔案
    with open('scope_419_0827.csv', newline='') as csvfile:
    
      # 讀取 CSV 檔案內容
      rows = csv.reader(csvfile)
      df=pd.read_csv(csvfile) 
      df=df.drop(0)
      df=df.dropna(axis=0,how='any')
      # print(df)
      # print(df['1'])
      # print(df['2'])
      # print(df['4'])
     
      # 以迴圈輸出每一列
      for row in df['1']:
            print(row)
            row= float(row)
            print(type(row))
            # k=df['1'][2]-df['1'][3]
            # print(k)
            # if df['1'][row]< df['1'][3]:
                # print("OK")
                # print(df['1'][row])
       
    # #去雜訊
    d = 1
    df['4'] = df['4'].rolling(d).mean()
    df['2'] = df['2'].rolling(d).mean()
    df['1'] = df['1'].rolling(d).mean()
    print("MMMM",df['1'])
    # # for L in range (df['1']):
    #     # print(L)
    
    # #斜率(反轉訊號)
    x1=df['1']
    x=x1.diff() #斜率
    off = x.diff().max()
    on = x.diff().min()
    #off = (x > 0) & (x.shift() < 0)
    y1=interp1d(x,df['x-axis'],kind='nearest')(off)
    y2=interp1d(x,df['x-axis'],kind='nearest')(on)
    z=abs(y2-y1)
    # print("Start time",y1)
    # print("end time",y2)
    # print("period time",z)
    
    
        
    
    # peak_id,peak_property = find_peaks(x, height=1, distance=10)
    # peak_freq = x[peak_id]
    # peak_height = peak_property['peak_heights']
    # print('peak_freq',peak_freq)
    # print('peak_height',peak_height)

    xpt = df['x-axis']
    
    
    plt.xticks([])
    plt.yticks([])
    plt.plot(xpt,x1) #
    #plt.plot(xpt,df['2'])
    #plt.plot(xpt,df['1'])
    plt.plot(xpt,x)
    
    plt.show() #顯示繪製的圖形
 
    
    
    
    
    
main()