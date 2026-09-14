from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import( QApplication)
from .modules import *
from .styles import styleString

app = QApplication([])

app.setStyleSheet(styleString)
app.setWindowIcon(QIcon("_internal/resources/UTDL100.png"))
mainwindow = MainWindow()


