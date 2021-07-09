from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from datetime import date

from public.components.authForm import AuthForm
from public.components.mainForm import MainForm
from src.firebase.realtimedb import RealTimeDB


FOOTER_TEXT = f"All rights reserved by choewy {date.today().year}"


class Central(QWidget):
    def __init__(self, window=None):
        QWidget.__init__(self, window)

        self.window = window

        # self.clientId = None
        # self.clientAuth = None
        
        self.clientId = "choewy"
        self.clientAuth = "개발자"

        self.authForm = None
        self.mainForm = None

        self.labelFooter = None

        self.realtimeDB = RealTimeDB(self)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        # self.setLayoutAuth()
        self.setLayoutMain()

    def setLayoutAuth(self):
        self.window.setObjectName("WindowAuthForm")
        self.realtimeDB.__setScheduler__()

        layout = self.layout()

        for cnt in range(self.layout().count()):
            layout.itemAt(cnt).widget().deleteLater()

        self.authForm = AuthForm(self)

        self.labelFooter = QLabel()
        self.labelFooter.setObjectName("CentralFooter")
        self.labelFooter.setText(FOOTER_TEXT)
        self.labelFooter.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.authForm)
        layout.addWidget(self.labelFooter)
        layout.setContentsMargins(0, 0, 0, 0)

    def setLayoutMain(self):
        self.window.setObjectName("WindowMainForm")
        self.realtimeDB.__setSurvey__()

        layout = self.layout()

        for cnt in range(self.layout().count()):
            layout.itemAt(cnt).widget().deleteLater()

        self.mainForm = MainForm(self)

        self.labelFooter = QLabel()
        self.labelFooter.setObjectName("CentralFooter")
        self.labelFooter.setText(FOOTER_TEXT)
        self.labelFooter.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.mainForm)
        layout.addWidget(self.labelFooter)
        layout.setContentsMargins(0, 0, 0, 0)
