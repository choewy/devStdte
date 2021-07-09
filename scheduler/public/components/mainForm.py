from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout
from src.widget.header import Header
from src.widget.navbar import NavBar


class MainForm(QWidget):
    def __init__(self, central):
        QWidget.__init__(self)
        self.central = central

        self.header = Header(central)
        self.navBar = NavBar(central)

        self.vLine = QFrame()
        self.vLine.setObjectName("vLine")
        self.vLine.setFrameShape(QFrame.VLine)
        self.vLine.setFrameShadow(QFrame.Sunken)

        self.layoutContents = QHBoxLayout()
        self.layoutContents.addWidget(self.navBar)
        self.layoutContents.addWidget(self.vLine)
        self.layoutContents.addWidget(QLabel(" "), 10)

        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addLayout(self.layoutContents)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
