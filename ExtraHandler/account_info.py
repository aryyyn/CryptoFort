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
import pymongo

class AccountInfo(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)



    def init_ui(self,Email):
        self.setFixedSize(400, 400)
        self.setWindowTitle("CryptoFort | AccountInfo")
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


        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(5)

        client = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = client["CryptoFort"] 
        collection = db["User_Details"]

        EmailText = "Email: " + Email.text()

        user_info = collection.find_one({"email": Email.text()})
        print(user_info["password"])

        
        email = QLabel(EmailText)
        layout.addWidget(email)

        RegistrationIPText = "Registration IP: " + (user_info.get("Registration_IP") or "N/A")
        layout.addWidget(QLabel(RegistrationIPText))

        DateTime = user_info.get("Date&Time_OF_Registration")
        if DateTime:
            date_time_string = DateTime.strftime("%Y-%m-%d %H:%M:%S")
            DateText = "Registration Date&Time: " + date_time_string
            layout.addWidget(QLabel(DateText))
        else:
            layout.addWidget(QLabel("Registration Date&Time: N/A"))

 

        self.show()