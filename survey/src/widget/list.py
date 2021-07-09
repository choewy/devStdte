from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


COLUMNS = ["상태", "제목", "생성일자", "참여자 수"]


class List(QWidget):
    def __init__(self, central):
        QWidget.__init__(self)

        self.central = central

        self.surveySources = None

        self.labelTitle = QLabel()
        self.labelTitle.setObjectName("ListLabel")
        self.labelTitle.setText("목록")
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.buttonNew = QPushButton()
        self.buttonNew.setObjectName("ListButton-new")
        self.buttonNew.setText("신규 등록")
        self.buttonNew.clicked.connect(self.handleButtonNewClick)

        self.tableSurvey = QTableWidget()
        self.tableSurvey.setObjectName("ListTable")
        self.tableSurvey.verticalHeader().setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.labelTitle, 0)
        layout.addWidget(self.tableSurvey, 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        try:
            self.setTableSurvey()
        except Exception as e:
            print(e)

    def setTableSurvey(self):
        self.surveySources = self.central.realtimeDB.getSurveySources(self.central.clientId)

        self.tableSurvey.clear()
        self.tableSurvey.setColumnCount(len(COLUMNS))
        self.tableSurvey.setHorizontalHeaderLabels(COLUMNS)
        self.tableSurvey.setRowCount(0)

        for row, (uuid, status, title, isView, createTime, answerCounts) in enumerate(self.surveySources):
            self.tableSurvey.insertRow(row)

            widgetStatus = QLineEdit()
            widgetStatus.setObjectName("ListLineEdit-item-status")
            widgetStatus.setText("진행" if status else "종료")
            widgetStatus.setAlignment(Qt.AlignCenter)
            widgetStatus.setEnabled(False)

            self.tableSurvey.setCellWidget(row, 0, widgetStatus)

            widgetTitle = QPushButton()
            widgetTitle.setObjectName("ListButton-item-title")
            widgetTitle.uuid = uuid
            widgetTitle.setText(title)
            widgetTitle.clicked.connect(self.handleButtonNewClick)

            if not isView and status:
                widgetIsView = QLabel(widgetTitle)
                widgetIsView.setObjectName("ListLabel-item-isView")
                widgetIsView.setText("●")

            self.tableSurvey.setCellWidget(row, 1, widgetTitle)

            itemCreateTime = QTableWidgetItem()
            itemCreateTime.setText(createTime)
            itemCreateTime.setTextAlignment(Qt.AlignCenter)
            itemCreateTime.setFlags(Qt.ItemIsEditable)

            self.tableSurvey.setItem(row, 2, itemCreateTime)

            itemAnswerCounts = QTableWidgetItem()
            itemAnswerCounts.setText(f"{answerCounts}")
            itemAnswerCounts.setTextAlignment(Qt.AlignCenter)
            itemAnswerCounts.setFlags(Qt.ItemIsEditable)

            self.tableSurvey.setItem(row, 3, itemAnswerCounts)

        self.tableSurvey.resizeColumnsToContents()

    def handleButtonNewClick(self):
        widgetTitle = self.sender()
        uuid = widgetTitle.uuid
        self.central.mainForm.navBar.setSurveyWidget(uuid)