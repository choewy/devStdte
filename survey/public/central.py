from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from datetime import date
from public.components.authForm import AuthForm
from public.components.mainForm import MainForm
from src.firebase.realtimedb import RealTimeDB
from webbrowser import open

FOOTER_TEXT = f"All rights reserved by choewy {date.today().year}"
GITHUB_URL = "https://github.com/choewy/devStdte/tree/master/survey"


class Central(QWidget):
    def __init__(self, window=None):
        QWidget.__init__(self, window)

        self.window = window

        self.clientId = None
        self.clientAuth = None
        self.clientId = "choewy"
        self.clientAuth = "개발자"

        self.authForm = None
        self.mainForm = None

        self.buttonFooter = None

        self.realtimeDB = RealTimeDB(self)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setLayoutAuth()
        # self.setLayoutMain()

    def setLayoutAuth(self):
        self.window.setObjectName("WindowAuthForm")
        self.realtimeDB.__setScheduler__()

        layout = self.layout()

        for cnt in range(self.layout().count()):
            layout.itemAt(cnt).widget().deleteLater()

        self.buttonFooter = QPushButton()
        self.buttonFooter.setObjectName("CentralFooter")
        self.buttonFooter.setText(FOOTER_TEXT)
        self.buttonFooter.setCursor(Qt.PointingHandCursor)
        self.buttonFooter.setFocusPolicy(Qt.NoFocus)
        self.buttonFooter.clicked.connect(self.handleButtonFooterClick)

        self.authForm = AuthForm(self)

        layout.addWidget(self.authForm)
        layout.addWidget(self.buttonFooter, alignment=Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

    def setLayoutMain(self):
        self.window.setObjectName("WindowMainForm")
        self.realtimeDB.__setSurvey__()

        layout = self.layout()

        for cnt in range(self.layout().count()):
            layout.itemAt(cnt).widget().deleteLater()

        self.buttonFooter = QPushButton()
        self.buttonFooter.setObjectName("CentralFooter")
        self.buttonFooter.setText(FOOTER_TEXT)
        self.buttonFooter.setCursor(Qt.PointingHandCursor)
        self.buttonFooter.setFocusPolicy(Qt.NoFocus)
        self.buttonFooter.clicked.connect(self.handleButtonFooterClick)

        self.mainForm = MainForm(self)

        layout.addWidget(self.mainForm)
        layout.setContentsMargins(0, 0, 0, 0)

        self.mainForm.navBar.setHomeWidget()

    def handleButtonFooterClick(self):
        open(GITHUB_URL)
