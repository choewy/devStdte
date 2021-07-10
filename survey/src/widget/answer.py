from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFontMetrics, QIcon
from PyQt5.QtWidgets import *


ANSWER_ICON_PATH = "images/survey-answer.png"
REMOVE_ICON_PATH = "images/answer-remove.png"


class Answer(QTextEdit):
    def __init__(self, survey, answerSource):
        QWidget.__init__(self)
        self.survey = survey

        self.setObjectName("AnswerTextEdit")
        self.setReadOnly(True)
        self.document().setPlainText(answerSource["answer"])
        font = self.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        size = fontMetrics.size(0, self.toPlainText())
        height = size.height() + 50
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

        self.labelIcon = QLabel(self)
        self.labelIcon.setObjectName("AnswerLabel-icon")
        self.labelIcon.setPixmap(QPixmap(ANSWER_ICON_PATH).scaledToHeight(40))

        self.labelUploadDate = QLabel(self)
        self.labelUploadDate.setObjectName("AnswerLabel-date")
        self.labelUploadDate.setText(answerSource["uploadTime"])
        self.labelUploadDate.setAlignment(Qt.AlignBottom)

        self.buttonRemove = QPushButton(self)
        self.buttonRemove.setObjectName("AnswerButton-remove")
        self.buttonRemove.setIcon(QIcon(QPixmap(REMOVE_ICON_PATH)))
        self.buttonRemove.setCursor(Qt.PointingHandCursor)
        self.buttonRemove.move(160, 0)
        if self.survey.central.clientAuth not in ["관리자", "개발자"]:
            self.buttonRemove.setVisible(False)

