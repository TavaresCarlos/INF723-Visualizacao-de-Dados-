#Each windows interface is a distinct class
#For example, this is a first initial interface

import os
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QDialog

class login_access_windows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI_login_access()

    def initUI_login_access(self):
        self.setGeometry(200,200,1500,750)
        self.setWindowTitle("First Interface")



        button1 = QPushButton(self)
        button1.setText("Button1")
        button1.move(100,100)
        button1.clicked.connect(self.testeB1)
    
    def testeB1(self):
        print("Press B1!")
