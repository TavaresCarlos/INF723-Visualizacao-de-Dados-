from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel

from static.SBES_ui import *
from static.MES_ui import *
from static.main_ui import *

def test_soma():
    app = QApplication(sys.argv)
    widget = QWidget()
    u = main_windows()
    assert 5 == u.soma(2,3)


