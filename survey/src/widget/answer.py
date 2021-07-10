from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFontMetrics, QIcon
from PyQt5.QtWidgets import *

from src.dialog.question import Question

ANSWER_ICON_PATH = "images/survey-answer.png"
REMOVE_ICON_PATH = "images/answer-remove.png"


class Answer(QTextEdit):
    def __init__(self, survey, key, answerSource):
        QWidget.__init__(self)
        self.survey = survey
        self.key = key

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
        self.buttonRemove.setFocusPolicy(Qt.NoFocus)
        self.buttonRemove.move(160, 0)
        self.buttonRemove.clicked.connect(self.handleButtonRemoveClick)

        if self.survey.central.clientAuth not in ["관리자", "개발자"]:
            self.buttonRemove.setVisible(False)

    def handleButtonRemoveClick(self):
        question = Question(self.survey.central, "답글을 삭제하시겠습니까?", "삭제", "취소")
        question.exec_()

        if question.answer:
            self.survey.central.realtimeDB.removeAnswer(self.survey.uuid, self.key)
            self.survey.setSurveySource()
            self.survey.setAnswerTable()
