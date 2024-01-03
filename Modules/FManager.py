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
    QFileDialog
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys


class FManagerWindow(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)

    def init_ui(self,Email):
        self.setFixedSize(300, 150)
        self.setWindowTitle("CryptoFort | FManager")
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
        
        FileUploadInfoLabel = QLabel()
        FileUploadInfoLabel.setText("No File Uploaded")

        FileUpload = QPushButton("Upload File")
        FileUpload.setFixedSize(50,50)
        FileUpload.clicked.connect(lambda: self.UploadFileHandler(Email))

        FooterButtonLayout = QHBoxLayout()
        GetCurrentFileBtn = QPushButton("Get Current DB File")
        DeleteCurrentFileBtn = QPushButton("Delete Current DB File")


        # Setting fixed sizes for buttons
        FileUpload.setFixedSize(120, 40)
        GetCurrentFileBtn.setFixedSize(120, 40)
        DeleteCurrentFileBtn.setFixedSize(120, 40)

        FooterButtonLayout.addWidget(GetCurrentFileBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        FooterButtonLayout.addWidget(DeleteCurrentFileBtn, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(FileUploadInfoLabel,alignment=Qt.AlignmentFlag.AlignCenter )
        layout.addWidget(FileUpload, alignment=Qt.AlignmentFlag.AlignCenter )
        layout.addLayout(FooterButtonLayout)
        self.show()

    def UploadFileHandler(self,Email):
        File = QFileDialog()
        File.exec()


