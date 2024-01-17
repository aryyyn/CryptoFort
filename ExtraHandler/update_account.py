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

class UpdateAccount(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)



    def init_ui(self,Email):
        self.setFixedSize(300, 200)
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

        UpdatePassword = QPushButton("Update Password")
        DeleteAccount = QPushButton("Delete Account")
        Enable2fa = QPushButton("Enable 2fa")
        UpdatePassword.setFixedSize(50,50)
        DeleteAccount.setFixedSize(50,50)
        Enable2fa.setFixedSize(50,50)
        layout.addWidget(UpdatePassword, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(DeleteAccount, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Enable2fa, alignment=Qt.AlignmentFlag.AlignCenter)
        UpdatePassword.clicked.connect(lambda: self.changePasswordUI(Email))
        DeleteAccount.clicked.connect(lambda: self.deleteAccountUI(Email))
        Enable2fa.clicked.connect(lambda: self.twoFactUI(Email))

        self.show()

    def twoFactUI(self, Email):

    
     
        key = "HelloFortCryptoSecretKey"

        topt = pyotp.TOTP(key)

        # print(topt.now())

        uri = pyotp.totp.TOTP(key).provisioning_uri(name=Email.text(), issuer_name="CryptoFortApp")
        qrcode.make(uri).save("Logo/2fa.png")


        dialog = QDialog(self)
        dialog.setWindowTitle("2fa Code")
        dialog.setFixedSize(500,600)

        layout = QVBoxLayout(dialog)

        label = QLabel(self)
        TextLabel = QLabel("Scan The Code On Your Google Auth App To Enable 2fa")
        pixmap = QPixmap('Logo/2fa.png')

        CodeInputLayout = QHBoxLayout()
        CodeInputLabel = QLabel("Enter Your Code: ")
        CodeInput = QLineEdit()

        SubmitButton = QPushButton("Submit")


        CodeInputLayout.addWidget(CodeInputLabel)
        CodeInputLayout.addWidget(CodeInput)
        label.setPixmap(pixmap)

        layout.addWidget(TextLabel)
        layout.addWidget(label)
        layout.addLayout(CodeInputLayout)

        layout.addWidget(SubmitButton,alignment=Qt.AlignmentFlag.AlignCenter)
        SubmitButton.clicked.connect(lambda: self.twoFactSetup(CodeInput.text(),topt.now(), Email.text()))
        
        dialog.exec()
    def twoFactSetup(self,codeinput, realcode, email):
        if(codeinput == realcode):
            print("correct code")
        else:
            return
        pass

    def deleteAccountUI(self,Email):
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
                QMessageBox.information(self, "Success!", "Account Has Been Successfully Deleted.")
                sys.exit()

            else:
                QMessageBox.information(self, "Error!", "An Internal Error Has Occurred.\nPlease Try Again Later.")
                return "Internal Error Has Occurred"


           

    def changePasswordUI(self, Email):
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
            QMessageBox.critical(self, "Error!", "Passwords Do Not Match.")
            return "Passwords Don't Match"
        
        if (Password!=CurrentPasswordInput):
            QMessageBox.critical(self, "Error!", "You Have Entered An Invalid Password")
            return "Invalid Password Entered"
        
        if (Password == CurrentPasswordInput):
            NewPassInput = enhancedEncryption(NewPassInput, Encryptioncode)
            UpdatePassword = collection.update_one(
                {"email": Email},
                {"$set": {"password": NewPassInput}}
            )
            if UpdatePassword.modified_count > 0:
                QMessageBox.information(self, "Success!", "Password Has Been Changed Successfully.")
                sys.exit()

            else:
                QMessageBox.information(self, "Error!", "An Internal Error Has Occurred.\nPlease Try Again Later.")
                return "Internal Error Has Occurred"
                

                



        

  
