from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from LasTree import treeWidgetFrmDict,get_txtdict,write_txtdict
import numpy as np
# from PIL.ImageQt import ImageQt
# from scipy.misc.pilutil import toimage
import lasio
import os
import pyqtgraph as pg
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
import time
# From files of app
import dockwidgets_rc
from LasLoadThread import LasLoadThread
from helper import *
from LogPlot import LogPlot
from LasTree import LasTree
def lag_ix(x,y,corrtype='+ve',dist2look=50):
        
    fullcorr = np.correlate(x,y,mode='full')
    halflen=round((fullcorr.size-1)/2)
    corr=fullcorr[halflen-dist2look:halflen+dist2look]
#     corr=fullcorr
    if corrtype=='+ve':
        pos_ix = np.argmax( corr) 
    elif corrtype=='-ve':
        pos_ix = np.argmin( corr)
    else:
        pos_ix = np.argmax( np.abs(corr) )
    lag_ix = pos_ix - (corr.size-1)/2
    return lag_ix
#     return halflen-dist2look+lag_ix
def get_delay(A,B,dt,corrtype='+ve',dist2look=50):
    timea=np.arange(0,len(A))
    timeb=np.arange(0,len(B))
    # compute cross correlation

    coor = np.correlate(A, B, 'full')
    maxlag = (coor.size-1)/2 
    lag = np.arange(-maxlag, maxlag+1)*dt
    delay_estimation = -(lag_ix(A,B,corrtype=corrtype,dist2look=dist2look)-0.5)*dt
    # line = ax[1].axvline(x=-delay_estimation, ymin=np.min(coor), ymax = np.max(coor), linewidth=1.5, color='c')
    # print('delay: %.2f and delay in terms of n samples: %.2f'%(delay_estimation,delay_estimation/dt))
    return delay_estimation,(lag, coor)


def mean_norm(A):
    A=A-np.mean(A)
    return A/np.linalg.norm(A)
    # def cross_correlate(a,b):
            

class LateralCorr(QMainWindow):
    def __init__(self,parent=None):
        super(LateralCorr, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle('Lateral Correlations')
        self.setGeometry(100,100, 900,400)

        layout = QHBoxLayout(self.centralWidget)
        self.logscrollArea = QScrollArea(self)
        # self.corrscrollArea = QScrollArea(self)

        # layout.addWidget(self.corrscrollArea)
        layout.addWidget(self.logscrollArea)
        self.setCentralWidget(self.centralWidget)

        # self.create_plotWindow()        
        self.createDockWindows()

    def logPlot(self):
        
        # self.corrscrollArea.setWidget(self.cw)       
        self.interestedLognames=[]
        for key in self.treeview_dict['Log']:
            self.interestedLognames.extend(self.treeview_dict['Log'][key]) 
        self.interestedLognames=np.array(self.interestedLognames).ravel()
        self.mw = MatplotlibWidget(size=(22.0, len(self.interestedLognames)*1.6), dpi=100)   
        # self.cw = MatplotlibWidget(size=(8.0, 8.0), dpi=100)     
        # self.mw.draw()
        self.logscrollArea.setWidget(self.mw) 
        
        dcol=self.las.keys()[find_depth_indx(self.las)]
        self.depth_col=self.las[dcol]
        dt=self.depth_col[1]-self.depth_col[0]
        print('Spacing = ',dt)
        self.gammacol=self.las[self.treeview_dict['Log']['GR'][0]]
        self.gammacol[np.isnan(self.gammacol)]=0
        self.ax=[]
        lag_corrs=[]
        self.delays=[]
        for i,keycol in enumerate(self.interestedLognames):
            self.ax.append(self.mw.getFigure().add_subplot(len(self.interestedLognames),1,i+1) )
            l, b, w, h = self.ax[-1].get_position().bounds 
            self.ax[-1].set_position([0.27,b,0.7,h])
            self.log_col=self.las[keycol]  
            self.log_col[np.isnan(self.log_col)]=0

            norm_gamma=mean_norm(self.gammacol)#[0:800]
            norm_blog=mean_norm(self.log_col)#[0:800]
            dist2look=100
            delay_estimation,lag_corr= get_delay(norm_gamma,norm_blog,dt,corrtype='abs',dist2look=dist2look)
            self.delays.append(-delay_estimation)
            lagcor_range=np.arange(round(len(lag_corr[0])/2)-4*dist2look,round(len(lag_corr[0])/2)+4*dist2look)
            lag_corrs.append((lag_corr[0][lagcor_range],lag_corr[1][lagcor_range]))
            depthb_shift=self.depth_col-delay_estimation
            self.ax[-1].plot(self.depth_col,norm_blog,'b')
            self.ax[-1].plot(self.depth_col,norm_gamma,'r')
            self.ax[-1].plot(depthb_shift,norm_blog,'magenta')
            # line = self.ax[-1].axvline(x=-delay_estimation, ymin=-1, ymax = +1, linewidth=1.5, color='c')
        lenax=len(self.ax)
        for i,keycol in enumerate(self.interestedLognames):
            self.ax.append(self.mw.getFigure().add_subplot(len(self.interestedLognames),2,lenax+i+1) )
            l, b, w, h = self.ax[i].get_position().bounds

            print(l, b, w, h)
            self.ax[-1].set_position([0.03,b,0.21,h])

            # self.log_col=self.las[keycol]  
            # self.log_col[np.isnan(self.log_col)]=0
            # norm_gamma=mean_norm(self.gammacol)#[0:800]
            # norm_blog=mean_norm(self.log_col)#[0:800]
            # # x = np.empty(len(A)-len(B))
            # # x[:]=0
            # # B=np.append(B,x)
            # delay_estimation,lag_corr=get_delay(norm_gamma,norm_blog,dt,corrtype='abs')
            # depthb_shift=self.depth_col-delay_estimation
            # print(self.depth_col)
            # print(norm_blog)
            self.ax[-1].plot(lag_corrs[i][0],lag_corrs[i][1],'b')
            self.ax[-1].text(self.delays[i],min(lag_corrs[i][1]),'Delay = %.2f'%self.delays[i])
            line = self.ax[-1].axvline(x=self.delays[i], ymin=-1, ymax = +1, linewidth=1.5, color='c')
            # self.ax[-1].plot(self.depth_col,norm_gamma,'r')
            # self.ax[-1].plot(depthb_shift,norm_blog,'magenta')
            

        
        self.mw.draw()
    def buildLogTree(self,files_w_path):
        w = LasTree()
        self.lasLoadThread = LasLoadThread(files=files_w_path)
        print(self.lasLoadThread.Lases)
        notloaded=True
        while notloaded:
            if (len(self.lasLoadThread.Lases)>0):
                if (len(self.lasLoadThread.Lases[0].keys())>0):
                    self.las=self.lasLoadThread.Lases[0]      
                    # print(self.logs) 
                    w.set_files(self.las.keys())
                    del w.treeview_dict['Log']['NA']
                    self.treeview_dict=w.treeview_dict
                    
                    w.buildTreeWidget()  
                    # print(self.interestedLognames)              
                    # w.tree.clear()
                    # w.buildTreeWidget()
                    notloaded=False
            time.sleep(1)
        # print(w.treeview_dict)
        self.dock.setWidget(w.tree) 
        
    # def create_plotWindow(self):
        
        
    def createDockWindows(self):        
        self.dock = QDockWidget("Log Files", self)
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # dock.setWidget(self.lastree.tree)        
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        
        # self.set_category_button = QPushButton('Set Category', self)
        # dock = QDockWidget("Set", self)
        # dock.setWidget(self.set_category_button)
        # self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        # self.set_category_button.clicked.connect(self.set_category)

        # dock = QDockWidget("Logs", self)        
        # dock.setWidget(self.logtree.tree)
        # self.addDockWidget(Qt.LeftDockWidgetArea, dock)
    
if __name__ == '__main__':
    
    import sys

    app = QApplication(sys.argv)
    mainWin = LateralCorr()
    wellFolder=r'D:\Ameyem Office\Projects\Cairn\W1\LAS\\'
        
    files=np.array(os.listdir(wellFolder)[:])
    

    files_w_path=[wellFolder+'W1_SUITE1_COMPOSITE.las']
    mainWin.buildLogTree(files_w_path)
    mainWin.logPlot()
    mainWin.show()
    sys.exit(app.exec_())