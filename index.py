from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5 import uic,QtWidgets
import sys,datetime,random, mysql.connector,time ,cv2,barcode,threading
from barcode import *
from barcode.writer import *
import barcode
from pyzbar.pyzbar import decode
from index2 import *
from login import *
import pyqtgraph as pg
from xlsxwriter import *
from xlrd import *

MainUI,_=loadUiType('des_v2.ui')

userid =  0
class main(QMainWindow,MainUI):################ handle interface
        
    def ok_button(self):### call window of payement 
        if self.tableWidget.rowCount() == 0 :
            QMessageBox.information(self ,"information" , "table deja vide")
        else :  
            self.pushButton_13.clicked.connect(self.calcul)
            self.w = Window2()
            self.w.show()
         
            self.w.pushButton_13.clicked.connect(self.vente)
            self.w.pushButton_13.clicked.connect(self.recette)
            self.w.pushButton_14.clicked.connect(self.annuler_payment)
    

    def __init__(self, parent=None):
        super(main, self).__init__(parent) # Call the inherited classes __init__ method
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui_change()
        self.w = Window2()
        
        self.db_connection()
        self.handle_button()
        self.ui_change()
        self.show_categorie()
        self.show_produit()
        self.show_users()
        self.historique()
        self.total()
        self.show_historique()
        self.dashboard()
        self.display_recette()
        
    def ui_change(self) :
    #UI changes in login
     self.tabWidget.tabBar().setVisible(False)#make the main tab bar invisible
     self.lineEdit_6.setText("0") 
      
    def db_connection(self) :
     self.db = mysql.connector.connect(
                        database="superette",
                        host="localhost",
                        user="root",
                        password="root"
                        )
     self.cur = self.db.cursor()
    print('db connected successful')

################ connect les button avec tab widgetS
    def handle_button(self) :
        self.pushButton_25.clicked.connect(self.open_login_tab)#connect button with tab widget
        self.pushButton.clicked.connect(self.open_vente_tab)
        self.pushButton_2.clicked.connect(self.open_produit_tab)
        self.pushButton_3.clicked.connect(self.open_client_tab)
        self.pushButton_4.clicked.connect(self.open_dashboard_tab)
        self.pushButton_5.clicked.connect(self.open_report_tab)
        self.pushButton_6.clicked.connect(self.open_parametre_tab)
        self.pushButton_19.clicked.connect(self.open_historique_tab)
        self.pushButton_23.clicked.connect(self.ajouter_categorie)
        self.pushButton_38.clicked.connect(self.delete_category)
        self.pushButton_9.clicked.connect(self.ajouter_produit)
        
        self.pushButton_33.clicked.connect(self.export_data)
        
        
        self.checkBox.stateChanged.connect(self.generate_barcode)
        self.pushButton_12.clicked.connect(self.search_produit)
    
        
        self.pushButton_28.clicked.connect(self.clear_all)
        self.pushButton_11.clicked.connect(self.modifie_produit)
        self.pushButton_10.clicked.connect(self.supprimer_produit)
        self.pushButton_29.clicked.connect(self.rechechre_stock)
        self.lineEdit_2.textChanged.connect(self.filter)
        #self.lineEdit_5.textChanged.connect(self.searrech_produit)
        self.pushButton_49.clicked.connect(self.employe)
        self.pushButton_34.clicked.connect(self.supprimer_row)
        self.pushButton_7.clicked.connect(self.copy_row)
        self.pushButton_14.clicked.connect(self.annuler_payment)
        self.pushButton_40.clicked.connect(self.verifier_user)
        self.pushButton_35.clicked.connect(self.modifier_users)
        self.pushButton_32.clicked.connect(self.BarcodeReader)
        self.pushButton_37.clicked.connect(self.BarcodeReader_product)
        #self.pushButton_13.clicked.connect(self.handle_item_changed)
        self.tableWidget.itemChanged.connect(self.calcul)
        self.pushButton_13.clicked.connect(self.calcul)
        #self.pushButton_13.clicked.connect(self.vente)
        self.pushButton_13.clicked.connect(self.ok_button)
        self.tableWidget_6.itemPressed.connect(self.copy_row)
        #self.tableWidget.itemPressed.connect(self.ok_button)
        self.lineEdit_3.textChanged.connect(self.rechechre_stock)   
        self.lineEdit.textChanged.connect(self.search_insert_by_code)   
        self.doubleSpinBox.valueChanged.connect(self.teaux)   
        self.doubleSpinBox_2.valueChanged.connect(self.teaux)   
        self.pushButton_36.clicked.connect(self.permission)
        self.pushButton_27.clicked.connect(self.user_login)
        self.pushButton_sup_his.clicked.connect(self.delete_historique)
        self.comboBox_cat.currentTextChanged.connect(self.display_category_lineedit)
        self.pushButton_39.clicked.connect(self.update_category)
        self.pushButton_45.clicked.connect(self.toggleFullScreen)
        #self.checkBox_28.stateChanged.connect(self.droi_admine_true)
     
     
     
     
 ##############################" link button side barre in tab widget
    def open_login_tab(self) :
        self.tabWidget.setCurrentIndex(0)#current index of tab widget    
        
    def open_vente_tab(self) :
        self.tabWidget.setCurrentIndex(1)   
          
    def open_produit_tab(self) :
        self.tabWidget.setCurrentIndex(2) 
        self.tabWidget_2.setCurrentIndex(0) 
        
    def open_client_tab(self) :
        self.tabWidget.setCurrentIndex(3)
        
    def open_dashboard_tab(self) :
        self.tabWidget.setCurrentIndex(4)
        
    def open_report_tab(self) :
        self.tabWidget.setCurrentIndex(5)
        
    def open_parametre_tab(self) :
        self.tabWidget.setCurrentIndex(6)
        
    def open_historique_tab(self) :
        self.tabWidget.setCurrentIndex(7)            
                    
############################# read barcode whene click button ################################     
    def BarcodeReader(self):

        vid = cv2.VideoCapture(1)
        camera = True
        while camera == True :
            
            success, img = vid.read()
            detectedBarcodes = decode(img)
            print('scanner barcode is open')
            for barcode in detectedBarcodes:
                print('aprouved')
                print(str(barcode.data))
                time.sleep(0.5)
                st=str(int(barcode.data))
                self.lineEdit.setText(st[0:11])
                break
            QApplication.processEvents() # solution not responding    

    def BarcodeReader_product(self):    
        self.checkBox.setEnabled (False)
        self.lineEdit_7.setEnabled (False)    
        
        vid = cv2.VideoCapture(1)
        camera = True
        
        while camera == True :
            
            success, img = vid.read()
            detectedBarcodes = decode(img)
            print('scanner barcode 22 is open')
            for barcode in detectedBarcodes:

                time.sleep(0.5)
                st=str(int(barcode.data))
                self.lineEdit_7.setText(st[0:11])
                break
            QApplication.processEvents() # solution of not responding (Threding)        
    
    def generate_barcode(self):
       ## t = threading.Thread(target=self.log)
       ## t.start()
       ##### generate code
        nom=self.lineEdit_4.text()
        prix=self.doubleSpinBox_2.value()
        x=10**(13-1)
        y=(10**13)-1
        number = str(int(random.randint(x,y)))
        print(number)
        barCodeImage = barcode.get('EAN13', number, writer=ImageWriter())
        barCodeImage.save(f"barcode/bare_code_{nom}")
        print(nom)
        self.lineEdit_7.setText(number)  
        print("code checked") 
           
#        QMessageBox.information(self,'Information','This code barre deja exister dans ton repertoire')  
 
 ##############################  function query set of catrgory ############################### 
    def ajouter_categorie(self) :   ############################"
       category_name = self.lineEdit_21.text()
       if len(category_name):
        self.cur.execute('''
            INSERT INTO category (category_name)
            VALUES (%s )
         ''' , (category_name,))
       
       
        global userid
        action = 3
        table = 2
        
        dat3 = datetime.datetime.utcnow()
        
        self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
            VALUES (%s, %s , %s, %s )
        ''' )  , (userid,action,table,dat3))         
    
       
       self.db.commit()      
       self.lineEdit_21.clear()
       QMessageBox.information(self,'succes','Categorie a été bien ajouter')
       print('categorie success added')
       self.comboBox_cat.clear()
       self.tableWidget_4.clear()
       self.show_historique()
       self.show_categorie()          
       
    def show_categorie(self) :  ############################
        
            all = self.cur.execute(''' SELECT category_name from category''')#select all data 
            data = self.cur.fetchall()#return all data    
            for category in data :
                
                self.comboBox_3.addItem(str(category[0]))
                self.comboBox_cat.addItem(category[0])
         
    def  delete_category(self): 
        
            item =self.comboBox_cat.currentText()
            sql = (''' DELETE FROM category WHERE category_name = %s
                    ''')
            self.cur.execute(sql,(item,))
            delete_message = QMessageBox.warning(self,'Attention','Categorie sera effacé', QMessageBox.Yes|QMessageBox.No) 
            if delete_message == QMessageBox.Yes :
                action = 5
                table = 2
                dat3 = datetime.datetime.utcnow()
                self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                    VALUES (%s, %s , %s, %s )
                ''' )  , (userid,action,table,dat3))   
                self.db.commit()
        
                
                self.comboBox_cat.clear()
                self.tableWidget_4.clear()
                self.show_historique()
                self.show_categorie()
          
    def display_category_lineedit(self):
        
            item =self.comboBox_cat.currentText()
            self.lineEdit_24.setText(item) 
            
    def update_category(self):    
           
            cat = self.lineEdit_24.text()
            item =self.comboBox_cat.currentText()
            print(cat)
            self.cur.execute('''
                    UPDATE category SET category_name = %s WHERE category_name = %s
                ''',(cat,item))      
            print('success updated')
            QMessageBox.information(self,'Succes','Categorie modifié')                
            action = 4
            table = 2
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                    VALUES (%s, %s , %s, %s )
                ''' )  , (userid,action,table,dat3))   
            self.db.commit()
        
            self.db.commit()
            self.lineEdit_24.clear()
            self.comboBox_cat.clear()
            self.tableWidget_4.clear()
            self.show_historique()
            self.show_categorie()
            
 ##############################  function query set of product ################################    

         
    def show_produit(self):
        
        self.cur.execute(''' SELECT code,nom,prix_achat,prix_vente,quantite,details,categorie,Teaux from produit''')
        data=self.cur.fetchall()
         
        for row , form in enumerate(data):
            self.tableWidget_2.insertRow(row)
            for col , item in enumerate(form):
                self.tableWidget_2.setItem(row,col, QTableWidgetItem(str(item)))
                col = col + 1
         
    def search_produit(self):
        nom=self.lineEdit_10.text()
        sql = ('''
                SELECT * FROM produit WHERE nom = %s
            ''')   
        self.cur.execute(sql , [(nom)])
        value = self.cur.fetchone()
        sql2 = ('''
                SELECT * FROM category  
            ''')   
        self.cur.execute(sql2)
        value2 = self.cur.fetchall()
   
        self.db.commit()
             
        if (value)  : 
                    self.lineEdit_11.setText(value[1])
                    self.plainTextEdit_2.setPlainText(value[2])
                    self.doubleSpinBox_3.setValue(value[3])
                    self.doubleSpinBox_4.setValue(value[4])
                    self.spinBox_2.setValue(value[5])
                    self.lineEdit_12.setText(value[6])
                    self.comboBox_15.setCurrentText(value[8])
        for x in value2 :
                self.comboBox_15.addItem(x[1])
              
            
    def clear_all(self)   :
     
       self.lineEdit_11.clear()
       self.lineEdit_10.clear()
       self.plainTextEdit_2.clear()
       self.doubleSpinBox_3.clear()
       self.doubleSpinBox_4.clear()
       self.spinBox_2.clear()
       self.lineEdit_12.clear()
       
    def ajouter_produit (self):#############################

            self.cur.execute(''' SELECT category_name from category''') #select all data 
            data = self.cur.fetchall()#return all data
            for category in data :
             self.comboBox_3.addItem(str(category[0]))
            
            nom = self.lineEdit_4.text()
            details = self.plainTextEdit.toPlainText()
            prix_achat = self.doubleSpinBox.value()
            prix_vente = self.doubleSpinBox_2.value()
            quantite = self.spinBox.value()
            code  = self.lineEdit_7.text()
            categorie = self.comboBox_3.currentText()
            date = datetime.datetime.now()
            teaux  = self.lineEdit_9.text()
            
            self.cur.execute(('''INSERT INTO Produit(nom , details , prix_achat , prix_vente ,quantite,code,date,categorie,Teaux)
                VALUES (%s  , %s, %s ,   %s , %s , %s , %s, %s, %s   )
            ''' )  , (nom,details,prix_achat,prix_vente,quantite,code[0:11],date,categorie,teaux))

            global userid
            action = 3
            table = 6
            
            dat3 = datetime.datetime.utcnow()
            
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))            
            
            
            
            self.db.commit()      
            self.statusBar().showMessage('Produit a été bien ajouter')
            QMessageBox.information(self,'Succes','Produit a été bien ajouter')
            print('product success added')
            self.tableWidget_2.clear()
            self.tableWidget_4.clear()
            self.show_historique()
            self.show_produit()
                   
    def supprimer_produit(self):
        
        nom = self.lineEdit_10.text()
        delete_message = QMessageBox.warning(self ,"Produit supprimé" , "Vous etes sur !!",QMessageBox.Yes | QMessageBox.No )
        if delete_message == QMessageBox.Yes :
            sql = (''' DELETE from Produit where nom=%s
                ''')
            self.cur.execute(sql,[(nom)])
            
            global userid
            action = 5
            table = 6
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))    
            
            self.db.commit()
            
            self.lineEdit_11.clear()
            self.lineEdit_10.clear()
            self.plainTextEdit_2.clear()
            self.doubleSpinBox_3.clear()
            self.doubleSpinBox_4.clear()
            self.spinBox_2.clear()
            self.lineEdit_12.clear()
        self.tableWidget_4.clear()
        self.show_historique()            
        self.tableWidget_2.clear()
        self.show_produit() 
                
    def modifie_produit(self):
        try :
            nome = self.lineEdit_11.text()
            details = self.plainTextEdit_2.toPlainText()
            prix_achat = self.doubleSpinBox_3.value()
            prix_vente = self.doubleSpinBox_4.value()
            quantite = self.spinBox_2.value()
            code = self.lineEdit_12.text()
            categorie = self.comboBox_15.currentText()
            
            self.cur.execute('''
                UPDATE Produit SET nom = %s ,details = %s , prix_achat = %s , prix_vente = %s , quantite = %s , code = %s , categorie = %s WHERE code = %s
            ''',(nome,details,prix_achat,prix_vente,quantite,code,categorie,code))      
                        
            global userid
            action = 4
            table = 6
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))    
            
            self.db.commit()
            print(userid)
            QMessageBox.information(self,'succes','Produit a été bien modifer')
            
            self.tableWidget_2.clear()
            self.tableWidget_4.clear()
            self.show_historique()
            self.show_produit()
        except :
            QMessageBox.warning(self,'Erreur','No modification')
   
    def rechechre_stock(self):
            
        nom = self.lineEdit_3.text()

        sql = ''' SELECT code,nom,prix_vente,quantite from Produit WHERE nom = %s 
              '''
        self.cur.execute(sql ,[(nom)])
        data = self.cur.fetchall()


        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        for row , form in enumerate(data):
            for col , item in enumerate(form):
                    self.tableWidget_6.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
            row_position = self.tableWidget_6.rowCount()
           
            self.tableWidget_6.selectRow(row_position)
                    
    def search_produit_nom(self):
        
        nom = self.lineEdit_2.text()
        
        if len(nom)  :
         sql = ''' SELECT code,nom,prix_achat,prix_vente,quantite,details,categorie,Teaux from Produit WHERE nom = %s 
              '''
         self.cur.execute(sql ,[(nom),])
         data = self.cur.fetchall()
         self.tableWidget_2.setRowCount(0)
         self.tableWidget_2.insertRow(0)
        
         for row , form in enumerate(data):
            for col , item in enumerate(form):
                   
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position) 
                             
    def employe(self):
        nom = self.lineEdit_45.text()
        email = self.lineEdit_46.text()
        phone = self.lineEdit_47.text()
        password = self.lineEdit_48.text()
        password2 = self.lineEdit_49.text()
        date = datetime.datetime.now()
        if password == password2 : 
         sql = self.cur.execute(''' insert into users(nom,email,phone,password,password2,date) values (%s,%s,%s,%s,%s,%s)
                               ''',(nom,email,phone,password,password2,date))
        
         global userid
         action = 3
         table = 7
         dat3 = datetime.datetime.utcnow()
         self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))            
            
         self.db.commit()
         
         QMessageBox.information(self,'success','user a été ajouté')
         print('user a été ajouté')
        else : 
         QMessageBox.warning(self,'failes','password not much')
         
    def supprimer_row(self):
            if self.tableWidget.rowCount() == 0 :
                QMessageBox.information(self ,"information" , "table deja vide")
            else :          
                row_selected= self.tableWidget.currentRow()
                self.tableWidget.removeRow(row_selected)
                             
    def copy_row(self):
        
            for row1 in range(self.tableWidget_6.rowCount()):
                it = self.tableWidget_6.item(row1, 3)
                if it is not None :
                    res= it.text()
                    par=int(res)
                    print(res)
                    if res != '0' :
                        row= self.tableWidget_6.currentRow() 
                        targetRow = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(targetRow)
                        for column in range(self.tableWidget_6.columnCount()):
                            self.tableWidget.selectRow(row) 
                            item = self.tableWidget_6.takeItem(row, column)
                        
                            self.tableWidget.setItem(targetRow, column, item)
                            self.tableWidget.setItem(targetRow, 3, QTableWidgetItem('1'))                    
                    elif res == '' :    
                        pass
                    else :         
                        QMessageBox.warning(self,'warning','Quantité limite')

    def calcul(self):
        nrows = self.tableWidget.rowCount()
        f=0
        for row in range(0,nrows):
            prix_item = self.tableWidget.item(row, 2)
            quantite_item = self.tableWidget.item(row, 3)
            if prix_item  and quantite_item : #check if column is not null 
             s=float(prix_item.text())
             s1=float(quantite_item.text())
             mult=s1*s
             f=f+mult
             row+=1
        result = str(f)
        self.lineEdit_6.setText(result) 
        self.w.lineEdit_6.setText(result) 
        
    def teaux(self):
        prix_achat = self.doubleSpinBox.value()
        prix_vente = self.doubleSpinBox_2.value()
        t =  prix_vente / prix_achat 
        s=(t-1)*100
        m=int(s)
        val= str(m)
        self.lineEdit_9.setText(val + '%')
        
    def annuler_payment(self) :
            if self.tableWidget.rowCount() == 0 :
                QMessageBox.information(self ,"information" , "table deja vide")
            else :     
                delete_message = QMessageBox.warning(self ,"Annuler payement" , "Vous etes sur !!",QMessageBox.Yes | QMessageBox.No )
                if delete_message == QMessageBox.Yes :
                    self.tableWidget.setRowCount(0)
                    self.lineEdit_6.setText("0") 
            
    def verifier_user(self) : 
        nom=self.lineEdit_30.text() 
        password=self.lineEdit_29.text()
        self.cur.execute(''' select * from users  ''')
        data=self.cur.fetchall()
    
        for row in data :
            if row[1] == nom and row[4] == password :
            
             self.groupBox_3.setEnabled(True)
             self.lineEdit_33.setText(row[1]) 
             self.lineEdit_31.setText(row[2]) 
             self.lineEdit_32.setText(row[3]) 
    
    def modifier_users(self):
        nom=self.lineEdit_33.text() 
        email=self.lineEdit_31.text() 
        telephone=self.lineEdit_32.text()  
        self.cur.execute('''
             UPDATE users SET nom = %s ,email = %s , phone = %s WHERE nom = %s
               ''',(nom,email,telephone,nom))   
                    
        global userid
        action = 4
        table = 7
        dat3 = datetime.datetime.utcnow()
        self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
            VALUES (%s, %s , %s, %s )
        ''' )  , (userid,action,table,dat3))    
            
        self.db.commit()
        self.tableWidget_4.clear()
        self.show_historique()        
                     
    def show_users(self):
             
       
        self.tableWidget_7.insertRow(0)
        sql = ''' SELECT nom,email,phone,permission from users  
              '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
         
        
        for row , form in enumerate(data):
            for col , item in enumerate(form):
                    
                    self.tableWidget_7.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
            row_position = self.tableWidget_7.rowCount()   
            self.tableWidget_7.insertRow(row_position)
        for it in data :
         self.comboBox.addItem(it[0])
    
    def user_login(self):
            username=self.lineEdit_22.text()
            password=self.lineEdit_23.text()
            self.cur.execute(""" SELECT id , nom , password FROM users""")
            data_ = self.cur.fetchall()
            for row in data_ :
                
                if username=='' or password=='' :
                    self.label_45.setText('Veuillez remplir tous les champs ')
                     
                elif row[1] == username and row[2] == password :
                   
                    global userid 
                    userid = row[0]
                    
                    self.cur.execute('''
                        SELECT * FROM permission WHERE emp_name = %s
                    ''',(username,))
                    user_permissions = self.cur.fetchone()
                  
                    try:
                        if user_permissions[1] == 1 :
                            self.pushButton.setEnabled(True)   
                        if user_permissions[2] == 1 :
                            self.pushButton_2.setEnabled(True)    

                        if user_permissions[3] == 1 :
                            self.pushButton_3.setEnabled(True)    

                        if user_permissions[4] == 1 :
                            self.pushButton_4.setEnabled(True)   

                        if user_permissions[5] == 1 :
                            self.pushButton_5.setEnabled(True)
                            
                        if user_permissions[6] == 1 :
                            self.pushButton_6.setEnabled(True)
                            
                        if user_permissions[7] == 1 :
                            self.pushButton_19.setEnabled(True)
                    except :
                        QMessageBox.warning(self,'warning','Ce utilisateur na aucun droit pour y acceder le systeme ')    
                        self.label_45.setText('Admin autoriser de vous donnée acess') 

                    
                    action = 1
                    table = 7
                    dat3 = datetime.datetime.utcnow()
                    self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                        VALUES (%s, %s , %s, %s )
                    ''' )  , (userid,action,table,dat3))   
                    self.db.commit()
                    
                    self.tableWidget_4.clear()
                    self.show_historique()
                    self.label_45.setText('Connecter') 
                    
    def permission(self):
     emp_name=self.comboBox.currentText()    
     if self.checkBox_28.isChecked(): 
        privilege_message = QMessageBox.warning(self ,"Ajouter comme  admin" , "Vous etes sur !!",QMessageBox.Yes | QMessageBox.No )
        if privilege_message == QMessageBox.Yes :
            
            self.cur.execute(''' INSERT INTO `permission` (ventetab,produittab,clientstab,dashtab,reporttab,partab,histab,voir_pro_tab,ajou_pro_tab,modi_pro_tab,voir_cli_tab,ajou_cli_tab,modi_cli_tab,ajou_emp_tab,mod_emp_tab,perm_tab,is_admin,emp_name)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ''',(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,emp_name) )   
            global userid
            action = 7
            table = 7
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
             ''' )  , (userid,action,table,dat3))   
            self.db.commit()
            QMessageBox.information(self,'Succes','Privilége admin a été attribué avec success : \n \n' + emp_name)
            emp_name = self.comboBox.setCurrentIndex(0) 
            self.checkBox_28.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_13.setChecked(False)
            self.checkBox_12.setChecked(False)
            self.checkBox_20.setChecked(False)
            self.checkBox_19.setChecked(False)
            self.checkBox_23.setChecked(False)
            self.checkBox_22.setChecked(False)
            self.checkBox_21.setChecked(False)
            self.checkBox_24.setChecked(False)
            self.checkBox_26.setChecked(False)
            self.checkBox_25.setChecked(False)
            self.checkBox_27.setChecked(False)       
    
     else :
            vente_tab=0
            produit_tab=0   
            clients_tab=0
            dash_tab=0
            report_tab=0
            parametre_tab=0
            historique_tab=0
            voir_pro=0
            ajou_pro=0
            mod_pro=0
            voir_cli=0
            ajou_cli=0
            mod_cli=0
            ajou_emp=0
            mod_emp=0
            permi=0
            if self.checkBox_2.isChecked() == True :
                vente_tab=1            
            if self.checkBox_3.isChecked() == True :
                produit_tab=1
            if self.checkBox_4.isChecked() == True :
                clients_tab=1
            if self.checkBox_5.isChecked() == True :
                dash_tab=1
            if self.checkBox_6.isChecked() == True :
                report_tab=1
            if self.checkBox_13.isChecked() == True :
                parametre_tab=1
            if self.checkBox_12.isChecked() == True :
                historique_tab=1
            if self.checkBox_20.isChecked() == True :
                voir_pro=1
            if self.checkBox_19.isChecked() == True :
                ajou_pro=1
            if self.checkBox_23.isChecked() == True :
                mod_pro=1
            if self.checkBox_22.isChecked() == True :
                voir_cli=1
            if self.checkBox_21.isChecked() == True :
                ajou_cli=1
            if self.checkBox_24.isChecked() == True :
                mod_cli=1
            if self.checkBox_26.isChecked() == True :
                ajou_emp=1
            if self.checkBox_25.isChecked() == True :
                mod_emp=1
            if self.checkBox_27.isChecked() == True :        
                permi=1
            
            self.cur.execute(''' INSERT INTO `permission` (ventetab,produittab,clientstab,dashtab,reporttab,partab,histab,voir_pro_tab,ajou_pro_tab,modi_pro_tab,voir_cli_tab,ajou_cli_tab,modi_cli_tab,ajou_emp_tab,mod_emp_tab,perm_tab,emp_name)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ''',(vente_tab,produit_tab,clients_tab,dash_tab,report_tab,parametre_tab,historique_tab,voir_pro,ajou_pro,mod_pro,voir_cli,ajou_cli,mod_cli,ajou_emp,mod_emp,permi,emp_name) )    
            self.db.commit()
            QMessageBox.information(self,'Succes','Permission a été attribué avec success : \n \n' + emp_name)
            
            emp_name = self.comboBox.setCurrentIndex(0) 
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_13.setChecked(False)
            self.checkBox_12.setChecked(False)
            self.checkBox_20.setChecked(False)
            self.checkBox_19.setChecked(False)
            self.checkBox_23.setChecked(False)
            self.checkBox_22.setChecked(False)
            self.checkBox_21.setChecked(False)
            self.checkBox_24.setChecked(False)
            self.checkBox_26.setChecked(False)
            self.checkBox_25.setChecked(False)
            self.checkBox_27.setChecked(False)       
            self.groupBox_4.setEnabled(True)
            self.groupBox_5.setEnabled(True)
            self.groupBox_6.setEnabled(True)
            self.groupBox_7.setEnabled(True)

    def historique(self):
        self.cur.execute(''' select * from users ''')
        data = self.cur.fetchall()
        for row in data :
         self.comboBox_8.addItem(row[1]) 
         
    def total(self):
        self.cur.execute(''' SELECT sum(prix_achat*quantite) as sum1 ,sum(prix_vente*quantite),(sum(prix_vente*quantite))-(sum(prix_achat*quantite))  FROM produit
                         ''')    
        data = self.cur.fetchall()
        for row in data : 
         self.lineEdit_69.setText(str(row[0]))
         self.lineEdit_70.setText(str(row[1]))
         self.lineEdit_71.setText(str(row[2]))
  
    def search_insert_by_code (self):
        
        code = self.lineEdit.text()
        sql = ''' SELECT code,nom,prix_vente,quantite from Produit WHERE code = %s 
              '''
        self.cur.execute(sql ,[(code)])
        data = self.cur.fetchall()
         
        self.tableWidget.insertRow(0)
        for row , form in enumerate(data):
            for col , item in enumerate(form):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
            
            self.tableWidget.setItem(row, 3, QTableWidgetItem('1'))
  
    def vente(self):
        
        
        self.tableWidget.insertRow(0)
        for row1 in range(self.tableWidget.rowCount()):
            it = self.tableWidget.item(row1, 1)
            it2 = self.tableWidget.item(row1, 3)
            if it and it2 is not None :
                res= it.text()
                res2= it2.text()
                par=int(res2)
                print(par)
                sql = self.cur.execute(''' update produit set quantite=(quantite-%s) where nom = %s and quantite > %s 
                            ''',(res2,res,0))
                self.db.commit()

        self.w.close()
        self.tableWidget.setRowCount(0)
        self.lineEdit_6.setText("0") 
        self.tableWidget_2.clear()
        self.show_produit()
        self.tableWidget_5.clear()
        self.display_recette()
      
    def show_historique (self ):
         
        self.cur.execute(''' SELECT users_id , his_action ,his_table , his_date from historique ''')
        data=self.cur.fetchall()
         
        for row , form in enumerate(data):
            self.tableWidget_4.insertRow(row)
            for col , item in enumerate(form):
   
                if col == 0 :
                    
                 sql = (''' SELECT nom FROM users WHERE id = %s ''')
                 self.cur.execute(sql , [(item)])
                 te = self.cur.fetchone()
              
                 result = te[0]
                 self.tableWidget_4.setItem(row,col, QTableWidgetItem(result))
      
                elif col == 1 :
                    action = ' '
                    if item == 1 :
                        action = 'Connecté'

                    if item == 2 :
                        action = 'Deconnecté'

                    if item == 3 :
                        action = 'Ajouter'

                    if item == 4 :
                        action = 'Modifier'

                    if item == 5 :
                        action = 'Supprimer'

                    if item == 6 :
                        action = 'Rechercher'
                        
                    if item == 7 :
                        action = 'Ajouter Permission '     
                        
                        
                    self.tableWidget_4.setItem(row,col, QTableWidgetItem(str(action)))
                    
                    
                elif col == 2 :
                    Table = ' '
                    if item == 1 :
                        Table = 'Achats'

                    if item == 2 :
                        Table = 'Categorie'

                    if item == 3 :
                        Table = 'Client'

                    if item == 4 :
                        Table = 'Historique'

                    if item == 5 :
                        Table = 'Permission'

                    if item == 6 :
                        Table = 'Produit'
                        
                    if item == 7 :
                        Table = 'Utilisateur'
    
                    self.tableWidget_4.setItem(row,col, QTableWidgetItem(str(Table)))    
                    
                else  :

                 self.tableWidget_4.setItem(row,col, QTableWidgetItem(str(item)))   
                col = col + 1
    
    def delete_historique(self):
       
     
       delete_message = QMessageBox.warning(self,'Attention','Tous historique sera supprimer',QMessageBox.Yes | QMessageBox.No)  
       if delete_message == QMessageBox.Yes :
            self.cur.execute(''' TRUNCATE TABLE historique
                            ''')  
           
            action = 5
            table = 4
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))   

            self.db.commit()
            self.tableWidget_4.clear()
            self.show_historique()
       
    def search_historique(self):
        pass   

    def dashboard(self):

        
        filter_date = self.dateEdit.date()
        filter_date = filter_date.toPyDate()
        year = str(filter_date).split('-')[0]
       
        self.cur.execute(""" 
            SELECT COUNT(id), EXTRACT(day FROM date) as day
            FROM vente
            GROUP BY day
        """ )
        data = self.cur.fetchall()
        
        vente_count = []
        date_count = []
        
        for row in data:
                vente_count.append(row[0])
                date_count.append(row[1])#we appen data to liset bcz the chart accept only data in list
                
        barchart = pg.BarGraphItem(x=date_count , height=vente_count , width=.2)
        
        self.widget.addItem(barchart)             
        pen = pg.mkPen(color = (165, 120, 255),size = 130)
        self.widget.setBackground('w')
        self.widget.setTitle('Statistique de vente dans dernier 30 jours', Size = 50 , color = 'Blue')
        self.widget.showGrid(x=True,y=True)
        self.widget.addLegend()
        self.widget.setLabel('left','vente',color='Blue',size = 130)
        self.widget.setLabel('bottom','30 jours',color='Blue',size = 130)

    def recette (self):
        total = self.w.lineEdit_6.text()    
       
        date = datetime.datetime.now()
        self.cur.execute('''
            INSERT INTO vente (total_vente,date)
            VALUES (%s ,%s)
         ''' , (total,date))
        self.db.commit()
        print('done')
     
    def display_recette(self):
        
        self.cur.execute(''' 
                            SELECT cast(date as date) as stat_day, SUM(total_vente)
                            from vente
                            GROUP BY cast(date as date)
                            order by date
               ''')
        data=self.cur.fetchall()
        print(data)
        for row , item in enumerate(data) :
            self.tableWidget_5.insertRow(row)
            for col , form in enumerate(item):
                self.tableWidget_5.setItem(row,col, QTableWidgetItem(str(form)))
        
    def filter(self, filter_text):
        
        for i in range(self.tableWidget_2.rowCount()):
            for j in range(self.tableWidget_2.columnCount()):
                item = self.tableWidget_2.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.tableWidget_2.setRowHidden(i, match)
                if not match:
                    break

    def export_data(self):
        ## export produit data to excel file
        self.cur.execute('''
            SELECT code , nom , categorie , prix_achat , prix_vente , date FROM produit
        ''')

        data = self.cur.fetchall()
        excel_file = Workbook('produit_rap.ods')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0,0,'Code produit')
        sheet1.write(0,1,'Nom produit')
        sheet1.write(0,2,'Categorie')
        sheet1.write(0,3,'Pix achat')
        sheet1.write(0,4,'Prix de vente')
        sheet1.write(0,5,'Date')
      
        row_number = 1
        for row in data :
            column_number = 0
            for item in row :
                sheet1.write(row_number,column_number,str(item))
                column_number += 1
            row_number += 1

        excel_file.close()
        QMessageBox.information(self,'information','Rapport exporté avec success')

########## ######################### button open tab
    
    
    
    def toggleFullScreen(self):
        
        if self.isFullScreen():
            self.showNormal()
            self.pushButton_45.setText('Mode plein ecran')
        else:
            self.pushButton_45.setText('Quitter plein ecran')
            self.showFullScreen()   
            
if __name__ == '__main__':
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = main()
    w.show()
    sys.exit(app.exec_())
    
           

    
       
  
  
  # def handle_item_changed(self):
    #     nrows = self.tableWidget.rowCount()
    #     f=0
    #     for row in range(0,nrows):
    #         item = self.tableWidget.item(row, 2)
    #         if item : #check if column is not null 
    #          item_text = item.text()
    #          s=float(item_text)
    #          f=f+s
    #          row+=1
    #     result = str(f)
    #     self.lineEdit_6.setText(result)