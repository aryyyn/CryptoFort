from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
    QFileDialog,
    QInputDialog,
    QDialog,
    QLineEdit,
    QMessageBox
    
)
from PyQt6.QtGui import QIcon,QPixmap
from PyQt6.QtCore import Qt
import sys,pymongo, os, time
from gridfs import GridFS
from bson.binary import Binary
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption
from datetime import datetime
from handler.showPassword import togglePassword

client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"]
collection = db["File_Details"]
logs_collection = db["User_Logs"]

class FManagerWindow(QMainWindow):
    def __init__(self, Email):
        super().__init__()
        self.init_ui(Email)

    def init_ui(self, Email):

        self.setFixedSize(400, 200)
        self.setWindowTitle("CryptoFort | FManager")
        icon = QIcon("logo/logo.png")
        self.setWindowIcon(icon)

        self.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
                font-size: 14px;
            }

            QPushButton {
                border: 2px solid #00FF00; 
                border-radius: 8px;
                background: #111111;
                min-width: 100px;
                color: #00FF00; 
                padding: 8px 16px;
            }

            QPushButton:hover {
                background: #222222;
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
        count = collection.count_documents({"email": Email})
        FileUploadInfoLabel = QLabel()
        if count == 0:
            FileUploadInfoLabel.setText("No File Uploaded")
        else:
            results = collection.find({"email": Email})
            for data in results:
                fileName = data["filename"]
            FileUploadInfoLabel.setText(f"Current File In Database: {fileName}")

        FileUpload = QPushButton("Upload File")
        

        FooterButtonLayout = QHBoxLayout()
        GetCurrentFileBtn = QPushButton("Get Current DB File")
        DeleteCurrentFileBtn = QPushButton("Delete Current DB File")

        FooterButtonLayout.addWidget(GetCurrentFileBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        FooterButtonLayout.addWidget(DeleteCurrentFileBtn, alignment=Qt.AlignmentFlag.AlignRight)

        FileUpload.setFixedHeight(40)
        GetCurrentFileBtn.setFixedHeight(40)
        DeleteCurrentFileBtn.setFixedHeight(40)

        layout.addWidget(FileUploadInfoLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(FileUpload, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(FooterButtonLayout)

        FileUpload.clicked.connect(lambda: self.UploadFileHandler(Email,FileUploadInfoLabel))
        DeleteCurrentFileBtn.clicked.connect(lambda: self.deleteCurrentFile(Email,FileUploadInfoLabel))
        GetCurrentFileBtn.clicked.connect(lambda:self.getCurrentFile(Email))

        self.show()

    def passInput(self):
        Hello = QDialog()
        Hello.setStyleSheet("""
            * {
                color: #00FF00; 
                background: #000000; 
                font-size: 14px;
            }

            QPushButton {
                border: 2px solid #00FF00; 
                border-radius: 8px;
                background: #111111;
                min-width: 100px;
                color: #00FF00; 
                padding: 8px 16px;
            }

            QPushButton:hover {
                background: #222222;
            }

            QLabel {
                color: #00FF00; 
                font-size: 16px;
                font-weight: bold;
            }
        """)
        Hello.setWindowTitle("Enter A Password")
        Hello.setBaseSize(200,200)
        layout = QVBoxLayout(Hello)
        HorizontalLayout = QHBoxLayout(Hello)
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setFixedWidth(200)

        icon_path = 'Logo/eye.png'
        hide = QPixmap(icon_path)

        ShowPasswordButton = QPushButton(QIcon(hide),"")
        EnterPasswordLabel = QLabel("Enter File Password: ")
        HorizontalLayout.addWidget(EnterPasswordLabel)
        HorizontalLayout.addWidget(password_input)
        HorizontalLayout.addWidget(ShowPasswordButton)
        
        layout.addLayout(HorizontalLayout)

        submitbtm = QPushButton("Submit")
        submitbtm.setFixedSize(20,50)
        layout.addWidget(submitbtm, alignment=Qt.AlignmentFlag.AlignCenter)
        submitbtm.clicked.connect(Hello.accept)
        ShowPasswordButton.clicked.connect(lambda: togglePassword(password_input, ShowPasswordButton))
        Hello.setLayout(layout)
        Hello.exec()
        return password_input.text()
    
    def UploadFileHandler(self, Email,FileInfoLabel: QLabel ):
        count = collection.count_documents({"email": Email})
        if count == 1:
            QMessageBox.critical(self, "Error", "The system allows for the upload of only one file.\nDelete the current file to upload a new one.")
            return
        
        FileDialog = QFileDialog()
        filename, _ = FileDialog.getOpenFileName()

        if filename:
            try:
                filesize = os.path.getsize(filename)
                basefilename = os.path.basename(filename)

                if (filesize > 16793598):
                    logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User fails to upload file due to file size limit at {datetime.now()}"}})
                    QMessageBox.critical(self, "File too large!", "The Limit is 16mb.")
                    return
                
                password_input = self.passInput()

                epoch = str(time.time())
                EncryptionCode = epoch.split('.')[1]
                EncryptionCode+=EncryptionCode
                EncryptionCode+=EncryptionCode
                password = password_input
                encrypted_password = enhancedEncryption(password, EncryptionCode)
                
                
                if (password):

                    
                    with open(filename, 'rb') as file:
                        file_content = file.read()

                        binary_content = Binary(file_content)

                        document = {
                            "email": Email,
                            "filename": basefilename,
                            "content": binary_content,
                            "password": encrypted_password,
                            "Encryption_code": EncryptionCode
                        }

                        result = collection.insert_one(document)
                        logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User uploads their file to the database at {datetime.now()}"}})
                        QMessageBox.information(self,"Success!","Your File Has Been Uploaded!")
                        FileInfoLabel.setText(f"Current File In Database: {basefilename}")
                else:
                    QMessageBox.information(self,"Error","Please Enter A Password!")

            except Exception as err:
                print(err)



    def deleteCurrentFile(self,Email,FileInfoLabel: QLabel ):
        count = collection.count_documents({"email": Email})
        if(count == 0):
            QMessageBox.information(self, "Error", "No File Found")
            return
        
        else:
            password = self.passInput()
            results = collection.find({"email": Email})
            for data in results:
                encrypted_db_password = data["password"]
                EncryptionCode = data["Encryption_code"]
            encrypted_password = enhancedEncryption(password, EncryptionCode) 

            if (encrypted_password != encrypted_db_password):
                logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User fails to match passwords while deleting file from database at {datetime.now()}"}})
                QMessageBox.critical(self, "Error", "Passwords do not match!")
                return
            
            result = collection.delete_one({"email": Email})
            if (result.deleted_count > 0):
                FileInfoLabel.setText("No File Uploaded")
                logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User deletes the uploaded file at {datetime.now()}"}})
                QMessageBox.information(self, "Success", "File has been deleted successfully!")

            else:
                logs_collection.update_one({"username": Email}, {"$push": {"logs": f"internal server error at {datetime.now()}"}})
                QMessageBox.critical(self, "Error", "An Internal Error Has Occurred!\nPlease Try Again Later")
                return "Internal Error Has Occurred"
            
    
    def getCurrentFile(self,Email):
        count = collection.count_documents({"email": Email})
        if(count == 0):
            logs_collection.update_one({"username": Email}, {"$push": {"logs": f"No file found for user in FManager Module at {datetime.now()}"}})
            QMessageBox.critical(self, "Error", "No File Found")
            return
        
        else:
            password = self.passInput()
            results = collection.find({"email": Email})
            for data in results:
                encrypted_db_password = data["password"]
                EncryptionCode = data["Encryption_code"]
                filecontent = data["content"]
            encrypted_password = enhancedEncryption(password, EncryptionCode) 

            if (encrypted_password != encrypted_db_password):
                logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User fails to mactch passwords while retrieving file from database at {datetime.now()}"}})
                QMessageBox.critical(self, "Error", "Passwords do not match!")
                return
            
            filepath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
            
            if filepath:
                try:
                    with open(filepath, 'wb') as file:
                        file.write(filecontent)
                    logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User retrieves file at {datetime.now()}"}})
                    QMessageBox.information(self, "Success", "File Saved Successfully")
                except Exception as err:
                    logs_collection.update_one({"username": Email}, {"$push": {"logs": f"User fails to save retrieved file at {datetime.now()}"}})
                    QMessageBox.critical(self, "Error", f"Failed to save file: {err}")
            
            







            

        





