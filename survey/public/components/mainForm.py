from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from src.widget.navbar import NavBar


class MainForm(QWidget):
    def __init__(self, central=None):
        QWidget.__init__(self, central)
        self.central = central

        self.navBar = NavBar(central)

        self.layoutContents = QVBoxLayout()
        self.layoutContents.addWidget(QLabel(" "), 10)
        self.layoutContents.addWidget(self.central.buttonFooter, alignment=Qt.AlignCenter)
        self.layoutContents.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.addWidget(self.navBar, 0)
        layout.addLayout(self.layoutContents, 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

