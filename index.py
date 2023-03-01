from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5 import uic,QtWidgets
import sys,datetime,random, mysql.connector,time ,cv2,barcode,threading,subprocess,pyqtgraph as pg,webbrowser
from barcode import *
from barcode.writer import *
from pyzbar.pyzbar import decode
from index2 import *
from xlsxwriter import *
from xlrd import *
from PIL import Image, ImageDraw, ImageFont


MainUI,_=loadUiType('des_v2.ui')

MainUI2,_=loadUiType('logv2.ui') 

MainUI3,_=loadUiType('info_prod.ui') 

user_profile = []

userid =  0

class info_prod1(QMainWindow,MainUI3):################ handle interface
    def __init__(self, parent=None):
        super(info_prod1, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.button()
        self.setWindowModality(Qt.ApplicationModal)
        self.db_connection()
        self.pushButton_12.setVisible(False)
        
    def db_connection(self) :
        self.db = mysql.connector.connect(
                        database="superette",
                        host="localhost",
                        user="root",
                        password="root"
                        )
        self.cur = self.db.cursor()    
        self.cur.execute(''' SELECT category_name from category''')#select all data 
        data = self.cur.fetchall()#return all data    
        for category in data :
                self.comboBox_15.addItem(str(category[0]))
          
    def button(self):

        self.pushButton_10.clicked.connect(self.delete_product)
        self.pushButton_11.clicked.connect(self.search_product)
        self.pushButton_12.clicked.connect(self.update_product)
        self.pushButton_13.clicked.connect(self.print_barcode)
            
    def search_product(self):
        
                    self.label_68.setVisible(False)
                    self.label_63.setVisible(False)
                    self.label_65.setVisible(False)
                    self.label_67.setVisible(False)
                    self.label_64.setVisible(False)
                    self.label_66.setVisible(False)
                    self.label_73.setVisible(False)
                    self.label_70.setVisible(False)
                    self.label_72.setVisible(False)
                    self.pushButton_12.setVisible(True)
                    
                    nom=self.label_68.text()
                   
                    sql = ('''
                            SELECT * FROM produit WHERE nom = %s
                        ''')   
                    self.cur.execute(sql , [(nom)])
                    value = self.cur.fetchone()
                    self.db.commit()
                    
                    if (value) : 
                                self.lineEdit_11.setText(value[1])
                                self.plainTextEdit_2.setPlainText(value[2])
                                self.doubleSpinBox_3.setValue(value[3])
                                self.doubleSpinBox_4.setValue(value[4])
                                self.spinBox_2.setValue(value[5])
                                code=self.lineEdit_12.setText(value[6])
                                self.comboBox_15.setCurrentText(value[8])
             
    def update_product(self):
            
            nome = self.lineEdit_11.text()
            details = self.plainTextEdit_2.toPlainText()
            prix_achat = self.doubleSpinBox_3.value()
            prix_vente = self.doubleSpinBox_4.value()
            quantite = self.spinBox_2.value()
            code = self.lineEdit_12.text()
            categorie = self.comboBox_15.currentText()
                        
            try:
                self.cur.execute('''
                    UPDATE Produit SET nom = %s ,details = %s , prix_achat = %s , prix_vente = %s , quantite = %s , code = %s , categorie = %s WHERE code = %s
                ''',(nome,details,prix_achat,prix_vente,quantite,code,categorie,code))
                self.db.commit()
            except Exception as e:
                print("Erreur lors de la mise à jour du produit : ", e)
                self.db.rollback()

                        
            global userid
            action = 4
            table = 6
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))    
            
            comm = self.db.commit()
            print(userid)
            QMessageBox.information(self,'succes','Produit a été bien modifer')
            self.ma=main()
            self.ma.tableWidget_2.setRowCount(0)
            self.ma.tableWidget_4.setRowCount(0)
            self.ma.show_historique()
            self.ma.show_product()
                          
    def delete_product(self):
        
        self.opp=main()

        
        nom = self.label_68.text()
        delete_message = QMessageBox.warning(self ,"produit sera supprimer" , "Vous etes sur !!",QMessageBox.Yes | QMessageBox.No )
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
            self.opp.tableWidget_4.setRowCount(0)
            self.opp.show_historique()            
            self.opp.tableWidget_2.setRowCount(0)
            self.opp.show_product()
            self.close()
    
    def print_barcode(self):
        
        if self.lineEdit_12.isEnabled() : 
            code=str(self.lineEdit_12.text())
            nom=str(self.lineEdit_11.text())
            price=str(self.doubleSpinBox_4.value())
        else :
            code=str(self.label_66.text())
            nom=str(self.label_68.text())
            price=str(self.label_67.text())
                

        # Create EAN13 barcode
        EAN13 = barcode.EAN13(code, writer=ImageWriter())

        # Generate an image of the barcode
        EAN13_image = EAN13.render()

        # Add text to the image
        font = ImageFont.truetype('arialbd.ttf', 30)
        text = nom + " : " +  price + 'DA'
        text_width, text_height = font.getsize(text)

        # Resize the barcode image to include the text
        image_width = EAN13_image.width
        image_height = EAN13_image.height + text_height 
        result_image = Image.new('RGB', (image_width, image_height), color='white')

        # Add the text to the image
        draw = ImageDraw.Draw(result_image)
        text_x = (image_width - text_width) / 2
        text_y = 0
        draw.text((text_x, text_y), text, font=font,  fill=(0, 0, 0))

        # Add the barcode to the image
        result_image.paste(EAN13_image, (0, text_height))
        
        #create folder in disk C://
        folder_name = "dossier de code barre"
        if not os.path.exists(f"C:/{folder_name}"):
            os.makedirs(f"C:/{folder_name}")
        
        # Save the result image in folder created above
        result_image.save(f"C:/dossier de code barre/bare_code_{nom}.png") 
        result_image_data = result_image.tobytes()
        
        # Get the default printer
        printer_name = win32print.GetDefaultPrinter()

        # Start the print job
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Code barre", None, "RAW"))
            try:
                # Encode the invoice as bytes
                win32print.WritePrinter(hPrinter, result_image_data)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter) 
        
        QMessageBox.information(self,'Succes',f'Code barre de {nom} exporter avec succes')
        
        
        
            
class Window3(QMainWindow,MainUI2):################ handle interface
    
    def __init__(self, parent=None):
        super(Window3, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connect_button()
        self.db_connection()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
       
    def connect_button (self):   
        self.pushButton_27.clicked.connect(self.user_login)  
        self.pushButton.clicked.connect(self.close_window)  
        
        self.pushButton_46.clicked.connect(self.open_face)
        self.pushButton_47.clicked.connect(self.open_github)
        self.pushButton_48.clicked.connect(self.open_in)
        self.pushButton_50.clicked.connect(self.open_instagram)
        
    def close_window(self):
        self.close()
    
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
                self.ind.lineEdit.setFocus()
                w.close()
                
                self.cur.execute('''
                                 SELECT nom from produit where quantite <= 0
                                 ''')
                data = self.cur.fetchall()
                print(data)
                
                for quan in data : 
                    QMessageBox.warning(self,'attention' , f'le produit {quan[0]} est vide' )
                
                global userid
                userid=row [2]
                print(userid)
                
                
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
                self.ind.tableWidget_4.setRowCount(0)
                self.ind.show_historique()    

            else :
                self.label_26.setText('username ou mot de pass invalide')

######################################## social network

    def open_face(self):
        webbrowser.open('https://www.facebook.com/majid.catalonia.7/')
        
    def open_github(self):
        webbrowser.open('https://github.com/majidBOUZAR')
        
    def open_in(self):
        webbrowser.open('https://www.linkedin.com/in/majid-bouzar1996/')
        
    def open_instagram(self):
        webbrowser.open('https://www.instagram.com/majid__bouzar/')              

class main(QMainWindow,MainUI):################ handle interface
       
    def ok_button(self):### call window of payement 
        
        if self.tableWidget.rowCount() == 0:
            QMessageBox.information(self, "information", "table de vente deja vide")
        else:
            show_window2 = True
            nrows = self.tableWidget.rowCount()
            for row in range(0, nrows):
                nom_item = self.tableWidget.item(row, 1)
                if nom_item is not None:
                    st = nom_item.text()
                    self.cur.execute(''' select quantite from produit where nom=%s ''', (st,))
                    donne = self.cur.fetchall()
                    try:
                        if donne[0][0] < int(self.tableWidget.item(row, 3).text()):
                            QMessageBox.information(self, 'Attention', f'<span style="font-size:16pt;"> La quantité de produit <b>"{st}"</b> ne suffit pas modifier sil vous plait </span>')
                            self.tableWidget.setCurrentCell(row,3)
                            show_window2 = False
                        elif int(self.tableWidget.item(row, 3).text()) <= 0:
                            QMessageBox.warning(self, 'Attention', f'<span style="font-size:16pt;"> La quantité de produit <b>{st}</b> doit être supérieure à zéro </span>')
                            self.tableWidget.removeRow(row)
                            show_window2 = False
                    except : 
                        QMessageBox.warning(self, 'Attention', f'<span style="font-size:16pt;">sil vous plait monsieur entrer valeur de quantité correcte </span>')
                        show_window2 = False
                                
            if show_window2:
                self.pushButton_13.clicked.connect(self.calcul)
                self.w = Window2()
                self.w.setWindowModality(Qt.ApplicationModal)
                self.w.show()
                self.w.activateWindow()
                self.w.raise_()
                self.w.pushButton_13.clicked.connect(self.vente)
                self.w.pushButton_13.clicked.connect(self.recette)
                self.w.pushButton_14.clicked.connect(self.annuler_payment)
                self.w.pushButton_33.clicked.connect(self.print_facture)
                self.show_client()
                self.display_recette()

##################################################### CONSTRUCTOR HANDLE SOME FUNCTION ##################################################### 
    
    def __init__(self, parent=None):
        super(main, self).__init__(parent) # Call the inherited classes __init__ method
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui_change()
        self.w = Window2()
        self.lineEdit.setFocus()
        self.startNew=1
        self.db_connection()
        self.handle_button()
        self.ui_change()
        self.show_category()
        self.show_product()
        self.show_users()
        self.historique()
        self.total()
        self.show_historique()
        self.statistic_recette()
        self.display_recette()
        self.all_vente()
        self.user_login()
        self.show_client()
        self.profile()
        self.retreive_all_product_stock()
        self.retreive_supplier()
        self.retreive_information()
        
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_label_time)
        self.timer.start()
     
    def update_label_time(self):
        import locale
        font = QtGui.QFont("DS-Digital", 22)
        font.setBold(True)
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        date_time = time.strftime("%d-%m-%Y, %H:%M:%S")
        self.label_129.setText(date_time)  
        self.label_129.setFont(font)
        QApplication.processEvents() # solution of not responding (Threding)    
          
    def ui_change(self) :
    #UI changes in login
        self.tabWidget.tabBar().setVisible(False)#make the main tab bar invisible
        font = QtGui.QFont("DS-Digital", 55)
        font.setBold(True)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setText("0") 
        self.lineEdit_101.setText("0") 
        self.lineEdit_101.setFont(font)
        self.lineEdit_102.setFocus()
        self.lineEdit_69.setFont(font)
        self.lineEdit_70.setFont(font)
      
############################################################# CONNECT TO DATABASE MYSQL ###################################################
      
    def db_connection(self) :
        self.db = mysql.connector.connect(
                            database="superette",
                            host="localhost",
                            user="root",
                            password="root"
                            )
        self.cur = self.db.cursor()
        print('db connected successful')

############################################ CONNECT BUTTON WITH FUNCTION (WITH SIGNALS) ########################################### 
    def keyPressEvent(self,event):
                
            if event.key() == 16777220 and self.tabWidget.currentIndex() == 0:
                self.calcul()
                self.ok_button()
                
    def handle_button(self) :
                
        self.pushButton_25.clicked.connect(self.open_login_tab)#connect button with tab widget
        self.pushButton.clicked.connect(self.open_vente_tab)
        self.pushButton_2.clicked.connect(self.open_product_tab)
        self.pushButton_3.clicked.connect(self.open_client_tab)
        self.pushButton_4.clicked.connect(self.open_dashboard_tab)
        self.pushButton_5.clicked.connect(self.open_report_tab)
        self.pushButton_6.clicked.connect(self.open_parametre_tab)
        self.pushButton_19.clicked.connect(self.open_historique_tab)
        self.pushButton_44.clicked.connect(self.menu_button)
        self.pushButton_8.clicked.connect(self.menu_button2)
        self.pushButton_21.clicked.connect(self.add_supplier)
        
        self.pushButton_23.clicked.connect(self.add_category)
        self.pushButton_38.clicked.connect(self.delete_category)
        self.pushButton_9.clicked.connect(self.add_product)  
        self.pushButton_15.clicked.connect(self.save_barcode)  
        self.pushButton_33.clicked.connect(self.export_data)
        
        self.pushButton_92.clicked.connect(self.browse_image)
        self.checkBox.stateChanged.connect(self.generate_barcode)
        self.checkBox_7.stateChanged.connect(self.generate_barcode_2)
        self.pushButton_12.clicked.connect(self.search_product)
        self.pushButton_90.clicked.connect(self.dialog_achats)
        self.pushButton_20.clicked.connect(self.add_row_achats)
        self.pushButton_22.clicked.connect(self.delete_row_achats)
        
        self.pushButton_13.clicked.connect(self.refresh_stock)
        self.pushButton_13.setDefault(True)
        self.pushButton_28.clicked.connect(self.clear_all)
        self.pushButton_11.clicked.connect(self.modifie_product)
        self.pushButton_10.clicked.connect(self.supprimer_product)
        
        self.lineEdit_2.textChanged.connect(self.filter)
        self.lineEdit_13.textChanged.connect(self.filter_table_client)
        self.lineEdit_19.textChanged.connect(self.filter_table_supplier)
        self.lineEdit_3.textChanged.connect(self.filtre_all_product)  
        self.dateEdit.dateChanged.connect(self.filter_recette)
        
        
        #self.lineEdit_3999.textChanged.connect(self.filter_recette)
        self.comboBox_8.currentTextChanged.connect(self.search_historique)
        self.comboBox_6.currentTextChanged.connect(self.search_historique)
        self.comboBox_7.currentTextChanged.connect(self.search_historique)
        self.comboBox_2.currentTextChanged.connect(self.handle_supplier)
        self.comboBox.currentTextChanged.connect(self.retreive_permission)
        
        
        #self.lineEdit_5.textChanged.connect(self.searrech_product)
        self.pushButton_49.clicked.connect(self.employe)
        self.pushButton_34.clicked.connect(self.delete_row)
        self.pushButton_7.clicked.connect(self.copy_row)
        self.pushButton_14.clicked.connect(self.annuler_payment)
        self.pushButton_91.clicked.connect(self.annuler_payement_achats)
        self.pushButton_40.clicked.connect(self.verifier_user)
        self.pushButton_35.clicked.connect(self.modifier_users)
        self.pushButton_32.clicked.connect(self.BarcodeReader)
        #self.pushButton.clicked.connect(self.BarcodeReader)
        #self.pushButton_37.clicked.connect(self.BarcodeReader_product)
        self.pushButton_dec.clicked.connect(self.deconnecter)
        self.pushButton_13.clicked.connect(self.calcul)
        self.pushButton_13.clicked.connect(self.ok_button)
        
        self.tableWidget.itemChanged.connect(self.calcul)
        self.tableWidget_2.itemPressed.connect(self.item_pressed_info_prod)
        self.tableWidget_6.itemPressed.connect(self.copy_row)
        self.tableWidget_20.itemChanged.connect(self.calcul_achats)
        #self.tableWidget.itemPressed.connect(self.ok_button)
        
        
        ######### VENTES
        self.startNew=1
        #initialise to empty string on start up
        self.lineEdit.setText(' ')
        self.lineEdit.returnPressed.connect(self.set_sample_name) #here is where I want to delete the previous entry without backspacing by hand
        self.lineEdit.textChanged.connect(self.delete_previous)
        self.lineEdit.textChanged.connect(self.search_insert_by_code)   

        ######### ACHATS
        self.startNew=1
        #initialise to empty string on start up
        self.lineEdit_102.setText(' ')
        self.lineEdit_102.returnPressed.connect(self.set_sample_name_achats) #here is where I want to delete the previous entry without backspacing by hand
        self.lineEdit_102.textChanged.connect(self.delete_previous_achats)
        self.lineEdit_102.textChanged.connect(self.search_insert_by_code_achats)   


        self.pushButton_36.clicked.connect(self.permission)
        #self.pushButton_27.clicked.connect(self.user_login)
        self.pushButton_sup_his.clicked.connect(self.delete_historique)
        self.comboBox_cat.currentTextChanged.connect(self.display_category_lineedit)
        self.pushButton_39.clicked.connect(self.update_category)
        self.pushButton_45.clicked.connect(self.toggleFullScreen)
        self.pushButton_24.clicked.connect(self.add_information)
        self.pushButton_93.clicked.connect(self.browse_image_information_section)
        self.pushButton_sup_his_2.clicked.connect(self.vider_recette)
        
        self.pushButton_43.clicked.connect(self.add_client)
        self.pushButton_16.clicked.connect(self.update_client)
        self.pushButton_18.clicked.connect(self.delete_client)
        self.pushButton_17.clicked.connect(self.search_client)
        
        #self.checkBox_28.stateChanged.connect(self.droi_admine_true) 
        self.pushButton_46.clicked.connect(self.open_face)
        self.pushButton_47.clicked.connect(self.open_github)
        self.pushButton_48.clicked.connect(self.open_in)
        self.pushButton_50.clicked.connect(self.open_instagram)
             
############################################################# HANDLE SIDE BUTTON #####################################################   

    def deconnecter (self):
        self.ii=Window3()
        self.ii.show()
        self.close()
          
    def menu_button2(self):
        
        self.groupBox_8.show()
        self.tabWidget.setGeometry(QtCore.QRect(230, 30, 1121, 701))
        self.pushButton_8.hide()
        self.pushButton_44.show()
        self.lineEdit.setFocus()
        
        self.lineEdit_3.setGeometry(QtCore.QRect(622, 60, 441, 41))
        
        self.tableWidget_6.setGeometry(QtCore.QRect(610, 110, 471, 471))
        self.tableWidget.setColumnWidth(1, 140)
        self.tableWidget.setColumnWidth(0, 165)
        self.tableWidget.setColumnWidth(2, 115)
        self.tableWidget.setColumnWidth(3, 110)
        
        
        
        self.pushButton_7.setGeometry(QtCore.QRect(610, 600, 451, 41))
        self.label_129.setGeometry(QtCore.QRect(740, 10, 301, 21))
        
        self.lineEdit_6.setGeometry(QtCore.QRect(12, 19, 271, 81))
        self.tableWidget.setGeometry(QtCore.QRect(10, 110, 571, 471))
        self.pushButton_13.setGeometry(QtCore.QRect(10, 600, 241, 51))
        self.pushButton_14.setGeometry(QtCore.QRect(310, 600, 261, 51))
        self.lineEdit.setGeometry(QtCore.QRect(300, 20, 271, 31))  
        self.pushButton_34.setGeometry(QtCore.QRect(300, 60, 146, 41))
        self.pushButton_32.setGeometry(QtCore.QRect(460 ,60, 111, 41))        
        
        self.pushButton_45.setGeometry(QtCore.QRect(80,10, 141, 31))        
            
    def menu_button(self):
        
        self.groupBox_8.hide()
        self.tabWidget.setGeometry(QtCore.QRect(70, 50, 1281, 701))
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(0, 175)
        self.tableWidget.setColumnWidth(2, 145)
        self.tableWidget.setColumnWidth(3, 145)
        
        self.pushButton_44.hide()
        self.pushButton_8.show()
        self.lineEdit.setFocus()
        
        self.lineEdit_3.setGeometry(QtCore.QRect(762, 60, 441, 41))

        self.tableWidget_6.setGeometry(QtCore.QRect(740, 110, 521, 471))
        self.pushButton_7.setGeometry(QtCore.QRect(870, 600, 301, 51))
        self.label_129.setGeometry(QtCore.QRect(850, 10, 311, 21))
        
        self.lineEdit_6.setGeometry(QtCore.QRect(12, 19, 381, 81))
        self.tableWidget.setGeometry(QtCore.QRect(0, 110, 681, 471))
        self.pushButton_13.setGeometry(QtCore.QRect(10, 600, 331, 51))
        self.pushButton_14.setGeometry(QtCore.QRect(360, 600, 331, 51))
        self.lineEdit.setGeometry(QtCore.QRect(410, 20, 271, 31))  
        self.pushButton_34.setGeometry(QtCore.QRect(410, 60, 146, 41))
        self.pushButton_32.setGeometry(QtCore.QRect(570,60, 111, 41))
                
        self.pushButton_45.setGeometry(QtCore.QRect(80,10, 141, 31))        
        
    def open_login_tab(self) :
        self.tabWidget.setCurrentIndex(0)   
        self.lineEdit.setFocus()
        self.tableWidget_6.setRowCount(0)
        self.retreive_all_product_stock()
        
    def open_vente_tab(self) :
        self.tabWidget.setCurrentIndex(1)#current index of tab widget    
        self.lineEdit_102.setFocus()   
        self.show_product()
        self.show_historique() 
          
    def open_product_tab(self) :
        self.tabWidget.setCurrentIndex(2) 
        self.tabWidget_2.setCurrentIndex(0) 
        self.lineEdit_2.setFocus()
        self.tableWidget_4.setRowCount(0)
        self.show_historique()            
        self.tableWidget_2.setRowCount(0)
        self.show_product()
        
    def open_client_tab(self) :
        self.tabWidget.setCurrentIndex(3)
        self.tableWidget_3.setRowCount(0)
        self.show_client()
        
    def open_dashboard_tab(self) :
        self.tabWidget.setCurrentIndex(4)
        self.tableWidget_9.setRowCount(0)
        self.retreive_supplier()
        
    def open_report_tab(self) :
        self.tabWidget.setCurrentIndex(5)
        self.tableWidget_5.setRowCount(0)
        self.display_recette()
        
    def open_parametre_tab(self) :
        self.tabWidget.setCurrentIndex(6)
        
    def open_historique_tab(self) :
        self.tabWidget.setCurrentIndex(7)  
        self.tableWidget_4.setRowCount(0)
        self.show_historique()   

    def item_pressed_info_prod(self,item):
        self.info = info_prod1()
        self.info.show()    
        row = item.row()
        row_items = []
        for col in range(self.tableWidget_2.columnCount()):
            item = self.tableWidget_2.item(row, col)
            if item:
                row_items.append(item.text())
        print('row' , row)
        
        nom = row_items[1]
        sql = ('''
                SELECT * FROM produit WHERE nom = %s
            ''')   
        self.cur.execute(sql , [(nom)])
        value = self.cur.fetchone()   
        self.db.commit()
        if (value) is not None : 
                    self.info.label_68.setText(value[1])
                    self.info.label_63.setText(value[2])
                    self.info.label_65.setText(str(value[3]))
                    self.info.label_67.setText(str(value[4]))
                    self.info.label_64.setText(str(value[5]))
                    self.info.label_66.setText(str(value[6]))
                    self.info.label_73.setText(str(value[7]))
                    self.info.label_70.setText(value[8])
                    if value[10] is not None :
                        with open("retrieved_image.jpg", "wb") as imageFile:
                            imageFile.write(value[10])
                        pixmap = QPixmap()
                        pixmap.loadFromData(value[10])
                        pixmap = pixmap.scaled(self.info.label_71.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.info.label_71.setPixmap(pixmap)    
                    
############################################################# HANDLE BARCODE #####################################################     
              
    def set_sample_name(self):

        self.sample_name = self.lineEdit.text()
        self.startNew=1
        
    def delete_previous(self,text):
        
        if self.startNew:
            self.lineEdit.setText(text[-1])
            self.startNew=0
          
    def BarcodeReader(self):
        vid = cv2.VideoCapture(0)
        camera = True
        while camera == True :
            
            success, img = vid.read()
            detectedBarcodes = decode(img)
            print('scanner barcode is open')
            for barcode in detectedBarcodes:
                print('aprouved')
                print(str(barcode.data))
                 
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
     
    def generate_barcode_2(self):
        
        nom=self.lineEdit_10.text()
        prix=self.doubleSpinBox_4.value()
        x=10**(13-1)
        y=(10**13)-1
        number = str(int(random.randint(x,y)))
        print(number)
        barCodeImage = barcode.get('EAN13', number, writer=ImageWriter())
        barCodeImage.save(f"barcode/bare_code_{nom}")
        print(nom)
        self.lineEdit_12.setText(number)  
        print("code checked") 
        
    def save_barcode(self):
        
        table = self.tableWidget_2.rowCount()

        for i in range(table):
            code = str(self.tableWidget_2.item(i, 0).text()) # 0 is the column index for code
            nom = str(self.tableWidget_2.item(i, 1).text()) # 1 is the column index for nom
            price = str(self.tableWidget_2.item(i, 3).text()) # 2 is the column index for price
                

            # Create EAN13 barcode
            EAN13 = barcode.EAN13(code, writer=ImageWriter())

            # Generate an image of the barcode
            EAN13_image = EAN13.render()

            # Add text to the image
            font = ImageFont.truetype('arialbd.ttf', 30)
            text = nom + " : " +  price + 'DA'
            text_width, text_height = font.getsize(text)

            # Resize the barcode image to include the text
            image_width = EAN13_image.width
            image_height = EAN13_image.height + text_height 
            result_image = Image.new('RGB', (image_width, image_height), color='white')

            # Add the text to the image
            draw = ImageDraw.Draw(result_image)
            text_x = (image_width - text_width) / 2
            text_y = 0
            draw.text((text_x, text_y), text, font=font,  fill=(0, 0, 0))

            # Add the barcode to the image
            result_image.paste(EAN13_image, (0, text_height))
            
            #create folder in disk C://
            folder_name = "dossier de code barre"
            if not os.path.exists(f"C:/{folder_name}/tous les codes barres"):
                os.makedirs(f"C:/{folder_name}/tous les codes barres")
            
            # Save the result image in folder created above
            result_image.save(f"C:/{folder_name}/tous les codes barres/{nom}.png") 
            result_image_data = result_image.tobytes()
            # Get the default printer
            printer_name = win32print.GetDefaultPrinter()

            # Start the print job
            hPrinter = win32print.OpenPrinter(printer_name)
            try:
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Code barre", None, "RAW"))
                try:
                    # Encode the invoice as bytes
                    win32print.WritePrinter(hPrinter, result_image_data)
                finally:
                    win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter) 
        
        QMessageBox.information(self,'information','Tous les codes barre sera créer et imprimer')
        
############################################################# HANDLE CATEGORY #####################################################                   
 
    def add_category(self) :   
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
       self.comboBox_cat.addItem('----------')
       
       self.comboBox_15.clear()
       self.comboBox_15.addItem('----------')
       
       self.comboBox_3.clear()
       self.comboBox_3.addItem('----------')            
                   
       
       self.tableWidget_4.setRowCount(0)
       self.show_historique()
       self.show_category()          
       
    def show_category(self) :  
            
            all = self.cur.execute(''' SELECT category_name from category''')#select all data 
            data = self.cur.fetchall()#return all data    
            for category in data :
                
                self.comboBox_3.addItem(str(category[0]))
                self.comboBox_15.addItem(str(category[0]))
                self.comboBox_cat.addItem(category[0])
      
    def delete_category(self): 
        
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
                
                self.cur.execute('''  
                                 UPDATE produit SET categorie = %s WHERE categorie = %s
                ''',(('------------'),item))
                
                self.db.commit()
                
                
                
                self.comboBox_cat.clear()
                self.comboBox_cat.addItem('----------')
                
                self.comboBox_15.clear()
                self.comboBox_15.addItem('----------')

                self.comboBox_3.clear()
                self.comboBox_3.addItem('----------')            
                            
                
                self.tableWidget_4.setRowCount(0)
                self.show_historique()
                self.show_category()
                          
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
            self.comboBox_cat.addItem('----------')
             
            
            self.comboBox_15.clear()
            self.comboBox_15.addItem('----------')
            
            self.comboBox_3.clear()
            self.comboBox_3.addItem('----------')            
            
            self.tableWidget_4.setRowCount(0)
            self.show_historique()
            self.show_category()
            
 ###################################################### OPEN LINK SOCIAL NETWORK IN BROWSER #####################################
 
    def open_face(self):
        webbrowser.open('https://www.facebook.com/majid.catalonia.7/')
        
    def open_github(self):
        webbrowser.open('https://github.com/majidBOUZAR')
        
    def open_in(self):
        webbrowser.open('https://www.linkedin.com/in/majid-bouzar1996/')
        
    def open_instagram(self):
        webbrowser.open('https://www.instagram.com/majid__bouzar/')                        
    
############################################################# HANDLE PRODUCT #####################################################                  
    def browse_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Parcourir Image", "", "Images (*.png *.xpm *.jpg *.bmp *.gif);;All Files (*)", options=options)
        if file_name:
            self.image_path = file_name
            self.label_128.setText(file_name) 
         
    def show_product(self):
        
        self.tableWidget_2.setColumnWidth(1, 220)
        self.tableWidget_2.setColumnWidth(0, 160)
        self.cur.execute(''' SELECT code,nom,prix_achat,prix_vente,quantite,details,categorie,id from produit''')
        data=self.cur.fetchall()
        
        for row , form in enumerate(data):
            self.tableWidget_2.insertRow(row)
            for col , item in enumerate(form):
                if col == 7 :
                    prix_achat = self.tableWidget_2.item(row,2)
                    prix_vente = self.tableWidget_2.item(row,3)
                    t =  float(str(prix_vente.text())) / float(str(prix_achat.text()) )
                    s=(t-1)*100
                    m=int(s)
                    val= str(m)
                    self.tableWidget_2.setItem(row,col, QTableWidgetItem(val + '%'))
                else:
                    self.tableWidget_2.setItem(row,col, QTableWidgetItem(str(item)))        
                col = col + 1
                
            
        for rows in range(self.tableWidget_2.rowCount()):
            color_item = self.tableWidget_2.item(rows, 4)
            if color_item is not None:
                if int(color_item.text()) == 0:
                    for cols in range(self.tableWidget_2.columnCount()):
                        items = self.tableWidget_2.item(rows, cols)
                        items.setBackground(QtGui.QColor('red'))
               
    def search_product(self):
        nom=self.lineEdit_10.text()
        sql = ('''
                SELECT * FROM produit WHERE nom = %s
            ''')   
        self.cur.execute(sql , [(nom)])
        value = self.cur.fetchone()

        self.db.commit()
           
        if (value)  : 
                    self.lineEdit_11.setText(value[1])
                    self.plainTextEdit_2.setPlainText(value[2])
                    self.doubleSpinBox_3.setValue(value[3])
                    self.doubleSpinBox_4.setValue(value[4])
                    self.spinBox_2.setValue(value[5])
                    code=self.lineEdit_12.setText(value[6])
                    self.comboBox_15.setCurrentText(value[8])
                    if code == '':
                        self.checkBox.setEnabled(True)
                        
                        x=10**(13-1)
                        y=(10**13)-1
                        number = str(int(random.randint(x,y)))
                    
                        barCodeImage = barcode.get('EAN13', number, writer=ImageWriter())
                        barCodeImage.save(f"barcode/bare_code_{nom}")
                    
                        self.lineEdit_12.setText(number)  
                        print("code checked") 
                    
    def clear_all(self)   :
     
       self.lineEdit_11.clear()
       self.lineEdit_10.clear()
       self.plainTextEdit_2.clear()
       self.doubleSpinBox_3.clear()
       self.doubleSpinBox_4.clear()
       self.spinBox_2.clear()
       self.lineEdit_12.clear()
       self.comboBox_15.setCurrentIndex(0)
       
    def add_product (self):
        try:
            
            if hasattr(self, 'image_path'):
                with open(self.image_path, "rb") as f:
                    binary_data = f.read()
            else:
                binary_data = None

               
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
            
            try :
                self.cur.execute(('''INSERT INTO Produit(nom , details , prix_achat , prix_vente ,quantite,code,date,categorie,image)
                    VALUES (%s , %s, %s , %s , %s , %s , %s, %s, %s)
                ''' )  , (nom,details,prix_achat,prix_vente,quantite,code,date,categorie,binary_data))
            except Exception as e:
                print("Erreur lors de la mise à jour du produit : ", e)
                self.db.rollback()    
                

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
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_4.setRowCount(0)
            self.show_historique()
            self.show_product()
            
        except:
            QMessageBox.warning(self,'Attention','Ce produit il existe')    
                   
    def supprimer_product(self):
        
        nom = self.lineEdit_10.text()
        delete_message = QMessageBox.warning(self ,"produit sera supprimer" , "Vous etes sur !!",QMessageBox.Yes | QMessageBox.No )
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
        self.tableWidget_4.setRowCount(0)
        self.show_historique()            
        self.tableWidget_2.setRowCount(0)
        self.show_product() 
                
    def modifie_product(self):
        try :
            nome = self.lineEdit_11.text()
            details = self.plainTextEdit_2.toPlainText()
            prix_achat = self.doubleSpinBox_3.value()
            prix_vente = self.doubleSpinBox_4.value()
            quantite = self.spinBox_2.value()
            code = self.lineEdit_12.text()
            categorie = self.comboBox_15.currentText()
                        
            try:
                self.cur.execute('''
                    UPDATE Produit SET nom = %s ,details = %s , prix_achat = %s , prix_vente = %s , quantite = %s , code = %s , categorie = %s WHERE code = %s
                ''',(nome,details,prix_achat,prix_vente,quantite,code,categorie,code))
                self.db.commit()
            except Exception as e:
                print("Erreur lors de la mise à jour du produit : ", e)
                self.db.rollback()

                        
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
            
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_4.setRowCount(0)
            self.show_historique()
            self.show_product()
            self.clear_all()
        except :
            QMessageBox.warning(self,'Erreur','No modification')
   
    def retreive_all_product_stock(self):
            
     
        self.cur.execute(''' SELECT code,nom,prix_vente,quantite from Produit 
              ''')
        data = self.cur.fetchall()


        for row , form in enumerate(data):
            self.tableWidget_6.insertRow(row)
            for col , item in enumerate(form):
                    self.tableWidget_6.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
            row_position = self.tableWidget_6.rowCount()
           
            self.tableWidget_6.selectRow(row_position)
        
            
        for rows in range(self.tableWidget_6.rowCount()):
            color_item = self.tableWidget_6.item(rows, 3)
            if color_item is not None:
                if int(color_item.text()) == 0:
                    for cols in range(self.tableWidget_6.columnCount()):
                        items = self.tableWidget_6.item(rows, cols)
                        items.setBackground(QtGui.QColor('red'))
                       
    def refresh_stock(self):
        self.tableWidget_6.setRowCount(0)
        self.retreive_all_product_stock() 
        print('stocke refreshed')   
           
    def filtre_all_product(self, filter_text):
        
        for i in range(self.tableWidget_6.rowCount()):
            for j in range(self.tableWidget_6.columnCount()):
                item = self.tableWidget_6.item(i, j)
                if item is not None:
                    match = filter_text.lower() not in item.text().lower()
                    self.tableWidget_6.setRowHidden(i, match)
                    if not match:
                        break      
                    
    def search_product_nom(self):
        
        nom = self.lineEdit_2.text()
        
        if len(nom)  :
         sql = ''' SELECT code,nom,prix_achat,prix_vente,quantite,details,categorie from Produit WHERE nom = %s 
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
        try : 
            if password == password2 : 
                
                self.cur.execute(''' insert into users(nom,email,phone,password,password2,date) values (%s,%s,%s,%s,%s,%s)
                                    ''',(nom,email,phone,password,password2,date))
                
                global userid
                action = 3
                table = 7
                dat3 = datetime.datetime.utcnow()
                
                self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                        VALUES (%s, %s , %s, %s )
                    ''' )  , (userid,action,table,dat3))
                
                self.cur.execute('''INSERT INTO `permission` (ventetab,produittab,clientstab,dashtab,reporttab,partab,histab,is_admin,emp_name)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ''',(0,0,0,0,0,0,0,0,nom) )           
                    
                self.db.commit()
                
                QMessageBox.information(self,'success','user a été ajouté')
                self.lineEdit_45.clear()
                self.lineEdit_46.clear()
                self.lineEdit_47.clear()
                self.lineEdit_48.clear()
                self.lineEdit_49.clear()
                self.tableWidget_7.setRowCount(0)
                self.show_users()
                
            else : 
                QMessageBox.warning(self,'Attention',"mot de passe n'est pas correct")
                
        except :
             QMessageBox.warning(self,'Attention','<span style="font-size:18pt;">Cette utilisateur existé déja<s/span>')        
         
    def delete_row(self):
            if self.tableWidget.rowCount() == 0 :
                QMessageBox.information(self ,"information" , "table deja vide")
            else :          
                row_selected= self.tableWidget.currentRow()
                self.tableWidget.removeRow(row_selected)
                             
    def copy_row(self):
        
            selected_item = self.tableWidget_6.selectedItems()

            if selected_item:
                selected_row = self.tableWidget_6.selectedItems()[0].row()
                item_data = []
                for column in range(self.tableWidget_6.columnCount()):
                    item_data.append(self.tableWidget_6.item(selected_row, column).text())
                if int(item_data[3]) == 0 :
                    QMessageBox.warning(self,'attention','Stock est vide !!')
                else :
                    duplicate = False
                    for row in range(self.tableWidget.rowCount()):
                        for column in range(self.tableWidget.columnCount()):
                            if item_data[column] == self.tableWidget.item(row, column).text():
                                duplicate = True
                                new_item = self.tableWidget.item(row, 3)
                                new_item.setText(str(int(new_item.text()) + 1))
                                break
                        if duplicate:
                            break
                    if not duplicate:
                        new_row = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(new_row)
                        for column, data in enumerate(item_data):
                            new_item = QtWidgets.QTableWidgetItem(data)
                            self.tableWidget.setItem(new_row, column, new_item)
                            self.tableWidget.setItem(new_row, 3, QTableWidgetItem('1'))


############################################################# USERS & PROFILE #####################################################                  
                  
    def verifier_user(self):
        nom = self.lineEdit_30.text()
        password = self.lineEdit_29.text()
        self.cur.execute('SELECT * FROM users')
        data = self.cur.fetchall()
        match_found = False
        for row in data:
            if row[1] == nom and row[4] == password:
                self.groupBox_3.setEnabled(True)
                self.lineEdit_33.setText(row[1])
                self.lineEdit_31.setText(row[2])
                self.lineEdit_32.setText(row[3])
                match_found = True
                break
        if not match_found:
            QMessageBox.warning(self, 'Attention', 'Le nom d\'utilisateur ou le mot de passe est incorrect !')

    def modifier_users(self):
        
        nom=self.lineEdit_33.text() 
        email=self.lineEdit_31.text() 
        telephone=self.lineEdit_32.text()  
        mdp1 = self.lineEdit_34.text()
        mdp2 = self.lineEdit_44.text()
        
        if str(mdp1) == str(mdp2) :
    
                self.cur.execute('''
                    UPDATE users SET nom = %s ,email = %s , phone = %s , password = %s , password2 = %s WHERE nom = %s
                    ''',(nom,email,telephone,mdp1,mdp2,nom))   
                            
                global userid
                action = 4
                table = 7
                dat3 = datetime.datetime.utcnow()
                self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                    VALUES (%s, %s , %s, %s )
                ''' )  , (userid,action,table,dat3))    
                    
                self.db.commit()
                self.tableWidget_4.setRowCount(0)
                self.show_historique()     
                QMessageBox.information(self, 'Success', f'Les informations sont bien modifie pour utilisateur {nom}')
                
                self.lineEdit_33.clear() 
                self.lineEdit_31.clear() 
                self.lineEdit_32.clear()  
                self.lineEdit_34.clear()
                self.lineEdit_44.clear()                
                self.lineEdit_30.clear()
                self.lineEdit_29.clear()
                self.groupBox_3.setEnabled(False)
                self.label_75.setText("")
                
        else : 
            self.label_75.setText("Les 2 mot de passe ne sont pas identique")
                            
    def show_users(self):
             
        self.tableWidget_7.insertRow(0)
        sql = ''' SELECT nom,email,phone,date from users  
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
  
    def profile(self):
        self.w1 = Window3()
        e=self.w1.user_login()
        
        print(self.user_login())
        
    def user_login(self):
            username=self.lineEdit_22.text()
            password=self.lineEdit_23.text()
           
            self.cur.execute(""" SELECT id , nom , password FROM users""")
            data_ = self.cur.fetchall()
            for row in data_ :
                if row[1] == username and row[2] == password :
                    global userid
                    userid = row[0]
                    print(row)
                    
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
                    
                    self.tableWidget_4.setRowCount(0)
                    self.show_historique()
                    self.label_45.setText('Connecter') 
                    
    def permission(self):
        
     emp_n=self.comboBox.currentText()    
     if self.checkBox_28.isChecked(): 
        privilege_message = QMessageBox.warning(self ,"Ajouter comme  admin" , "Vous etes sur !!",QMessageBox.Yes | QMessageBox.No )
        if privilege_message == QMessageBox.Yes :
            
            self.cur.execute(''' UPDATE permission SET ventetab=%s, produittab=%s, clientstab=%s, dashtab=%s, reporttab=%s, partab=%s, histab=%s, is_admin=%s WHERE emp_name=%s
                        ''',(1,1,1,1,1,1,1,1,emp_n) )   
            global userid
            action = 7
            table = 7
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
             ''' )  , (userid,action,table,dat3))   
            self.db.commit()
            QMessageBox.information(self,'Succes','Privilége admin a été attribué avec success : \n \n' + emp_n)
            emp_name = self.comboBox.setCurrentIndex(0) 
            self.checkBox_28.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_13.setChecked(False)
            self.checkBox_12.setChecked(False)    
    
     else :
            vente_tab=0
            produit_tab=0   
            clients_tab=0
            dash_tab=0
            report_tab=0
            parametre_tab=0
            historique_tab=0
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
            
            self.cur.execute(''' UPDATE permission SET ventetab=%s, produittab=%s, clientstab=%s, dashtab=%s, reporttab=%s, partab=%s, histab=%s
                                 WHERE emp_name = %s
                            ''',(vente_tab,produit_tab,clients_tab,dash_tab,report_tab,parametre_tab,historique_tab,emp_n) )    
            self.db.commit()
            QMessageBox.information(self,'Succes','Permission a été attribué avec success : \n \n' + emp_n)
            
            emp_name = self.comboBox.setCurrentIndex(0) 
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_13.setChecked(False)
            self.checkBox_12.setChecked(False)
            self.groupBox_4.setEnabled(True)

    def retreive_permission(self):
        
            nom = self.comboBox.currentText()
            self.cur.execute('''
                          SELECT * from permission where emp_name=%s
                          ''',(nom,))
            data=self.cur.fetchall()
            for x in data : 

               if x[1]==1:
                  self.checkBox_2.setChecked(True)                   
               if x[2]==1:
                  self.checkBox_3.setChecked(True) 
               if x[3]==1:
                  self.checkBox_4.setChecked(True)                   
               if x[4]==1:
                  self.checkBox_5.setChecked(True)          
               if x[5]==1:
                  self.checkBox_6.setChecked(True) 
               if x[6]==1:
                  self.checkBox_13.setChecked(True)                   
               if x[7]==1:
                  self.checkBox_12.setChecked(True)   
               if x[9]==1:
                  self.checkBox_28.setChecked(True)                                   
                  
############################################################# CALCUL & VENTE #####################################################
   
    def calcul(self):

        nrows = self.tableWidget.rowCount()
        f=0
        for row in range(0,nrows):
            nom_item = self.tableWidget.item(row, 1)
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
         
    def total(self):
        self.cur.execute(''' SELECT sum(prix_achat*quantite) as sum1 ,sum(prix_vente*quantite),(sum(prix_vente*quantite))-(sum(prix_achat*quantite))  FROM produit
                         ''')    
        data = self.cur.fetchall()
        for row in data : 
         self.lineEdit_69.setText(str(row[0]))
         self.lineEdit_70.setText(str(row[1]))
  
    def search_insert_by_code (self): 
        code = self.lineEdit.text()
        sql = ''' SELECT code,nom,prix_vente,quantite from Produit WHERE code = %s 
            '''
        self.cur.execute(sql ,[(code)])
        data = self.cur.fetchall()

        for quantite in data :

                if quantite[3] <= 0 :
                    QMessageBox.warning(self,'Attention','Le stocke de ' + quantite[1] + ' est vide')
                else :
                    duplicate = False
                    for row in range(self.tableWidget.rowCount()):
                        if self.tableWidget.item(row, 0).text() == str(quantite[0]):
                            new_item = self.tableWidget.item(row, 3)
                            new_item.setText(str(int(new_item.text()) + 1))
                            duplicate = True
                            break
                    if not duplicate:
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
        self.tableWidget_2.setRowCount(0)
        self.show_product()
        self.tableWidget_5.setRowCount(0)
        self.display_recette()
        self.tableWidget_8.setRowCount(0)
        self.all_vente()        

############################################################# HISTORIQUE #####################################################

    def historique(self):
        self.cur.execute(''' select * from users ''')
        data = self.cur.fetchall()
        for row in data :
         self.comboBox_8.addItem(row[1])     
        
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
                        
                    if item == 8 :
                        Table = 'Vente'
                        
                    if item == 9 :
                        Table = 'Fournisseur'                        
    
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
            self.tableWidget_4.setRowCount(0)
            self.show_historique()
       
    def search_historique(self,filter_text):
       for i in range(self.tableWidget_4.rowCount()):
            for j in range(self.tableWidget_4.columnCount()):
                item = self.tableWidget_4.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.tableWidget_4.setRowHidden(i, match)
                if not match:
                    break 

############################################################# RECETTE #####################################################

    def recette (self):
        
        total = self.w.lineEdit_6.text()  
        client = self.w.comboBox.currentText()  
        global userid
        date = datetime.datetime.now()
        self.cur.execute('''
            INSERT INTO vente (total_vente,date,users,client)
            VALUES (%s ,%s,%s,%s)
         ''' , (total,date,userid,client))
        self.db.commit()
     
    def display_recette(self):
        #select date w vente par day
        #select nonpayer-payer par day
        # SELECT cast(vente.date as date) as stat_day , SUM(vente.total_vente), SUM(nonpayer-payer) , cast(s.date as date) as stat_day2 
        # from vente
        # JOIN clients s ON stat_day = stat_day2 
        # GROUP BY stat_day
        # order by date
                         
        
        # Sélectionner les totaux de vente par jour
           # Sélectionner les totaux de vente par jour
        self.cur.execute(''' 
            SELECT cast(date as date) as day, SUM(total_vente)
            FROM vente
            GROUP BY day
        ''')
        vente_data = self.cur.fetchall()

        # Sélectionner les totaux d'achat par jour
        self.cur.execute(''' 
            SELECT cast(date as date) as day, SUM(total_achat)
            FROM achats
            GROUP BY day
        ''')
        achat_data = self.cur.fetchall()

        # Insérer les résultats dans la tableWidget_5
        for row, (vente_day, vente_total) in enumerate(vente_data):
            self.tableWidget_5.insertRow(row)
            self.tableWidget_5.setItem(row, 0, QTableWidgetItem(str(vente_day)))
            self.tableWidget_5.setItem(row, 1, QTableWidgetItem(str(vente_total)))
            for achat_day, achat_total in achat_data:
                if achat_day == vente_day:
                    self.tableWidget_5.setItem(row, 2, QTableWidgetItem(str(achat_total)))
                    break

            # Calculer la différence entre les totaux de vente et d'achat pour chaque jour
            diff = vente_total - achat_total if achat_day == vente_day else vente_total
            self.tableWidget_5.setItem(row, 3, QTableWidgetItem(str(diff)))
 
    def vider_recette(self):
        
       delete_message = QMessageBox.warning(self,'Attention','Tous la recette sera supprimer',QMessageBox.Yes | QMessageBox.No)  
       if delete_message == QMessageBox.Yes :
            self.cur.execute(''' TRUNCATE TABLE vente
                            ''')  
           
            action = 5
            table = 8
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))   

            self.db.commit()
            self.tableWidget_5.setRowCount(0)
            self.display_recette()
            self.show_historique() 
 
    def filter_recette(self,year):
        
        filter_date = self.dateEdit.date()
        filter_date = filter_date.toPyDate()
        year = str(filter_date).split('/')[0]
        
        print(year)
        
        for i in range(self.tableWidget_3.rowCount()):
                item = self.tableWidget_3.item(i, 0)
                match = year.lower() not in item.text().lower()
                self.tableWidget_3.setRowHidden(i, match)
                if not match:
                    break        
              
    def statistic_recette(self):

    
        filter_date = self.dateEdit.date()
        filter_date = filter_date.toPyDate()
        year = str(filter_date).split('/')[0]
       
        self.cur.execute(""" 
            SELECT SUM(total_vente), EXTRACT(day FROM date) as day
            FROM vente
            GROUP BY day
        """ )
        data = self.cur.fetchall()
        
        
        vente_count = []
        date_count = []
        
        for row in data:
                
                vente_count.append(row[0])
                date_count.append(row[1]) # we append data to liset bcz the chart accept only data in list
                
        barchart = pg.BarGraphItem(x=date_count , height=vente_count , width=2 ,color='red')
        
        self.widget.addItem(barchart)             
        pen = pg.mkPen(color = 'red',size = 900)
        self.widget.setBackground('w')
        self.widget.setTitle('<h2> <span style="font-size:16pt;"> Statistique de vente dans les derniers jours</h2></span>',color='Blue')
        self.widget.showGrid(x=True,y=True)
        
        self.widget.setLabel('left','<h2>Les ventes</h2>',color='red')
        self.widget.setLabel('bottom','<h2>Les jours</h2>',color='red')        
        
    def filter(self, filter_text):
        
        for i in range(self.tableWidget_2.rowCount()):
            for j in range(self.tableWidget_2.columnCount()):
                item = self.tableWidget_2.item(i, j)
                try:
                    match = filter_text.lower() not in item.text().lower()
                    self.tableWidget_2.setRowHidden(i, match)
                    if not match:
                        break
                except:
                    print('champ de seasir vide')    

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

    def all_vente(self)   :
        self.tableWidget_8.setColumnWidth(2, 220)
        self.cur.execute(''' 
                            SELECT users , total_vente , date , client
                            from vente
                            
               ''')
        data=self.cur.fetchall()
      
        for row , item in enumerate(data) :
            self.tableWidget_8.insertRow(row)
            for col , form in enumerate(item):
                if col == 0 :
                    sql = (''' SELECT nom FROM users WHERE id = %s ''')
                    self.cur.execute(sql , [(form)])
                    te = self.cur.fetchone()
                    if te is not None :
                        result = te[0]
                        self.tableWidget_8.setItem(row,col, QTableWidgetItem(result))
                
                else :
                    self.tableWidget_8.setItem(row,col, QTableWidgetItem(str(form)))
                
############################################################# CLIENT #####################################################

    def add_client(self):

       
        nom = self.lineEdit_36.text()
        onlyInt = QIntValidator()
        self.lineEdit_37.setValidator(onlyInt)
        phone = self.lineEdit_37.text()
        email = self.lineEdit_38.text()
        paye = self.lineEdit_39.text()
        nonpaye = self.lineEdit_40.text()
        detail = self.plainTextEdit_3.toPlainText()
        date = datetime.datetime.now()
        
        
        self.cur.execute('''
                         INSERT INTO clients (nom , detail , phone , email , payer , nonpayer ,date )
                         VALUES (%s,%s,%s,%s,%s,%s,%s)
                         ''',(nom,detail,phone,email,paye,nonpaye,date))    
        global userid
        action = 3
        table = 3
        dat3 = datetime.datetime.utcnow()
        self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
            VALUES (%s, %s , %s, %s )
        ''' )  , (userid,action,table,dat3))    
        
        self.db.commit()        
        
        self.db.commit()
        QMessageBox.information(self,'Succes','Client bien ajouté')
        self.tableWidget_3.setRowCount(0)
        self.show_client()
        
        self.tableWidget_4.setRowCount(0)
        self.show_historique()

    def show_client(self):
        self.lineEdit_39.setText('0')
        self.lineEdit_40.setText('0')
        
        self.tabWidget.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.groupBox_8.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.tabWidget_2.setStyleSheet("QTabWidget::pane { border: 0; }")

        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(0, 145)
        self.tableWidget_5.setColumnWidth(0, 145)
        self.tableWidget_20.setColumnWidth(1, 150)
        self.tableWidget_20.setColumnWidth(0, 135)
        self.tableWidget_6.setColumnWidth(0, 145)
        self.tableWidget_6.setColumnWidth(1, 150)
        self.tableWidget_9.setColumnWidth(1, 150)
        self.tableWidget_7.setColumnWidth(0, 130)
        self.tableWidget_7.setColumnWidth(1, 170)
        self.tableWidget_7.setColumnWidth(3, 190)
        self.tableWidget_6.setColumnWidth(2, 70)
        self.tableWidget_6.setColumnWidth(3, 80)
        self.tableWidget_4.setColumnWidth(0, 135)
        self.tableWidget_4.setColumnWidth(3, 190)
        self.tableWidget_3.setColumnWidth(5, 200)
        self.tableWidget_3.setColumnWidth(1, 100)
        
        sql = ('''
               SELECT nom , phone , nonpayer , payer , date FROM clients
              
               ''')
        self.cur.execute(sql)
        data = self.cur.fetchall()
    
        for row , form in enumerate(data):
            self.tableWidget_3.insertRow(row)
            for col , item in enumerate(form):
                if col == 4 :
                    item = self.tableWidget_3.item(row, 2)
                    item1 = self.tableWidget_3.item(row, 3)
                    s=int(item.text())
                    s1=int(item1.text())
                    summ=s-s1
                    if summ <=0 :
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem('no dette'))
                    else :     
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(summ)))
                else :    
                    self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(item)))
            col += 1    
            
    def filter_table_client(self, filter_text):
        
        for i in range(self.tableWidget_3.rowCount()):
            for j in range(self.tableWidget_3.columnCount()):
                item = self.tableWidget_3.item(i, j)
                if item is not None:
                    match = filter_text.lower() not in item.text().lower()
                    self.tableWidget_3.setRowHidden(i, match)
                    if not match:
                        break
        
    def update_client(self):
        
            nome = self.lineEdit_15.text()
            phone=self.lineEdit_14.text()
            email=self.lineEdit_17.text()
            pay=self.lineEdit_18.text()
            nopay=self.lineEdit_35.text()
            details=self.plainTextEdit_4.toPlainText()
            date=datetime.datetime.now()
            
            self.cur.execute('''
                UPDATE clients SET nom = %s ,detail = %s , phone = %s , email = %s , payer = %s , nonpayer = %s , date = %s WHERE nom = %s
            ''',(nome,details,phone,email,pay,nopay,date,nome))      
                        
            
            
            global userid
            action = 4
            table = 3
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))    
            
            self.db.commit()
            
            QMessageBox.information(self,'succes','Client bien modifer')
            
            result = int(nopay)-int(pay)
            if result >= 0 :
               self.lineEdit_71.setText(str(result))
            else:
               self.lineEdit_71.setText('no dette')
                
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_3.setRowCount(0)
            self.show_historique()
            self.show_client()
                
    def search_client(self):
        nom=self.lineEdit_16.text()
        sql = ('''
                SELECT * FROM clients WHERE nom = %s
            ''')   
        self.cur.execute(sql , [(nom)])
        value = self.cur.fetchone()
             
        if (value)  : 
                    self.lineEdit_15.setText(value[1])
                    self.lineEdit_14.setText(value[3])
                    self.lineEdit_17.setText(value[4])
                    self.lineEdit_18.setText(value[5])
                    self.lineEdit_35.setText(value[6])
                    self.plainTextEdit_4.setPlainText(value[2])

                    result = float(value[6])-float(value[5])
                    if result >= 0 :
                        self.lineEdit_71.setText(str(result))
                    else:
                        self.lineEdit_71.setText('no dette')                    
                  
                    
        else : 
            QMessageBox.information(self,'Information','ce client ne exist pas')
    
    def delete_client(self):
  
        
        nom = self.lineEdit_16.text()
        delete_message = QMessageBox.warning(self ,"Supprimer un client" , "Vous etes sur !!",QMessageBox.Yes | QMessageBox.No )
        if delete_message == QMessageBox.Yes :
            sql = (''' DELETE from clients where nom=%s
                ''')
            self.cur.execute(sql,[(nom)])
            
            global userid
            action = 5
            table = 3
            dat3 = datetime.datetime.utcnow()
            self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))    
            
            self.db.commit()
            
            self.lineEdit_16.clear()
            self.lineEdit_15.clear()
            self.lineEdit_17.clear()
            self.lineEdit_14.clear()
            self.lineEdit_18.clear()
            self.lineEdit_35.clear()
            self.plainTextEdit_4.clear()
            self.lineEdit_71.setText('0.0')
        self.tableWidget_4.setRowCount(0)
        self.show_historique()            
        self.tableWidget_3.setRowCount(0)
        self.show_client() 

############################################################# FACTURE #####################################################

    def print_facture(self):
        self.cur.execute('''
                         SELECT * FROM information 
                         ''')
        data = self.cur.fetchone()
        #print(data[0]+data[1]+data[2])
        nom_client = self.w.comboBox.currentText()
        total=self.w.lineEdit_6.text()
        date = datetime.datetime.now()
        if self.w.checkBox.isChecked() :
        
            facture = f"{data[0]}\n".rjust(30) + f"{data[1]}\n".rjust(30) + f"Tel : {data[2]}\n".rjust(30) + f"Date : {date}\n".rjust(30) 
            facture += "========================================\n"
            facture += f"Nom de client: {nom_client}\n"
            facture += "========================================\n"
            facture += "Article".ljust(20) + "Quantité".rjust(10) + "Prix\n".rjust(10)
            
            r =0
            r1 =0
            r2 =0
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row,1)
                item1 = self.tableWidget.item(row,2)
                item2 = self.tableWidget.item(row,3)
                if item and item1 and item2 is not None : 
                    r=item.text()
                    r1=item1.text()
                    r2=item2.text()
                    facture += "----------------------------------------\n"
                    facture += f"{r}".ljust(20) + f"x {r2}".rjust(10) + f"{r1}\n".rjust(10)
                    facture += "----------------------------------------\n"

                row = row + 1
                
    
            facture += "Total:".ljust(20) + f"{total}\n".rjust(10)
            
            facture += "========================================\n"
            facture += "Merci pour votre achat! n'hésitez \n pas de nous vister autre fois \n"
           


            print(facture)
        else :
            
            facture = "Nom de la facture: Facture #123\n\n"
            facture += "========================================\n"
            facture += f"{data[0]}\n" + f"{data[1]}\n" + f"Tel : {data[2]}\n" + f"Date : {date}\n"
            facture += "Facture\n"
            facture += "========================================\n"
            facture += f"Nom de client: passager\n"
            facture += "========================================\n"
                        
            facture += "Article".ljust(20) + "Quantité".rjust(10) + "Prix\n".rjust(10)
            
            r =0
            r1 =0
            r2 =0
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row,1)
                item1 = self.tableWidget.item(row,2)
                item2 = self.tableWidget.item(row,3)
                if item and item1 and item2 is not None : 
                    r=item.text()
                    r1=item1.text()
                    r2=item2.text()
                    facture += "----------------------------------------\n"
                    facture += f"{r}".ljust(20) + f"x {r2}".rjust(10) + f"{r1}\n".rjust(10)
                    facture += "----------------------------------------\n"

                row = row + 1
                
    
            facture += f"Total:                    {total}\n"
            
            facture += "========================================\n"
            facture += "Merci pour votre achat! n'hésitez pas de nous vister autre fois\n"


            print(facture)    
        # Get the default printer
        printer_name = win32print.GetDefaultPrinter()

        # Start the print job
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Facture", None, "RAW"))
            try:
                # Encode the invoice as bytes
                win32print.WritePrinter(hPrinter, facture.encode("utf-8"))
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)            

    def browse_image_information_section(self):
        
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Parcourir Image", "", "Images (*.png *.xpm *.jpg *.bmp *.gif);;All Files (*)", options=options)
        if file_name:
            self.image_path22 = file_name
            self.label_130.setText(file_name) 

    def retreive_information(self):
        
        self.cur.execute('''
                         SELECT * From information
                         ''')
        
        data = self.cur.fetchall()
        
        for xc in data :
            self.label_71.setText(xc[0])
            self.label_72.setText(xc[1])
            self.label_70.setText(xc[2])
            
            if xc[3] is not None :
                        with open("retrieved_image.jpg", "wb") as imageFile:
                            imageFile.write(xc[3])
                        pixmap = QPixmap()
                        pixmap.loadFromData(xc[3])
                        pixmap = pixmap.scaled(self.label_73.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.label_73.setPixmap(pixmap) 
            
    def add_information(self):
        
        if hasattr(self, 'image_path22'):
                with open(self.image_path22, "rb") as f:
                    binary_data = f.read()
        else:
                binary_data = None
        
        nom=self.lineEdit_41.text()
        adress=self.lineEdit_42.text()
        numero=self.lineEdit_43.text()
        try :
            self.cur.execute('''
                    UPDATE information 
                    SET nom = %s ,adresse = %s ,numero = %s , image = %s
                    ''',(nom,adress,numero,binary_data))
        except Exception as e:
                print("Erreur lors de la mise à jour de les informations : ", e)
                self.db.rollback()  

        self.db.commit()
        QMessageBox.information(self,'information','Les informations sont bien enregistrée')
        
        self.lineEdit_41.clear()
        self.lineEdit_42.clear()
        self.lineEdit_43.clear()
        self.label_130.clear()
        self.retreive_information()   
        # self.lineEdit_41.setEnabled(False)
        # self.lineEdit_42.setEnabled(False)
        # self.lineEdit_43.setEnabled(False)

############################################################ ACHAT ###############################################
    
    def set_sample_name_achats(self):

        self.sample_name = self.lineEdit_102.text()
        self.startNew=1
        
    def delete_previous_achats(self,text):
        
        if self.startNew:
            self.lineEdit_102.setText(text[-1])
            self.startNew=0    
    
    def search_insert_by_code_achats(self):
        code = self.lineEdit_102.text()
        sql = ''' SELECT code,nom,prix_achat,quantite from Produit WHERE code = %s 
            '''
        self.cur.execute(sql ,[(code)])
        data = self.cur.fetchall()

        for quantite in data :

                    duplicate = False
                    for row in range(self.tableWidget_20.rowCount()):
                        if self.tableWidget_20.item(row, 0).text() == str(quantite[0]):
                            new_item = self.tableWidget_20.item(row, 3)
                            new_item.setText(str(int(new_item.text()) + 1))
                            duplicate = True
                            break
                    if not duplicate:
                        self.tableWidget_20.insertRow(0)  
                        for row , form in enumerate(data):
                            for col , item in enumerate(form):
                                self.tableWidget_20.setItem(row, col, QTableWidgetItem(str(item)))
                                col += 1
                        self.tableWidget_20.setItem(row, 3, QTableWidgetItem('1'))
    
    def dialog_achats(self):
        
        total_achats = self.lineEdit_101.text() 
        date = datetime.datetime.now()
        for row in range(self.tableWidget_20.rowCount()):
            quantity = self.tableWidget_20.item(row,3).text()
            c = self.tableWidget_20.item(row,0)
            if c is not None:
               code = c.text()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("<span style='font-size:16pt;'> vous voulez verser ? </span>")
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:
                item = self.comboBox_2.currentText()
                if item == "-------------------":
                    QMessageBox.warning(self, "Message", "<span style='font-size:16pt;'> Please selectionner le fournisseur pour verser.</span>")
                else:
                    text, okPressed = QInputDialog.getText(self, "Entrer la somme", "<span style='font-size:16pt;'> Enter le versement: </span>")

                    if okPressed and text != '': 
                        QMessageBox.information(self, "Message", f" <span style='font-size:16pt;'> Verser : {text}</span>")
                        self.cur.execute('''
                                        UPDATE fournisseur SET payement = payement + %s , non_payement =  non_payement + %s  WHERE nom = %s
                                        ''', (text, total_achats , item ))
                        self.cur.execute('''
                                         UPDATE produit SET quantite = quantite + %s
                                         WHERE code = %s
                                         ''',(quantity,code))
                        
                        self.cur.execute('''
                                         INSERT INTO achats (total_achat,fournisseur_,date)
                                         VALUES (%s,%s,%s)
                                         ''',(total_achats,item,date))
                        
                        action = 3
                        table = 1
                        dat3 = datetime.datetime.utcnow()
                        self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                            VALUES (%s, %s , %s, %s )
                        ''' )  , (userid,action,table,dat3))   
                        
                        self.db.commit()
                        self.tableWidget_20.setRowCount(0)
                        self.lineEdit_101.setText('0')
                        self.handle_supplier() 
                    else:
                     QMessageBox.warning(self, "Message", "<span style='font-size:16pt;'> Vous n'avez entré aucune somme.</span>")
      
    def calcul_achats(self):
        nrows = self.tableWidget_20.rowCount()
        f=0
        for row1 in range(0,nrows):
            it = self.tableWidget_20.item(row1, 2)
            it2 = self.tableWidget_20.item(row1, 3)
            if it and it2 is not None :
                    s=float(it.text())
                    s1=float(it2.text())
                    mult=s1*s
                    f=f+mult
                    row1+=1
            result = str(f)
            self.lineEdit_101.setText(result) 
        
    def handle_supplier(self):
        
        nom = self.comboBox_2.currentText()
        self.cur.execute('''
                         SELECT nom ,non_payement,payement from fournisseur
                         WHERE nom = (%s)
                         ''',(nom,))
        data = self.cur.fetchall()
        for ret in data :
              self.label_65.setText(f"<span style='font-size:16pt;'>{ret[0].upper()} </span>: V <font color='red'>{float(ret[2]):.2f} DA </font>NP <font color='red'>{float(ret[1]):.2f} DA </font> ")
              self.label_66.setText(f"<span style='font-size:16pt;'> Total </span>: <font color='red'>{float(ret[2])-float(ret[1]):.2f} DA ")
              
    def add_row_achats(self):
        self.tableWidget_20.insertRow(0)  
        
    def delete_row_achats(self):    
        
        if self.tableWidget_20.rowCount() == 0 :
            QMessageBox.information(self ,"information" , "table deja vide")
        else :          
            row_selected= self.tableWidget_20.currentRow()
            self.tableWidget_20.removeRow(row_selected)         
  
    def annuler_payement_achats(self):
        
            if self.tableWidget_20.rowCount() == 0 :
                QMessageBox.information(self ,"information" , "table deja vide")
            else :     
                delete_message = QMessageBox.warning(self ,"Annuler payement" , "Vous etes sur !!",QMessageBox.Yes | QMessageBox.No )
                if delete_message == QMessageBox.Yes :
                    self.tableWidget_20.setRowCount(0)
                    self.lineEdit_101.setText("0")    
         
    def facture_achat(self):
        pass     
         
############################################################ FOURNISSEUR ###############################################

    def add_supplier(self):
        
        nom = self.lineEdit_25.text()
        phone = self.lineEdit_20.text()
        email = self.lineEdit_26.text()
        details= self.plainTextEdit_5.toPlainText()
        date = datetime.datetime.now()
        
        self.cur.execute(''' INSERT INTO fournisseur (nom,phone,email,details,payement,non_payement,date)
                         VALUES(%s,%s,%s,%s,%s,%s,%s)
                         ''',(nom,phone,email,details,0,0,date))
        action = 3
        table = 9
        dat3 = datetime.datetime.utcnow()
        self.cur.execute(('''INSERT INTO historique(users_id , his_action ,his_table , his_date)
                VALUES (%s, %s , %s, %s )
            ''' )  , (userid,action,table,dat3))   
        
        self.db.commit()  
        QMessageBox.information(self,'Information',f'Le fournisseur {nom} bien ajouter')
        self.lineEdit_25.clear()
        self.lineEdit_20.clear()
        self.lineEdit_26.clear()
        self.plainTextEdit_5.clear()
        self.tableWidget_9.setRowCount(0)
        
        self.retreive_supplier()
        
    def retreive_supplier(self):
        self.cur.execute('''
                         SELECT nom,phone,non_payement,payement,id FROM fournisseur
                         ''')

        data = self.cur.fetchall()
        for row , form in enumerate(data):
            self.tableWidget_9.insertRow(row)
            for col , item in enumerate(form):
                if col == 4 :
                    col2=self.tableWidget_9.item(row,2).text()
                    col3=self.tableWidget_9.item(row,3).text()
                    if col2 and col3 is not None :
                        result= float(col3)-float(col2)
                        self.tableWidget_9.setItem(row, 4, QTableWidgetItem(str(result)))
                else : 
                    self.tableWidget_9.setItem(row, col, QTableWidgetItem(item))
                col += 1
    
        for res in data :
            self.comboBox_2.addItem(res[0])
        
    def filter_table_supplier(self, filter_text):
        
        for i in range(self.tableWidget_9.rowCount()):
            for j in range(self.tableWidget_9.columnCount()):
                item = self.tableWidget_9.item(i, j)
                if item is not None:
                    match = filter_text.lower() not in item.text().lower()
                    self.tableWidget_9.setRowHidden(i, match)
                    if not match:
                        break    
        
############################################################ button open tab ###############################################
    
    def toggleFullScreen(self):
        if self.isFullScreen():
            self.groupBox_8.show()
            self.showNormal()
            self.pushButton_45.setText('Mode plein ecran')
            self.lineEdit.setFocus()
        else:
            #self.groupBox_8.hide()
            self.pushButton_45.setText('Quitter plein ecran')
            self.showFullScreen()   
            self.lineEdit.setFocus()
            
            
           
if __name__ == '__main__':
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = main()
    w.show()
    sys.exit(app.exec_())
        