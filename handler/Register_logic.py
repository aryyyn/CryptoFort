import pymongo
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog,QDialogButtonBox,QVBoxLayout,QLabel
import socket
import requests
import random

def get_ip_address():
    IP = requests.get("https://ipv4.icanhazip.com").text.strip()
    print(IP)
    return IP

def registerLogic(eemail,epassword,erepassword):
    try:
        email = eemail.text()
        password = epassword.text()
        repassword = erepassword.text()

        if (password!=repassword):
            PasswordMismatch = QMessageBox()
            PasswordMismatch.setWindowTitle("Error")
            PasswordMismatch.setText("Password dont match")
            button = PasswordMismatch.exec()
            return "Password Mismatch"
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")  
        db = client["CryptoFort"] 
        collection = db["User_Details"]
        
        IP = get_ip_address() 
        LastLoggedInIP = IP
        user_data = {
        "email": email,
        "password": password,
        "Registration_IP": IP,
        "Last_LoggedIn_IP": LastLoggedInIP,
        "Secret_Code":123456789123456789,

        }


        collection.insert_one(user_data)
    except Exception as err:
        return err
    
    


    