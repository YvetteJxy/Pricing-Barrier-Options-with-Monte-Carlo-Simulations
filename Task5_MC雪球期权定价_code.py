import numpy as np
import pandas as pd

date_view = pd.date_range('2022-12-01', '2023-09-30', freq='M')
view_point = []
for i in date_view:
    temp = str(pd.to_datetime(i) - pd.to_datetime('2022-09-30'))
    view_point.append(int(temp.split(' ')[0]))

time_span = 365
j = 0
coupon = []
call_obs = view_point
ki_obs = list(range(1, time_span+1))
df = []
for i in view_point:
    df.append(np.exp(-0.03 * i / time_span))
    coupon.append(0.2 * i / time_span)
    j += 1


def simulation(S, r, T, sigma, I, q, steps=time_span+1):
    delta_t = T / steps
    path = np.zeros((steps + 1, I))
    path[0] = S

    for t in range(1, steps + 1):
        z = np.random.standard_normal(I)
        middle1 = path[t - 1, 0:I] * np.exp((r - q - 0.5 * sigma ** 2) * delta_t + sigma * np.sqrt(delta_t) * z)
        up_limit = path[t - 1] * 1.1
        low_limit = path[t - 1] * 0.9
        temp = np.where(up_limit < middle1, up_limit, middle1)
        temp = np.where(low_limit > middle1, low_limit, temp)
        path[t, 0:I] = temp
    return path.T


def Snowball(path,  # 路径矩阵
             coupon,  # 票息
             call_barrier,  # 赎回障碍
             call_obs,  # 赎回观察日
             ki_barrier,  # 敲入障碍
             ki_obs,  # 敲入观察日
             min_gain,  # 敲入最小净值（最大损失）
             max_gain,  # 敲入最大净值
             df,  # 每个观察日的贴现因子
             notional  # 本金
             ):
    obs = path[:, call_obs] > call_barrier  # 观察日是否敲出
    called = obs.any(axis=1)  # 每条路径是否敲出
    called_value = np.eye(len(call_obs))[obs[called].argmax(axis=1)] * coupon * df  # 观察日所获coupon贴现
    ki = (path[~called][:, ki_obs] < ki_barrier).any(axis=1)  # 未敲出但敲入
    ki_value = ((path[~called][ki, -1].clip(min=min_gain, max=max_gain)) - 100) * np.array(df[-1]) / 100  # 敲入损失贴现
    nki_value = (~ki).sum() * coupon[-1] * np.array(df[-1])  # 未敲出未敲入全额coupon贴现
    return (called_value.sum() + ki_value.sum() + nki_value) / path.shape[0] * notional  # 相加平均


np.random.seed(2022213286)
path = simulation(100, 0.03, time_span / 365, 0.2, 300000, 0.02)
print(Snowball(path, coupon, 105, call_obs, 75, ki_obs, 0, 100, df, 100))