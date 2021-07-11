from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *

from src.dialog.question import Question

ICON_PATHS = {
    0: "images/status-false.png",
    1: "images/status-true.png"
}

ENCODE_STATUS = {
    0: "종료",
    1: "진행"
}

DECODE_STATUS = {
    "종료": 0,
    "진행": 1
}


class Header(QLabel):
    def __init__(self, survey):
        QWidget.__init__(self, survey.central)
        self.survey = survey

        self.setFixedHeight(70)
        self.setObjectName("Header")

        self.labelIcon = QLabel()
        self.labelIcon.setObjectName("HeaderLabel-icon")

        self.labelTitle = QLabel()
        self.labelTitle.setObjectName("HeaderLabel-title")

        self.comboStatus = QComboBox()
        self.comboStatus.setObjectName("SurveyCombo-status")
        self.comboStatus.addItems(ENCODE_STATUS.values())
        self.comboStatus.setVisible(False)

        self.buttonEdit = QPushButton()
        self.buttonEdit.setObjectName("SurveyButton-edit")
        self.buttonEdit.mode = "edit"
        self.buttonEdit.setIcon(QIcon(QPixmap("images/survey-edit.png").scaledToHeight(30)))
        self.buttonEdit.setCursor(Qt.PointingHandCursor)
        self.buttonEdit.setFocusPolicy(Qt.NoFocus)
        self.buttonEdit.clicked.connect(self.handleButtonEditClick)

        self.buttonRemove = QPushButton()
        self.buttonRemove.setObjectName("SurveyButton-remove")
        self.buttonRemove.setIcon(QIcon(QPixmap("images/survey-remove.png").scaledToHeight(30)))
        self.buttonRemove.setVisible(False)
        self.buttonRemove.setCursor(Qt.PointingHandCursor)
        self.buttonRemove.setFocusPolicy(Qt.NoFocus)
        self.buttonRemove.clicked.connect(self.handleButtonRemoveClick)

        layout = QHBoxLayout()
        layout.addWidget(self.labelIcon, 0)
        layout.addWidget(self.labelTitle, 10)
        layout.addWidget(self.comboStatus, 0)
        layout.addWidget(self.buttonEdit, 0)
        layout.addWidget(self.buttonRemove, 0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def setHeader(self):
        status = self.survey.surveySource["status"]
        self.comboStatus.setCurrentText(ENCODE_STATUS[status])
        self.labelIcon.setPixmap(QPixmap(ICON_PATHS[status]).scaledToHeight(20))

        admin = self.survey.surveySource["admin"]
        adminFlag = (self.survey.central.clientId == admin) or (self.survey.central.clientAuth in ["관리자", "개발자"])
        self.buttonEdit.setVisible(adminFlag)

        title = self.survey.surveySource["title"]
        self.labelTitle.setText(title)

    def handleButtonEditClick(self):
        if self.buttonEdit.mode == "edit":
            self.buttonEdit.mode = "save"
            self.buttonEdit.setIcon(QIcon(QPixmap("images/survey-save.png").scaledToHeight(30)))
            self.buttonRemove.setVisible(True)
            self.comboStatus.setVisible(True)
            self.survey.textTitle.setVisible(True)
            self.survey.textTitle.setReadOnly(False)
            self.survey.textContents.setReadOnly(False)

        else:
            oldSurveySource = {
                "title": self.survey.surveySource["title"],
                "contents": self.survey.surveySource["contents"],
                "status": self.survey.surveySource["status"]
            }

            newSurveySource = {
                "title": self.survey.textTitle.text(),
                "contents": self.survey.textContents.toPlainText(),
                "status": DECODE_STATUS[self.comboStatus.currentText()]
            }

            if oldSurveySource != newSurveySource:
                self.survey.central.realtimeDB.setSurveySource(self.survey.uuid, newSurveySource)
                self.survey.setSurveySource()
                # self.survey.setAnswerTable()
                self.survey.setAnswerArea()

            self.buttonEdit.mode = "edit"
            self.buttonEdit.setIcon(QIcon(QPixmap("images/survey-edit.png").scaledToHeight(30)))
            self.buttonRemove.setVisible(False)
            self.comboStatus.setVisible(False)
            self.survey.textTitle.setVisible(False)
            self.survey.textTitle.setReadOnly(True)
            self.survey.textContents.setReadOnly(True)

    def handleButtonRemoveClick(self):
        question = Question(self.survey.central, "이슈를 삭제하시겠습니까?", "삭제", "취소")
        question.exec_()

        if question.answer:
            self.survey.central.realtimeDB.removeSurveySource(self.survey.uuid)
            self.survey.central.mainForm.navBar.setSurveyList()