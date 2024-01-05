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
import sys
from Algorithm.ceaser_cipher import simpleEcnryption, SimpleDecription


class EncryptoWindow(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)

    def init_ui(self,Email):
        self.setFixedSize(700, 700)
        self.setWindowTitle("CryptoFort | Encyrpto")
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


        InputBox = QTextEdit()
        InputBox.setPlaceholderText("Enter Your Data Here")
        InputBox.setFixedHeight(250)

        OutputBox = QTextEdit()
        OutputBox.setReadOnly(True)
        OutputBox.setPlaceholderText("Output")
        OutputBox.setFixedHeight(250)
        
        
        ButtonLayout = QHBoxLayout()

        Encrypt = QPushButton("Encrypt")
        Encrypt.setFixedSize(50,50)
        Decrypt = QPushButton("Decrypt")
        Decrypt.setFixedSize(50,50)

        ButtonLayout.addWidget(Encrypt)
        ButtonLayout.addWidget(Decrypt)

        layout.addWidget(InputBox)
        layout.addLayout(ButtonLayout)
        layout.addWidget(OutputBox)

        Encrypt.clicked.connect(lambda: self.EncryptText(InputBox.toPlainText(), OutputBox))
        Decrypt.clicked.connect(lambda: self.DecryptText(InputBox.toPlainText(), OutputBox) )

        
        

        self.show()

    def EncryptText(self, TextToEncrypt, OutputBox : QTextEdit):
        EncryptedText = simpleEcnryption(TextToEncrypt)
        OutputBox.setText(EncryptedText)

    def DecryptText(self, TextToDecrypt, OutputBox: QTextEdit):
        DecryptedText = SimpleDecription(TextToDecrypt)
        OutputBox.setText(DecryptedText)
        

