from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import( QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit ,
                            QHBoxLayout, QVBoxLayout, QFrame, QCheckBox)


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
    
    def __init__(self):
        super().__init__()
        
        new_btn = TDButton("new")  
        import_btn = TDButton("open")   
        settings_btn = TDButton("settings")   
        extra_btn = TDButton("extra")
        self.buttonList = [new_btn, 
                           import_btn,
                           settings_btn,
                           extra_btn]
        for b in self.buttonList:
            self.addWidget(b)


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
        


class ListWindow(QWidget):
    
    def __init__(self, path: str, title: str | None):
        super().__init__()
        
        print(path)
        print(title)
        
        if title is not None:
            self.title = Heading(title)
            self.title.setFont(self.title.getBigFont())
        
        self.taskbox = QVBoxLayout()
        self.task_input = TaskInput(self.taskbox)
        
        with open(path,'r') as tdl:
            tasklist = tdl.read().split("\n")       
            for task in tasklist:
                if task is not '':
                    self.taskbox.addLayout(Task(task, self.taskbox))         
        
        mainframe = QVBoxLayout()
        mainframe.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        #mainframe.addWidget(self.task_input, alignment=Qt.AlignmentFlag.AlignCenter)
        mainframe.addLayout(self.task_input.taskInputFrame)
        mainframe.addLayout(self.taskbox)
        mainframe.setSpacing(20)
        
        self.setLayout(mainframe)


class TaskInput(QLineEdit):
    def __init__(self, taskbox:QVBoxLayout):
        super().__init__()
        
        self.setPlaceholderText("Type a Task")
        self.add_btn = TDButton("add")
        self.add_btn.pressed.connect(self.addTask)
        self.returnPressed.connect(self.addTask)
        self.taskbox = taskbox
        self.setFont(self.add_btn.getBigFont())
        
        self.taskInputFrame = QHBoxLayout()
        self.taskInputFrame.addWidget(self, alignment=Qt.AlignmentFlag.AlignRight)
        self.taskInputFrame.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignLeft)
    
    
    def addTask(self):
        task = Task(self.text(), self.taskbox)
        self.taskbox.addLayout(task)
        self.clear()


class Task(QHBoxLayout):
    def __init__(self, text: str, taskbox: QVBoxLayout):
        super().__init__()
        
        self.text = QLabel(text)
        self.checkbox = QCheckBox()
        self.delete_btn = TDButton("X")
        self.taskbox = taskbox
        
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
        self.text.hide()
        self.checkbox.hide()
        self.delete_btn.hide()
        self.taskbox.removeItem(self)
    
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
    
        