from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from public.central import Central
from src.dialog.message import Message
from src.dialog.question import Question

APP_TITLE = "화재안전팀 - 시간관리"
APP_VERSION = "1.0.0"
ICON_PATH = "images/Icon.png"
STYLE_PATH = "src/style.qss"


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowTitle(f"{APP_TITLE} - {APP_VERSION}")

        self.central = Central(self)
        self.setCentralWidget(self.central)

        self.setMinimumSize(1200, 800)
        self.setStyleSheet(self.getStyleSheet())

    def showQuestion(self, question="", btnYes="예", btnNo="아니오"):
        dialog = Question(self, question, btnYes, btnNo)
        dialog.exec_()
        return dialog.answer

    def showMessage(self, message="", btnOk="확인"):
        Message(self, message=message, btnOk=btnOk).exec_()

    def getStyleSheet(self):
        return open(STYLE_PATH, "r", encoding="utf-8").read()