from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QListView,
                             QComboBox, QWidget, QVBoxLayout, QMessageBox)

from PyQt5.QtCore import QSize, Qt, QStringListModel

import sys

class MainW(QWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()

        self.setFixedSize(400, 300)
        self.setWindowTitle("Weather app.")

        layout = QVBoxLayout()

        label = QLabel("Welcome to my weather app")
        label.setAlignment(Qt.AlignTop)
        layout.addWidget(label) 

        self.setLayout(layout)     

        self.show()

    #def initUI(self):
        

if __name__ == "__main__":

    app = QApplication([]) # No parameters used, as of yet
    ex = MainW()
    sys.exit(app.exec()) # Starting the event loop. exec_ is archaic.