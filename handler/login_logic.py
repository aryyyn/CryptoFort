import requests
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog,QDialogButtonBox,QVBoxLayout,QLabel,QInputDialog,QPushButton
from PyQt6.QtCore import Qt
import time
import pymongo
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption
import sys, random
from handler.send_email import email_verification

client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"] 
collection = db["User_Details"]


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
            Password = enhancedEncryption(password, Encryptioncode)

            if DecryptedPassword == Password:
                if (IsVerified == "True"):
                    return "Correct Password"

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

                    CodeSubmit.clicked.connect(lambda: codeCheck(email, EnterCode))
                    ResendCode.clicked.connect(lambda: resendCode(email))
                    NotVerified.exec()
            else:
                return "InCorrect Password"
                

                #NotVerified = QInputDialog()
                #NotVerified.setWindowTitle("Test")
                #text, ok = QInputDialog.getText(None, "Verify Email", "Enter the code that was sent to your email:")
                #if ok:
                   # print(text)
               # NotVerified.exec()
def codeCheck(email, InputCode):
    try:
        results = collection.find({"email": email})
        
        for data in results:
            Code = data["Verification_code"]
            if (int(InputCode.text()) == int(Code)):
                dialog = QInputDialog()
                QMessageBox.information(dialog, "Verification Success", "Code Verified Successfully!\nPlease ReLogin")
                collection.update_one({"email": email},{"$set": {"is_Verified": "True"}})
                sys.exit()
                
            else:
                dialog = QInputDialog()
                QMessageBox.information(dialog, "Error", "Wrong Code")
            
    except Exception as err:
        dialog = QInputDialog()
        QMessageBox.information(dialog, "Error", "There Has Been An Error While Processing Your Request\nPlease Try Again")
            

def resendCode(email):
    try:
        random_number = random.randint(000000, 999999)
        results = collection.find({"email": email})
        for data in results:
            collection.update_one({"email": email},{"$set": {"Verification_code": random_number}})
            dialog = QInputDialog()
            email_verification(email,random_number)
            QMessageBox.information(dialog, "Code Reset Successful", "Please Check Your Email For The New Code")

    except Exception as err:
        dialog = QInputDialog()
        QMessageBox.information(dialog, err, "There Has Been An Error While Processing Your Request\nPlease Try Again")



                






       


