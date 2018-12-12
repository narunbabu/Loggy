import numpy as np
import sys
from matplotlib import pyplot as plt
sys.path.append('D:\SoftwareWebApps\Python\pyQt\LogSpliceUI\\')
from LateralCorr import mean_norm,get_delay
from flex import FlexXY
from Filters import *
projectFolder=r'D:\Ameyem Office\Projects\Cairn\W1\\'
log_bundle=np.load(projectFolder+'proc_logs_bundle.npy')
print(log_bundle[0].keys())
logname='GR';depthcol_name='DEPTH'


def common_depth_of_bundles(log_bundle):
    if len(log_bundle)>2:
        print('Please input a bundle with two sets of logs...')
        return
    dranges=[]
    dointersect=False
    for lb in log_bundle:
        dranges.append([lb[depthcol_name].min(),lb[depthcol_name].max()])
    for mx in max(dranges):
        for mn in min(dranges):
            if not dointersect:
                dointersect=mx<mn   
    if dointersect:
        return [min(max(dranges)),max(min(dranges))]
    else:
        return [np.nan, np.nan]
# def common_depth_logexists(log_bundle):  
#     depth_range=common_depth(log_bundle)
#     d,a=getCurveWRange(lb[depthcol_name],fa,drange)

def getCurveWRange(deptharr,dataarr,drange):
    indxs= (deptharr>=drange[0]) & (deptharr<=drange[1])
    
    d,a=deptharr[indxs],dataarr[indxs]
    print(np.unique(np.diff(d)))
    dt=d[1]-d[0]
    nan_indxs=np.isnan(a)
    return d[~nan_indxs],a[~nan_indxs],dt
    
# drange=common_depth(log_bundle)
ma=[]
expand_range=50
flt_arrs=[]
fg=plt.figure()
ax1=fg.add_subplot(211)
dt=0
for lb in log_bundle:
    flt_arrs.append(hist_filter(lb[logname].copy(),n_big_patches=1,hist_bins=100))
for lb,fa,color in zip(log_bundle,flt_arrs,['b','y']):
    drange=common_depth_of_bundles(log_bundle[0:2])
    drange=np.array(drange)+np.array([-expand_range, expand_range])
    d,a,dt=getCurveWRange(lb[depthcol_name],fa,drange)
    if len(ma)==0:
        new_d=np.arange(d[0],d[-1]+dt,dt)
    logXY=np.column_stack((d,a))
    flex_xy=FlexXY(logXY)
    a=flex_xy.resampleY(new_d)
    # print(min(d),max(d))    
    print('dt = ',dt)
    a=mean_norm(a)
    a[np.isnan(a)]=0   
    ma.append(a)
    if len(ma)>1:
        ax1.plot(new_d,a-0.2,color)
    else:
        ax1.plot(new_d,a,color)
# if len(ma[1])<len()
delay,corr=get_delay(ma[0],ma[1],dt,corrtype='+ve',dist2look=30)
print(delay)
ax1.plot(new_d-delay,a,'r')
# ax1.plot(d+delay,a+25)
ax2=fg.add_subplot(212)
ax2.plot(corr[0],corr[1])
# print(corr[1])
plt.show()

