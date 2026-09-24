import os
import pathlib
import random
import sqlite3
from PyQt6 import sip
from PyQt6.QtCore import QEvent, Qt, QSize, QEvent, QVariantAnimation, QEasingCurve
from PyQt6.QtCore import QObject, pyqtProperty #type:ignore
from PyQt6.QtGui import QFont, QIcon, QMouseEvent, QPixmap, QColor
from PyQt6.QtWidgets import( QWidget, QLabel, QPushButton, QMainWindow, QLineEdit , 
                            QHBoxLayout, QVBoxLayout, QCheckBox, QDialog, QDialogButtonBox, QScrollArea,
                            QFileDialog, QToolButton, QStyle)


FONT_NAME = "Bahnschrift"
DB = "_internal/Lists.db"


class TDList(QHBoxLayout):
    
    
    def __init__(self, list_title: str, parent: QWidget, frame:ListFrame):
        super().__init__()
        self.title = list_title
        
        self.p = parent
        self.frame = frame
        self.button = QPushButton()
        self.button.setText(list_title)
        self.button.pressed.connect(self.openList)
        self.button.setFont(QFont(FONT_NAME, 18, 600))  
        self.button.setObjectName("TDL")
        
        self.taskCount = QLabel()
        self.taskCount.setText(f"- - - {self.countTasks()} Tasks - - -")
        self.taskCount.setFont(QFont(FONT_NAME, 14, 400))
        
        self.deleteBTN = QPushButton("Delete")
        self.deleteBTN.setObjectName("ListDeleteButton")
        self.deleteBTN.setFont(QFont(FONT_NAME, 14, 500))
        self.deleteBTN.pressed.connect(self.deleteList)
        
        export_icon = QIcon()
        export_icon.addFile("_internal/resources/export_icon.png")
        self.export_btn = QPushButton("Export")
        self.export_btn.pressed.connect(self.exportList)
        self.export_btn.setFont(QFont(FONT_NAME, 14, 500))
        self.export_btn.setObjectName("ListExportButton")
        self.export_btn.setIcon(export_icon)
        
        self.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.addStretch()
        self.addWidget(self.taskCount, alignment=Qt.AlignmentFlag.AlignCenter)
        self.addStretch()
        self.addWidget(self.export_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.deleteBTN, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.setObjectName("TDL")
        
        
    
    
    def countTasks(self):
        count = 0
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        
        cursor.execute(f"""
        --sql
        SELECT * FROM {self.title}
        ;
        """)
        
        count = len(cursor.fetchall())
          
        conn.commit()
        conn.close()
                
        return count
    
    
    def deleteList(self):
        dialog = DeleteListDialog(self.p, self, self.frame)
        dialog.show()
        dialog.exec()
    
    def openList(self):
        
        self.list_window = ListWindow(self.title, self.frame)
        self.list_window.show()
    
    def exportList(self):
            if not os.path.exists("exports"):
                os.mkdir("exports")
                
            list_db = sqlite3.connect(f"exports/{self.title}.db")
            list_cursor = list_db.cursor()
            isNotExported = True
            
            
            
            list_cursor.execute(f"""
            --sql
             SELECT name FROM sqlite_master WHERE TYPE='table'
            ;
            """)

            for table in list_cursor.fetchall():
                if table:
                    print(table)
                    if table[0] == self.title:
                        isNotExported = False
                        warning_dialog = ExportDialog(self.p, "This List Has Already Been Exported", True)
                        warning_dialog.show()
                        warning_dialog.exec()
                        
            
            if isNotExported:      
            
                list_cursor.execute(f"""
                --sql
                ATTACH DATABASE "{DB}" as 'Y'
                ;
                """)    
                
                list_cursor.execute(f"""
                --sql
                CREATE TABLE IF NOT EXISTS {self.title} (
                    task_id INTEGER PRIMARY KEY NOT NULL,
                    task_text TEXT NOT NULL,
                    checked BOOLEAN NOT NULL 
                ) 
                ;
                """)
                
                list_cursor.execute(f"""
                --sql
                INSERT INTO {self.title} SELECT * FROM Y.{self.title}
                ;
                """)
                
                
                list_cursor.execute(f"""
                --sql
                SELECT * FROM {self.title}
                ;
                """)
                
                dialog = ExportDialog(self.p, "The List Has Been Exported Successfully!")
                dialog.show()
                dialog.exec()

                
            list_db.commit()
            list_db.close()
    

class ExportDialog(QDialog):
    
    def __init__(self, parent: QWidget, text: str , isWarning :bool = False) -> None:
        super().__init__(parent)
        
        buttons = (QDialogButtonBox.StandardButton.Ok)
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.setObjectName("DialogButton")
        self.buttonBox.accepted.connect(self.accept)
        
        self.text = QLabel(text)
        self.text.setFont(QFont(FONT_NAME, 14, 400))
        if isWarning:
            self.text.setObjectName("WarningText")
        else:
            self.text.setObjectName("ReqularText")
        
        self.mainframe = QVBoxLayout()
        self.mainframe.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainframe.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.mainframe)
    

  

class DeleteListDialog(QDialog):
    def __init__(self, parent: QWidget | None, tdlist: TDList, listframe: ListFrame):
        super().__init__(parent)
        self.mainframe = QVBoxLayout()
        
        self.tdl = tdlist
        self.frame = listframe
        
        self.text = QLabel("are you sure you want to delete this list?")
        self.text.setFont(QFont(FONT_NAME, 14, 400))
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
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        
        cursor.execute(f"""
        DROP TABLE IF EXISTS {self.tdl.title} 
        ;
        """)
        conn.commit()
        conn.close()
        self.frame.refresh()
        self.close()

class CreatNewListDialog(QDialog):
    def __init__(self, parent: QWidget, frame:ListFrame):
        super().__init__(parent)
        
        self.setWindowTitle("Creat a New List")
        
        
        self.mainframe = QVBoxLayout()
        #line input for name
        self.inputBox = QLineEdit(self)
        self.inputBox.setFont(QFont(FONT_NAME, 15, 400))
        self.inputBox.setPlaceholderText("List Name")
        
        #button box
        buttons = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.setObjectName("DialogButton")
        
        self.frame = frame
        
        self.warning = QLabel("The Entered Filename is Invalid, Make Sure to not use any of the following characters \n [  / ? : ; \\ \"  * | > <  ]")
        self.warning.setObjectName("InvalidWarning")
        self.warning.setFont(QFont(FONT_NAME, 11, 500))
        self.warning.setWordWrap(True)
        
        self.buttonBox.accepted.connect(self.createNew)
        self.buttonBox.rejected.connect(self.reject)
        self.inputBox.returnPressed.connect(self.createNew)
        
        self.mainframe.addWidget(self.inputBox, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainframe.addWidget(self.warning, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainframe.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.warning.hide()
        self.setLayout(self.mainframe)
        #creat txt file
    
    def createNew(self):
        
        
        
        invalid_list = str("/?:;\\\" *|>< ")
        
        is_valid = True
        
        for char in invalid_list:
            if char in self.inputBox.text():
                is_valid = False
                break
            
        
        if is_valid:
            self.warning.hide()
            conn = sqlite3.connect(DB)
                            
            cursor = conn.cursor()

            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.inputBox.text()} (
                task_id INTEGER PRIMARY KEY NOT NULL,
                task_text TEXT NOT NULL,
                checked BOOLEAN NOT NULL 
            )
            ;
            """)
            
            conn.commit()
            conn.close()
            self.frame.refresh()
            
            self.close()
        
        else:
            print("invalid filename")
            self.warning.show()
            return

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
        
        conn = sqlite3.connect(DB)
                
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT name FROM sqlite_master WHERE TYPE= 'table'
        ;
        """)
        
        conn.commit()
        
        self.lists = [list[0] for list in cursor.fetchall()]
        self.lists.reverse()
        
        
        for list in self.lists:
            
            tdl = TDList(list, parent, self)
            self.addLayout(tdl)
        
        conn.close()
        self.setSpacing(0)
    
    def refresh(self):
        
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        
        
        listCount = self.count()
        lists = []
        for index in range(0, listCount):
            l = self.itemAt(index)
            lists.append(l)
        
        for list in lists:
            for i in range(0, list.count()): # type: ignore 
                childWidget = list.itemAt(i).widget()# type: ignore
                if childWidget != None:
                    childWidget.deleteLater() # type: ignore
            sip.delete(list) # type: ignore

        
        cursor.execute("""
        --sql
        SELECT name FROM sqlite_master WHERE TYPE= 'table'
        ;
        """)
        
        
        self.lists = [list[0] for list in cursor.fetchall()]
        self.lists.reverse()
        
        conn.commit()
        conn.close()
        
        for list in self.lists:
            tdl = TDList(list, self.p, self)
            self.addLayout(tdl)

class ListWindow(QMainWindow):
    
    def __init__(self, title: str, frame:ListFrame):
        super().__init__()

        self.resize(600, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle(title)
        
        self.setObjectName("ListWindow")
        
        self.name = title
        self.frame = frame
        
        
        self.scrollarea = QScrollArea()
        
        self.widget = QWidget()
        
        
        if title is not None:
            self.title = Heading(title)
            self.title.setFont(self.title.getBigFont())
        
        self.taskbox = QVBoxLayout()
        self.task_input = TaskInput()
        self.mixButton = TDButton("mix")
        self.titleBar = TitleBar(self)
        self.titleBar.maximize_btn.setEnabled(True)
        self.titleBar.maximize_btn.setStyleSheet("""
            #Disabledutton{
                background-color: #383838; 
                border: 0.3px solid mintcream;
                border-radius: 0.4em;
                icon-size: 1.8em;
            }
            #DisabledButton:hover{
                background-color: #454545;
            }
                                                 """)
        
        
        self.taskbox.setObjectName("TaskBox")
        
        self.mixButton.pressed.connect(self.mixTasks)
        self.task_input.add_btn.pressed.connect(self.addTask)
        self.task_input.returnPressed.connect(self.addTask)
        
        self.task_input.taskInputFrame.addWidget(self.mixButton, alignment= Qt.AlignmentFlag.AlignCenter)
        self.task_input.taskInputFrame.addStretch()
        
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
                
        cursor.execute(f"""
        SELECT * from {title}
        ;
        """) 
        
        conn.commit()
        tasklist = cursor.fetchall() 
        conn.close()
        
              
        for task in tasklist:
            self.taskbox.addLayout(Task(task[1], title, task[2], self.frame))         
  
  

        
  
        
        mainframe = QVBoxLayout()
        mainframe.addWidget(self.titleBar)
        mainframe.addStretch()
        mainframe.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        mainframe.addLayout(self.task_input.taskInputFrame)
        mainframe.addLayout(self.taskbox)
        mainframe.addStretch()
        mainframe.setSpacing(20)
        self.taskbox.setSpacing(20)
        
        self.widget.setLayout(mainframe)
        
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.widget)
        self.scrollarea.setObjectName("Container")
        
        self.setCentralWidget(self.scrollarea)
        
        
    def addTask(self):
        if not self.task_input.text() == "" and not self.task_input.text() == " ":
            task = Task(self.task_input.text(), self.name, False, self.frame)
            self.taskbox.addLayout(task)
            
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()

            cursor.execute(f"""
            INSERT INTO {self.name} ( task_text, checked ) VALUES (:text, FALSE)
            ;
            """, {"text":self.task_input.text()})
            
            conn.commit()
            conn.close()
            self.task_input.clear()
            taskcount = self.frame.children()[0].itemAt(2).widget() #type: ignore
            newCount = int(taskcount.text().split(" ")[3]) + 1
            taskcount.setText(f"- - - {newCount} Tasks - - -")
            
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
        self.taskInputFrame.addStretch()
        self.taskInputFrame.addWidget(self, alignment=Qt.AlignmentFlag.AlignCenter)
        self.taskInputFrame.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignCenter)



class Task(QHBoxLayout):
    
    
    def __init__(self, text: str, title: str, checked: bool, frame: ListFrame):
        super().__init__()
        
        self.text = QLabel(text)
        self.checkbox = QCheckBox()
        self.delete_btn = QPushButton()
        self.list_title = title
        self.frame = frame
        

        self.titleSizeAnimation = QVariantAnimation(self.text)
        self.titleColorAnimation = QVariantAnimation(self.text)
        
        
        
        self.checked = checked
        
        self.checkbox.setFont(QFont(FONT_NAME, 15, 500))
        self.checkbox.checkStateChanged.connect(self.checkTask)
        self.checkbox.setChecked(self.checked)

        self.text.setFont(self.getBigFont())
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.checkTask()
        
        minus_icon = QIcon()
        minus_icon.addFile("_internal/resources/minus_icon.png")
        self.delete_btn.setIcon(minus_icon)
        self.delete_btn.pressed.connect(self.deleteTask)
        self.delete_btn.setObjectName("TaskDeleteButton")
        
        #animation

        self.titleSizeAnimation.setEasingCurve(QEasingCurve().Type.OutBounce)
        self.titleSizeAnimation.setDuration(250)
        self.titleSizeAnimation.setKeyValueAt(0, self.getBigFont().pointSize())
        self.titleSizeAnimation.setKeyValueAt(0.5, 24)
        self.titleSizeAnimation.setKeyValueAt(1, self.getBigFont().pointSize())
        self.titleSizeAnimation.valueChanged.connect(self.updateTitleFontSize)
        

        self.titleColorAnimation.setEasingCurve(QEasingCurve.Type.BezierSpline)
        self.titleColorAnimation.setDuration(300)
        self.titleColorAnimation.setStartValue(QColor(245, 255, 250, 255))
        self.titleColorAnimation.setEndValue(QColor(144, 238, 144, 255))
        self.titleColorAnimation.valueChanged.connect(self.updateTitleColor)
        
        
        
        self.addStretch()
        self.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignRight)
        self.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.delete_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.addStretch()
        
    
    def updateTitleFontSize(self, value):
        self.text.setFont(QFont(FONT_NAME, value, 600))
    
    def updateTitleColor(self, color: QColor):
        self.text.setStyleSheet(f"color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});")
        
    
        
    def checkTask(self):
        if self.checkbox.isChecked():
            self.titleColorAnimation.setDirection(self.titleColorAnimation.Direction.Forward)
            if self.titleSizeAnimation.state() == QVariantAnimation.State.Stopped:
                self.titleSizeAnimation.start()
                
            if self.titleColorAnimation.state() == QVariantAnimation.State.Stopped:
                self.titleColorAnimation.start()
            
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            
            cursor.execute(F"""
            --sql
            UPDATE {self.list_title}
            SET checked = TRUE 
            WHERE task_text = :tasktext
            ;
            """, {"tasktext": self.text.text()})
            
            conn.commit()
            conn.close()
        else:
            self.titleColorAnimation.setDirection(self.titleColorAnimation.Direction.Backward)
            if self.titleSizeAnimation.state() == QVariantAnimation.State.Stopped:
                self.titleSizeAnimation.start()
                
            if self.titleColorAnimation.state() == QVariantAnimation.State.Stopped:
                self.titleColorAnimation.start()
            
            self.checked = False
            
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            
            cursor.execute(F"""
            --sql
            UPDATE {self.list_title}
            SET checked = FALSE 
            WHERE task_text = :tasktext
            ;
            """, {"tasktext": self.text.text()})
            
            conn.commit()
            conn.close()
            
            
    
    def deleteTask(self):
        
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        
        cursor.execute(f"""
        DELETE FROM {self.list_title} WHERE task_text= :text
        ;
        """, {"text": self.text.text()})
                  
        conn.commit()
        conn.close()
        
        self.text.deleteLater()
        self.checkbox.deleteLater()
        self.delete_btn.deleteLater()
        sip.delete(self)
        
        taskcount = self.frame.children()[0].itemAt(2).widget() #type: ignore
        newCount = int(taskcount.text().split(" ")[3]) - 1
        taskcount.setText(f"- - - {newCount} Tasks - - -")
    
    
    
    def getGrayFont(self):
        font = QFont(FONT_NAME)
        font.setPointSize(20)
        font.setWeight(300)
        font.setStrikeOut(True)
        self.text.setObjectName("Checked")
        self.text.setStyleSheet("""
            #Checked{
                color: lightgreen;
            }
                                """)
        return font
    
    def getBigFont(self):
        font = QFont(FONT_NAME)
        font.setPointSize(20)
        font.setWeight(600)
        self.text.setObjectName("Unchecked")
        self.text.setStyleSheet("""
            #Unchecked{
                color: mintcream;
            }
                                """)
        return font
    

class TitleBar(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.setAutoFillBackground(True)
        self.initialPos = None
        barLayout = QHBoxLayout()
        barLayout.setSpacing(2)
        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if title := parent.windowTitle():
            self.title.setText(title)
        self.title.setFont(QFont(FONT_NAME, 12, 500))
        
        self.wicon = QLabel()
        self.wiconPM = QPixmap("_internal/resources/UTDL24.png")
        self.wicon.setPixmap(self.wiconPM.scaled(20, 20))
        barLayout.addWidget(self.wicon, alignment=Qt.AlignmentFlag.AlignLeft)
        barLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
        
        
        self.minimize_btn = QToolButton(self)
        min_icon = QIcon("_internal/resources/minus_icon.png") #type: ignore
        self.minimize_btn.setIcon(min_icon)
        self.minimize_btn.clicked.connect(self.window().showMinimized) #type: ignore
        
        self.maximize_btn = QToolButton(self)
        max_icon = QIcon("_internal/resources/max_icon.png") #type: ignore
        self.maximize_btn.setIcon(max_icon)
        self.maximize_btn.clicked.connect(self.window().showMaximized) #type: ignore
        self.maximize_btn.setEnabled(False)
        
        self.close_btn = QToolButton(self)
        close_icon = QIcon("_internal/resources/close_icon.png") #type: ignore
        self.close_btn.setIcon(close_icon)
        self.close_btn.clicked.connect(self.window().close) #type: ignore
        
        self.normal_btn = QToolButton(self)
        normal_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton) #type: ignore
        self.normal_btn.setIcon(normal_icon)
        self.normal_btn.clicked.connect(self.window().showNormal) #type: ignore
        self.normal_btn.setVisible(False)
        
        buttons = [
            self.minimize_btn,
            self.normal_btn,
            self.maximize_btn,
            self.close_btn
        ]
        
        barLayout.addStretch()
        barLayout.addStretch()
        for btn in buttons:
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            if btn.isEnabled():
                btn.setObjectName("ToolButton")
            else:
                btn.setObjectName("DisabledToolButton")
            barLayout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        barLayout.setContentsMargins(0,0,0,0)
        
    
        
        self.setLayout(barLayout)
    
    def windowStateChanged(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_btn.setVisible(True)
            self.maximize_btn.setVisible(False)
        else:
            self.normal_btn.setVisible(False)
            self.maximize_btn.setVisible(True)
    
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == Qt.MouseButton.LeftButton: #type: ignore
            self.initialPos = a0.position().toPoint() #type: ignore    
        super().mousePressEvent(a0)
        a0.accept()  #type: ignore  
    
    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if self.initialPos is not None:
            delta = a0.position().toPoint() - self.initialPos  #type: ignore   
            self.window().move(          #type: ignore   
                self.window().x() + delta.x(),   #type: ignore   
                self.window().y() + delta.y()        #type: ignore   
            )
        super().mouseMoveEvent(a0) 
        a0.accept()      #type: ignore   
        
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        self.initialPos = None
        super().mouseReleaseEvent(a0)
        a0.accept()          #type: ignore   


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setObjectName("MainWindow")
        self.setWindowTitle("UTDL")
        self.resize(600, 400)
        self.setMaximumSize(600, 400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        
        self.listbox = ListFrame(self)
        
        self.new_btn = TDButton("new")  
        file_icon = QIcon()
        file_icon.addFile("_internal/resources/file_icon.png")
        self.new_btn.setIcon(file_icon)
        self.new_btn.setObjectName("MenuButton")

        
        self.new_btn.pressed.connect(self.creatList)

        self.mainframe = QVBoxLayout()
        self.listContainer = QVBoxLayout()
        self.mainHeader = QHBoxLayout()
        
        self.scrollbox = QScrollArea()
        self.scrollwidget = QWidget()
        
        refresh_icon = QIcon()
        refresh_icon.addFile("_internal/resources/refresh_icon.png")
        self.refreshButton = TDButton("refresh")
        self.refreshButton.setFont(QFont(FONT_NAME, 16, 400))
        self.refreshButton.setObjectName("RefreshButton")
        self.refreshButton.setIcon(refresh_icon)
        self.refreshButton.pressed.connect(self.listbox.refresh)
        
        import_icon = QIcon()
        import_icon.addFile("_internal/resources/import_icon.png")
        self.import_btn = TDButton("import")
        self.import_btn.pressed.connect(self.importList)
        self.import_btn.setObjectName("MenuButton")
        self.import_btn.setFont(QFont(FONT_NAME, 16, 400))
        self.import_btn.setIcon(import_icon)
        
        self.mainHeader.addWidget(self.new_btn, alignment= Qt.AlignmentFlag.AlignLeft)
        self.mainHeader.addStretch()
        self.mainHeader.addWidget(self.import_btn, alignment=Qt.AlignmentFlag.AlignRight)
        self.mainHeader.addWidget(self.refreshButton, alignment= Qt.AlignmentFlag.AlignRight)
        
        
        self.scrollwidget.setLayout(self.listbox)
        self.scrollbox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollbox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollbox.setWidgetResizable(True)
        self.scrollbox.setWidget(self.scrollwidget)
        
        self.scrollbox.setMinimumWidth(self.width())
        self.scrollbox.setMinimumHeight(self.height() - 200)
        self.listbox.setSpacing(10)
        
        self.listContainer.addStretch()
        self.listContainer.addLayout(self.mainHeader)
        self.listContainer.addWidget(self.scrollbox, alignment=Qt.AlignmentFlag.AlignCenter, stretch=0)
        self.listContainer.addStretch()
        
        self.icon = QIcon("_internal/resources/UTDL100.png")
        self.bannerPM = QPixmap("_internal/resources/UTDL100.png")
        self.banner = QLabel(self)
        
        self.banner.setPixmap(self.bannerPM)
        

        
        self.title = QLabel("Ultimate To-Do-List")
        self.title.setFont(QFont(FONT_NAME, 30, 800))
        
        self.title.setObjectName("MainTitle")
        self.banner.setObjectName("Banner")
        
        
        self.titleBox = QHBoxLayout()
        self.titleBox.addStretch()
        self.titleBox.addWidget(self.banner)
        self.titleBox.addWidget(self.title)
        self.titleBox.addStretch()
        
        self.titleBar = TitleBar(self)
        
        
        
        
        self.mainframe.addWidget(self.titleBar)
        self.mainframe.addStretch()
        self.mainframe.addLayout(self.titleBox)
        self.mainframe.addStretch()
        #self.mainframe.addLayout(self.menu)
        self.mainframe.addLayout(self.listContainer)
        
        self.cWidget = QWidget()
        self.cWidget.setObjectName("Container")
        
        self.cWidget.setLayout(self.mainframe)
        
        self.setWindowIcon(self.icon)
        
        self.setCentralWidget(self.cWidget)

    
    
    def changeEvent(self, a0: QEvent | None) -> None:
        if a0.type() == QEvent.Type.WindowStateChange: #type: ignore
            self.titleBar.windowStateChanged(self.windowState())
        super().changeEvent(a0)
        a0.accept() #type: ignore
    
    def creatList(self):
        self.dialog_CNL = CreatNewListDialog(self, self.listbox)
        self.dialog_CNL.show()
        self.dialog_CNL.exec()
    
    def importList(self):
        
        newDB, ok = QFileDialog.getOpenFileName(
            self, 
            "Select a File",
            "",
            "Lists (*db)"
        )
        
        if newDB:
            newList = newDB.split("/")[-1].removesuffix(".db")
            conn = sqlite3.connect(DB)
            db_cursor = conn.cursor()
            isNotImported = True
            
            db_cursor.execute(f"""
            --sql
             SELECT name FROM sqlite_master WHERE TYPE='table'
            ;
            """)

            for table in db_cursor.fetchall():
                if table:
                    if table[0] == newList:
                        isNotImported = False
                        dialog = ExportDialog(self, "This List Has Already Been Imported Before", True)
                        dialog.show()
                        dialog.exec()
            
            
            if isNotImported:
                db_cursor.execute(f"""
                --sql
                ATTACH DATABASE "{newDB}" AS IMP
                ;
                """)
                
                db_cursor.execute(f"""
                --sql
                CREATE TABLE IF NOT EXISTS {newList} (
                    task_id INTEGER PRIMARY KEY NOT NULL,
                    task_text TEXT NOT NULL,
                    checked BOOLEAN NOT NULL 
                )
                ;
                """)
                
                db_cursor.execute(f"""
                --sql
                INSERT INTO {newList} SELECT * FROM IMP.{newList}
                ;
                """)
                
                dialog_S = ExportDialog(self, "List Imported Successfully!")
                dialog_S.show()
                dialog_S.exec()

                
            
            conn.commit()
            conn.close()
            
            self.listbox.refresh()     
       
        