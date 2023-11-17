import math
import numpy as np
import matplotlib.pyplot as plt
X = 99
s = [100]
r = 0.05
rf = 0.02
mu = r-rf
sig = 0.1
T = 1
n1 = 365
dieta_t = T/n1
s_temp = 0
payoff = []
 ###定义日knockout的条件
 ##条件1 前三个月大于等于U
Ua = 118; nc1a = 31+28+31
 #条件2 4-7月小于等于L
L = 82; nc2_1a = nc1a+1; nc2_2a = 31+28+31+30+31+31+31
 #条件2 9、11月在两个之间
I_L = 101.5; nc3_1a = nc2_2a+31+1; nc3_2a = nc2_2a+31+30+31+30
I_H = 102

def knockout_day(n1,s):
    flag = 1
    if ((n1<=nc1a) and (s>=Ua)):
        flag = 0
    elif((nc2_1a<=n1<=nc2_2a) and (s<=L)):
        flag = 0
    elif ((nc3_1a <= n1 <= nc3_2a) and (I_L <= s <= I_H)):
        flag = 0
    return(flag)
####定义week的条件
Ub = 120; nc1b = 12
 #条件2 4-7月小于等于L
nc2_1b = 13; nc2_2b = 28
 #条件2 9、11月在两个之间
nc3_1b = 8*4+1; nc3_2b = 11*4
def knockout_week(n3,s):
    flag2 = 1
    if ((n3<=nc1b) and (s>=Ub)):
        flag2 = 0
    elif((nc2_1b<=n3<=nc2_2b) and (s<=L)):
        flag2 = 0
    elif ((nc3_1b <= n3 <= nc3_2b) and (I_L <= s <= I_H)):
        flag2 = 0
    return(flag2)

 ###定义月knockout的条件
 ##条件1 前三个月大于等于U
U = 120; nc1c = 3
 #条件2 4-7月小于等于L
nc2_1c = 4; nc2_2c = 7
 #条件2 9、11月在两个之间
nc3_1c = 9; nc3_2c = 11
def knockout_month(n2,s):
    flag3 = 1
    if ((n2<=nc1c) and (s>=U)):
        flag3 = 0
    elif((nc2_1c<=n2<=nc2_2c) and (s<=L)):
        flag3 = 0
    elif ((nc3_1c <= n2 <= nc3_2c) and (I_L <= s <= I_H)):
        flag3 = 0
    return(flag3)
###############################################begin#########################################

flag_temp=1
n1=365
end=1000
step=100
times=[]
start=100
payoff_fin=[]
payoff_fin2=[]
payoff_fin3=[]
payoff_in=[]
for kk in range(start,end,step):
    times.append(kk)
    payoff_in=[]
    s=[100]
    for m in range(1, kk):
        payoff = []
        flag_temp = 1
        s_temp = 0
        aa = 100
        for k in range(1, n1):
            flag_temp = 1
            s_temp = s[k - 1] * dieta_t * mu + s[k - 1] + sig * s[k - 1] * math.sqrt(dieta_t) * \
                     np.random.normal(0, 1, 1)[0]
            flag_temp = knockout_day(k, s_temp)
            s.append(s_temp)
            if (flag_temp == 0): aa = 0
            if (flag_temp == 0): break
        if (aa == 0):
            payoff = 0
        else:
            payoff = max(0, s_temp - X)
        # print(s_temp)
        # print(aa)
        # print(payoff)
        payoff_in.append(payoff)
    payoff_fin.append(np.mean(payoff_in) * np.e ** (-r * T))

####周
    aa=100
    payoff = []
    s2 = [100]
    n2 = 48
    dieta_t = T / n2
    payoff_in = []
    payoff_fin2 = []
    for m in range(1, kk):
        payoff = []
        flag_temp2 = 1
        s_temp2 = 0
        aa = 100
        for k in range(1, n2):
            flag_temp2 = 1
            s_temp2 = s2[k - 1] * dieta_t * mu + s2[k - 1] + sig * s2[k - 1] * math.sqrt(dieta_t) * \
                      np.random.normal(0, 1, 1)[0]
            s2.append(s_temp2)
            flag_temp2 = knockout_week(k, s_temp2)
            if (flag_temp2 == 0): aa = 0
            if (flag_temp2 == 0): break
        if (aa == 0):
            payoff = 0
        else:
            payoff = max(0, s_temp2 - X)
        # print(s_temp2)
        # print(payoff)
        payoff_in.append(payoff)
    payoff_fin2.append(np.mean(payoff_in) * np.e ** (-r * T))
###########清空 接下去by month
    aa=100
    payoff = []
    s3 = [100]
    n3 = 12
    dieta_t = T / n3
    payoff_in = []
    payoff_fin3 = []
    for kk in range(start, end, step):
        payoff_in = []
        for m in range(1, kk):
            payoff = []
            flag_temp2 = 1
            s_temp2 = 0
            aa = 100
            for k in range(1, n3):
                flag_temp2 = 1
                s_temp2 = s3[k - 1] * dieta_t * mu + s3[k - 1] + sig * s3[k - 1] * math.sqrt(dieta_t) * \
                          np.random.normal(0, 1, 1)[0]
                s3.append(s_temp2)
                flag_temp2 = knockout_month(k, s_temp2)
                if (flag_temp2 == 0): aa = 0
                if (flag_temp2 == 0): break
            if (aa == 0):
                payoff = 0
            else:
                payoff = max(0, s_temp2 - X)
            # print(s_temp2)
            # print(payoff)
            payoff_in.append(payoff)
        payoff_fin3.append(np.mean(payoff_in) * np.e ** (-r * T))


print(times)
print(payoff_fin)
print(payoff_fin2)
print(payoff_fin3)

plt.plot(times,payoff_fin,label='N=365')
plt.plot(times,payoff_fin2,label='N=48')
plt.plot(times,payoff_fin3,label='N=12')

#plt.ylim([85,125])
plt.legend()
plt.title("Pricing Discretely-monitored Barrier Options(T=1)")
plt.xlabel("Number of simulations")
plt.ylabel("")
plt.show()
