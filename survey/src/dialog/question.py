from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class Question(QDialog):
    def __init__(self, central, question="", btnYes="예", btnNo="아니오"):
        QDialog.__init__(self, central)
        self.answer = False

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.labelQuestion = QLabel()
        self.labelQuestion.setObjectName("QuestionLabel")
        self.labelQuestion.setAlignment(Qt.AlignCenter)
        self.labelQuestion.setText(question)

        self.buttonYes = QPushButton()
        self.buttonYes.setObjectName("QuestionButtonYes")
        self.buttonYes.setText(btnYes)
        self.buttonYes.setCursor(Qt.PointingHandCursor)
        self.buttonYes.clicked.connect(self.handleButtonYesClick)

        self.buttonNo = QPushButton()
        self.buttonNo.setObjectName("QuestionButtonNo")
        self.buttonNo.setText(btnNo)
        self.buttonNo.setCursor(Qt.PointingHandCursor)
        self.buttonNo.clicked.connect(self.close)

        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.buttonYes)
        layoutBtn.addWidget(self.buttonNo)
        layoutBtn.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(self.labelQuestion)
        layout.addLayout(layoutBtn)

        self.setLayout(layout)

    def handleButtonYesClick(self):
        self.answer = True
        self.close()
