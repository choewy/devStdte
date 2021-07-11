from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton
from src.dialog.question import Question

ANSWER_ICON_PATH = "images/survey-answer.png"
REMOVE_ICON_PATH = "images/answer-remove.png"


class Answer(QLabel):

    def __init__(self, survey, key, answerSource):
        QLabel.__init__(self)
        self.survey = survey
        self.key = key

        self.setObjectName("AnswerLabel-answer")
        self.setText(answerSource["answer"])
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setWordWrap(True)

        self.labelIcon = QLabel(self)
        self.labelIcon.setObjectName("AnswerLabel-icon")
        self.labelIcon.setPixmap(QPixmap(ANSWER_ICON_PATH).scaledToHeight(40))

        self.labelUploadDate = QLabel(self)
        self.labelUploadDate.setObjectName("AnswerLabel-date")
        self.labelUploadDate.setText(answerSource["uploadTime"])
        self.labelUploadDate.setAlignment(Qt.AlignBottom)
        self.labelUploadDate.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.buttonRemove = QPushButton(self)
        self.buttonRemove.setObjectName("AnswerButton-remove")
        self.buttonRemove.setIcon(QIcon(QPixmap(REMOVE_ICON_PATH)))
        self.buttonRemove.setCursor(Qt.PointingHandCursor)
        self.buttonRemove.setFocusPolicy(Qt.NoFocus)
        self.buttonRemove.move(50, 0)
        self.buttonRemove.clicked.connect(self.handleButtonRemoveClick)

        if self.survey.central.clientAuth not in ["관리자", "개발자"]:
            self.buttonRemove.setVisible(False)

    def handleButtonRemoveClick(self):
        question = Question(self.survey.central, "답글을 삭제하시겠습니까?", "삭제", "취소")
        question.exec_()

        if question.answer:
            self.survey.central.realtimeDB.removeAnswer(self.survey.uuid, self.key)
            self.survey.setSurveySource()
            self.survey.setAnswerArea()
