from PyQt6.QtCore import Qt
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
        pass
    
    
    
class MainMenu(QVBoxLayout):
    
    def __init__(self):
        super().__init__()
        new_btn = QPushButton("new")  
        import_btn = QPushButton("open")   
        settings_btn = QPushButton("settings")   
        extra_btn = QPushButton("extra")
        self.buttonList = [new_btn, 
                           import_btn,
                           settings_btn,
                           extra_btn]


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