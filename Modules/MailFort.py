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
    QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys
import pymongo
import json,requests


client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"] 
collection = db["User_Details"]
MailCollection = db["Mail_Details"]


class MailFort(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)

    def init_ui(self,Email):
        self.setFixedSize(800, 800)
        self.setWindowTitle("CryptoFort | IPC")
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


        CreateMail = QPushButton("Mail")
        CreateMail.setFixedSize(50,50)

        MailDisplay = QTextEdit()
        MailDisplay.setBaseSize(300,500)
        MailDisplay.setReadOnly(True)

        Mail_logs = MailCollection.find_one({"email": Email})
        if(Mail_logs):
            print("working")
            SentLogs = Mail_logs.get("email_sent", [])
            ReceivedLogs = Mail_logs.get("email_received", [])

    # CombineEmail = f"{subject}CryptoFortMailModule{content}CryptoFortMailSent{Email}"
            
            for mail_logs in SentLogs:
                finalsubjectSent = mail_logs.split('CryptoFortMailModule')[0]
                finalcontentandEmailSent = mail_logs.split('CryptoFortMailModule')[1]
                finalcontentSent = finalcontentandEmailSent.split('CryptoFortMailSent')[0]
                finalSentBy = finalcontentandEmailSent.split('CryptoFortMailSent')[1]

                finalmailSent = f"[Sent]: {finalsubjectSent}\n{finalcontentSent}\nSent To: {finalSentBy} \n------------------------------------------------------------------------------"
                MailDisplay.append(finalmailSent)

            for mail_Received_logs in ReceivedLogs:

                finalsubjectReceived = mail_Received_logs.split('CryptoFortMailModule')[0]
                finalcontentandEmailReceived = mail_Received_logs.split('CryptoFortMailModule')[1]
                finalcontentReceived = finalcontentandEmailReceived.split('CryptoFortMailSent')[0]
                finalReceivedBy = finalcontentandEmailReceived.split('CryptoFortMailSent')[1]

                finalmailReceived = f"[Received]: {finalsubjectReceived}\n{finalcontentReceived}\nSent By: {finalReceivedBy}\n------------------------------------------------------------------------------"
                MailDisplay.append(finalmailReceived)
            
            

        else:
            MailDisplay.setText("No Emails Found")

        Close = QPushButton("Close")
        Close.setFixedSize(50,50)

        layout.addWidget(CreateMail,alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(MailDisplay)
        layout.addWidget(Close,alignment=Qt.AlignmentFlag.AlignCenter)


        CreateMail.clicked.connect(lambda: self.MailCreate(Email))




        
        # user_info = collection.find_one({"email": Email})
        
        # RegisterdIP = user_info["Registration_IP"]
        # Registered_IPLabel = QLabel(f"Registered IP: {RegisterdIP}")
 
        # layout.addWidget(Registered_IPLabel)

        self.show()

    def MailCreate(self, Email):

        dialog = QDialog(self)
        dialog.setWindowTitle("Mail Module")
        dialog.setFixedSize(550,600)

        layout = QVBoxLayout(dialog)

        self.EmailLabel = QLabel("To Email: ")
        self.SubjectLabel = QLabel("Subject: ")
        self.ContentLabel = QLabel("Content: ")

        self.EmailInput = QTextEdit()
        self.EmailInput.setFixedHeight(75)

        self.SubjectInput = QTextEdit()
        self.SubjectInput.setFixedHeight(75)
        self.ContentInput = QTextEdit()

        self.submitButton = QPushButton("Submit")
        self.submitButton.setFixedSize(50,50)

        layout.addWidget(self.EmailLabel)
        layout.addWidget(self.EmailInput)
        layout.addSpacing(20)
        layout.addWidget(self.SubjectLabel)
        layout.addWidget(self.SubjectInput)
        layout.addSpacing(20)
        layout.addWidget(self.ContentLabel)
        layout.addWidget(self.ContentInput)
        layout.addSpacing(20)
        layout.addWidget(self.submitButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.submitButton.clicked.connect(lambda: self.handleEmailFunction(Email,self.SubjectInput.toPlainText(), self.ContentInput.toPlainText(), self.EmailInput.toPlainText()))
        
        dialog.exec()

    def handleEmailFunction(self, UserEmail,subject,content,Email):

        if subject == "":
            QMessageBox.critical(self, "Error", "Subject Can Not Be Empty.")
            return "Empty Text Field"
        
        if Email == "":
            QMessageBox.critical(self, "Error", "Email Can Not Be Empty.")
            return "Empty Text Field"
        
        if content == "":
            QMessageBox.critical(self, "Error", "Content Can Not Be Empty.")
            return "Empty Text Field"
        
        if Email == UserEmail:
            QMessageBox.critical(self, "Error", "You Can Not Send Email To Your Own Account.")
            return "Error"

        
        user_info_count = collection.count_documents({"email": Email})
        if (user_info_count<1):
            QMessageBox.critical(self, "Error", "Email Not Found.\nPlease Re-Check Your Email And Try Again.")
            return "Empty Text Field"
        try:
            MailCollection_count = MailCollection.count_documents({"email": Email})
            SelfMailCollection_count = MailCollection.count_documents({"email": UserEmail})

            if (MailCollection_count<1):

                user_mail_data = {
                "email": Email.lower(),
                "email_sent": [],
                "email_received": [],
                "NewMessageAlert": False
                

                }
                MailCollection.insert_one(user_mail_data)

            
            if (SelfMailCollection_count<1):

                user_mail_data = {
                "email": UserEmail.lower(),
                "email_sent": [],
                "email_received": [],
                "NewMessageAlert": False

                }
                MailCollection.insert_one(user_mail_data)

            CombineEmail = f"{subject}CryptoFortMailModule{content}CryptoFortMailSent{Email}"
            CombineEmailSent = f"{subject}CryptoFortMailModule{content}CryptoFortMailSent{UserEmail}"
            MailCollection.update_one({"email": Email}, {"$push": {"email_received": CombineEmailSent}})
            MailCollection.update_one({"email": UserEmail}, {"$push": {"email_sent": CombineEmail}})

            QMessageBox.critical(self, "Success", "Email Has Been Sent.")
        
        except Exception as err:
            QMessageBox.critical(self, "Error", f"Error: {err}")
        



        # logs_collection.update_one({"username": email}, {"$push": {"logs": f"User enters an invalid email at {datetime.now()}"}})
        # logs_entry = {"username": email.lower(), "logs": ["User logs:"]}
        # logs_collection.insert_one(logs_entry)

        # if (user_info):
        #     print("found")
        #     print(user_info)

        # else:
        #     print("not found")

        







    

