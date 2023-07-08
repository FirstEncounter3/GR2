from datetime import datetime, timedelta
import os

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDateTime
from requests import exceptions

from api.evo import (
    get_stores,
    get_receipts,
    get_receipt_by_uuid,
    get_all_goods,
    get_good_by_uuid,
)
from designe import child_window_designe
from decoding.decoding_assistant import decoder
from exceptions.error_messages import create_window_with_error_text
from helper import file_reader

time_pattern = "%Y-%m-%d %H:%M:%S"

doc_types = [
    "ACCEPT",
    "INVENTORY",
    "REVALUATION",
    "RETURN",
    "WRITE_OFF",
    "SELL",
    "PAYBACK",
    "BUY",
    "BUYBACK",
    "OPEN_TARE",
    "OPEN_SESSION",
    "CLOSE_SESSION",
    "POS_OPEN_SESSION",
    "CASH_INCOME",
    "CASH_OUTCOME",
    "X_REPORT",
    "Z_REPORT",
    "CORRECTION",
]


class ChildWindow(QDialog):
    def __init__(self, token):
        super().__init__()
        self.ui = child_window_designe.Ui_Dialog()
        self.ui.setupUi(self)
        self.token = token
        self.datetime_default()

        # radio_btn_default
        self.ui.receipt_btn.setChecked(True)
        self.ui.products_btn.toggled.connect(self.products_mode)
        self.ui.receipt_btn.toggled.connect(self.receipts_mode)

        # doc_types combobox
        self.ui.document_type_combobox.addItems(doc_types)
        self.ui.document_type_combobox.setCurrentIndex(doc_types.index("SELL"))

        # stores combobox
        self.ui.stores_combobox.addItems(get_stores(token))

        # buttons
        self.ui.ok_btn.clicked.connect(self.accept)
        self.ui.close_btn.clicked.connect(self.reject)
        self.ui.today_btn.clicked.connect(self.quick_pattern_today)
        self.ui.yesterday_btn.clicked.connect(self.quick_pattern_yesterday)
        self.ui.restore_btn.clicked.connect(self.restore_previous_query_parameters)

        # actions

    def datetime_default(self) -> None:
        """The function substitutes the time template"""
        self.ui.since_date_time.setDateTime(QDateTime.currentDateTime())
        self.ui.until_date_time.setDateTime(QDateTime.currentDateTime())

    def get_datetime(self) -> tuple:
        """Take the time specified by the user"""
        since_dt = datetime.strptime(
            self.ui.since_date_time.dateTime().toString("yyyy-MM-dd H:mm:ss"),
            time_pattern,
        )
        until_dt = datetime.strptime(
            self.ui.until_date_time.dateTime().toString("yyyy-MM-dd H:mm:ss"),
            time_pattern,
        )

        since_uts = int(since_dt.timestamp()) * 1000
        until_uts = int(until_dt.timestamp()) * 1000

        return (
            since_uts,
            until_uts,
            since_dt.strftime(time_pattern),
            until_dt.strftime(time_pattern),
        )

    def quick_pattern_today(self) -> None:
        today_date = datetime.now().strftime("%Y-%m-%d ")

        self.ui.since_date_time.setDateTime(
            datetime.strptime(today_date + "00:00:00", time_pattern)
        )
        self.ui.until_date_time.setDateTime(
            datetime.strptime(today_date + "23:59:59", time_pattern)
        )

    def quick_pattern_yesterday(self) -> None:
        today_date = datetime.now() - timedelta(days=1)
        yesterday_date = today_date.strftime("%Y-%m-%d ")

        self.ui.since_date_time.setDateTime(
            datetime.strptime(yesterday_date + "00:00:00", time_pattern)
        )
        self.ui.until_date_time.setDateTime(
            datetime.strptime(yesterday_date + "23:59:59", time_pattern)
        )

    def get_store_uuid(self) -> str:
        return self.ui.stores_combobox.currentText().split(",")[1].strip()

    def get_doc_type(self) -> str:
        return self.ui.document_type_combobox.currentText().strip()

    def make_a_request_for_all_doc_in_time(self) -> str:
        utc = self.get_datetime()
        store = self.get_store_uuid()
        doc_type = self.get_doc_type()
        try:
            return decoder(get_receipts(utc[0], utc[1], self.token, store, doc_type))
        except exceptions.HTTPError as e:
            create_window_with_error_text(e, "HTTP Error")

    def make_a_request_for_doc_by_uuid(self) -> str:
        store = self.get_store_uuid()
        receipt_uuid = self.ui.receipt_uuid_lineEdit.text().strip()
        try:
            return decoder(get_receipt_by_uuid(store, self.token, receipt_uuid))
        except exceptions.HTTPError as e:
            create_window_with_error_text(e, "HTTP Error")

    def make_a_request_for_all_goods(self) -> str:
        store = self.get_store_uuid()
        try:
            return decoder(get_all_goods(store, self.token))
        except exceptions.HTTPError as e:
            create_window_with_error_text(e, "HTTP Error")

    def make_a_request_for_good_by_uuid(self) -> str:
        store = self.get_store_uuid()
        product_uuid = self.ui.receipt_uuid_lineEdit.text().strip()
        try:
            return decoder(get_good_by_uuid(store, self.token, product_uuid))
        except exceptions.HTTPError as e:
            create_window_with_error_text(e, "HTTP Error")

    def save_request_to_file(self) -> None:
        utc = self.get_datetime()
        with open("metadata_file", "w", encoding="utf-8") as metadate_file:
            if self.ui.receipt_btn.isChecked():
                metadate_file.write(
                    str(
                        {
                            "since": utc[2],
                            "until": utc[3],
                            "token": self.token,
                            "doc_type": self.ui.document_type_combobox.currentIndex(),
                            "store": self.ui.stores_combobox.currentIndex(),
                            "receipt_uuid": self.ui.receipt_uuid_lineEdit.text(),
                            "product_uuid": "",
                        }
                    )
                )
            else:
                metadate_file.write(
                    str(
                        {
                            "since": utc[2],
                            "until": utc[3],
                            "token": self.token,
                            "doc_type": self.ui.document_type_combobox.currentIndex(),
                            "store": self.ui.stores_combobox.currentIndex(),
                            "receipt_uuid": "",
                            "product_uuid": self.ui.receipt_uuid_lineEdit.text(),
                        }
                    )
                )

    def restore_previous_query_parameters(self) -> None:
        meta_data_file = os.path.exists("metadata_file")
        if meta_data_file:
            metadata_file = file_reader.read_request_from_file()
            if self.ui.products_btn.isChecked():
                self.ui.stores_combobox.setCurrentIndex(metadata_file.get("store"))
                self.ui.receipt_uuid_lineEdit.setText(metadata_file.get("product_uuid"))
            else:
                self.ui.since_date_time.setDateTime(
                    datetime.strptime(metadata_file.get("since"), time_pattern)
                )
                self.ui.until_date_time.setDateTime(
                    datetime.strptime(metadata_file.get("until"), time_pattern)
                )
                self.ui.document_type_combobox.setCurrentIndex(
                    metadata_file.get("doc_type")
                )
                self.ui.stores_combobox.setCurrentIndex(metadata_file.get("store"))
                self.ui.receipt_uuid_lineEdit.setText(metadata_file.get("receipt_uuid"))

    def products_mode(self) -> None:
        self.ui.splitter_2.hide()
        self.ui.splitter_4.hide()
        self.ui.splitter_5.hide()
        self.ui.splitter_6.hide()
        self.ui.receipt_uuid_label.setText("UUID товара")
        self.ui.receipt_uuid_lineEdit.setToolTip("Поиск по UUID товара")
        self.adjustSize()

    def receipts_mode(self) -> None:
        self.ui.splitter_2.show()
        self.ui.splitter_4.show()
        self.ui.splitter_5.show()
        self.ui.splitter_6.show()
        self.ui.receipt_uuid_label.setText("UUID чека")
        self.ui.receipt_uuid_lineEdit.setToolTip("Поиск по UUID чека")
        self.adjustSize()
