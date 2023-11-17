import math
import numpy as np
import scipy.stats as stats
#####连续的时候
s=100
k=95
b=115
t=1
sig = 0.1
r=0.05

def sigplus(T,u):
    cal=1/(sig*math.sqrt(T))*(math.log(u)+(r+0.5*sig*sig)*T)
    return(cal)

def sigmin(T,u):
    cal=1/(sig*math.sqrt(T))*(math.log(u)-(r+0.5*sig*sig)*T)
    return(cal)

i1=stats.norm.cdf(sigplus(t,s/k))-stats.norm.cdf(sigplus(t,s/b))
i2=math.exp(r*t)*(stats.norm.cdf(sigmin(t,s/k))-stats.norm.cdf(t,s/b))
i3=math.pow(s/b,-2*r/(sig*sig)-1)*(stats.norm.cdf(sigplus(t,b*b/k/s))-stats.norm.cdf(sigplus(t,b/s)))
i4=math.exp(-r*t)*math.pow(s/b,-2*r/(sig*sig)+1)*(stats.norm.cdf(sigmin(t,b*b/k/s))-stats.norm.cdf(sigmin(t,b/s)))
price=s*i1-k*i2-s*i3+k*i4
print(price)