from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sys
from handler.joke import joke
from handler.showPassword import togglePassword

app = QApplication(sys.argv)
window = QMainWindow() 

window.setMinimumSize(750, 550)
window.setWindowTitle("CryptoFort | Register")
icon = QIcon("logo/logo.png")
window.setWindowIcon(icon)
window.setStyleSheet("""
                     
    * {
    color: white; 
    background: black; 
}
                     

QLineEdit {
    border: 2px solid #C0C0C0;
    border-radius: 8px;
    padding: 25px;
    selection-background-color: #A9A9A9;
    background-color: black;
    color: white;
    font-size: 14px;
}

QPushButton {
    border: 2px solid #8f8f91;
    border-radius: 8px;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #EEEEEE, stop: 0.5 #DDDDDD, stop: 1 #EEEEEE);
    min-width: 100px;
    font-size: 12px;
    color:black;
                     

   
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 green, stop: 0.5 white, stop: 1 green);
}
                     
                     

QLabel {
    color: white;
    font-size: 16px;
    font-weight: bold;
}

                     
""")




central_widget = QWidget()
window.setCentralWidget(central_widget)

layout = QVBoxLayout(central_widget)
layout.setContentsMargins(100, 100, 100, 100)
layout.setSpacing(5)  

RegisterTitle = QLabel("CryptoFort || Register")
RegisterTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
RegisterTitle.setFont(QFont("Arial", 20)) #changing the font for the title


email_layout = QHBoxLayout()

registeremaillabel = QLabel("Email: ")
registeremail = QLineEdit()

registeremail.setFixedHeight(30)
registeremail.setPlaceholderText("Enter your email")

email_layout.addWidget(registeremaillabel)
email_layout.addWidget(registeremail)

password_layout = QHBoxLayout()
registerpasslabel = QLabel("Password: ")
registerpassword = QLineEdit()
registerpassword.setFixedHeight(30)
registerpassword.setPlaceholderText("Enter your password")
registerpassword.setEchoMode(QLineEdit.EchoMode.Password)
showregisterpassword = QPushButton("SHOW")
showregisterpassword.setFixedSize(50,25)




password_layout.addWidget(registerpasslabel)
password_layout.addWidget(registerpassword)
password_layout.addWidget(showregisterpassword)

repassword_layout = QHBoxLayout()

repasswordlabel = QLabel("Re-Enter Password: ")
repassword = QLineEdit()
repassword.setFixedHeight(30)
repassword.setPlaceholderText("Re-enter your password")
repassword.setEchoMode(QLineEdit.EchoMode.Password)
showconfirmregisterpassword = QPushButton("SHOW")
showconfirmregisterpassword.setFixedSize(50,25)

repassword_layout.addWidget(repasswordlabel)
repassword_layout.addWidget(repassword)
repassword_layout.addWidget(showconfirmregisterpassword)



rrsubmit = QPushButton("Register")
rrsubmit.setFixedSize(100, 50)


layout.addWidget(RegisterTitle)
layout.addLayout(email_layout)
layout.addLayout(password_layout)
layout.addLayout(repassword_layout)
layout.addWidget(rrsubmit, alignment=Qt.AlignmentFlag.AlignCenter)

rrsubmit.clicked.connect(joke)
showregisterpassword.clicked.connect(lambda: togglePassword(registerpassword))
showconfirmregisterpassword.clicked.connect(lambda: togglePassword(repassword))

window.show()
sys.exit(app.exec())
