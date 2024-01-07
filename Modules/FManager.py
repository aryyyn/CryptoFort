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
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys,pymongo, os, time
from gridfs import GridFS
from bson.binary import Binary
from Algorithm.ceasers_enhanced_algorithm import enhancedEncryption

client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["CryptoFort"]
collection = db["File_Details"]

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
        FileUpload.clicked.connect(lambda: self.UploadFileHandler(Email,FileUploadInfoLabel))

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

        self.show()
    
    def UploadFileHandler(self, Email,FileInfoLabel: QLabel ):
        count = collection.count_documents({"email": Email})
        if count == 1:
            dialog = QInputDialog()
            QMessageBox.information(dialog, "Error", "The system allows for the upload of only one file.\nDelete the current file to upload a new one.")
            dialog.accept()
            return
        
        FileDialog = QFileDialog()
        filename, _ = FileDialog.getOpenFileName()

        if filename:
            try:
                filesize = os.path.getsize(filename)
                basefilename = os.path.basename(filename)

                if (filesize > 16793598):
                    dialog = QInputDialog()
                    QMessageBox.information(dialog, "File too large!", "The Limit is 16mb.")
                    dialog.accept()
                    return
                
                Hello = QDialog()
                Hello.setWindowTitle("Enter A Password")
                layout = QVBoxLayout()
                password_input = QLineEdit()
                layout.addWidget(password_input)

                submitbtm = QPushButton("Submit")
                layout.addWidget(submitbtm)
                submitbtm.clicked.connect(Hello.accept)

                Hello.setLayout(layout)
                Hello.exec()

                epoch = str(time.time())
                EncryptionCode = epoch.split('.')[1]
                EncryptionCode+=EncryptionCode
                EncryptionCode+=EncryptionCode
                password = password_input.text()
                encrypted_password = enhancedEncryption(password, EncryptionCode)
                
                
                if (password):

                    
                    with open(filename, 'rb') as file:
                        file_content = file.read()

                        binary_content = Binary(file_content)

                        document = {
                            "email": Email,
                            "filename": basefilename,
                            "content": binary_content,
                            "password": encrypted_password
                        }

                        result = collection.insert_one(document)
                        dialog = QInputDialog()
                        QMessageBox.information(dialog,"Success!","Your File Has Been Uploaded!")
                        FileInfoLabel.setText(f"Current File In Database: {basefilename}")

                        dialog.accept()
                else:
                    dialog = QInputDialog()
                    QMessageBox.information(dialog,"Error","Please Enter A Password!")
                    dialog.accept()

            except Exception as err:
                print(err)





