from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDialog,
    QTextEdit,
    QHBoxLayout,
    QMessageBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys,pymongo,os
from datetime import datetime


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["CryptoFort"] 
logs_collection = db["User_Logs"]
user_data = db["User_Details"]

class AdminWindow(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)

    def init_ui(self,Email):
        
        self.setFixedSize(450, 450)
        self.setWindowTitle("CryptoFort | ADMIN WINDOW")
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
            }

          QTextEdit {
        border: 2px solid #00FF00;
        border-radius: 8px;
        padding: 10px; 
        selection-background-color: #00FF00;
        background-color: #111111;
        color: #00FF00;
        font-size: 14px;
    }
    
    QTextEdit:focus {
        border: 2px solid #00FF00; 
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


        WelcomeLabel = QLabel(f"Welcome, {Email.text()}")
        
        Button1 = QPushButton("View User Info")
        Button1.setFixedSize(75,50)

        Button2 = QPushButton("Modify User Info")
        Button2.setFixedSize(75,50)

        Button3 = QPushButton("View User Logs")
        Button3.setFixedSize(75,50)

        LogoutButton = QPushButton("Exit")
        LogoutButton.setFixedSize(25,25)

        layout.addWidget(WelcomeLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Button1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Button2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(Button3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(LogoutButton, alignment=Qt.AlignmentFlag.AlignRight)

        Button1.clicked.connect(lambda: self.showUserInfo())
        Button2.clicked.connect(lambda: self.updateUserInfo())
        Button3.clicked.connect(lambda: self.showUserLogs())
        LogoutButton.clicked.connect(lambda: self.Logout())
        self.show()

    def showUserInfo(self):
        dialog = QDialog(self)
        dialog.setBaseSize(800,800)
        dialog.setWindowTitle("CryptoFort | Show User Info")
        layout = QVBoxLayout(dialog)
        Headerlayout = QHBoxLayout(dialog)

        HeaderLabel = QLabel("Enter Email: ")
        EmailInput = QLineEdit()

        Headerlayout.addWidget(HeaderLabel)
        Headerlayout.addWidget(EmailInput)

        SearchButton = QPushButton("Search")
        SearchButton.setFixedSize(50,25)


        InputBox = QTextEdit()
        InputBox.setPlaceholderText("User Data Output")
        InputBox.setFixedHeight(350)
        InputBox.setFixedWidth(350)

        layout.addLayout(Headerlayout)
        layout.addWidget(SearchButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(InputBox)

        SearchButton.clicked.connect(lambda: self.userDataAction(EmailInput.text(), InputBox))

        dialog.exec()

    def userDataAction(self,email, InputBox: QTextEdit):
        if (str(email) == ""):
            QMessageBox.information(self, "Failure!", f"Please Enter An Email")
            return
        else:
            user_d = user_data.find({"email": email})
            if user_d:
                for data in user_d:
                    Registration_IP = data["Registration_IP"]
                    Last_LoggedIn_IP = data["Last_LoggedIn_IP"]
                    DateAndTime_OF_Registration = data["Date&Time_OF_Registration"]
                    isVerified = data["is_Verified"]
                    is2faEnabled = data["is_2fa_enabled"]

                # Registration_IP = user_d.get("Registration_IP")
                # Last_LoggedIn_IP = user_d.get("Last_LoggedIn_IP")
                # DateAndTime_OF_Registration = user_d.get("Date&Time_OF_Registration")
                # isVerified = user_d.get("is_Verified")
                # is2faEnabled = user_d.get("is_2fa_enabled")
                
                InputBox.setText(f"Email: {email}\nRegistration_IP:{Registration_IP}\nLast_LoggedIn_IP:{Last_LoggedIn_IP}\nDateAndTime_OF_Registration:{DateAndTime_OF_Registration}\nisVerified:{isVerified}\nis2faEnabled:{is2faEnabled}")



            else:
                QMessageBox.information(self, "Failure!", f"No data Found with email: {email}")
                return


        pass

    def updateUserInfo(self):
        dialog = QDialog(self)
        dialog.setFixedSize(300,300)
        dialog.setWindowTitle("CryptoFort | Update User Info")
        dialog.exec()

    def showUserLogs(self):
        dialog = QDialog(self)
        dialog.setBaseSize(800,500)
        dialog.setWindowTitle("CryptoFort | UserLogs")

        layout = QVBoxLayout(dialog)
        Headerlayout = QHBoxLayout(dialog)

        HeaderLabel = QLabel("Enter Email: ")
        EmailInput = QLineEdit()

        Headerlayout.addWidget(HeaderLabel)
        Headerlayout.addWidget(EmailInput)

        SearchButton = QPushButton("Search")
        SearchButton.setFixedSize(50,25)

        SaveButton = QPushButton("Save Data")
        SaveButton.setFixedSize(50,25)

        InputBox = QTextEdit()
        InputBox.setPlaceholderText("Log Data Output")
        InputBox.setFixedHeight(600)
        InputBox.setFixedWidth(600)

        

        layout.addLayout(Headerlayout)
        layout.addWidget(SearchButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(InputBox)
        layout.addWidget(SaveButton, alignment=Qt.AlignmentFlag.AlignCenter)

        SearchButton.clicked.connect(lambda: self.userLogsAction(EmailInput.text(),InputBox, SaveButton))
        SaveButton.setVisible(False)
        dialog.exec()

    def userLogsAction(self, email, InputBox: QTextEdit, SaveButton = QPushButton):
        if (str(email) == ""):
            QMessageBox.information(self, "Failure!", f"Please Enter An Email")
            return
        else:
            user_logs = logs_collection.find_one({"username": email})
            if(user_logs):
                SaveButton.setVisible(True)
                SaveButton.clicked.connect(lambda: self.saveLogsAction(email, user_logs))
                Logs = user_logs.get("logs", [])

                for log_entry in Logs:
                    InputBox.append(log_entry)
            else:
                QMessageBox.information(self, "Failure!", f"No data Found with email: {email}")
                return
            
    def saveLogsAction(self, email, user_logs):
        Logs = user_logs.get("logs", [])

        os.makedirs("Logs", exist_ok=True)

        with open(f"Logs/{email}_logs.txt", "w") as file:
            for log_entry in Logs:
                file.write(f"{log_entry}\n")
        QMessageBox.information(self, "Success!", f"Saved Logs for Email: {email} in {email}_logs.txt")

            

    def Logout(self):
        sys.exit()
