#Display the corrects views to the user 
from sys import *
from static.main_ui import *

class user_view:
    def __init__(self):
        global app
        app = QApplication(argv)
        
        global user_interface
        user_interface = main_windows()
        user_interface.showMaximized()
        app.exec_()
