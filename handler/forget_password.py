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
    QInputDialog,
    QMessageBox,
)
from PyQt6.QtGui import QFont,QPainter, QPen,QPixmap,QIcon
from PyQt6.QtCore import Qt
import pymongo,time,sys,random
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption
from handler.showPassword import togglePassword
from handler.send_email import email_verification


class ForgetPassword(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        client = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = client["CryptoFort"] 
        self.collection = db["User_Details"]



    def init_ui(self):
        self.setBaseSize(250, 300)
        self.setWindowTitle("CryptoFort | Password Reset")
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
                font-size: 14px;
            }

            QLabel {
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton {
                border: 2px solid #00FF00; 
                border-radius: 8px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #111111, stop: 0.5 #222222, stop: 1 #111111);
                min-width: 100px;
                font-size: 14px;
                color: #00FF00; 
            }

            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #222222, stop: 0.5 #111111, stop: 1 #222222);
            }
        """)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        HeaderLayout = QHBoxLayout()
        ForgotPasswordLabel = QLabel("Forgot Password?")
        HeaderLayout.addWidget(ForgotPasswordLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        
        email_reset_code = random.randint(000000, 999999)
        EmailLayout = QHBoxLayout()
        EnterEmailLabel = QLabel("Enter Email: ")
        EnterEmailInput = QLineEdit()
        EmailLayout.addWidget(EnterEmailLabel)
        EmailLayout.addWidget(EnterEmailInput)
        
        SendCode = QPushButton("Send Code")
        SendCode.setMaximumSize(25,25)

        CodeLayout = QHBoxLayout()
        EnterCodeLabel = QLabel("Enter Code: ")
        EnterCodeInput = QLineEdit()
        CodeLayout.addWidget(EnterCodeLabel)
        CodeLayout.addWidget(EnterCodeInput)


        PasswordLayout = QHBoxLayout()
        EnterPassowrdLabel = QLabel("Enter New Password: ")
        EnterPasswordInput = QLineEdit()

        icon_path = 'Logo/eye.png'
        hide = QPixmap(icon_path)

        ShowPasswordButton = QPushButton(QIcon(hide),"")
        ShowPasswordButton.setMaximumSize(25,25)

        
        PasswordLayout.addWidget(EnterPassowrdLabel)
        PasswordLayout.addWidget(EnterPasswordInput)
        PasswordLayout.addWidget(ShowPasswordButton, alignment=Qt.AlignmentFlag.AlignCenter)
        EnterPasswordInput.setEchoMode(QLineEdit.EchoMode.Password)
        ShowPasswordButton.clicked.connect(lambda: togglePassword(EnterPasswordInput,ShowPasswordButton))

        SendCode.clicked.connect(lambda: self.sendCode(EnterEmailInput.text(),email_reset_code))

        SubmitButton = QPushButton("Submit")
        SubmitButton.setMaximumSize(25,50)
        SubmitButton.clicked.connect(lambda: self.submitCode(EnterEmailInput.text(), EnterPasswordInput.text(),EnterCodeInput.text() ,email_reset_code))

        layout.addLayout(HeaderLayout)
        layout.addLayout(EmailLayout)
        layout.addWidget(SendCode, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(CodeLayout)
        
        layout.addLayout(PasswordLayout)
        layout.addWidget(SubmitButton, alignment=Qt.AlignmentFlag.AlignCenter)
        


    def sendCode(self, email, email_reset_code):
        count = self.collection.count_documents({"email": email})
        if count == 0:
            dialog = QInputDialog()
            QMessageBox.information(dialog, "Error", "No Email Found!")
        else:
            email_verification(email,email_reset_code)
            dialog = QInputDialog()
            QMessageBox.information(dialog, "Code Reset Successful", "Please Check Your Email For The Code To Reset Your Password")

    
    def submitCode(self, email, password,email_reset_code_input, email_reset_code):
        count = self.collection.count_documents({"email": email})
        if count == 0:
            dialog = QInputDialog()
            QMessageBox.information(dialog, "Error", "No Email Found!")

        else:
            if (int(email_reset_code)!=int(email_reset_code_input)):
                print(email_reset_code)
                print(email_reset_code_input)
                dialog = QInputDialog()
                QMessageBox.information(dialog, "Error", "Codes do not match!\nPlease Try Again.")

            else:
                result = self.collection.find_one({"email": email})  
                Encryptioncode = result.get("Encryption_code")
                encrypted_password = enhancedEncryption(password, Encryptioncode)
                UpdatePassword = self.collection.update_one(
                {"email": email},
                {"$set": {"password": encrypted_password}}
                )
                dialog = QInputDialog()
                QMessageBox.information(dialog, "Success!", "Your Password Has Been Reset!\nPlease Proceed To Login")
                dialog.accept()
                self.hide()





