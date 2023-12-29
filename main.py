from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys

app = QApplication(sys.argv)
window = QMainWindow() 

window.setMinimumSize(750, 550)
window.setWindowTitle("CryptoFort | Register")
icon = QIcon("logo/logo.png")
window.setWindowIcon(icon)
window.setStyleSheet("background-color: white;")

central_widget = QWidget()
window.setCentralWidget(central_widget)

layout = QVBoxLayout(central_widget)
layout.setContentsMargins(100, 100, 100, 100)
layout.setSpacing(5)  # Adjust the spacing between widgets

RegisterTitle = QLabel("CryptoFort || Register")
registeremaillabel = QLabel("Email: ")
registerpasslabel = QLabel("Password: ")

rsubmit = QPushButton("Joke")
rsubmit.setFixedSize(100, 50)

rrsubmit = QPushButton("Register")
rrsubmit.setFixedSize(100, 50)

registeremail = QLineEdit()
registeremail.setFixedSize(300, 20)
registeremail.setEchoMode(QLineEdit.EchoMode.Normal)

registerpassword = QLineEdit()
registerpassword.setFixedSize(300, 20)
registerpassword.setEchoMode(QLineEdit.EchoMode.Password)

email_layout = QHBoxLayout()
email_layout.addWidget(registeremaillabel)
email_layout.addWidget(registeremail)

layout.addWidget(RegisterTitle, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addLayout(email_layout)
layout.addWidget(registerpasslabel, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(registerpassword, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(rrsubmit, alignment=Qt.AlignmentFlag.AlignCenter)

window.show()
sys.exit(app.exec())
