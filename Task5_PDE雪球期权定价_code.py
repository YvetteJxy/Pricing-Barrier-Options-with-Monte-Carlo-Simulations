import pandas as pd
import numpy as np

def snowball_price(K, r, sigma, knock_out, knock_in, dt, S_grid_size, T_grid_size, Smax, q, coupon, date_view, date_correct):
    ds = Smax / S_grid_size
    M = np.zeros([S_grid_size - 1, S_grid_size - 1])
    V_1 = np.zeros([S_grid_size - 1])
    V_2 = np.zeros([S_grid_size - 1])
    # 构造隐式差分使用的M矩阵
    a = []
    b = []
    c = []
    for j in range(1, S_grid_size):
        a.append(1 / 2 * (r - q) * j * dt - 1 / 2 * sigma ** 2 * j ** 2 * dt)
        b.append(1 + r * dt + sigma ** 2 * j ** 2 * dt)
        c.append(-1 / 2 * (r - q) * j * dt - 1 / 2 * sigma ** 2 * j ** 2 * dt)
    for i in range(1, S_grid_size - 2):
        M[i][i - 1] = a[i]
        M[i][i] = b[i]
        M[i][i + 1] = c[i]
    M[0][0], M[0][1], M[-1][-1], M[-1][-2] = b[0], c[0], b[-1], a[-1]
    M = np.linalg.inv(M)

    # 第一类情况：发生敲出，未发生敲入
    # m用于寻找敲出边界的位置
    m = 0
    for i in range(S_grid_size - 1):
        if i * ds >= knock_out:
            m = i
            break
    j = 1
    for i in range(T_grid_size, 0, -1):
        if date_correct[i] in date_view:
            V_2[m-1:-1] = K * coupon[-j]  # 当i==T_grid_size时即为边界赋值，i！=T_grid_size时为观察日赋值
            j += 1
        V_1 = np.matmul(M, V_2)
        V_2 = V_1
    result = V_1

    # 第二类情况：双边触碰生效
    V_1 = np.zeros([S_grid_size - 1])
    V_2 = np.zeros([S_grid_size - 1])
    m, n = 0, 0
    for i in range(S_grid_size - 1):
        if i * ds >= knock_out:
            m = i
            break
    for i in range(S_grid_size - 1):
        if i * ds >= knock_in:
            n = i
            break
    # 为边界赋值
    V_2[n:m - 1] = K * coupon[-1]
    for i in range(T_grid_size, 0, -1):
        if date_correct[i] in date_view and i != T_grid_size:  # ‘i != T_grid_size’保证只在观察日赋值
            V_2[m:] = 0
        V_2[:n+1] = 0
        V_1 = np.matmul(M, V_2)
        V_2 = V_1
    result += V_1

    # 第三类情况：上涨失效看跌
    V_1 = np.zeros([S_grid_size - 1])
    V_2 = np.zeros([S_grid_size - 1])
    m = 0
    for i in range(S_grid_size - 1):
        if i * ds >= knock_out:
            m = i
            break
    # 为边界赋值
    for i in range(len(V_2)):
        V_2[i] = max(K - (i + 1) * ds, 0)
    for i in range(T_grid_size, 0, -1):
        if date_correct[i] in date_view and i != T_grid_size:
            V_2[m:] = 0
        V_1 = np.matmul(M, V_2)
        V_2 = V_1
    result -= V_1

    # 第四种情况：双边失效看跌
    V_1 = np.zeros([S_grid_size - 1])
    V_2 = np.zeros([S_grid_size - 1])
    m, n = 0, 0
    for i in range(S_grid_size - 1):
        if i * ds >= knock_out:
            m = i
            break
    for i in range(S_grid_size - 1):
        if i * ds >= knock_in:
            n = i
            break
    # 为边界赋值
    for i in range(n + 1, m):
        V_2[i] = max(K - i * ds, 0)
    for i in range(T_grid_size, 0, -1):
        if date_correct[i] in date_view and i != T_grid_size:
            V_2[m:] = 0
        V_2[:n+1] = 0
        V_1 = np.matmul(M, V_2)
        V_2 = V_1
    return result + V_1


# 代码逻辑：raw_date_view保存观察日数据，date_correct保存自然日数据，在snowball_price函数中判断当前日是否为观察日
raw_date_view = pd.date_range('2022-12-01', '2023-09-30', freq='M')
date_correct = pd.date_range('2022-09-30', '2023-09-30')
T_daily = int(str(raw_date_view[-1] - date_correct[0]).split(' ')[0])
coupon = []
coupon_rate = 0.2
for i in range(len(raw_date_view)):
    coupon.append(coupon_rate * int(str(raw_date_view[i] - date_correct[0]).split(' ')[0]) / 365)
dt = 1/365
Smax = 150
S_gird_size = 3000
index = 2000 # 标的价格对应的索引位置
temp = snowball_price(100, 0.03, 0.2, 105, 75, dt, 3000, T_daily, Smax, 0.02, coupon, raw_date_view, date_correct)
price = temp[index]
price
delta = (temp[index + 1] - temp[index - 1]) / (2 * Smax / S_gird_size)