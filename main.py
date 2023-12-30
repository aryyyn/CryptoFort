from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sys
from handler.joke import joke
from handler.showPassword import togglePassword

app = QApplication(sys.argv)
window = QMainWindow() 

window.setFixedSize(750, 550)
window.setWindowTitle("CryptoFort | Register")
icon = QIcon("logo/logo.png")
window.setWindowIcon(icon)
window.setStyleSheet("""
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
    border: 2px solid #00FF00; /* Neon green border */
    border-radius: 8px;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #111111, stop: 0.5 #222222, stop: 1 #111111);
    min-width: 100px;
    font-size: 12px;
    color: #00FF00; /* Neon green text color */
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
window.setCentralWidget(central_widget)

layout = QVBoxLayout(central_widget)
layout.setContentsMargins(100, 100, 100, 100)
layout.setSpacing(5)  

RegisterTitle = QLabel("CryptoFort || Register")
RegisterTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)



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


promptlogin_layout = QHBoxLayout()

promptlogin = QLabel("Already have an account? ")
promptlogin.setAlignment(Qt.AlignmentFlag.AlignRight)


promptloginbtn = QPushButton("Login")
promptloginbtn.setFixedSize(50, 25)

promptlogin_layout.addWidget(promptlogin)
promptlogin_layout.addSpacing(2)  # Adjust the horizontal spacing here
promptlogin_layout.addWidget(promptloginbtn, alignment=Qt.AlignmentFlag.AlignLeft)



rrsubmit = QPushButton("Register")
rrsubmit.setFixedSize(70, 50)


layout.addWidget(RegisterTitle)
layout.addLayout(email_layout)
layout.addLayout(password_layout)
layout.addLayout(repassword_layout)
layout.addWidget(rrsubmit, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addLayout(promptlogin_layout)

rrsubmit.clicked.connect(joke)
showregisterpassword.clicked.connect(lambda: togglePassword(registerpassword))
showconfirmregisterpassword.clicked.connect(lambda: togglePassword(repassword))
promptloginbtn.clicked.connect(joke)

window.show()
sys.exit(app.exec())
