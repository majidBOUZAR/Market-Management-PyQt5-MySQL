from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5 import uic,QtWidgets
from barcode import *
from barcode.writer import *
from barcode import EAN13
import datetime,mysql.connector
from MainWindow2 import *
from index import * 

MainUI2,_=loadUiType('login.ui') 

user_profile = []
userid =  0



class Window3(QMainWindow,MainUI2):################ handle interface
    def __init__(self, parent=None):
        super(Window3, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connect_button()
        self.db_connection()
     
        
        
    def connect_button (self):   
        self.pushButton_27.clicked.connect(self.user_login)  

    def db_connection(self) :
     self.db = mysql.connector.connect(
                        database="superette",
                        host="localhost",
                        user="root",
                        password="root"
                        )
     self.cur = self.db.cursor()

        
    def user_login(self):



        username=self.lineEdit_22.text()
        password=self.lineEdit_23.text()
        
        sql = self.cur.execute(""" SELECT nom , password , id FROM users""")
        data_ = self.cur.fetchall()
        for row in data_ :
            if row[0] == username and row[1] == password :
               
 
                self.ind= main()
                self.ind.show()
                w.close()
                
                self.uid=row [2]
                print(self.uid)
                
                
                self.cur.execute('''
                    SELECT * FROM permission WHERE emp_name = %s
                ''',(username,))
                user_permissions = self.cur.fetchone()
               
                if user_permissions[1] == 1 :
                    self.ind.pushButton.setEnabled(True)
                    
                if user_permissions[2] == 1 :
                    self.ind.pushButton_2.setEnabled(True)

                if user_permissions[3] == 1 :
                    self.ind.pushButton_3.setEnabled(True)

                if user_permissions[4] == 1 :
                    self.ind.pushButton_4.setEnabled(True)

                if user_permissions[5] == 1 :
                    self.ind.pushButton_5.setEnabled(True)

                if user_permissions[6] == 1 :
                    self.ind.pushButton_6.setEnabled(True)

                if user_permissions[7] == 1 :
                    self.ind.pushButton_19.setEnabled(True)
                    
             
                action = 1
                table = 7
                dat3 = datetime.datetime.utcnow()
                self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                    VALUES (%s, %s , %s, %s )
                ''' )  , (userid,action,table,dat3))   

                self.db.commit()
                self.ind.tableWidget_4.clear()
                self.ind.show_historique()    
       
      
    
if __name__ == '__main__':
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
 
    
    w = Window3()
    w.show()
    sys.exit(app.exec_())
    
       