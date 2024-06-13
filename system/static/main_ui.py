import sys
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *

from static.index_ui import *

class main_windows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("A System to View and Identify Wind Turbine Faults")

        label_background_logo = QLabel(self)
        pixmap_logo = QPixmap('./asserts/image/logo.png')
        label_background_logo.setPixmap(pixmap_logo)

        label_background_logo.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label_background_logo)

        # Create a menu bar
        menu_bar = self.menuBar()
        
        # Add File menu and actions
        index_dashboard = menu_bar.addMenu('Run')
        
        index_action = QAction('Start', self)
        index_action.triggered.connect(self.index_windows)
        index_dashboard.addAction(index_action)

        index_action = QAction('Visualization Historic', self)
        #index_action.triggered.connect(self.index_windows)
        index_dashboard.addAction(index_action)
        
        # Add Edit menu and actions
        
        edit_menu = menu_bar.addMenu('Wind Farm Layout Analysis')
        
        cut_action = QAction('Start Complex Network Analysis', self)
        #cut_action.triggered.connect(self.cut_text)
        edit_menu.addAction(cut_action)
        
        '''
        copy_action = QAction('Copy', self)
        copy_action.triggered.connect(self.copy_text)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('Paste', self)
        paste_action.triggered.connect(self.paste_text)
        edit_menu.addAction(paste_action)
        '''
        
    def index_windows(self):
        self.index_w = index_windows()
        self.index_w.show()
    
    def soma(self, x, y):
        return x+y
    '''     
    def cut_text(self):
        print('Cut action triggered.')
        
    def copy_text(self):
        print('Copy action triggered.')
        
    def paste_text(self):
        print('Paste action triggered.')
    '''
