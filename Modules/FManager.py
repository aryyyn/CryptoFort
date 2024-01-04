from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
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

    def init_ui(self, Email):
        self.setFixedSize(400, 200)
        self.setWindowTitle("CryptoFort | FManager")
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
                font-size: 14px;
            }

            QPushButton {
                border: 2px solid #00FF00; 
                border-radius: 8px;
                background: #111111;
                min-width: 100px;
                color: #00FF00; 
                padding: 8px 16px;
            }

            QPushButton:hover {
                background: #222222;
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

        FileUploadInfoLabel = QLabel("No File Uploaded")

        FileUpload = QPushButton("Upload File")
        FileUpload.clicked.connect(lambda: self.UploadFileHandler(Email))

        FooterButtonLayout = QHBoxLayout()
        GetCurrentFileBtn = QPushButton("Get Current DB File")
        DeleteCurrentFileBtn = QPushButton("Delete Current DB File")

        FooterButtonLayout.addWidget(GetCurrentFileBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        FooterButtonLayout.addWidget(DeleteCurrentFileBtn, alignment=Qt.AlignmentFlag.AlignRight)

        FileUpload.setFixedHeight(40)
        GetCurrentFileBtn.setFixedHeight(40)
        DeleteCurrentFileBtn.setFixedHeight(40)

        layout.addWidget(FileUploadInfoLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(FileUpload, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(FooterButtonLayout)

        self.show()

    def UploadFileHandler(self, Email):
        FileDialog = QFileDialog()
        FileDialog.exec()


