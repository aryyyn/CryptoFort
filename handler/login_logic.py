import requests
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog,QDialogButtonBox,QVBoxLayout,QLabel,QInputDialog,QPushButton
from PyQt6.QtCore import Qt
import time
import pymongo
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption

def loginLogic(eemail, epassword):
    email = eemail.text().lower()
    password = epassword.text()

    client = pymongo.MongoClient("mongodb://localhost:27017/")  
    db = client["CryptoFort"] 
    collection = db["User_Details"]

    count = collection.count_documents({"email": email})

    if count == 0:
        NoEmailFound = QMessageBox()
        NoEmailFound.setWindowTitle("Error!")
        NoEmailFound.setText("Email Has Not Been Registered.")
        button = NoEmailFound.exec()
        return "No Email Found"
    else:
        results = collection.find({"email": email})
        for data in results:
            IsVerified = data["is_Verified"]
            if (IsVerified == "True"):
                DecryptedPassword = data["password"]
                Encryptioncode = data ["Encryption_code"]
                Password = enhancedEncryption(password, Encryptioncode)
                
                if DecryptedPassword == Password:
                    return "Correct Password"
                else:
                    return "InCorrect Password"
            else:
                NotVerified = QDialog()
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

                CodeSubmit.clicked.connect(codeCheck(email, CodeSubmit.text()))
                NotVerified.exec()

                #NotVerified = QInputDialog()
                #NotVerified.setWindowTitle("Test")
                #text, ok = QInputDialog.getText(None, "Verify Email", "Enter the code that was sent to your email:")
                #if ok:
                   # print(text)
               # NotVerified.exec()
def codeCheck(email, InputCode):
    client = pymongo.MongoClient("mongodb://localhost:27017/")  
    db = client["CryptoFort"] 
    collection = db["User_Details"]

    results = collection.find({"email": email})

    for data in results:
        Code = data["Verification_code"]
        if (InputCode == Code):
            return "Correct Password"


                






       


