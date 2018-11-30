from PyQt5.QtCore import QDate, QFile, Qt, QTextStream
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)
from PyQt5.QtGui import QPixmap,QImage,QPainter,QColor,QBrush,QMouseEvent,QPen
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QDockWidget,QWidgetItem,
        QScrollArea,QVBoxLayout,QHBoxLayout,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit,QLabel,QWidget)
# import pyqtgraph as pg
import numpy as np
from PIL.ImageQt import ImageQt
from scipy.misc.pilutil import toimage
import dockwidgets_rc
import lasio
import os
import pyqtgraph as pg
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
from helper import *
from LogPlot import LogPlot
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100,100, 600,900)

        self.centralWidget = QWidget()
        # GrphicsWidget()
        layout = QHBoxLayout(self.centralWidget)
        self.scrollArea = QScrollArea(self)

        # gwidget=GrphicsWidget()

        self.mw = MatplotlibWidget(size=(3.0, 40.0), dpi=100)
        lplot=self.mw.getFigure().add_subplot(121) 
        # print(dir(self.mw.getFigure()))
        
        # self.mw.getFigure().set_axes([0.85, 0.1, 0.075, 0.8])
        self.ax=self.mw.getFigure().gca()   
        self.ax.set_position([0.1,0.05,0.8,0.94])
        self.ax.invert_yaxis()
        # l, b, w, h = self.ax.get_position().bounds     
        # print(l, b, w, h)
        self.mw.draw()
        # self.plotlayout.addWidget(self.mw)

        self.scrollArea.setWidget(self.mw)

        layout.addWidget(self.scrollArea)

        self.setCentralWidget(self.centralWidget)
        self.createDockWindows()
        self.wellLoad()
        self.logFileList.itemSelectionChanged.connect(self.lasLoad)
        # if not self.las_just_selected:
        self.logList.itemSelectionChanged.connect(self.logPlot)


        self.setWindowTitle("Loggy")

        # self.newLetter()
    def wellLoad(self):
        self.wellFolder=r'D:\Ameyem Office\Projects\Cairn\W1\LAS\\'
        
        files=os.listdir(self.wellFolder)[:]
        self.logFileList.addItems(files)
        
    def lasLoad (self):        
        las_name=self.logFileList.selectedItems()[0].text()
        self.las=lasio.read(self.wellFolder+las_name)
        if len(self.logList.selectedItems())>0:
            item = self.logList.selectedItems()[0]
            print(dir(item))
            item.setSelected= False
        self.logList.clear()
        self.logList.addItems(self.las.keys() )
        dcol=self.las.keys()[find_depth_indx(self.las)]
        self.depth_col=str_array2floats(self.las[dcol])
        # self.las_just_selected = True

        
        
    def logPlot(self):
        # print(self.mw.getFigure().)
        # pass
        # if not self.las_just_selected:
        if len(self.logList.selectedItems())>0:
            keycol=self.logList.selectedItems()[0].text()
            self.log_col=str_array2floats(self.las[keycol])            
            self.ax=LogPlot.basicPlot(self.ax,self.depth_col,self.log_col,lcolor='#800000')
        # else:
        #     self.las_just_selected=False

        
        # fig.subplots_adjust(top=0.75,wspace=0.1)
        
        # ax.invert_yaxis()
        # ax.plot([1,2,3],[2,1,4],'*')
        self.mw.draw()
        # self.subplot1 = self.mw.getFigure().add_subplot(121)

    def createDockWindows(self):
        
        dock = QDockWidget("Log Files", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.logFileList = QListWidget(dock)
        # self.customerList.addItems(('Hello','How are you'))
        dock.setWidget(self.logFileList)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Logs", self)
        self.logList = QListWidget(dock)
        self.logList.addItems(('Good morning','Hope you are doing well'))
        dock.setWidget(self.logList)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())

        # self.customerList.currentTextChanged.connect(self.insertCustomer)
        # self.logList.currentTextChanged.connect(self.addParagraph)

# class GrphicsWidget(QWidget):

#     def __init__(self):
#         super(GrphicsWidget, self).__init__()
#         self.initUI()
#         # self.pixmap=QPixmap("screenshot-camera.jpg")
#         self.pixmap=self.getSeispixmap()
		
#     def initUI(self):
#         self.text = "hello world"
#         self.setGeometry(0,0, 200,200)
#         self.setWindowTitle('Draw Demo')
#         self.center = None
#         self.horx=[]
#         self.hory=[]
#     #   self.show()
#     def mousePressEvent(self, event):
#         self.horx.append(event.pos().x())
#         self.hory.append(event.pos().y())
#         print('event',event.pos().x(),event.pos().y())
#         if event.button() == QtCore.Qt.LeftButton:
#             event = QMouseEvent(QtCore.QEvent.MouseButtonRelease, event.pos(), QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
#             # if (abs(event.pos().x())<=self.rect().width()): 
#             self.center = event.pos()
#             self.update()
#             QtWidgets.QWidget.mousePressEvent(self, event)
#     def paintEvent(self, event):
#         qp = QPainter()
#         qp.begin(self)
#         # qp.setPen(QColor(Qt.red))
#         # qp.setFont(QFont('Arial', 20))
            
#         # qp.drawText(10,50, "hello Python")
#         # qp.setPen(QColor(Qt.blue))
#         # qp.drawLine(10,100,100,100)
#         # qp.drawRect(10,150,150,100)
            
#         # qp.setPen(QColor(Qt.yellow))
#         # qp.drawEllipse(100,50,100,50)
        
#         qp.drawPixmap(0,0,self.pixmap)
#         if (self.center):
#         #     qp.drawEllipse(self.center, 24, 24)  
#         # qp.fillRect(200,175,150,100,QBrush(Qt.SolidPattern))
#             self.drawPoints( qp)
#         qp.end()
#         self.resize(self.pixmap.width(),self.pixmap.height())
#     def getSeispixmap(self):
#         folder=r'D:\Arun\Blade_project\Seismic data\\'
#         filename = folder+'RTM_uncalibrated_DTC.sgy'
#         self.scaleFactor_x=4
#         self.scaleFactor_y=0.3
#         # image_data =  np.random.randint(255, size=(200, 400))

#         with segyio.open(filename) as src:
#             ilines = src.ilines[:500]
#             xlines = src.xlines[:500]
#             image_data = src.iline[ilines[255]]
#         pilImage = toimage(image_data.T)
#         qtImage = ImageQt(pilImage)
#         # print(image_data)
#         image = QImage(qtImage)
#         image = image.scaled(self.scaleFactor_x*image.width(), self.scaleFactor_y*image.height())
#         return QPixmap.fromImage(image)
#     def drawPoints(self,qp):          
        
#         pen=QPen(Qt.green, 3, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin);
#         qp.setPen(pen)
#         # pen.setStyle(Qt.DashDotLine);
#         # pen.setWidth(3);
#         # pen.setBrush(Qt.green);
#         # pen.setCapStyle(Qt.RoundCap);
#         # pen.setJoinStyle(Qt.RoundJoin);
#         size = self.size()
        
#         for x,y in zip(self.horx,self.hory):
#             # x = np.random.randint(1, size.width()-1)
#             # y = np.random.randint(1, size.height()-1)
#             print(x,y,end='; ')
#             qp.drawPoint(x, y)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
