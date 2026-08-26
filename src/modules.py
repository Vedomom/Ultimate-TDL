from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import( QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit ,
                            QHBoxLayout, QVBoxLayout, QFrame)


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
        
        with open(path,'r') as tdl:
            tasklist = tdl.read().split("\n")       
            for task in tasklist:
                self.taskbox.addWidget(QLabel(task), alignment=Qt.AlignmentFlag.AlignCenter)         
        
        mainframe = QVBoxLayout()
        mainframe.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        mainframe.addLayout(self.taskbox)
        
        self.setLayout(mainframe)