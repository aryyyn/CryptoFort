import requests
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog,QDialogButtonBox,QVBoxLayout,QLabel
import time
import pymongo
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption

def loginLogic(eemail, epassword):
    email = eemail.text().lower()
    password = epassword.text()

    client = pymongo.MongoClient("mongodb://localhost:27017/")  
    db = client["CryptoFort"] 
    collection = db["User_Details"]

    count = collection.count_documents({"email": email})

    if count == 0:
        return "No Email Found"
    else:
        results = collection.find({"email": email})
        for data in results:
            DecryptedPassword = data["password"]
            Encryptioncode = data ["Encryption_code"]
            Password = enhancedEncryption(password, Encryptioncode)
            
            if DecryptedPassword == Password:
                return "Correct Password"
            else:
                return "InCorrect Password"





       


