from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5 import uic,QtWidgets
import sys
import  mysql.connector
from barcode import *
from barcode.writer import *
from barcode import EAN13
import datetime
from MainWindow2 import *

MainUI2,_=loadUiType('des_test.ui') 
    
class Window2(QMainWindow,MainUI2):################ handle interface
    def __init__(self, parent=None):
        super(Window2, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.button() 
        
    def button(self):    
        self.lineEdit_6.textChanged.connect(self.total)
    
    def total (self):
      pay=self.lineEdit_6.text()
      pay2=self.lineEdit_7.setText('0')
      if pay and pay2 is not None :
       result=float(pay)-float(pay2)   
       print(result)
       pay2=self.lineEdit_8.text(result)
       