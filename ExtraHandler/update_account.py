import random
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
    QMessageBox,
    
)
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QRegion
from PyQt6.QtCore import Qt
import pymongo,time,sys
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption
import time,pyotp,qrcode
from dotenv import load_dotenv
import os,requests
from datetime import datetime
load_dotenv()

client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"] 
collection = db["User_Details"]
logs_collection = db["User_Logs"]



class UpdateAccount(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)



    def init_ui(self,Email):
        self.setFixedSize(300, 280)
        self.setWindowTitle("Update Account")
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
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
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        key = os.environ.get("SECRET_CODE_2FA")
        topt = pyotp.TOTP(key)
        
        uri = pyotp.totp.TOTP(key).provisioning_uri(name=Email.text(), issuer_name="CryptoFortApp")
        qrcode.make(uri).save("Logo/2fa.png")
        
        # headerLayout = QHBoxLayout()
        UpdatePassword = QPushButton("Update Password")
        DeleteAccount = QPushButton("Delete Account")
        Enable2fa = QPushButton("Enable 2fa")
        Disable2fa = QPushButton("Disable 2fa")
        # Disable2fa = QPushButton("Disable 2fa")
        UpdatePassword.setFixedSize(50,50)
        DeleteAccount.setFixedSize(50,50)
        Enable2fa.setFixedSize(50,50)
        Disable2fa.setFixedSize(50,50)
        layout.addWidget(UpdatePassword, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(DeleteAccount, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Enable2fa, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Disable2fa, alignment=Qt.AlignmentFlag.AlignCenter)

        results = collection.find({"email": Email.text()})
        for data in results:
            # print("checking")
            if (data["is_2fa_enabled"]):
                print(data["is_2fa_enabled"])
                Enable2fa.setDisabled(True)
                Disable2fa.setDisabled(False)
            else:
                Enable2fa.setDisabled(False)
                Disable2fa.setDisabled(True)
            
        UpdatePassword.clicked.connect(lambda: self.changePasswordUI(Email))
        DeleteAccount.clicked.connect(lambda: self.deleteAccountUI(Email))
        Enable2fa.clicked.connect(lambda: self.twoFactUI(topt,Email))
        Disable2fa.clicked.connect(lambda:self.disable2faUI(topt,Email.text()))

        self.show()

    def twoFactUI(self,topt, Email):

        logs_collection.update_one({"username": Email.text()}, {"$push": {"logs": f"Users clicks on the enable 2fa button at {datetime.now()}"}})
        dialog = QDialog(self)
        dialog.setWindowTitle("2fa Code")
        dialog.setFixedSize(550,600)

        layout = QVBoxLayout(dialog)
        headerLayout = QHBoxLayout(dialog)

        label = QLabel(self)
        TextLabel = QLabel("Scan The Code On Your Google Auth App To Enable 2fa")
        pixmap = QPixmap('Logo/2fa.png')

        CodeInputLayout = QHBoxLayout()
        CodeInputLabel = QLabel("Enter Your Code: ")
        CodeInput = QLineEdit()

        # Disable2fa = QPushButton("Disable 2fa")
        SubmitButton = QPushButton("Submit")


        CodeInputLayout.addWidget(CodeInputLabel)
        CodeInputLayout.addWidget(CodeInput)
        label.setPixmap(pixmap)

        headerLayout.addWidget(TextLabel)
        # headerLayout.addWidget(Disable2fa, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(headerLayout)
        layout.addWidget(label)
        layout.addLayout(CodeInputLayout)

        layout.addWidget(SubmitButton,alignment=Qt.AlignmentFlag.AlignCenter)
        SubmitButton.clicked.connect(lambda: self.twoFactSetup(CodeInput.text(),topt,Email.text(), dialog))
        # Disable2fa.clicked.connect(lambda: self.disable2faUI(topt,Email.text(), dialog))
        dialog.exec()

    def twoFactSetup(self,codeinput,topt,email, dialog: QDialog):
        realcode = topt.now()
        try:
            if(codeinput == realcode):
                results = collection.find({"email": email})
                
                for data in results:
                    random_number = random.randint(000000, 999999)
                    collection.update_one(
                            {"email": data["email"]},  
                            {
                                "$set": {
                                    "is_2fa_enabled": True,
                                    "2fa_backupcode": random_number
                                }
                            }
                        )
                    logs_collection.update_one({"username": email}, {"$push": {"logs": f"Users enables 2fa with backup code {random_number} at {datetime.now()}"}})
                    QMessageBox.information(self, "Success!", f"2fa Enabled!\nYour Backup Code is: {random_number}")
                    dialog.hide()
                    self.hide()

        
            else:
                logs_collection.update_one({"username": email}, {"$push": {"logs": f"Users enters an invalid 2fa code at {datetime.now()}"}})
                QMessageBox.critical(self, "Error", "Wrong Code!")
            
        except Exception as err:
            logs_collection.update_one({"username":email}, {"$push": {"logs": f"Users enounters an internal server error at {datetime.now()}"}})
            QMessageBox.information(self, "Error!", f"There has been an error: {err}")

    def disable2faUI(self,topt,email):
        logs_collection.update_one({"username":email}, {"$push": {"logs": f"Users clicks on the disable 2fa button at {datetime.now()}"}})
        InputDialog = QDialog(self)
        InputDialog.setWindowTitle("Disable 2fa")
        InputDialog.setFixedSize(600,100)
        
        layout = QHBoxLayout(InputDialog)
        Vlayout = QHBoxLayout(InputDialog)
        InputLabel = QLabel("Enter the code from your app: ")
        Input = QLineEdit()
        Submit = QPushButton("Submit")
        layout.addWidget(InputLabel)
        layout.addWidget(Input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Submit)
        Submit.clicked.connect(lambda: self.check2fa(email,topt,Input.text(),InputDialog))

        InputDialog.exec()

    def check2fa(self,email,topt ,inputcode,InputDialog: QDialog):
        try:
            realcode = topt.now()
            results = collection.find({"email": email})
            for data in results:
                backupcode = data["2fa_backupcode"]
                
            if(inputcode == realcode or int(inputcode) == int(backupcode)):
            
                results = collection.find({"email": email})
                
                for data in results:
                    random_number = random.randint(000000, 999999)
                    collection.update_one(
                            {"email": data["email"]},  
                            {
                                "$set": {
                                    "is_2fa_enabled": False,
                                    "2fa_backupcode": ""
                                }
                            }
                        )
                    logs_collection.update_one({"username":email}, {"$push": {"logs": f"Users disables 2fa on their account at {datetime.now()}"}})
                    QMessageBox.information(self, "Success!", f"2fa Has Been Disabled!")
                    InputDialog.hide()
                    self.hide()
            else:
                logs_collection.update_one({"username":email}, {"$push": {"logs": f"Users enters an invalid code {inputcode} while disabling 2fa at {datetime.now()}"}})
                QMessageBox.critical(self, "Error", "Wrong Code!")

        except Exception as err:
            QMessageBox.information(self, "Error!", f"There has been an error: {err}")

        

    def deleteAccountUI(self,Email):
        logs_collection.update_one({"username":Email.text()}, {"$push": {"logs": f"Users clicks on delete Account at {datetime.now()}"}})
        dialog = QDialog(self)
        dialog.setWindowTitle("Account Deletetion")
        dialog.setBaseSize(300,300)

        layout = QVBoxLayout(dialog)
        DisplayEmail = QLabel(f"Your Email is:  {Email.text()}")
        CurrentPassLabel = QLabel("Current Password:")
        CurrentPassInput = QLineEdit()
        CurrentPassInput.setEchoMode(QLineEdit.EchoMode.Password)
        
        layout.addWidget(DisplayEmail)
        layout.addWidget(CurrentPassLabel)
        layout.addWidget(CurrentPassInput)

        submit_button = QPushButton("Delete Account")
        layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.deleteAccount(Email.text(), CurrentPassInput.text()))
        dialog.exec()

    def deleteAccount(self, Email, CurrentPassInput):
        client = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = client["CryptoFort"] 
        collection = db["User_Details"]

        result = collection.find_one({"email": Email})  

        Password = result.get("password")
        Encryptioncode = result.get("Encryption_code")

        CurrentPassInput = enhancedEncryption(CurrentPassInput, Encryptioncode)
        if (Password!=CurrentPassInput):
            PasswordMismatch = QMessageBox()
            PasswordMismatch.setWindowTitle("Error")
            PasswordMismatch.setText("You Have Entered An Invalid Password")
            button = PasswordMismatch.exec()
            return "Invalid Password Entered"     

        if (Password == CurrentPassInput):
            result = collection.delete_one({"email": Email})

            if (result.deleted_count > 0):
                IP = requests.get("https://ipv4.icanhazip.com").text.strip()
                logs_collection.update_one({"username":Email}, {"$push": {"logs": f"Users deletes their account at {datetime.now()} with IP {IP}"}})

                QMessageBox.information(self, "Success!", "Account Has Been Successfully Deleted.")
                sys.exit()

            else:
                logs_collection.update_one({"username":Email}, {"$push": {"logs": f"Users fails to delete their account at {datetime.now()} with IP {IP}"}})
                QMessageBox.information(self, "Error!", "An Internal Error Has Occurred.\nPlease Try Again Later.")
                return "Internal Error Has Occurred"


           

    def changePasswordUI(self, Email):
        logs_collection.update_one({"username":Email.text()}, {"$push": {"logs": f"Users clicks on the change password button at {datetime.now()}"}})
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Your Password")
        dialog.setBaseSize(300,300)

        layout = QVBoxLayout(dialog)
        CurrentPassLabel = QLabel("Current Password:")
        CurrentPassInput = QLineEdit()
        CurrentPassInput.setEchoMode(QLineEdit.EchoMode.Password)
        NewPassLabel = QLabel("New Password:")
        NewPassInput = QLineEdit()
        NewPassInput.setEchoMode(QLineEdit.EchoMode.Password)
        ConfirmNewPassLabel = QLabel("Confirm New Password: ")
        ConfirmNewPassInput = QLineEdit()
        ConfirmNewPassInput.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(CurrentPassLabel)
        layout.addWidget(CurrentPassInput)
        layout.addWidget(NewPassLabel)
        layout.addWidget(NewPassInput)
        layout.addWidget(ConfirmNewPassLabel)
        layout.addWidget(ConfirmNewPassInput)

        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.changePassword(Email.text(), CurrentPassInput.text(), NewPassInput.text(), ConfirmNewPassInput.text()))
        dialog.exec()

    def changePassword(self, Email, CurrentPasswordInput, NewPassInput, ConfirmNewPassInput):
        client = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = client["CryptoFort"] 
        collection = db["User_Details"]

        result = collection.find_one({"email": Email})  
        Password = result.get("password")
        Encryptioncode = result.get("Encryption_code")
        CurrentPasswordInput = enhancedEncryption(CurrentPasswordInput, Encryptioncode)

        if (NewPassInput!=ConfirmNewPassInput):
            logs_collection.update_one({"username":Email}, {"$push": {"logs": f"Users passwords do not match while changing their password at {datetime.now()}"}})
            QMessageBox.critical(self, "Error!", "Passwords Do Not Match.")
            return "Passwords Don't Match"
        
        if (Password!=CurrentPasswordInput):
            logs_collection.update_one({"username":Email}, {"$push": {"logs": f"Users passwords do not match while changing their password at {datetime.now()}"}})
            QMessageBox.critical(self, "Error!", "You Have Entered An Invalid Password")
            return "Invalid Password Entered"
        
        if (Password == CurrentPasswordInput):
            NewPassInput = enhancedEncryption(NewPassInput, Encryptioncode)
            UpdatePassword = collection.update_one(
                {"email": Email},
                {"$set": {"password": NewPassInput}}
            )
            if UpdatePassword.modified_count > 0:
                logs_collection.update_one({"username":Email}, {"$push": {"logs": f"User has changed their password at {datetime.now()}"}})
                QMessageBox.information(self, "Success!", "Password Has Been Changed Successfully.")
                sys.exit()

            else:
                logs_collection.update_one({"username":Email}, {"$push": {"logs": f"User has encountered an error while changing their password at {datetime.now()}"}})
                QMessageBox.information(self, "Error!", "An Internal Error Has Occurred.\nPlease Try Again Later.")
                return "Internal Error Has Occurred"
                

                



        

  
