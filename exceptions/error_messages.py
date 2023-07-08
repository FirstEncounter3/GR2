from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui


def create_window_with_error_text(e, text):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(".\\ico/cloud_72.png"))
    msg = QMessageBox()
    msg.setWindowTitle("Ошибка")
    msg.setWindowIcon(icon)
    msg.setText(text)
    msg.setInformativeText(str(e))
    msg.setIcon(QMessageBox.Information)
    msg.exec_()
