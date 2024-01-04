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
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys
from handler.Register_logic import registerLogic
from handler.showPassword import togglePassword
from handler.login_logic import loginLogic
from handler.forget_password import forgetPassword
from ExtraHandler.account_info import AccountInfo
from ExtraHandler.update_account import UpdateAccount
from Modules.Encrypto import EncryptoWindow
from Modules.FManager import FManagerWindow
from Modules.IPC import IPCWindow

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
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(5)

        RegisterTitle = QLabel("CryptoFort || Register")
        RegisterTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        email_layout = QHBoxLayout()
        registeremaillabel = QLabel("Email: ")
        self.registeremail = QLineEdit()
        self.registeremail.setFixedHeight(30)
        self.registeremail.setPlaceholderText("Enter your email")

        email_layout.addWidget(registeremaillabel)
        email_layout.addWidget(self.registeremail)

        password_layout = QHBoxLayout()
        registerpasslabel = QLabel("Password: ")
        self.registerpassword = QLineEdit()
        self.registerpassword.setFixedHeight(30)
        self.registerpassword.setPlaceholderText("Enter your password")
        self.registerpassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.showregisterpassword = QPushButton("SHOW")
        self.showregisterpassword.setFixedSize(50, 25)

        password_layout.addWidget(registerpasslabel)
        password_layout.addWidget(self.registerpassword)
        password_layout.addWidget(self.showregisterpassword)

        repassword_layout = QHBoxLayout()
        repasswordlabel = QLabel("Re-Enter Password: ")
        self.repassword = QLineEdit()
        self.repassword.setFixedHeight(30)
        self.repassword.setPlaceholderText("Re-enter your password")
        self.repassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.showconfirmregisterpassword = QPushButton("SHOW")
        self.showconfirmregisterpassword.setFixedSize(50, 25)

        repassword_layout.addWidget(repasswordlabel)
        repassword_layout.addWidget(self.repassword)
        repassword_layout.addWidget(self.showconfirmregisterpassword)

        promptlogin_layout = QHBoxLayout()
        promptlogin = QLabel("Already have an account? ")
        promptlogin.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.promptloginbtn = QPushButton("Login")
        self.promptloginbtn.setFixedSize(50, 25)

        promptlogin_layout.addWidget(promptlogin)
        promptlogin_layout.addSpacing(2)
        promptlogin_layout.addWidget(self.promptloginbtn, alignment=Qt.AlignmentFlag.AlignLeft)

        rrsubmit = QPushButton("Register")
        rrsubmit.setFixedSize(70, 30)

        layout.addWidget(RegisterTitle)
        layout.addLayout(email_layout)
        layout.addLayout(password_layout)
        layout.addLayout(repassword_layout)
        layout.addWidget(rrsubmit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(promptlogin_layout)

        rrsubmit.clicked.connect(self.regiserGuide)
        self.showregisterpassword.clicked.connect(lambda: togglePassword(self.registerpassword,self.showregisterpassword))
        self.showconfirmregisterpassword.clicked.connect(lambda: togglePassword(self.repassword, self.showconfirmregisterpassword))
        self.promptloginbtn.clicked.connect(self.openLogin)

        self.show()

    def regiserGuide(self):
       RegisterText =  registerLogic(self.registeremail, self.registerpassword, self.repassword)


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


        layout.addLayout(HeaderLayout)
        layout.addWidget(widget1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(widget2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(widget3, alignment=Qt.AlignmentFlag.AlignCenter)

        AccountInfo.clicked.connect(lambda: self.display_account_info_methods(Email))
        UpdateAccount.clicked.connect(lambda: self.display_update_account_methods(Email))

        Module1.clicked.connect(lambda: self.display_Encrypto_Module(Email.text()))
        Module2.clicked.connect(lambda: self.display_FManager_Module(Email.text()))
        Module3.clicked.connect(lambda: self.display_IPC_Module(Email.text()))
        self.show()

    def display_Encrypto_Module(self, Email):
        self.Encrypto = EncryptoWindow(Email)
        self.Encrypto.show()

    def display_FManager_Module(self, Email):
        self.FManager = FManagerWindow(Email)
        self.FManager.show()

    def display_IPC_Module(self, Email):
        self.IPC = IPCWindow(Email)
        self.IPC.show()
        
    def display_account_info_methods(self, Email):
        self.AI = AccountInfo(Email)
        self.AI.show()

    def display_update_account_methods(self, Email):
        self.UA = UpdateAccount(Email)
        self.UA.show()

        
        
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(750, 550)
        self.setWindowTitle("CryptoFort | Login")
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
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(5)

        LoginTitle = QLabel("CryptoFort || Login")
        LoginTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        email_layout = QHBoxLayout()
        loginlabel = QLabel("Email: ")
        self.loginInput = QLineEdit()
        self.loginInput.setFixedHeight(30)
        self.loginInput.setPlaceholderText("Enter your email")

        email_layout.addWidget(loginlabel)
        email_layout.addWidget(self.loginInput)

        ResetPassword = QPushButton("Forgot Password?")
        ResetPassword.setFixedSize(50,25)

        password_layout = QHBoxLayout()
        passwordlabel = QLabel("Password: ")
        self.PasswordInput = QLineEdit()
        self.PasswordInput.setFixedHeight(30)
        self.PasswordInput.setPlaceholderText("Enter your password")
        self.PasswordInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.ShowLoginPass = QPushButton("SHOW")
        self.ShowLoginPass.setFixedSize(50, 25)

        password_layout.addWidget(passwordlabel)
        password_layout.addWidget(self.PasswordInput)
        password_layout.addWidget(self.ShowLoginPass)
        password_layout.addWidget(ResetPassword)

        rrsubmit = QPushButton("Login")
        rrsubmit.setFixedSize(70, 30)
        
        promptRegister_layout = QHBoxLayout()
        promptRegister = QLabel("Not A Member?")
        promptRegister.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.promptRegisterbtn = QPushButton("Register")
        self.promptRegisterbtn.setFixedSize(50, 25)

        promptRegister_layout.addWidget(promptRegister)
        promptRegister_layout.addSpacing(2)
        promptRegister_layout.addWidget(self.promptRegisterbtn, alignment=Qt.AlignmentFlag.AlignLeft)

    
        
    
        layout.addWidget(LoginTitle)
        layout.addLayout(email_layout)
        layout.addLayout(password_layout)
        layout.addWidget(rrsubmit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(promptRegister_layout)

        self.ShowLoginPass.clicked.connect(lambda: togglePassword(self.PasswordInput, self.ShowLoginPass))
        rrsubmit.clicked.connect(self.loginGuide)
        self.promptRegisterbtn.clicked.connect(self.showRegister)
        ResetPassword.clicked.connect(forgetPassword)
        self.show()
 
    def showRegister(self):
        self.hide()
        self.RW = RegisterWindow()
        self.RW.show()

    def loginGuide(self):
       LoginResult = loginLogic(self.loginInput, self.PasswordInput)
       if (LoginResult == "No Email Found"):
            NoEmail = PromptDialog("Error!", "No Data Found With This Email")
            NoEmail.exec()
       elif(LoginResult == "InCorrect Password"):
           WrongPass = PromptDialog("Error!", "Wrong Password")
           WrongPass.exec()
       elif(LoginResult == "Correct Password"):
           self.hide()
           self.MM = ModuleWindow(self.loginInput)
           self.MM.show() 
           
           
       

  
def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
