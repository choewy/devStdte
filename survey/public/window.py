from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from public.central import Central

APP_TITLE = "화재안전팀 - 의견수렴"
APP_VERSION = "1.0.0"
ICON_PATH = "images/icon.png"
STYLE_PATH = "src/style.qss"


def getStyleSheet():
    return open(STYLE_PATH, "r", encoding="utf-8").read()


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        print(1)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowTitle(f"{APP_TITLE} - {APP_VERSION}")

        self.central = Central(self)
        self.setCentralWidget(self.central)

        self.setMinimumSize(820, 800)
        self.setStyleSheet(getStyleSheet())

        self.objectNameChanged.connect(self.handleObjectNameChange)

    def handleObjectNameChange(self, _):
        self.setStyleSheet(getStyleSheet())
