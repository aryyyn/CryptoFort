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
        self.setBaseSize(400, 400)
        self.setWindowTitle("AccountInfo")
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

        client = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = client["CryptoFort"] 
        collection = db["User_Details"]

        EmailText = "Email: " + Email.text()

        user_info = collection.find_one({"email": Email.text()})
        
        layout.addWidget(QLabel(EmailText))

        RegistrationIPText = "Registration IP: " + (user_info.get("Registration_IP"))
        layout.addWidget(QLabel(RegistrationIPText))


        date_time_string = user_info.get("Date&Time_OF_Registration").strftime("%Y-%m-%D %H:%M:%S")
        DateText = "Registration Date&Time: " + date_time_string
        layout.addWidget(QLabel(DateText), alignment=Qt.AlignmentFlag.AlignLeft)

 

        self.show()