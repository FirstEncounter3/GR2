import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

import designe

VERSION = '1.9.9'


class GR2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = designe.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_version.setText(VERSION)
        self.setWindowTitle('GNRQT')
        self.setWindowIcon(QIcon('ico/cloud_16.png'))

        self.ui.lineEdit.setPlaceholderText('00000000-0000-0000-0000-000000000000')
        self.ui.textEdit.setPlaceholderText('{"key": "value"}')

        self.ui.statusbar.showMessage('Listen...')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GR2()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
