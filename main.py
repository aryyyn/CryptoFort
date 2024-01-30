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
    
)
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont,QPainter, QPen,QPixmap,QIcon

import sys
from handler.Register_logic import registerLogic
from handler.showPassword import togglePassword
from handler.login_logic import loginLogic
from ExtraHandler.account_info import AccountInfo
from ExtraHandler.update_account import UpdateAccount
from Modules.Encrypto import EncryptoWindow
from Modules.FManager import FManagerWindow
from Modules.MailFort import MailFort
from Modules.IPC import IPCWindow
from handler.forget_password import ForgetPassword
import pymongo
from datetime import datetime
from Admin.adminUI import AdminWindow


client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"] 
logs_collection = db["User_Logs"]

class PromptDialog(QDialog):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        layout = QVBoxLayout()

        descriptionL = QLabel(description)
        layout.addWidget(descriptionL)

        ok = QPushButton("OK")
        ok.clicked.connect(self.accept) 
        layout.addWidget(ok)

        self.setLayout(layout)    

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(750, 550)
        self.setWindowTitle("CryptoFort | Register")
        icon = QIcon("Logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
                
                
            }

            QLineEdit {
                border: 1px solid #00FF00; 
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #00FF00; 
                background-color: #000000; 
                color: #00FF00; 
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #00FF00; 
                          
            }

            QPushButton {
                border: 1px solid #00FF00; 
                border-radius: 5px;
                background: #111111;
                min-width: 100px;
                font-size: 12px;
                color: #00FF00; 
            }

            QPushButton:hover {
                background: #222222;
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
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        RegisterTitle = QLabel("CryptoFort || Register")
        RegisterTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        email_layout = QVBoxLayout()
        registeremaillabel = QLabel("Email: ")
        self.registeremail = QLineEdit()
        self.registeremail.setFixedHeight(40)
        self.registeremail.setPlaceholderText("Enter your email")

        email_layout.addWidget(registeremaillabel)
        email_layout.addWidget(self.registeremail)

        icon_path = 'Logo/eye.png'
        hide = QPixmap(icon_path)

        password_layout = QHBoxLayout()
        registerpasslabel = QLabel("Password: ")
        self.registerpassword = QLineEdit()
        self.registerpassword.setFixedHeight(40)
        self.registerpassword.setFixedWidth(650)
        self.registerpassword.setPlaceholderText("Enter your password")
        self.registerpassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.showregisterpassword = QPushButton(QIcon(hide),"")
        self.showregisterpassword.setFixedSize(10, 40)

        # password_layout.addWidget(registerpasslabel)
        password_layout.addWidget(self.registerpassword)
        password_layout.addWidget(self.showregisterpassword)

        repassword_layout = QHBoxLayout()
        repasswordlabel = QLabel("Re-Enter Password: ")
        self.repassword = QLineEdit()
        self.repassword.setFixedHeight(40)
        self.repassword.setFixedWidth(650)
        self.repassword.setPlaceholderText("Re-enter your password")
        self.repassword.setEchoMode(QLineEdit.EchoMode.Password)



        self.showconfirmregisterpassword = QPushButton(QIcon(hide),"")
        self.showconfirmregisterpassword.setFixedSize(10, 40)

        # repassword_layout.addWidget(repasswordlabel)
        repassword_layout.addWidget(self.repassword)
        repassword_layout.addWidget(self.showconfirmregisterpassword)

        promptlogin_layout = QHBoxLayout()
        promptlogin = QLabel("Already have an account? ")
        self.promptloginbtn = QPushButton("Login")
        self.promptloginbtn.setFixedSize(50, 25)

        promptlogin_layout.addWidget(promptlogin, alignment=Qt.AlignmentFlag.AlignRight)
        # promptlogin_layout.addSpacing(2)
        promptlogin_layout.addWidget(self.promptloginbtn)

        rrsubmit = QPushButton("Register")
        rrsubmit.setFixedHeight(40)

        layout.addWidget(RegisterTitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addLayout(email_layout)
        layout.addSpacing(20)
        layout.addWidget(registerpasslabel)
        layout.addLayout(password_layout)
        layout.addWidget(repasswordlabel)
        layout.addLayout(repassword_layout)
        layout.addWidget(rrsubmit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addLayout(promptlogin_layout)

        rrsubmit.clicked.connect(self.regiserGuide)
        self.showregisterpassword.clicked.connect(lambda: togglePassword(self.registerpassword,self.showregisterpassword))
        self.showconfirmregisterpassword.clicked.connect(lambda: togglePassword(self.repassword, self.showconfirmregisterpassword))
        self.promptloginbtn.clicked.connect(self.openLogin)


        SubmitEnterShortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        SubmitEnterShortcut.activated.connect(rrsubmit.click)

        self.show()

    def regiserGuide(self):
       RegisterText =  registerLogic(self.registeremail, self.registerpassword, self.repassword)
       if (RegisterText == "Success"):
           self.hide()
           self.LoginWindow = LoginWindow()
           self.LoginWindow.show()


    def openLogin(self):
        self.hide()
        self.LoginWindow = LoginWindow()
        self.LoginWindow.show()

class ModuleWindow(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)
        
    def init_ui(self, Email):
        self.setFixedSize(750, 550)
        self.setWindowTitle("CryptoFort | ModuleMenu")
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
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
        self.setGeometry(100, 100, 400, 300)
        layout.setSpacing(10)

        HeaderLayout = QHBoxLayout()
        WelcomeUserName = Email.text().split('@')[0]
        TitleMessage = QLabel(f"CryptoFort || Modules \n Welcome back,  {WelcomeUserName}")
    


        AccountInfo = QPushButton("Account Info")
        UpdateAccount = QPushButton("Update Account")

        HeaderLayout.addWidget(AccountInfo, alignment=Qt.AlignmentFlag.AlignLeft)
        HeaderLayout.addWidget(TitleMessage, alignment=Qt.AlignmentFlag.AlignCenter)
        HeaderLayout.addWidget(UpdateAccount, alignment=Qt.AlignmentFlag.AlignRight)

       
        
        Module1 = QPushButton("Encrypto")
        Module1.setFixedSize(400,70)
        Module2 = QPushButton("FManager")
        Module2.setFixedSize(400,70)
        Module3 = QPushButton("IPC")
        Module3.setFixedSize(400,70)
        Module4 = QPushButton("MailFort")
        Module4.setFixedSize(400,70)

        widget1 = QWidget()
        widget1.setFixedSize(300, 100)
        widget1.setLayout(QVBoxLayout())
        widget1.layout().addWidget(Module1)

        widget2 = QWidget()
        widget2.setFixedSize(300, 100)
        widget2.setLayout(QVBoxLayout())
        widget2.layout().addWidget(Module2)

        widget3 = QWidget()
        widget3.setFixedSize(300, 100)
        widget3.setLayout(QVBoxLayout())
        widget3.layout().addWidget(Module3)
        

        widget4 = QWidget()
        widget4.setFixedSize(300, 100)
        widget4.setLayout(QVBoxLayout())
        widget4.layout().addWidget(Module4)


        BottomLayout = QHBoxLayout()

        ExitButton = QPushButton("Exit")
        ExitButton.setFixedSize(25,25)
        BottomLayout.addWidget(ExitButton, alignment=Qt.AlignmentFlag.AlignLeft)

        LogoutButton = QPushButton("Logout")
        LogoutButton.setFixedSize(25,25)
        BottomLayout.addWidget(LogoutButton, alignment=Qt.AlignmentFlag.AlignRight)




        layout.addLayout(HeaderLayout)
        layout.addWidget(widget1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(widget2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(widget3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(widget4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(BottomLayout)

        AccountInfo.clicked.connect(lambda: self.display_account_info_methods(Email))
        UpdateAccount.clicked.connect(lambda: self.display_update_account_methods(Email))
        Module1.clicked.connect(lambda: self.display_Encrypto_Module(Email.text()))
        Module2.clicked.connect(lambda: self.display_FManager_Module(Email.text()))
        Module3.clicked.connect(lambda: self.display_IPC_Module(Email.text()))
        Module4.clicked.connect(lambda: self.display_MailFort_Module(Email.text()))
        ExitButton.clicked.connect(self.handleExit)
        LogoutButton.clicked.connect(self.handleLogout)

        module1shortcut = QShortcut(QKeySequence("Ctrl+1"), self)
        module1shortcut.activated.connect(Module1.click)

        module2shortcut = QShortcut(QKeySequence("Ctrl+2"), self)
        module2shortcut.activated.connect(Module2.click)

        module3shortcut = QShortcut(QKeySequence("Ctrl+3"), self)
        module3shortcut.activated.connect(Module3.click)
        



        self.show()
    
    def handleExit(self):
        sys.exit()

    def handleLogout(self):
        self.hide()
        self.Login = LoginWindow()
        self.Login.show()


    def display_Encrypto_Module(self, Email):
        logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User clicks on the Encrypto module at  {datetime.now()}"}})
        self.Encrypto = EncryptoWindow(Email)
        self.Encrypto.show()

    def display_FManager_Module(self, Email):
        logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User clicks on the FManager module at  {datetime.now()}"}})
        self.FManager = FManagerWindow(Email)
        self.FManager.show()

    def display_IPC_Module(self, Email):
        logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User clicks on the IPC module at  {datetime.now()}"}})
        self.IPC = IPCWindow(Email)
        self.IPC.show()


    def display_MailFort_Module(self, Email):
        logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User clicks on the MailFort module at  {datetime.now()}"}})
        self.MF = MailFort(Email)
        self.MF.show()
        
    def display_account_info_methods(self, Email):
        logs_collection.update_one({"username": Email.text()}, {"$push": {"logs": f"User clicks on the account_info module at  {datetime.now()}"}})
        self.AI = AccountInfo(Email)
        self.AI.show()

    def display_update_account_methods(self, Email):
        logs_collection.update_one({"username": Email.text()}, {"$push": {"logs": f"User clicks on the update_account module at  {datetime.now()}"}})
        self.UA = UpdateAccount(Email)
        self.UA.show()

        
        
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):


        self.setFixedSize(750, 550)
        self.setWindowTitle("CryptoFort | Login")
        # Note: The icon path should be adjusted based on the actual location of your logo
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
                
            }

            QLineEdit {
                border: 1px solid #00FF00; 
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #00FF00; 
                background-color: #000000; 
                color: #00FF00; 
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #00FF00; 
               
            }

            QPushButton {
                border: 1px solid #00FF00; 
                border-radius: 5px;
                background: #111111;
                min-width: 100px;
                font-size: 12px;
                color: #00FF00; 
            }

            QPushButton:hover {
                background: #222222;
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
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        LoginTitle = QLabel("CryptoFort || Login")
        LoginTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        email_layout = QVBoxLayout()
        loginlabel = QLabel("Email: ")
        self.loginInput = QLineEdit()
        self.loginInput.setFixedHeight(40)
        self.loginInput.setPlaceholderText("Enter your email")

        email_layout.addWidget(loginlabel)
        email_layout.addWidget(self.loginInput)

        ResetPassword = QPushButton("Forgot Password?")
        ResetPassword.setFixedHeight(40)
       
        

        password_layout = QHBoxLayout()
        # password_layout2 = QHBoxLayout()
        passwordlabel = QLabel("Password: ")
        self.PasswordInput = QLineEdit()
        self.PasswordInput.setFixedHeight(40)
        self.PasswordInput.setFixedWidth(650)
        self.PasswordInput.setPlaceholderText("Enter your password")
        self.PasswordInput.setEchoMode(QLineEdit.EchoMode.Password)


        icon_path = 'Logo/eye.png'
        hide = QPixmap(icon_path)

        self.ShowLoginPass = QPushButton(QIcon(hide),"")
        

        self.ShowLoginPass.setFixedSize(10,40)


        password_layout.addWidget(self.PasswordInput)
        password_layout.addWidget(self.ShowLoginPass, alignment=Qt.AlignmentFlag.AlignRight)
        

        rrsubmit = QPushButton("Login")
        rrsubmit.setFixedHeight(40)

        promptRegister_layout = QHBoxLayout()
        promptRegister = QLabel("Not A Member?")
        promptRegister.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.promptRegisterbtn = QPushButton("Register")
        self.promptRegisterbtn.setFixedSize(50, 25)
       

        promptRegister_layout.addWidget(promptRegister, alignment=Qt.AlignmentFlag.AlignRight)
        promptRegister_layout.addWidget(self.promptRegisterbtn)

        layout.addWidget(LoginTitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addLayout(email_layout)
        layout.addSpacing(20)
        layout.addWidget(passwordlabel)
        layout.addLayout(password_layout)
        layout.addWidget(ResetPassword)
        layout.addSpacing(20)
        layout.addWidget(rrsubmit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(promptRegister_layout)

        self.ShowLoginPass.clicked.connect(lambda: togglePassword(self.PasswordInput, self.ShowLoginPass))
        rrsubmit.clicked.connect(self.loginGuide)
        self.promptRegisterbtn.clicked.connect(self.showRegister)
        ResetPassword.clicked.connect(self.showForgetPassword)


        SubmitEnterShortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        SubmitEnterShortcut.activated.connect(rrsubmit.click)
        self.show()
    
    def showForgetPassword(self):
        self.FP = ForgetPassword()
        self.FP.show()

    def showRegister(self):
        self.hide()
        self.RW = RegisterWindow()
        self.RW.show()

    def loginGuide(self):
        LoginResult = loginLogic(self.loginInput, self.PasswordInput)

        if LoginResult == "Error":
            InvalidResult = PromptDialog("Error!", "There Has Been An Error!")
            InvalidResult.exec()  
        elif LoginResult == "InvalidIP":
            InvalidIP = PromptDialog("Invalid IP!", "IPS Do Not Match")
            InvalidIP.exec()
        elif LoginResult == "Correct Password":
            if str(self.loginInput.text()) == "admin":
                self.hide()
                self.Admin = AdminWindow(self.loginInput)
                self.Admin.show()
            else:
                self.hide()
                self.MM = ModuleWindow(self.loginInput)
                self.MM.show()
            
           
       

  
def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
