import requests
from PyQt6.QtWidgets import QMessageBox

def joke():
    try:
        response = requests.get("https://api.chucknorris.io/jokes/random")
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Joke")
        msg_box.setText(response.text)
        msg_box.exec()
    except Exception as err:
        errorbox = QMessageBox()
        errorbox.setWindowTitle("Error")
        errorbox.setText(err)
