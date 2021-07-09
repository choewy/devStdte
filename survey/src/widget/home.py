from PyQt5.QtWidgets import *


class Home(QWidget):
    def __init__(self, central):
        QWidget.__init__(self)

        self.central = central

