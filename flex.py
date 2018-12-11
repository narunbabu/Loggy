import numpy as np
import matplotlib.pyplot as plt
class FlexArray():
    #Input only a sorted array
    """
    This program is to find out the left and right value inside an array for a given values 
    """
    def __init__(self,sortedarray):
        self.flexarray=np.asarray(sortedarray) 
        self.stepsize=int(np.sqrt(self.flexarray.__len__()))
#         if self.flexarray.__len__()-1<self.stepsize:
#             self.stepsize=self.flexarray.__len__()-1

        self.flexarrIndexRangeArray=np.append(np.arange(0,len(self.flexarray)-1,self.stepsize),self.flexarray.__len__()-1)
    def get_stepsize(self):
        return self.stepsize
        
    def find_indx_nearest(self,array, value):
        array = np.asarray(array)
        return (np.abs(array - value)).argmin()    
        
    def find_indx_leftright(self,array,value):

        if (value>=array[-1]) | (value<=array[0]):
            if (value==array[-1]) | (value==array[0]):
                if (value==array[-1]):
                    return -2,array.__len__()-1
                else:
                    return 0,1
            print ('Value out of range!!')
            return 0
#         array = 
        nearidx=(np.abs(array - value)).argmin()
        if value>array[nearidx]:
            return nearidx,nearidx+1
        elif value<array[nearidx]:
            return nearidx-1,nearidx
        else:
            return nearidx-1,nearidx+1
#         for i in range(self.flexarrIndexRangeArray.__len__()-1):
#             self.flexarray[self.flexarrIndexRangeArray[i]:self.flexarrIndexRangeArrayi+1]]
    def find_leftright_indxs(self,value):
        steparray=self.flexarray[self.flexarrIndexRangeArray]
        # print('step array : ',steparray)
        # print('val =',value)
        li,ri=self.find_indx_leftright(steparray,value)
        # if li==ri:
        #     return 0,0
#         print(li,ri,self.flexarrIndexRangeArray[[li,ri]])
        
        smallarray=self.flexarray[self.flexarrIndexRangeArray[li]:self.flexarrIndexRangeArray[ri]+1]
        # print('hey',smallarray)
        lgi,rgi=self.find_indx_leftright(smallarray,value)
        return self.flexarrIndexRangeArray[li]+lgi,self.flexarrIndexRangeArray[li]+rgi     

    def find_leftright_vlaues(self,value):
#         steparray=self.flexarray[self.flexarrIndexRangeArray]
# #         print(steparray)
#         li,ri=self.find_indx_leftright(steparray,value)
#         print(li,ri,self.flexarrIndexRangeArray[[li,ri]])
        
#         smallarray=self.flexarray[self.flexarrIndexRangeArray[li]:self.flexarrIndexRangeArray[ri]+1]
# #         print('hey',smallarray)
#         lgi,rgi=self.find_indx_leftright(smallarray,value)
#         return smallarray[[lgi,rgi]]
            if (value<self.flexarray[0]):
                return [np.nan,self.flexarray[0]]
            elif(value>self.flexarray[-1]):
                return [self.flexarray[-1],np.nan] 
            else:
                return self.flexarray[[self.find_leftright_indxs(self,value)]]
        
class FlexXY(FlexArray): 
    def __init__(self,XY):# XY should be an (N,2) shape np array
        self.XY=XY
        super(FlexXY,self).__init__(self.XY[:,0])
    def get_LRofXYs(self,xvalue):
        
        if (xvalue<self.XY[0,0]):
            return np.array([[self.XY[0,0]-self.stepsize,np.nan],[self.XY[0,0],self.XY[0,1]] ])
        elif(xvalue>self.XY[-1,0]):            
            return np.array([[self.XY[-1,0],self.XY[-1,1]],[self.XY[-1,0]+self.stepsize,np.nan] ])
        else:
            li,ri=self.find_leftright_indxs(xvalue)
    #         print(li,ri)
            return self.XY[[li,ri],:]
    def get_LRindxOfXYs(self,xvalue):
        li,ri=self.find_leftright_indxs(xvalue)
#         print(li,ri)
        return li,ri
    def predictYgivenX(self,xvalue):
        lr=self.get_LRofXYs(xvalue)
        return lr[0,1]+(xvalue-lr[0,0])*(lr[1,1]-lr[0,1])/(lr[1,0]-lr[0,0])     
        
    
    def resampleY(self,new_xarray):
        # print(new_xarray)
        newY=np.zeros(len(new_xarray))
        for i in range(len(new_xarray)):
            newY[i]=self.predictYgivenX(new_xarray[i])
        return newY
    def resampleXY(self,new_xarray):
        newy=self.resampleY(new_xarray)#         
        return np.append(new_xarray.T,newy.T)

class FlexLog(FlexXY):
    def __init__(self,XY):
        super(FlexLog,self).__init__(XY)
        self.logstep=self.XY[:,1]-self.XY[:,0]
        # np.unique(np.diff(self.XY[:,0].T))        
        # if self.logstep.__len__()>1:
        #     print( 'log step size varies... not a log array')
        #     return None
    def logExtend(self,newLog,depthminmax=(None,None),replace='top'):
#         newLog=FlexLog(newLog)
        self.toplog='existing'
        if not depthminmax[0]:
            if(newLog[0,0]<self.XY[0,0]):
                depthminmax[0]=newLog[0,0]
                self.toplog='incoming'
            else:                
                depthminmax[0]=self.XY[0,0]
            if(newLog[-1,0]>self.XY[-1,0]):
                depthminmax[1]=newLog[-1,0]
            else:
                depthminmax[1]=self.XY[-1,0]
        flexnewLog=FlexLog(newLog)
        merged_xarray=np.arange(depthminmax[0],depthminmax[1],self.logstep)
        if self.toplog=='existing':
            if replace=='top':
                start_depth_bottom_log=newLog[0,0]
            else:
                start_depth_bottom_log=self.XY[-1,0]+self.logstep[0]
        else:
            if replace=='top':
                start_depth_bottom_log=self.XY[0,0]
            else:
                start_depth_bottom_log=newLog[-1,0]+self.logstep[0]
        
    def clip(self,drange=(None,None)):
        self.XY=self.XY[(self.XY[:,0]>=drange[0]) & (self.XY[:,0]<=drange[1])]
            
if __name__=='__main__':
    np.set_printoptions(edgeitems=3,infstr='inf',linewidth=75, nanstr='nan', precision=2,suppress=False, threshold=1000, formatter=None)

    a=np.arange(0,20,0.05)
    a.shape=len(a),1
    c=np.arange(0,20,0.1)
    b=np.sin(a)
    xy=np.append(a,b,axis=1)
    plt.plot(xy[:,0],xy[:,1],'-*')
    # plt.plot(a,b)
    flexXY=FlexLog(xy)

    newxy=flexXY.resampleXY(c)

    plt.plot(newxy[:,0],newxy[:,1])
    plt.show()
