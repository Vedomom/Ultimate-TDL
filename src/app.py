from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import( QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit ,
                            QHBoxLayout, QVBoxLayout, QFrame)
from modules import *

app = QApplication([])

mainwindow = QWidget()


layout = QHBoxLayout()

tdl1 = TDList("features","features.txt")
lframe = ListFrame()
lframe.addWidget(tdl1)
menu = MainMenu()


layout.addLayout(menu)
layout.addLayout(lframe)

mainwindow.setLayout(layout)



mainwindow.show()
app.exec()