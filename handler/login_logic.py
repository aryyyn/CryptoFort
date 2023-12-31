import requests
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QDialog,QDialogButtonBox,QVBoxLayout,QLabel
import time


def loginLogic(email,password):
    if email.text() == "admin":
        if password.text() == "admin":
            dlg = QMessageBox()
            dlg.setWindowTitle("Success")
            dlg.setText("Logging in!")
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.hide()
            button = dlg.exec()
           
    else:
        dlg = QMessageBox()
        dlg.setWindowTitle("Error")
        dlg.setText("Wrong Email Or Pass")
        button = dlg.exec()
       


