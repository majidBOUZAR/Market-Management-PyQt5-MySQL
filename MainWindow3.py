# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 333)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit_23 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_23.setGeometry(QtCore.QRect(280, 100, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lineEdit_23.setFont(font)
        self.lineEdit_23.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_23.setCursorPosition(0)
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(110, 100, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.pushButton_26 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_26.setGeometry(QtCore.QRect(370, 210, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_26.setFont(font)
        self.pushButton_26.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icone/reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_26.setIcon(icon)
        self.pushButton_26.setIconSize(QtCore.QSize(22, 22))
        self.pushButton_26.setObjectName("pushButton_26")
        self.pushButton_27 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_27.setGeometry(QtCore.QRect(110, 150, 391, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_27.setFont(font)
        self.pushButton_27.setStyleSheet("background-color: rgb(112, 255, 133);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icone/login.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_27.setIcon(icon1)
        self.pushButton_27.setObjectName("pushButton_27")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(110, 40, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.lineEdit_22 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_22.setGeometry(QtCore.QRect(280, 40, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lineEdit_22.setFont(font)
        self.lineEdit_22.setCursorPosition(0)
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(130, 210, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("color: rgb(0, 170, 255);")
        self.label_24.setObjectName("label_24")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit_23.setPlaceholderText(_translate("MainWindow", "Mot de pass"))
        self.label_23.setText(_translate("MainWindow", "Mot de pass "))
        self.pushButton_26.setText(_translate("MainWindow", "Réinitialiser "))
        self.pushButton_27.setText(_translate("MainWindow", "Login"))
        self.label_22.setText(_translate("MainWindow", "Nom Utilisateur "))
        self.lineEdit_22.setPlaceholderText(_translate("MainWindow", "Utilisateur"))
        self.label_24.setText(_translate("MainWindow", "Mot de pass oublié ? "))
import iconne_rc
