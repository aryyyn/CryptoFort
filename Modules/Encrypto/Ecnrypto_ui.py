from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDialog,
    QHBoxLayout,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys


class EncryptoWindow(QMainWindow):
    def __init__(self, Email):
        print("Hello, I am working!!")
        super().__init__()
        self.init_ui(Email)

    def init_ui(self,Email):
        self.setFixedSize(1200, 400)
        self.setWindowTitle("CryptoFort | Encyrpto")
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

            QLineEdit {
                border: 2px solid #00FF00; 
                border-radius: 8px;
                padding: 25px;
                selection-background-color: #00FF00; 
                background-color: #111111; 
                color: #00FF00; 
                font-size: 14px;
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


        InputBox = QLineEdit()
        InputBox.setPlaceholderText("Enter Your Data Here")
       

        OutputBox = QLineEdit()
        

        ButtonLayout = QHBoxLayout()
        Encrypt = QPushButton("Encrypt")
        Decrypt = QPushButton("Decrypt")

        ButtonLayout.addWidget(Encrypt)
        ButtonLayout.addWidget(Decrypt)

        layout.addWidget(InputBox)
        layout.addWidget(Encrypt)
        layout.addLayout(ButtonLayout)
        layout.addWidget(OutputBox)
        self.show()

