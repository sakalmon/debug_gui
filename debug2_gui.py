# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debug2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import os 
import time
import webbrowser
import mysql.connector
import re
import threading
from os.path import isfile
from os.path import join
from PyQt5 import QtCore, QtGui, QtWidgets
from mysql.connector import Error


class Ui_MainWindow(object):

    #path = "\\\\midgard\\release"
    path = "C:\\Users\\Sakal\\Dropbox\\Programs\\Git\\repo\\debug_gui"

    def altium_thread(self):

        self.thread = threading.Thread(target=self.open_altium)
        self.thread.start()
        
    def schematic_thread(self):

        self.thread = threading.Thread(target=self.open_schematic)
        self.thread.start()

    def overlays_thread(self):

        self.thread = threading.Thread(target=self.open_overlays)
        self.thread.start()

    def search(self):       

        try:
            print(re.search("^[a-zA-Z]", self.rev))
            if re.search("^[a-zA-Z]", self.rev) is None:  # No revision entered
                self.pushButton.setEnabled(False)
                self.pushButton_2.setEnabled(False)
                self.pushButton_3.setEnabled(False) 
            else:
                self.pushButton_3.setEnabled(True)  # Overlays button is always enabled when a revision is entered

            if self.altium_exists():  # Check if the altium file exists                  
                self.pushButton.setEnabled(True)
            else:            
                self.pushButton.setEnabled(False)

            if self.schematic_exists():  # Check if the schematic file exists
                self.pushButton_2.setEnabled(True)
            else:
                self.pushButton_2.setEnabled(False)
        except:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False) 

    def altium_exists(self):

        try:
            query = f"SELECT component_ID FROM new_PCB_BOM WHERE code = '{self.bom}{self.rev}' AND designator REGEXP '^PCB'"
            connection = mysql.connector.connect(host="midgard", user="userconnect", password="", database="cms")
            cursor = connection.cursor()
            cursor.execute(query)
            self.pcbid = cursor.fetchone()[0]

            if os.path.isfile(f"{self.path}\\{self.pcbid}\\Inspection\\{self.pcbid}.pcbdoc"):
                return True
            else:
                return False

        except Error as e:
            print(f"Error '{e}' has occured")

            return False

    def schematic_exists(self):
        print("schematic_exists function")
        try:
            sch_path = f"{self.path}\\{self.bom}\\{self.rev}"

            print(f"Schematic path is: {self.path}\\{self.bom}\\{self.rev}")

            if (os.path.exists(sch_path)):

                os.chdir(sch_path)
                
                print(f"Looking for: SCH{self.bom}{self.rev}.pdf")

                if(os.path.isfile(f"SCH{self.bom}{self.rev}.pdf")):
                    return True         
                else:
                    return False
        except:
            return False

    def open_altium(self):
        
        try:
            altium_path = f"{self.path}\\{self.pcbid}\\Inspection"
            os.chdir(altium_path)

            for f in os.listdir():
                if isfile(join(os.getcwd(), f)):
                    if re.search(f"^{self.pcbid}", f):  # Implemented for when a file name ends with an x or x1, etc.
                        os.startfile(f)
                        self.pushButton.setText("Opening...")
                        QtWidgets.qApp.processEvents()
                        time.sleep(3)
                        self.pushButton.setText("Altium")
                        QtWidgets.qApp.processEvents()    
            
        except Error as e:
            print(f"Error '{e}' has occured.")      

    def open_schematic(self):

        sch_path = f"{self.path}\\{self.bom}\\{self.rev}"

        try:
            os.chdir(sch_path)
            os.startfile(f"SCH{self.bom}{self.rev}.pdf")

            self.pushButton_2.setEnabled(True)

            self.pushButton_2.setText("Opening...")
            QtWidgets.qApp.processEvents()
            time.sleep(3)
            self.pushButton_2.setText("Schematic")
            QtWidgets.qApp.processEvents()

        except:
            pass

    def open_overlays(self):

        ovl_path = "http://midgard/cms/overlays_new/overlay_magic.cgi?bom_code="
        top = "&layer=Top&Go="
        bot = "&layer=Bottom&Go="

        self.pushButton_3.setText("Opening...")
        QtWidgets.qApp.processEvents()
        time.sleep(3)
        self.pushButton_3.setText("Overlays")
        QtWidgets.qApp.processEvents()

        webbrowser.open_new_tab(f"{ovl_path}{self.bom}{self.rev}{top}")
        webbrowser.open_new_tab(f"{ovl_path}{self.bom}{self.rev}{bot}")

    @property
    def bom(self):

        bom_rev = self.lineEdit.text()        

        if bom_rev[-2].isnumeric():
            bom = bom_rev[:-1]

            return bom
        else:  
            bom = bom_rev[:-2]
            
            return bom        
            
    @property
    def rev(self):

        bom_rev = self.lineEdit.text()        

        if bom_rev[-2].isnumeric():
            rev = bom_rev[-1]

            return rev
        else:  
            rev = bom_rev[-2:]
            
            return rev.upper()  

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(767, 554)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(160, 290, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled(False) # Change to false once finished debugging
        self.pushButton.clicked.connect(self.altium_thread)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 290, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.schematic_thread) 
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 290, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.clicked.connect(self.overlays_thread) 
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(310, 190, 141, 31))
        self.lineEdit.setFocus()
        self.lineEdit.returnPressed.connect(self.search)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        #self.lineEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.lineEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.lineEdit.setTabChangesFocus(True)
        #self.lineEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        #self.lineEdit.setTabStopWidth(5)
        self.lineEdit.setObjectName("lineEdit")        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 180, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(460, 190, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.search)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 767, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hardware Tech Debug"))
        self.pushButton.setText(_translate("MainWindow", "Altium"))
        self.pushButton_2.setText(_translate("MainWindow", "Schematic"))
        self.pushButton_3.setText(_translate("MainWindow", "Overlays"))
        self.label.setText(_translate("MainWindow", "BOM & Rev:"))
        self.pushButton_4.setText(_translate("MainWindow", "Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
