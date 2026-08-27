import os
import pathlib
from PyQt6 import sip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import( QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit ,
                            QHBoxLayout, QVBoxLayout, QFrame, QCheckBox, QDialog, QDialogButtonBox)

LIST_PATH = "./lists"

class TDList(QPushButton):
    
    
    def __init__(self, list_title: str, list_path: str):
        super().__init__()
        self.path = list_path
        self.title = list_title
        self.setText(list_title)
        self.pressed.connect(self.openList)
        
        #styling
    
    
    def openList(self):
        
        self.list_window = ListWindow(self.path, self.title)
        self.list_window.show()
    
    
    
class MainMenu(QVBoxLayout):
    
    def __init__(self, window : QWidget):
        super().__init__()
        
        self.window = window
        self.new_btn = TDButton("new")  
        self.import_btn = TDButton("open")   
        self.settings_btn = TDButton("settings")   
        self.extra_btn = TDButton("extra")
        
        self.new_btn.pressed.connect(self.creatList)
        
        
        
        self.buttonList = [self.new_btn, 
                           self.import_btn,
                           self.settings_btn,
                           self.extra_btn]
        for b in self.buttonList:
            self.addWidget(b)
        
    def creatList(self):
        self.dialog_CNL = CreatNewListDialog(self.window)
        self.dialog_CNL.show()
        self.dialog_CNL.exec()


class CreatNewListDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.mainframe = QVBoxLayout()
        #line input for name
        self.inputBox = QLineEdit(self)
        
        #button box
        buttons = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox = QDialogButtonBox(buttons)
        
        self.buttonBox.accepted.connect(self.createNew)
        self.buttonBox.rejected.connect(self.reject)
        self.inputBox.returnPressed.connect(self.createNew)
        
        self.mainframe.addWidget(self.inputBox, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainframe.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.mainframe)
        #creat txt file
    
    def createNew(self):
        
        if not os.path.exists(LIST_PATH):
            os.mkdir(LIST_PATH)
        
        with open(f"{LIST_PATH}/{self.inputBox.text()}.txt", 'w'):
            self.list = ListWindow(f"{LIST_PATH}/{self.inputBox.text()}.txt", self.inputBox.text())
        
        self.close()

class Heading(QLabel):
    
    def __Init__(self, text:str):
        super().__init__()
        
        self.setText(text)

    
    def getBigFont(self):
        font = self.font()
        font.setPointSize(50)
        font.setWeight(800)
        return font
    
    lable = None
    

class TDButton(QPushButton):
    
    def __init__(self, text: str | None ):
        super().__init__(text)
        
        self.setFont(self.getBigFont())
    
    
    def getBigFont(self):
        font = self.font()
        font.setPointSize(20)
        font.setWeight(500)
        return font


class ListFrame(QVBoxLayout):
    
    def __init__(self):
        super().__init__()
        
        self.setSpacing(1)
        
        self.lists = [f for f in pathlib.Path().glob(f"{LIST_PATH}/*.txt")]
        
        for list in self.lists:
            
            tdl = TDList(list.name.removesuffix(".txt"), f"{LIST_PATH}/{list.name}")
            self.addWidget(tdl, alignment=Qt.AlignmentFlag.AlignHCenter)

class ListWindow(QWidget):
    
    def __init__(self, path: str, title: str | None):
        super().__init__()
 
        self.path = path 
        self.list_title = title
        
        if title is not None:
            self.title = Heading(title)
            self.title.setFont(self.title.getBigFont())
        
        self.taskbox = QVBoxLayout()
        self.task_input = TaskInput()
        
        self.task_input.add_btn.pressed.connect(self.addTask)
        self.task_input.returnPressed.connect(self.addTask)
        
        with open(path,'r') as tdl:
            tasklist = tdl.read().split("\n")       
            for task in tasklist:
                if task != '':
                    self.taskbox.addLayout(Task(task,self.path))         
        
        mainframe = QVBoxLayout()
        mainframe.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        #mainframe.addWidget(self.task_input, alignment=Qt.AlignmentFlag.AlignCenter)
        mainframe.addLayout(self.task_input.taskInputFrame)
        mainframe.addLayout(self.taskbox)
        mainframe.setSpacing(20)
        
        self.setLayout(mainframe)
        
    def addTask(self):
        if not self.task_input.text() == "" and not self.task_input.text() == " ":
            task = Task(self.task_input.text(), self.path)
            self.taskbox.addLayout(task)
            
            with open(self.path, "a") as listFile:
                listFile.write(f"{task.text.text()}\n")
                
            
            self.task_input.clear()
        else:
            return


class TaskInput(QLineEdit):
    def __init__(self):
        super().__init__()
        
        self.setPlaceholderText("Type a Task")
        self.add_btn = TDButton("add")
        self.setFont(self.add_btn.getBigFont())
        
        self.taskInputFrame = QHBoxLayout()
        self.taskInputFrame.addWidget(self, alignment=Qt.AlignmentFlag.AlignRight)
        self.taskInputFrame.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignLeft)
    

class Task(QHBoxLayout):
    def __init__(self, text: str, path: str):
        super().__init__()
        
        self.text = QLabel(text)
        self.checkbox = QCheckBox()
        self.delete_btn = TDButton("X")
        self.path = path
        
        self.checkbox.checkStateChanged.connect(self.checkTask)
        self.checkbox.setFont(self.getBigFont())
        self.text.setFont(self.getBigFont())
        self.delete_btn.pressed.connect(self.deleteTask)
        self.delete_btn.setFont(self.getBigFont())
        
        self.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignRight)
        self.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.delete_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        
    def checkTask(self):
        if self.checkbox.isChecked():
            self.text.setFont(self.getGrayFont())
        else:
            self.text.setFont(self.getBigFont())
    
    def deleteTask(self):
        
        with open(self.path, "r") as listFile_R:
            lines = listFile_R.readlines()
            
            with open(self.path, "w") as listFile_W:
                for line in lines:
                    if line.strip("\n") != self.text.text():
                        listFile_W.write(line)
        
        self.text.deleteLater()
        self.checkbox.deleteLater()
        self.delete_btn.deleteLater()
        sip.delete(self)
    
    def getGrayFont(self):
        font = QLabel().font()
        font.setPointSize(20)
        font.setWeight(300)
        font.setStrikeOut(True)
        return font
    
    def getBigFont(self):
        font = QLabel().font()
        font.setPointSize(20)
        font.setWeight(600)
        return font
    

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.menu = MainMenu(self)
        self.listbox = ListFrame()

        self.mainframe = QHBoxLayout()
        self.mainframe.addLayout(self.menu)
        self.mainframe.addLayout(self.listbox)
        
        self.setLayout(self.mainframe)
            