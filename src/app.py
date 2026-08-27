from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import( QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit ,
                            QHBoxLayout, QVBoxLayout, QFrame)
from modules import *

app = QApplication([])

mainwindow = MainWindow()


mainwindow.show()
app.exec()