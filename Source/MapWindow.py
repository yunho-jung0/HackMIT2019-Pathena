import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui


class MapWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.statusBar()
        placeholder = QAction('Exit', self)

        menu = self.menuBar()
        fileMenu = menu.addMenu('&File')
        fileMenu.addAction(placeholder)

        self.start_loc = ''
        self.destination_loc = ''
        self.setWindowTitle("DangerMap_demo")
        self.set_label_and_textbox()
        self.set_submit_button()

    def set_submit_button(self):
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.move(605, 40)
        self.submit_button.clicked.connect(self.__register_loc)

    @pyqtSlot()
    def __register_loc(self):
        self.start_loc = self.start_box.text()
        self.destination_loc = self.destination_box.text()
        self.start_box.setText('')
        self.destination_box.setText('')

        print(self.start_loc)
        print(self.destination_loc)

    def set_label_and_textbox(self):
        self.start_label = QLabel("Starting Location", self)
        self.start_label.move(20, 20)
        self.start_box = QLineEdit(self)
        self.start_box.resize(250, 20)
        self.start_box.move(20, 60)

        self.destination_label = QLabel("Ending Location", self)
        self.destination_label.move(320, 20)
        self.destination_box = QLineEdit(self)
        self.destination_box.resize(250, 20)
        self.destination_box.move(320, 60)
