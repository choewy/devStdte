from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout


class Question(QDialog):
    def __init__(self, window, question="", btnYes="예", btnNo="아니오"):
        QDialog.__init__(self, window)

        self.answer = False

        self.setObjectName("QuestionDialog")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setMinimumSize(200, 120)

        self.labelQuestion = QLabel()
        self.labelQuestion.setObjectName("QuestionLabel")
        self.labelQuestion.setText(question)
        self.labelQuestion.setAlignment(Qt.AlignCenter)

        self.btnYes = QPushButton()
        self.btnYes.setObjectName("QuestionButtonYes")
        self.btnYes.setText(btnYes)
        self.btnYes.setCursor(Qt.PointingHandCursor)
        self.btnYes.clicked.connect(self.handleBtnYesClick)

        self.btnNo = QPushButton()
        self.btnNo.setObjectName("QuestionButtonNo")
        self.btnNo.setText(btnNo)
        self.btnNo.setCursor(Qt.PointingHandCursor)
        self.btnNo.clicked.connect(self.close)

        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnYes)
        layoutBtn.addWidget(self.btnNo)
        layoutBtn.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(self.labelQuestion)
        layout.addLayout(layoutBtn)

        self.setLayout(layout)

    def handleBtnYesClick(self):
        self.answer = True
        self.close()
