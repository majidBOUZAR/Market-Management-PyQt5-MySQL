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
import win32print

MainUI2,_=loadUiType('des_test.ui') 
    
    
    
class Window2(QMainWindow,MainUI2):################ handle interface
    
    def __init__(self, parent=None):
        super(Window2, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.button() 

        self.db_connection()
        self.client()
               
    def db_connection(self) :
        self.db = mysql.connector.connect(
                        database="superette",
                        host="localhost",
                        user="root",
                        password="root"
                        )
        self.cur = self.db.cursor()    
        
    def button(self):    
        self.lineEdit_6.textChanged.connect(self.total)
        self.checkBox.stateChanged.connect(self.handle_client)
        self.pushButton_13.clicked.connect(self.insert_in_client)
    
    def total (self):
        font = QtGui.QFont("DS-Digital", 55)
        font.setBold(True)
        self.lineEdit_6.setFont(font)
        self.lineEdit_7.setFont(font)
        pay=self.lineEdit_6.text()
        pay2=self.lineEdit_7.setText('0')
        if pay and pay2 is not None :
            result=float(pay)-float(pay2)   
            print(result)
            pay2=self.lineEdit_8.text(result)
    
    def handle_client(self):

            self.comboBox.setEnabled(True)
                 
    def insert_in_client(self):
       
            nonpayer1=self.lineEdit_6.text()
            payer1=self.lineEdit_7.text()
            nom=self.comboBox.currentText()
            date=datetime.datetime.now()
            
            self.cur.execute('''
                            UPDATE clients set nom=%s , payer=(payer + %s) , nonpayer=(nonpayer + %s) , date =%s
                            WHERE nom=%s
                            ''',(nom,payer1,nonpayer1,date,nom))
            tr = self.db.commit()
            if tr is True :
                print('done')
                     
    def client (self) :
        self.cur.execute('''
                         SELECT * FROM clients
                         ''')
        data = self.cur.fetchall()
        for x in data :
            self.comboBox.addItem(x[1])

    def keyPressEvent(self,event):
                
            if event.key() == 16777220 :
                self.insert_in_client()

          