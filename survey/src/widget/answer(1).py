from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFontMetrics
from PyQt5.QtWidgets import *


ICON_PATH = "images/survey-answer.png"


# QTextEdit으로 상속하고 padding으로 조절,
# 그 상단에 아이콘과 날짜 배치
class Answer(QWidget):
    def __init__(self, survey, answerSource):
        QWidget.__init__(self)
        self.survey = survey

        self.labelIcon = QLabel()
        self.labelIcon.setObjectName("AnswerLabel-icon")
        self.labelIcon.setPixmap(QPixmap(ICON_PATH).scaledToHeight(30))

        self.labelUploadDate = QLabel()
        self.labelUploadDate.setObjectName("AnswerLabel-date")
        self.labelUploadDate.setText(answerSource["uploadTime"])
        self.labelUploadDate.setAlignment(Qt.AlignBottom)

        layoutUser = QHBoxLayout()
        layoutUser.addWidget(self.labelIcon, stretch=0, alignment=Qt.AlignLeft)
        layoutUser.addWidget(self.labelUploadDate, stretch=10)
        layoutUser.setContentsMargins(0, 0, 0, 0)

        self.textAnswer = QTextEdit()
        self.textAnswer.setObjectName("AnswerTextEdit")
        self.textAnswer.setReadOnly(True)
        self.textAnswer.document().setPlainText(answerSource["answer"])

        font = self.textAnswer.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        size = fontMetrics.size(0, self.textAnswer.toPlainText())
        height = size.height() + 15
        self.textAnswer.setMinimumHeight(height)
        self.textAnswer.setMaximumHeight(height)

        layout = QVBoxLayout()
        layout.addLayout(layoutUser, 0)
        layout.addWidget(self.textAnswer, 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
