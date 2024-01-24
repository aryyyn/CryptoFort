from PyQt6.QtWidgets import QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap,QIcon
def togglePassword(password_field: QLineEdit, show_password: QPushButton):

    if password_field.echoMode() == QLineEdit.EchoMode.Normal:
        icon_path = 'Logo/eye.png'
        hide = QPixmap(icon_path)
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
        show_password.setIcon(QIcon(hide))
    else:
        icon_path = 'Logo/eyecrossed.png'
        show = QPixmap(icon_path)
        password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        show_password.setIcon(QIcon(show))




