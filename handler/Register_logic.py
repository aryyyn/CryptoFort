import pymongo
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog,QDialogButtonBox,QVBoxLayout,QLabel
import socket
import requests
import random, time
from validate_email_address import validate_email
from datetime import datetime
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption
from handler.send_email import email_verification

def email_validator(email):
    is_valid = validate_email(email)
    return is_valid

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
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = client["CryptoFort"] 
        collection = db["User_Details"]

        email = eemail.text().lower()
        password = epassword.text()
        repassword = erepassword.text()

        count = collection.count_documents({"email": email})
        

        if (email_validator(email)) == False:
            hi = QDialog()
            QMessageBox.critical(hi, "Error", "Invalid Email")
            return "Invalid Email"
        
        if (count>0):
            EmailAlreadyRegistered = QMessageBox()
            EmailAlreadyRegistered.setWindowTitle("Error")
            EmailAlreadyRegistered.setText("Email Has Already Been Registered")
            button = EmailAlreadyRegistered.exec()
            return "Email Already Registered"
        

        


        if (password!=repassword):
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
            "is_Verified": "False",
            "Verification_code": random_number

            }
            collection.insert_one(user_data)

            RegisterSuccess = QMessageBox()
            RegisterSuccess.setWindowTitle("Account Created!")
            email_verification(email,random_number)
            RegisterSuccess.setText("Account Has Been Successfully Created!")
            button = RegisterSuccess.exec()
            return "Success"
        
        except Exception as err:
            internal_error()
            return err


        
    except Exception as err:
        internal_error()
        return err
    
    


    