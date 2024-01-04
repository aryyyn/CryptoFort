from PyQt6.QtWidgets import QLineEdit, QPushButton

def togglePassword(password_field: QLineEdit, show_password: QPushButton):
    if password_field.echoMode() == QLineEdit.EchoMode.Normal:
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
        show_password.setText("SHOW")
    else:
        password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        show_password.setText("HIDE")
