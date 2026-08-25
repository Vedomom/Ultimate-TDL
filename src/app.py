from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import( QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit ,
                            QHBoxLayout, QVBoxLayout, QFrame)
from modules import *

app = QApplication([])

mainwindow = QWidget()


layout = QHBoxLayout()

tdl1 = TDList("features","features.txt")
menu = MainMenu()
vbox = QVBoxLayout()
title = Heading("Hello world")
title.setFont(title.getBigFont())

for btn in menu.buttonList:
    vbox.addWidget(btn)

layout.addLayout(vbox)
layout.addWidget(tdl1)
layout.addWidget(title)
mainwindow.setLayout(layout)

mainwindow.show()
app.exec()