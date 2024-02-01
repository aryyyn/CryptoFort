import requests
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QHBoxLayout,QDialog,QDialogButtonBox,QVBoxLayout,QLabel,QInputDialog,QPushButton
from PyQt6.QtCore import Qt
import time
import pymongo
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption
import sys, random
from handler.send_email import email_verification
from dotenv import load_dotenv
import os,pyotp,requests
from datetime import datetime

load_dotenv()

client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"] 
collection = db["User_Details"]
logs_collection = db["User_Logs"]
IP_collection = db["IP_Details"]

loginMessage = "InCorrect Password"
VerificationMessage = "Wrong Code"

def get_ip_address():
    IP = requests.get("https://ipv4.icanhazip.com").text.strip()
    return IP

def user_login_logs(email):
    log_entry = f"User logged in at {datetime.now()} with IP address {get_ip_address()}"
    logs_collection.update_one({"username": email}, {"$push": {"logs": log_entry}})


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


def loginLogic(eemail, epassword):

    IP = get_ip_address()
    
    
    IPResult = IP_collection.count_documents({"IP": IP})

    if(IPResult == 0):
        IP_Data = {
            "IP": IP,
            "IP_Attempt_Count": 1,
            "isBanned": False,
            "Time": "2024-01-28 19:46:11.978236"

        }
    
        IP_collection.insert_one(IP_Data)
    
    
    isBannedResult = IP_collection.find_one({"IP": IP})
    isIPBanned = isBannedResult.get("isBanned")
    IPTime = isBannedResult.get("Time")

    specified_time = datetime.strptime(IPTime, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.now()
    time_difference = specified_time - current_time
    hours_passed = int(time_difference.total_seconds() / 3600)

    if(isIPBanned and hours_passed<1):
        CustomMessage("IP Banned","Your IP is been banned due to multiple login attempts.")
        return "IP Banned."

    
    
    email = eemail.text().lower()
    password = epassword.text()


    if email == "":
        CustomMessage("Error","Email Field Cannot be Empty")
        return "Email Field Empty"
    
    if password == "":
        CustomMessage("Error","Password Field Cannot be Empty")
        return "Password Field Empty"
    
    count = collection.count_documents({"email": email})
   
    if count == 0:
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"User enters an invalid email at {datetime.now()}"}})
        CustomMessage("Error","No Data Found With This Email")
        return "Password Field Empty"
    else:
        results = collection.find({"email": email})
        for data in results:
            IsVerified = data["is_Verified"]
            DecryptedPassword = data["password"]
            Encryptioncode = data ["Encryption_code"]
            Is2faEnabled = data["is_2fa_enabled"]
            Last_LoggedIn_IP = data["Last_LoggedIn_IP"]
            
            Password = enhancedEncryption(password, Encryptioncode)

            if DecryptedPassword == Password:
                if (IsVerified):
                    if(str(get_ip_address())==str(Last_LoggedIn_IP)):
                        if(Is2faEnabled):
                            Verify2fa = QDialog()
                            Verify2fa.setStyleSheet("""
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
                            Verify2fa.setWindowTitle("User Verification")
                            Verify2fa.setBaseSize(300,300)

                            layout = QVBoxLayout(Verify2fa)

                            FooterLayout = QHBoxLayout()
                            HeaderLayout = QHBoxLayout()

                            titleLabel = QLabel("Enter the 2fa code: ")
                            titeltext = QLineEdit()
                            SubmitButton = QPushButton("Submit")

                            HeaderLayout.addWidget(titleLabel)
                            HeaderLayout.addWidget(titeltext)
                            FooterLayout.addWidget(SubmitButton, alignment=Qt.AlignmentFlag.AlignCenter)

                            layout.addLayout(HeaderLayout)
                            layout.addLayout(FooterLayout)
                            SubmitButton.clicked.connect(lambda: authCheck(email,titeltext,Verify2fa))
                            Verify2fa.exec()
                            
                            

                            
                            
                            if (loginMessage == "Correct Password"):
                                user_login_logs(email)
                                return "Correct Password"
                            else:
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
                                QMessageBox.information(dialog, "Wrong Code", "Please Try Again")

                        else:
                            user_login_logs(email)
                            return "Correct Password"
                    else:
                        random_number = random.randint(000000, 999999)
                        email_verification(email,random_number)
                        collection.update_one(
                            {"email": data["email"]},  
                            {
                                "$set": {
                                    "is_Verified": False,
                                    "Verification_code": random_number
                                }
                            }
                        )
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
                        QMessageBox.information(dialog, "New Location Detected", "Please Check Your Email For The Verification Code and ReLogin")
                        dialog.accept()
                else:
                    NotVerified = QDialog()
                    NotVerified.setStyleSheet("""
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
            
                    NotVerified.setWindowTitle("Verify Your Email")
                    NotVerified.setBaseSize(300,300)

                    layout = QVBoxLayout(NotVerified)

                    HeaderLayout = QVBoxLayout()
                    FooterLayout = QVBoxLayout()

                    EnterCodeLabel = QLabel("Enter the code that was sent to your email: ")
                    EnterCode = QLineEdit()

                    HeaderLayout.addWidget(EnterCodeLabel)
                    HeaderLayout.addWidget(EnterCode)

                    CodeSubmit = QPushButton("Submit")
                    CodeSubmit.setBaseSize(50,25)

                    ResendCode = QPushButton("Resend Code")
                    ResendCode.setBaseSize(50,25)

                    FooterLayout.addWidget(CodeSubmit, alignment=Qt.AlignmentFlag.AlignCenter)
                    FooterLayout.addWidget(ResendCode, alignment=Qt.AlignmentFlag.AlignCenter)

                    layout.addLayout(HeaderLayout)
                    layout.addLayout(FooterLayout)

                    CodeSubmit.clicked.connect(lambda: codeCheck(email, EnterCode,NotVerified))
                    ResendCode.clicked.connect(lambda: resendCode(email))
                    NotVerified.exec()

                    if VerificationMessage == "Correct Password":
                        pass
                    else:
                        return "Error"

            else:
                IP = get_ip_address()
                IPResult = IP_collection.count_documents({"IP": IP})

                if(IPResult == 0):
                    IP_Data = {
                        "IP": IP,
                        "IP_Attempt_Count": 1,
                        "isBanned": False,
                        "Time": "2024-01-28 19:46:11.978236"

                    }
                    
                    IP_collection.insert_one(IP_Data)
                    logs_collection.update_one({"username": email}, {"$push": {"logs": f"User enters an invalid password at {datetime.now()}"}})
                    CustomMessage("Error","Wrong Passowrd\nPlease Re-Check Your Password And Try Again.")


                else:


                    IPResult = IP_collection.find({"IP": IP})
                    for data in IPResult:
                        IP_Attempt_Count = int(data["IP_Attempt_Count"])
                        isBanned = data["isBanned"]
                        Time = data["Time"]

                        specified_time = datetime.strptime(Time, "%Y-%m-%d %H:%M:%S.%f")
                        current_time = datetime.now()
                        time_difference = specified_time - current_time
                        hours_passed = int(time_difference.total_seconds() / 3600)
                        # print(hours_passed)
                        
                        
                        if isBanned and hours_passed >= 1:
                            IP_collection.update_one(
                            {"IP": IP},
                            {
                                "$set": {
                                    "IP_Attempt_Count": 1,
                                    "isBanned": False
                                }
                                }
                            )
                            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User enters an invalid password at {datetime.now()}"}})
                            CustomMessage("IP Banned","Wrong Passowrd\nPlease Re-Check Your Password And Try Again.")
                            return "Wrong Password"


                        if IP_Attempt_Count>=10:
                            if not isBanned:
                                IP_collection.update_one(
                                {"IP": IP},
                                {
                                    "$set": {
                                        "isBanned": True,
                                        "Time": str(datetime.now())
                                    }
                                    }
                                )
                                logs_collection.update_one({"username": email}, {"$push": {"logs": f"User gets IP banned at {datetime.now()} with IP: {IP}"}})
                                CustomMessage("IP Banned","Too Many Login Attempts\nYour IP has been banned due to multiple login attempts.")

                        if isBanned:
                            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User enters an invalid password at {datetime.now()}"}})
                            CustomMessage("IP Banned","Too Many Login Attempts\nYour IP has been banned due to multiple login attempts.")

                        if(not isBanned):
                            IP_collection.update_one(
                            {"IP": IP},
                            {"$inc": {"IP_Attempt_Count": 1}})
 

                        if IP_Attempt_Count<10 and not isBanned:
                            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User enters an invalid password at {datetime.now()}"}})
                            CustomMessage("Error","Wrong Passowrd\nPlease Re-Check Your Password And Try Again.")
                            return "Wrong Password"

                        # if isBanned and hours_passed > 1:
                        #     IP_collection.update_one(
                        #     {"IP": IP},
                        #     {
                        #         "$set": {
                        #             "IP_Attempt_Count": 1,
                        #             "isBanned": False
                        #         }
                        #         }
                        #     )
                        #     logs_collection.update_one({"username": email}, {"$push": {"logs": f"User enters an invalid password at {datetime.now()}"}})
                        #     CustomMessage("Error","Wrong Passowrd\nPlease Re-Check Your Password And Try Again.")
                        #     return "Wrong Password"
                        


                            



          
                    
               
            
                

                
def authCheck(email, InputCode,Verify2fa: QDialog):
    log_entry = f"User is asked for 2fa verification at {datetime.now()}"
    logs_collection.update_one({"username": email}, {"$push": {"logs": log_entry}})

    global loginMessage
    results = collection.find({"email": email})
    for data in results:
        backupcode = data["2fa_backupcode"]
    key = os.environ.get("SECRET_CODE_2FA")
    topt = pyotp.TOTP(key)
    RealCode = topt.now()
    InputCode = InputCode.text()
    if(str(InputCode) == str(RealCode) or str(InputCode) == str(backupcode)):
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"User inserted a correct 2fa code {RealCode} at {datetime.now()}"}})
        loginMessage = "Correct Password"
        Verify2fa.accept()
    else:
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"User fails to enter the 2fa code at {datetime.now()}"}})
        loginMessage = "ReCheck Code"
        Verify2fa.accept()
    pass
    # QMessageBox.information("Verification Success", "Code Verified Successfully!\nPlease ReLogin")

def codeCheck(email, InputCode,NotVerified: QDialog):
    try:
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"User is checked for the verification code at {datetime.now()}"}})
        results = collection.find({"email": email})
        global VerificationMessage
        for data in results:
            Code = data["Verification_code"]
            if (int(InputCode.text()) == int(Code)):
                dialog = QInputDialog()
                logs_collection.update_one({"username": email}, {"$push": {"logs": f"User's account is verified at {datetime.now()}"}})
                QMessageBox.information(dialog, "Verification Success", "Account Verified Successfully!")
                collection.update_one({"email": email},{"$set": {"is_Verified": True, "Last_LoggedIn_IP":get_ip_address()}})
                VerificationMessage = "Correct Password"
                NotVerified.accept()

                
            else:
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
                logs_collection.update_one({"username": email}, {"$push": {"logs": f"User inserts a wrong code at {datetime.now()}"}})
                # QMessageBox.information(dialog, "Error", "Wrong Code")
                CustomMessage("Error","Invalid Code.")

    except Exception as err:
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
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"User encounters an unknown error at {datetime.now()}"}})
        QMessageBox.information(dialog, "Error", "There Has Been An Error While Processing Your Request\nPlease Try Again")
            

def resendCode(email):
    try:
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"User clicks on the reset code at {datetime.now()}"}})
        random_number = random.randint(000000, 999999)
        results = collection.find({"email": email})
        for data in results:
            collection.update_one({"email": email},{"$set": {"Verification_code": random_number}})
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
            email_verification(email,random_number)
            logs_collection.update_one({"username": email}, {"$push": {"logs": f"User receives a code {random_number} in their email at {datetime.now()}"}})
            QMessageBox.information(dialog, "Code Reset Successful", "Please Check Your Email For The New Code")

    except Exception as err:
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
        logs_collection.update_one({"username": email}, {"$push": {"logs": f"User encounters an unknown error at {datetime.now()}"}})
        QMessageBox.information(dialog, err, "There Has Been An Error While Processing Your Request\nPlease Try Again")



                






       


