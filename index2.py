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
from index import *

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
    
    def total (self):
        pay=self.lineEdit_6.text()
        pay2=self.lineEdit_7.setText('0')
        if pay and pay2 is not None :
            result=float(pay)-float(pay2)   
            print(result)
            pay2=self.lineEdit_8.text(result)
    def client (self) :
        self.cur.execute('''
                         SELECT * FROM clients
                         ''')
        data = self.cur.fetchall()
        print(data)
        for x in data :
            self.comboBox.addItem(x[1])
if __name__ == '__main__':
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window2()
    w.show()
    sys.exit(app.exec_())
                