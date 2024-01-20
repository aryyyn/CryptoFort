from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDialog,
    QTextEdit,
    QHBoxLayout,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys,pymongo
from datetime import datetime


class AdminWindow(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)

    def init_ui(self,Email):
        
        self.setFixedSize(450, 450)
        self.setWindowTitle("CryptoFort | ADMIN WINDOW")
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

          QTextEdit {
        border: 2px solid #00FF00;
        border-radius: 8px;
        padding: 10px; 
        selection-background-color: #00FF00;
        background-color: #111111;
        color: #00FF00;
        font-size: 14px;
    }
    
    QTextEdit:focus {
        border: 2px solid #00FF00; 
    }

            QPushButton {
                border: 2px solid #00FF00; 
                border-radius: 8px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #111111, stop: 0.5 #222222, stop: 1 #111111);
                min-width: 100px;
                font-size: 12px;
                color: #00FF00; 
            }

            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #222222, stop: 0.5 #111111, stop: 1 #222222);
            }

            QLabel {
                color: #00FF00; 
                font-size: 16px;
                font-weight: bold;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)


        WelcomeLabel = QLabel(f"Welcome, {Email.text()}")
        
        Button1 = QPushButton("View User Info")
        Button1.setFixedSize(75,50)

        Button2 = QPushButton("Modify User Info")
        Button2.setFixedSize(75,50)

        Button3 = QPushButton("View User Logs")
        Button3.setFixedSize(75,50)

        LogoutButton = QPushButton("Exit")
        LogoutButton.setFixedSize(25,25)

        layout.addWidget(WelcomeLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Button1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Button2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Button3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(LogoutButton, alignment=Qt.AlignmentFlag.AlignRight)

        Button1.clicked.connect(lambda: self.showUserInfo())
        Button2.clicked.connect(lambda: self.updateUserInfo())
        Button3.clicked.connect(lambda: self.showUserLogs())
        LogoutButton.clicked.connect(lambda: self.Logout())

        

        self.show()

    def showUserInfo(self):
        print("working1")
    def updateUserInfo(self):
        print("working2")
    def showUserLogs(self):
        print("working3")
    def Logout(self):
        sys.exit()
