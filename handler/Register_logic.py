import pymongo
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog,QDialogButtonBox,QVBoxLayout,QLabel,QInputDialog
import socket
import requests
import random, time
from validate_email_address import validate_email
from datetime import datetime
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption
from handler.send_email import email_verification
import json
from dotenv import load_dotenv
import os
import re
load_dotenv()

client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"] 
collection = db["User_Details"]
logs_collection = db["User_Logs"]

def email_validator(email):
    
    url = "https://mailcheck.p.rapidapi.com/"

    querystring = {f"domain":email}

    headers = {
        "X-RapidAPI-Key": os.environ.get("EMAIL_CODE"),
        "X-RapidAPI-Host": "mailcheck.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring).text
    parsed_email_data = json.loads(response)
    if (str((parsed_email_data["valid"])) == "True"):
        if (str((parsed_email_data["text"])) == "Looks okay"):
            if(str((parsed_email_data["disposable"])) == "False"):
                return True
    else:
        return False
        

def getDateAndTime():
    DateAndTime = datetime.now()
    return DateAndTime

def is_strong_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))

def internal_error(err):
    InternalError = QMessageBox()
    InternalError.setWindowTitle("Errpr")
    InternalError.setText(f"An Internal Error Has Occurred\nPlease Try Again Later\nError is {err}")
    button = InternalError.exec()

def get_ip_address():
    IP = requests.get("https://ipv4.icanhazip.com").text.strip()
    return IP


def CustomMessage(title,description):
    dialog = QInputDialog()
    dialog.setStyleSheet("""
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
    QMessageBox.information(dialog,title,description)

    
def registerLogic(eemail,epassword,erepassword):
    try:
        


        email = eemail.text().lower()
        password = epassword.text()
        repassword = erepassword.text()

        if email == "":
            # EmailFieldEmpty = QMessageBox()
            # EmailFieldEmpty.setWindowTitle("Error")
            # EmailFieldEmpty.setText("Email Field Cannot Be Empty")
            # button = EmailFieldEmpty.exec()

            CustomMessage("Error","Email Field Cannot be Empty")
            return "Email Field Empty"
        
        if (is_strong_password(password) == False):
            CustomMessage("Password Is Not Strong Enough", "Make Sure To Include At Lease One Uppercase and One Digit")
            return "Password Not Strong Enough"
        
       

        if password == "":
            # PasswordFieldEmpty = QMessageBox()
            # PasswordFieldEmpty.setWindowTitle("Error")
            # PasswordFieldEmpty.setText("Password Field Cannot Be Empty")
            # button = PasswordFieldEmpty.exec()
            CustomMessage("Error","Password Field Cannot be Empty")
            return "Password Field Empty"
        
        if repassword == "":
            # RePasswordFieldEmpty = QMessageBox()
            # RePasswordFieldEmpty.setWindowTitle("Error")
            # RePasswordFieldEmpty.setText("RePassword Field Cannot Be Empty")
            # button = RePasswordFieldEmpty.exec()
            CustomMessage("Error","Password Field Cannot be Empty")
            return "RePassword Field Empty"



        logs_entry = {"username": email.lower(), "logs": ["User logs:"]}
        logs_collection.insert_one(logs_entry)

        count = collection.count_documents({"email": email})
        

        if (email_validator(email)):
            pass
        else:
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User tries registering with an invalid email at {datetime.now()} with IP {get_ip_address()}"}})
            # hi = QDialog()
            # QMessageBox.critical(hi, "Error", "Invalid Email")
            CustomMessage("Error","Invalid Email!")
            return "Invalid Email"
        
        if (count>0):
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User tries registering with an already registered email at {datetime.now()} with IP {get_ip_address()}"}})
            # EmailAlreadyRegistered = QMessageBox()
            # EmailAlreadyRegistered.setWindowTitle("Error")
            # EmailAlreadyRegistered.setText("Email Has Already Been Registered")
            # button = EmailAlreadyRegistered.exec()
            CustomMessage("Error","Email Has Already Been Registered")
            return "Email Already Registered"
        

        


        if (password!=repassword):
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"Users passwords do not match while registering at {datetime.now()} with IP {get_ip_address()}"}})
            # PasswordMismatch = QMessageBox()
            # PasswordMismatch.setWindowTitle("Error")
            # PasswordMismatch.setText("Passwords dont match")
            # button = PasswordMismatch.exec()
            CustomMessage("Error","Passwords dont match")
            return "Password Mismatch"
        

        try:
            epoch = str(time.time())
            EncryptionCode = epoch.split('.')[1]
            EncryptionCode+=EncryptionCode
            EncryptionCode+=EncryptionCode
            encrypted_password = enhancedEncryption(password, EncryptionCode)
            random_number = random.randint(000000, 999999)
            IP = get_ip_address() 
            LastLoggedInIP = IP
            user_data = {
            "email": email.lower(),
            "password": encrypted_password,
            "Encryption_code": EncryptionCode,
            "Registration_IP": IP,
            "Last_LoggedIn_IP": LastLoggedInIP,
            "Date&Time_OF_Registration": getDateAndTime(),
            "is_Verified": False,
            "Verification_code": random_number,
            "is_2fa_enabled": False,
            "2fa_backupcode": ""

            }
            collection.insert_one(user_data)
            email_verification(email,random_number)
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User with {email.lower()} creates a new account at {datetime.now()} with IP {IP}"}})
            # RegisterSuccess = QMessageBox()
            # RegisterSuccess.setWindowTitle("Account Created!")
            # RegisterSuccess.setText("Account Has Been Successfully Created!")
            # button = RegisterSuccess.exec()
            CustomMessage("Success!","Account Has Been Successfully Created!\nPlease Check Your Email For Verification Code")
            return "Success"
        
        except Exception as err:
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"Internal Server Error at {datetime.now()}"}})
            internal_error(err)
            return err


        
    except Exception as err:
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"Internal Server Error at {datetime.now()}"}})
        internal_error(err)
        return err
    
    


    