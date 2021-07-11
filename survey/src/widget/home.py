from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import *

STDTE_ICON_PATH = "images/stdte.png"


class Home(QLabel):
    def __init__(self, central):
        QWidget.__init__(self)
        self.central = central

        self.setObjectName("HomeLabel-logo-stdte")
        self.setPixmap(QPixmap(STDTE_ICON_PATH).scaledToHeight(160))
        self.setAlignment(Qt.AlignCenter)
