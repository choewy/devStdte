from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class Message(QDialog):
    def __init__(self, window=None, message="", btnOk="확인"):
        QDialog.__init__(self, window)

        self.setObjectName("MessageDialog")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setMinimumSize(200, 120)

        self.labelMessage = QLabel()
        self.labelMessage.setObjectName("MessageLabel")
        self.labelMessage.setText(message)
        self.labelMessage.setAlignment(Qt.AlignCenter)

        self.btnOk = QPushButton()
        self.btnOk.setObjectName("MessageButton")
        self.btnOk.setText(btnOk)
        self.btnOk.setCursor(Qt.PointingHandCursor)
        self.btnOk.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.labelMessage, alignment=Qt.AlignCenter)
        layout.addWidget(self.btnOk, alignment=Qt.AlignCenter)

        self.setLayout(layout)
