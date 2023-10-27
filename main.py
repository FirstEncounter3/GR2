#!/usr/bin/python3

import json
import sys
import os
import platform

import requests

from PyQt5 import QtWidgets
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QFileDialog

from child_window.child import ChildWindow
from decoding.decoding_assistant import decoder
from designe import main_window_designe
from exceptions.error_messages import create_window_with_error_text
from exceptions.custom_exceptions import EmptyTokenField
from helper import file_reader

VERSION = "2.0.0"
MSG_LSTN = " ● Listen..."
MSG_DN = " ● Done!"
MSG_ER = " ● Error!"
MSG_DT_RC = " ● Data received!"
MSG_NO_DT = " ● No data!"
MSG_NOT_SAVED = " ● Not saved! "

COLOR_DEFAULT = "#F0FFFF"
COLOR_DONE = "#20E631"
COLOR_ERROR = "#DC143C"
COLOR_DT_RC = "#FF8C00"


class GR2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window_designe.Ui_MainWindow()
        self.ui.setupUi(self)

        # version
        self.ui.label_version.setText(VERSION)

        # set_status_bar_default
        self.ui.statusbar.showMessage(MSG_LSTN)

        # buttons
        self.ui.btn_backspace.clicked.connect(self.clear_token_field)
        self.ui.btn_clear.clicked.connect(self.clear_json_field)
        self.ui.btn_save_as.clicked.connect(self.save_as)
        self.ui.btn_paste.clicked.connect(self.paste)
        self.ui.btn_decode.clicked.connect(self.decode_without_saving)
        self.ui.btn_get.clicked.connect(self.to_get_data)

    # actions

    def status_bar_msgs(self, color: str, msg: str) -> None:
        """Sets the text and color of the status bar message"""
        self.ui.statusbar.setStyleSheet(f"color:{color}")
        self.ui.statusbar.showMessage(msg)

    def check_token_input(self) -> bool:
        """Check for a non-empty string in the token field"""
        if self.ui.lineEdit_token.text().strip():
            return True
        else:
            raise EmptyTokenField("Передана пустая строка в поле для токена")

    def clear_token_field(self) -> None:
        self.ui.lineEdit_token.clear()

    def clear_json_field(self) -> None:
        self.ui.textEdit_json.clear()
        self.status_bar_msgs(COLOR_DEFAULT, MSG_LSTN)

    def save_as(self) -> None:
        """Save formatted json to file"""
        raw_json = self.ui.textEdit_json.toPlainText()
        destination = QFileDialog.getSaveFileName(
            self, "Save file", "magic_json", "json (*.json)"
        )
        try:
            if platform.system() == 'Linux':
                with open(destination[0]+'.json', "w", encoding="utf-8") as f:
                    f.write(decoder(raw_json))
                self.status_bar_msgs(COLOR_DONE, MSG_DN)
            else:
                with open(destination[0], "w", encoding="utf-8") as f:
                    f.write(decoder(raw_json))
                self.status_bar_msgs(COLOR_DONE, MSG_DN)
        except FileNotFoundError:
            self.status_bar_msgs(COLOR_DEFAULT, MSG_NOT_SAVED)
        except json.decoder.JSONDecodeError as e:
            create_window_with_error_text(e, "Вставлен некорректный JSON")
            self.status_bar_msgs(COLOR_ERROR, MSG_ER)

    def paste(self) -> None:
        self.ui.textEdit_json.setText(QGuiApplication.clipboard().text())

    def decode_without_saving(self) -> None:
        """Perform serialization in the same window"""
        raw_json = self.ui.textEdit_json.toPlainText()
        try:
            self.ui.textEdit_json.clear()
            self.ui.textEdit_json.setText(decoder(raw_json))
            self.status_bar_msgs(COLOR_DONE, MSG_DN)
        except json.decoder.JSONDecodeError as e:
            create_window_with_error_text(e, "Вставлен некорректный JSON")
            self.ui.textEdit_json.setText(raw_json)
            self.status_bar_msgs(COLOR_ERROR, MSG_ER)

    def checking_a_previously_used_token(self) -> None:
        """Checking the existence of a previously used token and substituting it"""
        meta_data_file = os.path.exists("metadata_file")
        if meta_data_file:
            metadate_file = file_reader.read_request_from_file()
            self.ui.lineEdit_token.clear()
            self.ui.lineEdit_token.setText(metadate_file.get("token"))

    def create_window(self) -> int:
        self.child_window = ChildWindow(self.ui.lineEdit_token.text().strip())
        result = self.child_window.exec_()
        return result

    def goods(self) -> None:
        if len(self.child_window.ui.receipt_uuid_lineEdit.text()) == 36:
            self.ui.textEdit_json.setText(
                self.child_window.make_a_request_for_good_by_uuid()
            )
        else:
            self.ui.textEdit_json.setText(
                self.child_window.make_a_request_for_all_goods()
            )

    def receipts(self) -> None:
        if len(self.child_window.ui.receipt_uuid_lineEdit.text()) == 36:
            self.ui.textEdit_json.setText(
                self.child_window.make_a_request_for_doc_by_uuid()
            )
        else:
            self.ui.textEdit_json.setText(
                self.child_window.make_a_request_for_all_doc_in_time()
            )

    def to_get_data(self) -> None:
        try:
            self.check_token_input()

            if self.create_window():

                self.ui.textEdit_json.clear()

                if self.child_window.ui.products_btn.isChecked():
                    self.goods()
                else:
                    self.receipts()

                self.child_window.save_request_to_file()
                self.status_bar_msgs(COLOR_DT_RC, MSG_DT_RC)
            else:
                self.status_bar_msgs(COLOR_DEFAULT, MSG_NO_DT)
        except EmptyTokenField as e:
            create_window_with_error_text(e, "Empty token field")
        except requests.exceptions.HTTPError as e:
            create_window_with_error_text(e, "HTTP Error")


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = GR2()
    window.show()
    window.checking_a_previously_used_token()
    app.exec_()


if __name__ == "__main__":
    main()
