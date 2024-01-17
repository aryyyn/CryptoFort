import requests
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QHBoxLayout,QDialog,QDialogButtonBox,QVBoxLayout,QLabel,QInputDialog,QPushButton
from PyQt6.QtCore import Qt
import time
import pymongo
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption
import sys, random
from handler.send_email import email_verification
from dotenv import load_dotenv
import os,pyotp
load_dotenv()

client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"] 
collection = db["User_Details"]

loginMessage = "InCorrect Password"
VerificationMessage = "Wrong Code"


def loginLogic(eemail, epassword):
    
    email = eemail.text().lower()
    password = epassword.text()



    count = collection.count_documents({"email": email})
   
    if count == 0:
        return "No Email Found"
    else:
        results = collection.find({"email": email})
        for data in results:
            IsVerified = data["is_Verified"]
            DecryptedPassword = data["password"]
            Encryptioncode = data ["Encryption_code"]
            Is2faEnabled = data["is_2fa_enabled"]
            Password = enhancedEncryption(password, Encryptioncode)

            if DecryptedPassword == Password:
                if (IsVerified):
                    if(Is2faEnabled):
                        Verify2fa = QDialog()
                        Verify2fa.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

                           
            Qlabel {
            font-size: 3px
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
                        Verify2fa.setWindowTitle("User Verification")
                        Verify2fa.setBaseSize(300,300)

                        layout = QVBoxLayout(Verify2fa)

                        FooterLayout = QHBoxLayout()
                        HeaderLayout = QHBoxLayout()

                        titleLabel = QLabel("Enter the 2fa code: ")
                        titeltext = QLineEdit()
                        SubmitButton = QPushButton("Submit")

                        HeaderLayout.addWidget(titleLabel)
                        HeaderLayout.addWidget(titeltext)
                        FooterLayout.addWidget(SubmitButton, alignment=Qt.AlignmentFlag.AlignCenter)

                        layout.addLayout(HeaderLayout)
                        layout.addLayout(FooterLayout)
                        SubmitButton.clicked.connect(lambda: authCheck(email,titeltext,Verify2fa))
                        Verify2fa.exec()
                        
                        

                        
                        
                        if (loginMessage == "Correct Password"):
                            return "Correct Password"
                        else:
                            dialog = QInputDialog()
                            dialog.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

                           
            Qlabel {
            font-size: 3px
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
                            QMessageBox.information(dialog, "Wrong Code", "Please Try Again")

                    else:
                        return "Correct Password"

                else:
                    NotVerified = QDialog()
                    NotVerified.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

                           
            Qlabel {
            font-size: 3px
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
            
                    NotVerified.setWindowTitle("Verify Your Email")
                    NotVerified.setBaseSize(300,300)

                    layout = QVBoxLayout(NotVerified)

                    HeaderLayout = QVBoxLayout()
                    FooterLayout = QVBoxLayout()

                    EnterCodeLabel = QLabel("Enter the code that was sent to your email: ")
                    EnterCode = QLineEdit()

                    HeaderLayout.addWidget(EnterCodeLabel)
                    HeaderLayout.addWidget(EnterCode)

                    CodeSubmit = QPushButton("Submit")
                    CodeSubmit.setBaseSize(50,25)

                    ResendCode = QPushButton("Resend Code")
                    ResendCode.setBaseSize(50,25)

                    FooterLayout.addWidget(CodeSubmit, alignment=Qt.AlignmentFlag.AlignCenter)
                    FooterLayout.addWidget(ResendCode, alignment=Qt.AlignmentFlag.AlignCenter)

                    layout.addLayout(HeaderLayout)
                    layout.addLayout(FooterLayout)

                    CodeSubmit.clicked.connect(lambda: codeCheck(email, EnterCode,NotVerified))
                    ResendCode.clicked.connect(lambda: resendCode(email))
                    NotVerified.exec()

                    if VerificationMessage == "Correct Password":
                        return "Correct Password"
                    else:
                        return "Error"

            else:
                
                return "InCorrect Password"
            
                

                
def authCheck(email, InputCode,Verify2fa: QDialog):
    global loginMessage
    results = collection.find({"email": email})
    for data in results:
        backupcode = data["2fa_backupcode"]
    key = os.environ.get("SECRET_CODE_2FA")
    topt = pyotp.TOTP(key)
    RealCode = topt.now()
    InputCode = InputCode.text()
    if(str(InputCode) == str(RealCode) or str(InputCode) == str(backupcode)):
        loginMessage = "Correct Password"
        Verify2fa.accept()
    else:
        loginMessage = "ReCheck Code"
        Verify2fa.accept()
    pass
    # QMessageBox.information("Verification Success", "Code Verified Successfully!\nPlease ReLogin")

def codeCheck(email, InputCode,NotVerified: QDialog):
    try:
        results = collection.find({"email": email})
        global VerificationMessage
        for data in results:
            Code = data["Verification_code"]
            if (int(InputCode.text()) == int(Code)):
                dialog = QInputDialog()
                QMessageBox.information(dialog, "Verification Success", "Account Verified Successfully!")
                collection.update_one({"email": email},{"$set": {"is_Verified": "True"}})
                VerificationMessage = "Correct Password"
                NotVerified.accept()

                
            else:
                dialog = QInputDialog()
                dialog.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

                           
            Qlabel {
            font-size: 3px
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
                QMessageBox.information(dialog, "Error", "Wrong Code")
            
    except Exception as err:
        dialog = QInputDialog()
        dialog.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

                           
            Qlabel {
            font-size: 3px
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
        QMessageBox.information(dialog, "Error", "There Has Been An Error While Processing Your Request\nPlease Try Again")
            

def resendCode(email):
    try:
        random_number = random.randint(000000, 999999)
        results = collection.find({"email": email})
        for data in results:
            collection.update_one({"email": email},{"$set": {"Verification_code": random_number}})
            dialog = QInputDialog()
            dialog.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

                           
            Qlabel {
            font-size: 3px
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
            email_verification(email,random_number)
            QMessageBox.information(dialog, "Code Reset Successful", "Please Check Your Email For The New Code")

    except Exception as err:
        dialog = QInputDialog()
        dialog.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

                           
            Qlabel {
            font-size: 3px
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
        QMessageBox.information(dialog, err, "There Has Been An Error While Processing Your Request\nPlease Try Again")



                






       


