from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox,QLabel
from PyQt6.QtGui import QIcon  #will be able to read image files
from PyQt6.QtCore import Qt
from handler.joke import joke


app = QApplication([])
window = QMainWindow() 

window.setMinimumSize(750,550)
window.setWindowTitle("CryptoFort | Register")
icon = QIcon("logo/logo.png")
window.setWindowIcon(icon) #settings the minimum width and height

#adding widgets
central_widget = QWidget()
window.setCentralWidget(central_widget)

layout = QVBoxLayout()
central_widget.setLayout(layout)


label = QLabel("The Register page", alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(label)

rsubmit = QPushButton("Register")
rsubmit.setFixedSize(50,50)
layout.addWidget(rsubmit)

rsubmit.clicked.connect(joke)



window.show() #for the window to be shown
app.exec()