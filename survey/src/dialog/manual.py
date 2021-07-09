from PyQt5.QtWidgets import *


class Manual(QDialog):
    def __init__(self, central):
        QDialog.__init__(self)
        self.central = central
