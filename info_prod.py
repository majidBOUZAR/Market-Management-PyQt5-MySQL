# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info_prod.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(635, 447)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_11.setGeometry(QtCore.QRect(10, 80, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setStyleSheet("border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;")
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(400, 241, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.spinBox_2.setFont(font)
        self.spinBox_2.setStyleSheet("border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;")
        self.spinBox_2.setMaximum(999999999)
        self.spinBox_2.setObjectName("spinBox_2")
        self.comboBox_15 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_15.setGeometry(QtCore.QRect(10, 300, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.comboBox_15.setFont(font)
        self.comboBox_15.setStyleSheet("background-color: rgb(246, 239, 255);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;")
        self.comboBox_15.setObjectName("comboBox_15")
        self.comboBox_15.addItem("")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(10, 130, 211, 151))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.plainTextEdit_2.setFont(font)
        self.plainTextEdit_2.setStyleSheet("border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(400, 160, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.doubleSpinBox_4.setFont(font)
        self.doubleSpinBox_4.setStyleSheet("border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;")
        self.doubleSpinBox_4.setMaximum(9999999999999.99)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_12.setEnabled(False)
        self.lineEdit_12.setGeometry(QtCore.QRect(400, 300, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lineEdit_12.setFont(font)
        self.lineEdit_12.setStyleSheet("border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;")
        self.lineEdit_12.setText("")
        self.lineEdit_12.setClearButtonEnabled(False)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(400, 90, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.doubleSpinBox_3.setFont(font)
        self.doubleSpinBox_3.setStyleSheet("border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;")
        self.doubleSpinBox_3.setMaximum(1000000000000000.0)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 635, 21))
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
        self.lineEdit_11.setPlaceholderText(_translate("MainWindow", "Nom de produit"))
        self.comboBox_15.setItemText(0, _translate("MainWindow", "----------"))
        self.lineEdit_12.setPlaceholderText(_translate("MainWindow", "Code barre"))
