from PyQt6.QtWidgets import QLineEdit

def togglePassword(password_field: QLineEdit):
    if password_field.echoMode() == QLineEdit.EchoMode.Normal:
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
    else:
        password_field.setEchoMode(QLineEdit.EchoMode.Normal)
