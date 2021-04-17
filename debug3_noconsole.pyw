# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\debug3.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
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

    if os.path.exists("\\\\midgard\\release"):  # If at work
        print("Detected program is run at work - Setting path to \\\\midgard\\release")
        path = "\\\\midgard\\release"

    else:
        path = "C:\\Users\\Sakal\\Documents\\Git\\repo\\debug_gui"  # If at home
        print("Detected program is run at home - Setting path to C:\\Users\\Sakal\\Documents\\Git\\repo\\debug_gui")

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
            print("Checking if revision was entered")

            if re.search("^[a-zA-Z]", self.rev) is None:  # No revision entered
                print("No revision was entered - Greying out all buttons")
                self.altiumButton.setEnabled(False)
                self.schematicButton.setEnabled(False)
                self.overlaysButton.setEnabled(False) 

            else:
                self.overlaysButton.setEnabled(True)  # Overlays button is always enabled when a revision is entered
                print("A revision was entered\nEnabling overlays button")

            if self.altium_exists():  # Check if the altium file exists   
                print("Altium file exits... Enabling altium button")               
                self.altiumButton.setEnabled(True)

            else: 
                print("Altium file not found... Greying out altium button")           
                self.altiumButton.setEnabled(False)

            if self.schematic_exists():  # Check if the schematic file exists
                print("Schematic file exists... Enabling schematic button") 
                self.schematicButton.setEnabled(True)

            else:
                print("Schematic file not found... Greying out schematic button") 
                self.schematicButton.setEnabled(False)

        except:
            self.altiumButton.setEnabled(False)
            self.schematicButton.setEnabled(False)
            self.overlaysButton.setEnabled(False) 

       
        if self.altiumButton.isEnabled():
            self.openAllButton.setEnabled(True)

        elif self.schematicButton.isEnabled():
            self.openAllButton.setEnabled(True)

        elif self.overlaysButton.isEnabled():
            self.openAllButton.setEnabled(True)

        else:
            self.openAllButton.setEnabled(False)

    def altium_exists(self):

        try:
            print("Creating query from entered BOM and revision...")
            query = f"SELECT component_ID FROM new_PCB_BOM WHERE code = '{self.bom}{self.rev}' AND designator REGEXP '^PCB'"
            print("Connecting to MySQL server...")
            connection = mysql.connector.connect(host="midgard", user="userconnect", password="", database="cms")
            cursor = connection.cursor()
            print("Connected to server")
            print("Executing query...")
            cursor.execute(query)
            self.pcbid = cursor.fetchone()[0]
            print(f"Retrieved PCB ID of: {self.pcbid}")

            print("Locating pcbdoc file on release...")
            if os.path.isfile(f"{self.path}\\{self.pcbid}\\Inspection\\{self.pcbid}.pcbdoc"):
                print("Altium file found")
                return True
            else:
                print("Altium file not found")
                return False

        except Error as e:
            print(f"Error '{e}' has occured")

            return False

    def schematic_exists(self):
        
        try:
            sch_path = f"{self.path}\\{self.bom}\\{self.rev}"

            print(f"Locating schematic file on release...")
    
            if (os.path.exists(sch_path)):

                os.chdir(sch_path)

                if(os.path.isfile(f"SCH{self.bom}{self.rev}.pdf")):
                    print("Schematic file found")
                    return True         
                else:
                    return False
        except:
            return False

    def open_altium(self):
        
        try:
            print("Opening altium file...")

            altium_path = f"{self.path}\\{self.pcbid}\\Inspection"
            os.chdir(altium_path)

            for f in os.listdir():
                if isfile(join(os.getcwd(), f)):
                    if re.search(f"^{self.pcbid}", f):  # Implemented for when a file name ends with an x or x1, etc.
                        os.startfile(f)
                        self.altiumButton.setText("Opening...")
                        QtWidgets.qApp.processEvents()
                        time.sleep(3)
                        self.altiumButton.setText("Altium")
                        QtWidgets.qApp.processEvents()    
            
        except Error as e:
            print(f"Error '{e}' has occured.")      

    def open_schematic(self):

        sch_path = f"{self.path}\\{self.bom}\\{self.rev}"

        try:
            print("Opening schematic file...")
            os.chdir(sch_path)
            os.startfile(f"SCH{self.bom}{self.rev}.pdf")

            self.schematicButton.setText("Opening...")
            QtWidgets.qApp.processEvents()
            time.sleep(3)
            self.schematicButton.setText("Schematic")
            QtWidgets.qApp.processEvents()

        except:
            pass

    def open_overlays(self):

        print("Opening top and bottom overlays...")
        ovl_path = "http://midgard/cms/overlays_new/overlay_magic.cgi?bom_code="
        top = "&layer=Top&Go="
        bot = "&layer=Bottom&Go="

        self.overlaysButton.setText("Opening...")
        QtWidgets.qApp.processEvents()
        time.sleep(3)
        self.overlaysButton.setText("Overlays")
        QtWidgets.qApp.processEvents()

        webbrowser.open_new_tab(f"{ovl_path}{self.bom}{self.rev}{top}")
        webbrowser.open_new_tab(f"{ovl_path}{self.bom}{self.rev}{bot}")

    def open_all(self):

        print("Opening all available...")

        try:
            self.altium_thread()
            self.schematic_thread()
            self.overlays_thread()

        except:
            pass

    @property
    def bom(self):

        bom_rev = self.lineEdit.text()        

        if bom_rev[-2].isnumeric():
            bom = bom_rev[:-1]

            return bom
        else:  
            bom = bom_rev[:-2]

            print(f"BOM: {bom}")
            
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
        self.altiumButton = QtWidgets.QPushButton(self.centralwidget)
        self.altiumButton.setGeometry(QtCore.QRect(160, 290, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.altiumButton.setFont(font)
        self.altiumButton.setObjectName("altiumButton")
        self.altiumButton.setEnabled(False) # Change to false once finished debugging
        self.altiumButton.clicked.connect(self.altium_thread)
        self.schematicButton = QtWidgets.QPushButton(self.centralwidget)
        self.schematicButton.setGeometry(QtCore.QRect(310, 290, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.schematicButton.setFont(font)
        self.schematicButton.setObjectName("schematicButton")
        self.schematicButton.setEnabled(False)
        self.schematicButton.clicked.connect(self.schematic_thread) 
        self.overlaysButton = QtWidgets.QPushButton(self.centralwidget)
        self.overlaysButton.setGeometry(QtCore.QRect(460, 290, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.overlaysButton.setFont(font)
        self.overlaysButton.setObjectName("overlaysButton")
        self.overlaysButton.setEnabled(False)
        self.overlaysButton.clicked.connect(self.overlays_thread)
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
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(460, 190, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.search)
        self.openAllButton = QtWidgets.QPushButton(self.centralwidget)
        self.openAllButton.setGeometry(QtCore.QRect(160, 380, 441, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.openAllButton.setFont(font)
        self.openAllButton.setObjectName("openAllButton")
        self.openAllButton.clicked.connect(self.open_all)
        self.openAllButton.setEnabled(False)
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
        self.altiumButton.setText(_translate("MainWindow", "Altium"))
        self.schematicButton.setText(_translate("MainWindow", "Schematic"))
        self.overlaysButton.setText(_translate("MainWindow", "Overlays"))
        self.label.setText(_translate("MainWindow", "BOM & Rev:"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.openAllButton.setText(_translate("MainWindow", "Open All"))
       
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
