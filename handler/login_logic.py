import requests
from PyQt6.QtWidgets import QMessageBox, QLineEdit

def loginLogic(email,password):
    if email.text() == "admin":
        if password.text() == "admin":
            print("Welcome to the admin pannel")
    else:
        print("Bad Email")
       


