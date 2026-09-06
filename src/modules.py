import os
import pathlib
import random
from PyQt6 import sip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import( QApplication, QWidget, QLabel, QPushButton, QMainWindow, QLineEdit ,
                            QHBoxLayout, QVBoxLayout, QFrame, QCheckBox, QDialog, QDialogButtonBox, QScrollArea)

LIST_PATH = "./lists"

class TDList(QHBoxLayout):
    
    
    def __init__(self, list_title: str, list_path: str, parent: QWidget, frame:ListFrame):
        super().__init__()
        self.path = list_path
        self.title = list_title
        
        self.p = parent
        self.frame = frame
        self.button = QPushButton()
        self.button.setText(list_title)
        self.button.pressed.connect(self.openList)
        self.button.setFont(QFont("arial", 18, 600))  
        self.button.setObjectName("TDL")
        
        self.taskCount = QLabel()
        self.taskCount.setText(f"- - - {self.countTasks()} Tasks - - -")
        self.taskCount.setFont(QFont("arial", 14, 400))
        
        self.deleteBTN = QPushButton("delete")
        self.deleteBTN.setObjectName("ListDeleteButton")
        self.deleteBTN.setFont(QFont("arial", 14, 500))
        self.deleteBTN.pressed.connect(self.deleteList)
        
        self.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.taskCount, alignment=Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.deleteBTN, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.setObjectName("TDL")
        
        
    
    
    def countTasks(self):
        count = 0
        with open(self.path, "r") as tdl:
            tasks = tdl.readlines()
            for task in tasks:
                count += 1
                
        return count
    
    
    def deleteList(self):
        dialog = DeleteListDialog(self.p, self, self.frame)
        dialog.show()
        dialog.exec()
    
    def openList(self):
        
        self.list_window = ListWindow(self.path, self.title)
        self.list_window.show()
    
    
class MainMenu(QVBoxLayout):
    
    def __init__(self, window : QWidget, frame:ListFrame):
        super().__init__()
        
        self.window = window
        self.new_btn = TDButton("new")  

        
        self.new_btn.pressed.connect(self.creatList)
        
        self.frame = frame
        
        
        self.buttonList = [self.new_btn]
        for b in self.buttonList:
            self.addWidget(b)
            b.setObjectName("MenuButton")
            
        self.setSpacing(2)
        
    def creatList(self):
        self.dialog_CNL = CreatNewListDialog(self.window, self.frame)
        self.dialog_CNL.show()
        self.dialog_CNL.exec()

class DeleteListDialog(QDialog):
    def __init__(self, parent: QWidget | None, tdlist: TDList, listframe: ListFrame):
        super().__init__(parent)
        self.mainframe = QVBoxLayout()
        
        self.tdl = tdlist
        self.frame = listframe
        
        self.text = QLabel("are you sure you want to delete this list?")
        self.text.setFont(QFont("Georgia", 14, 400))
        #button box
        buttons = (QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.setObjectName("DialogButton")
        
        self.mainframe.setSpacing(20)
        self.buttonBox.accepted.connect(self.deleteList)
        self.buttonBox.rejected.connect(self.reject)
        
        self.mainframe.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainframe.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.mainframe)
    
    def deleteList(self):
        if os.path.exists(self.tdl.path):
            os.remove(self.tdl.path)
        else:
            print("path doesn't exist")
        self.frame.refresh()
        self.close()

class CreatNewListDialog(QDialog):
    def __init__(self, parent: QWidget, frame:ListFrame):
        super().__init__(parent)
        
        self.mainframe = QVBoxLayout()
        #line input for name
        self.inputBox = QLineEdit(self)
        self.inputBox.setFont(QFont("arial", 15, 400))
        self.inputBox.setPlaceholderText("List Name")
        
        #button box
        buttons = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.setObjectName("DialogButton")
        
        self.frame = frame
        
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
        
        self.frame.refresh()
        
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
    
    def __init__(self, parent: QWidget):
        super().__init__()
        
        self.setSpacing(1)
        self.p = parent
        
        self.lists = [f for f in pathlib.Path().glob(f"{LIST_PATH}/*.txt")]
        
        for list in self.lists:
            
            tdl = TDList(list.name.removesuffix(".txt"), f"{LIST_PATH}/{list.name}", parent, self)
            self.addLayout(tdl)
        
        self.setSpacing(0)
    
    def refresh(self):
        
        listCount = self.count()
        lists = []
        for index in range(0, listCount):
            l = self.itemAt(index)
            lists.append(l)
            
        for list in lists:
            for i in range(0, list.count()): # type: ignore
                childWidget = list.itemAt(i).widget()# type: ignore
                childWidget.deleteLater() # type: ignore
            sip.delete(list) # type: ignore
        
        self.lists = [f for f in pathlib.Path().glob(f"{LIST_PATH}/*.txt")]
        
        for list in self.lists:
            
            tdl = TDList(list.name.removesuffix(".txt"), f"{LIST_PATH}/{list.name}", self.p, self)
            self.addLayout(tdl)

class ListWindow(QMainWindow):
    
    def __init__(self, path: str, title: str | None):
        super().__init__()

        self.resize(500, 700)
        
        self.path = path 
        self.list_title = title
        
        self.scrollarea = QScrollArea()
        
        self.widget = QWidget()
        
        
        if title is not None:
            self.title = Heading(title)
            self.title.setFont(self.title.getBigFont())
        
        self.taskbox = QVBoxLayout()
        self.task_input = TaskInput()
        self.mixButton = TDButton("mix")
        
        self.mixButton.pressed.connect(self.mixTasks)
        self.task_input.add_btn.pressed.connect(self.addTask)
        self.task_input.returnPressed.connect(self.addTask)
        
        self.task_input.taskInputFrame.addWidget(self.mixButton)
        
        with open(path,'r') as tdl:
            tasklist = tdl.read().split("\n")       
            for task in tasklist:
                if task != '':
                    self.taskbox.addLayout(Task(task,self.path))         
        
        mainframe = QVBoxLayout()
        mainframe.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        mainframe.addLayout(self.task_input.taskInputFrame)
        mainframe.addLayout(self.taskbox)
        mainframe.setSpacing(10)
        
        self.widget.setLayout(mainframe)
        
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.widget)
        
        self.setCentralWidget(self.scrollarea)
        
        
    def addTask(self):
        if not self.task_input.text() == "" and not self.task_input.text() == " ":
            task = Task(self.task_input.text(), self.path)
            self.taskbox.addLayout(task)
            
            with open(self.path, "a") as listFile:
                listFile.write(f"{task.text.text()}\n")
                
            
            self.task_input.clear()
        else:
            return

    def mixTasks(self):
        tasklist = [t for t in self.taskbox.children()]
        
        for t in self.taskbox.children():
            self.taskbox.removeItem(t) #type:ignore
            
        for i in range(0, len(tasklist)):
            t = random.choice(tasklist)
            self.taskbox.addLayout(t) # type: ignore
            tasklist.remove(t)
            

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

        self.text.setFont(self.getBigFont())
        self.text.setWordWrap(True)
        
        self.delete_btn.pressed.connect(self.deleteTask)
        self.delete_btn.setFont(self.getBigFont())
        self.delete_btn.setObjectName("TaskDeleteButton")
        
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
        font = QFont("Georgia")
        font.setPointSize(20)
        font.setWeight(300)
        font.setStrikeOut(True)
        return font
    
    def getBigFont(self):
        font = QFont("Georgia")
        font.setPointSize(20)
        font.setWeight(600)
        return font
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.resize(600, 400)
        self.setMaximumSize(600, 400)
        
        self.listbox = ListFrame(self)
        self.menu = MainMenu(self, self.listbox)

        self.mainframe = QVBoxLayout()
        self.listContainer = QVBoxLayout()
        self.mainHeader = QHBoxLayout()
        
        self.scrollbox = QScrollArea()
        self.scrollwidget = QWidget()
        
        self.refreshButton = TDButton("refresh")
        self.refreshButton.setFont(QFont("arial", 16, 400))
        self.refreshButton.setObjectName("RefreshButton")
        self.refreshButton.pressed.connect(self.listbox.refresh)
        self.listboxTitle = QLabel("Lists")
        self.listboxTitle.setObjectName("ListBoxTitle")
        self.listboxTitle.setFont(QFont("arial", 16, 400))
        
        self.mainHeader.addWidget(self.menu.buttonList[0])
        self.mainHeader.addWidget(self.listboxTitle, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainHeader.addWidget(self.refreshButton)
        
        
        self.scrollwidget.setLayout(self.listbox)
        self.scrollbox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollbox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollbox.setWidgetResizable(True)
        self.scrollbox.setWidget(self.scrollwidget)
        
        self.scrollbox.setMinimumWidth(self.width())
        self.listbox.setSpacing(10)
        
        self.listContainer.addStretch()
        self.listContainer.addLayout(self.mainHeader)
        self.listContainer.addWidget(self.scrollbox, alignment=Qt.AlignmentFlag.AlignCenter, stretch=0)
        self.listContainer.addStretch()
        
        #self.mainframe.addLayout(self.menu)
        self.mainframe.addLayout(self.listContainer)
        
        self.cWidget = QWidget()
        
        self.cWidget.setLayout(self.mainframe)
        
        self.setCentralWidget(self.cWidget)
        
            