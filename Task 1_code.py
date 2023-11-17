# -*- coding: utf-8 -*-
"""
Created on Sun May  7 09:37:31 2023

@author: Acer
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"问题参数设置"
T=1
U=1.71 #1-6个月里的上限
L=1.29 #8-11月的下线
I1=1.3
I2=1.8#最后一个月的区间
X=1.4

"模拟参数"
N=1000
miu=0.03
sig=0.12
m=T/N

mean=[]
se=[]

"模拟1次"
df=pd.DataFrame(columns=range(1001))
payoff=[]
for M in range(10000):
    S0=1.5
    S=[S0]
    for i in range(N):
        t=i+1
        Z=np.random.randn()
        S1=S0+miu*S0*m+sig*S0*(m**0.5)*Z
        S0=S1
        S.append(S1)        
        if m*t<=6/12 and S1>U:
            b = np.zeros(1000-t)
            S=np.hstack((S, b))
            break
        if 7/12<m*t<=11/12 and S1<L:
            b = np.zeros(1000-t)
            S=np.hstack((S, b))
            break
        if 11/12<=m*t<=1 and (S1>I2 or S1<I1):
            b = np.zeros(1000-t)
            S=np.hstack((S, b))
            break

    df.loc[len(df)]=(S)
    
payoff=[]
for i in range(10000):
    payoff.append(max(df.loc[i,1000]-1.4,0))
mean.append(np.mean(payoff))
se.append(np.std(payoff,ddof=0)/(10000**0.5))

"绘制模拟图像"
x=list(np.linspace(0,1,1001))
plt.figure(figsize=(20, 10), dpi=100)
plt.plot(x,list(df.loc[1,:]),c='b')
plt.plot(x,list(df.loc[2,:]),c='purple')
plt.plot(x,list(df.loc[9999,:]),c='orange')
plt.plot(x,list(df.loc[100,:]),c='r')
plt.plot(x,list(df.loc[4,:]),c='green')
plt.plot(np.linspace(0,6/12,100),[U]*100,lw=6,c='red')
plt.plot(np.linspace(7/12,11/12,100),[L]*100,lw=6,c='black')
plt.plot(np.linspace(11/12,1,100),[I1]*100,lw=6,c='lightgreen')
plt.plot(np.linspace(11/12,1,100),[I2]*100,lw=6,c='lightgreen')
plt.ylim(0,2)

"模拟9次"
for i in range(9):
    df=pd.DataFrame(columns=range(1001))
    payoff=[]
    for M in range(10000):
        S0=1.5
        S=[S0]
        for i in range(N):
            t=i+1
            Z=np.random.randn()
            S1=S0+miu*S0*m+sig*S0*(m**0.5)*Z
            S0=S1
            S.append(S1)
            if m*t<=6/12 and S1>U:
                b = np.zeros(1000-t)
                S=np.hstack((S, b))
                break
            if 7/12<m*t<=11/12 and S1<L:
                b = np.zeros(1000-t)
                S=np.hstack((S, b))
                break
            if 11/12<=m*t<=1 and (S1>I2 or S1<I1):
                b = np.zeros(1000-t)
                S=np.hstack((S, b))
                break
        df.loc[len(df)]=(S)
    
    payoff=[]
    for i in range(10000):
        payoff.append(max(df.loc[i,999]-1.4,0))
    mean.append(np.mean(payoff))
    se.append(np.std(payoff,ddof=0)/(10000**0.5))

print(mean)
print(se)

np.mean(mean)

