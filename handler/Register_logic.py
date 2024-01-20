import pymongo
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog,QDialogButtonBox,QVBoxLayout,QLabel
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
    print(parsed_email_data)
    if (str((parsed_email_data["valid"])) == "True"):
        if (str((parsed_email_data["text"])) == "Looks okay"):
            if(str((parsed_email_data["disposable"])) == "False"):
                return True
    else:
        return False
        

def getDateAndTime():
    DateAndTime = datetime.now()
    return DateAndTime

def internal_error():
    InternalError = QMessageBox()
    InternalError.setWindowTitle("Error")
    InternalError.setText("An Internal Error Has Occurred\nPlease Try Again Later")
    button = InternalError.exec()

def get_ip_address():
    IP = requests.get("https://ipv4.icanhazip.com").text.strip()
    return IP

def registerLogic(eemail,epassword,erepassword):
    try:
        


        email = eemail.text().lower()
        password = epassword.text()
        repassword = erepassword.text()
        logs_entry = {"username": email.lower(), "logs": ["User logs:"]}
        logs_collection.insert_one(logs_entry)

        count = collection.count_documents({"email": email})
        

        if (email_validator(email)):
            pass
        else:
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User tries registering with an invalid email at {datetime.now()} with IP {get_ip_address()}"}})
            hi = QDialog()
            QMessageBox.critical(hi, "Error", "Invalid Email")
            return "Invalid Email"
        
        if (count>0):
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User tries registering with an already registered email at {datetime.now()} with IP {get_ip_address()}"}})
            EmailAlreadyRegistered = QMessageBox()
            EmailAlreadyRegistered.setWindowTitle("Error")
            EmailAlreadyRegistered.setText("Email Has Already Been Registered")
            button = EmailAlreadyRegistered.exec()
            return "Email Already Registered"
        

        


        if (password!=repassword):
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"Users passwords do not match while registering at {datetime.now()} with IP {get_ip_address()}"}})
            PasswordMismatch = QMessageBox()
            PasswordMismatch.setWindowTitle("Error")
            PasswordMismatch.setText("Passwords dont match")
            button = PasswordMismatch.exec()
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
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User with {email.lower()} creates a new account at {datetime.now()} with IP {IP}"}})
            RegisterSuccess = QMessageBox()
            RegisterSuccess.setWindowTitle("Account Created!")
            email_verification(email,random_number)
            RegisterSuccess.setText("Account Has Been Successfully Created!")
            button = RegisterSuccess.exec()
            return "Success"
        
        except Exception as err:
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"Internal Server Error at {datetime.now()}"}})
            internal_error()
            return err


        
    except Exception as err:
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"Internal Server Error at {datetime.now()}"}})
        internal_error()
        return err
    
    


    