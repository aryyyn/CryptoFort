from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sys


def loginWindowLogic(app):
    print("working")
    window = QMainWindow()

    window.setFixedSize(750,550)
    window.setWindowTitle("CryptoFort | Login")
    icon = QIcon("logo/logo.png")
    window.setWindowIcon(icon)
    window.show()
    app.exec()

    