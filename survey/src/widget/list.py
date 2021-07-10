from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import *


COLUMNS = ["상태", "제목", "생성일자", "참여자 수"]
NEW_ICON_PATH = "images/survey-new.png"


class List(QWidget):
    def __init__(self, central):
        QWidget.__init__(self)

        self.central = central

        self.surveySources = None

        self.tableSurvey = QTableWidget()
        self.tableSurvey.setObjectName("ListTable")
        self.tableSurvey.verticalHeader().setVisible(False)
        self.tableSurvey.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableSurvey.setFocusPolicy(Qt.NoFocus)
        self.tableSurvey.setVisible(False)

        self.labelSurvey = QLabel()
        self.labelSurvey.setObjectName("ListLabel")
        self.labelSurvey.setText("이슈사항이 없습니다.")
        self.labelSurvey.setAlignment(Qt.AlignCenter)
        self.labelSurvey.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.tableSurvey)
        layout.addWidget(self.labelSurvey)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self.setTableSurvey()

    def setTableSurvey(self):
        self.surveySources = self.central.realtimeDB.getSurveySources(self.central.clientId)

        if self.surveySources:
            self.tableSurvey.clear()
            self.tableSurvey.setColumnCount(len(COLUMNS))
            self.tableSurvey.setHorizontalHeaderLabels(COLUMNS)
            self.tableSurvey.setRowCount(0)

            for row, (uuid, status, title, isView, createTime, answerCounts) in enumerate(self.surveySources):
                self.tableSurvey.insertRow(row)

                widgetStatus = QLineEdit()
                if status:
                    widgetStatus.setObjectName("ListLineEdit-item-status-1")
                    widgetStatus.setText("진행")
                else:
                    widgetStatus.setObjectName("ListLineEdit-item-status-0")
                    widgetStatus.setText("종료")

                widgetStatus.setAlignment(Qt.AlignCenter)
                widgetStatus.setEnabled(False)

                self.tableSurvey.setCellWidget(row, 0, widgetStatus)

                widgetTitle = QPushButton()
                widgetTitle.setObjectName("ListButton-item-title")
                widgetTitle.uuid = uuid
                widgetTitle.setText(title)
                widgetTitle.setCursor(Qt.PointingHandCursor)
                widgetTitle.setFocusPolicy(Qt.NoFocus)
                widgetTitle.clicked.connect(self.handleButtonTitleClick)

                if not isView and status:
                    widgetTitle.setIcon(QIcon(QPixmap(NEW_ICON_PATH)))
                    widgetTitle.setIconSize(QSize(60, 30))

                self.tableSurvey.setCellWidget(row, 1, widgetTitle)

                itemCreateTime = QTableWidgetItem()
                itemCreateTime.setText(f"  {createTime}  ")
                itemCreateTime.setTextAlignment(Qt.AlignCenter)
                itemCreateTime.setFlags(Qt.ItemIsEditable)

                self.tableSurvey.setItem(row, 2, itemCreateTime)

                itemAnswerCounts = QTableWidgetItem()
                itemAnswerCounts.setText(f"  {answerCounts}  ")
                itemAnswerCounts.setTextAlignment(Qt.AlignCenter)
                itemAnswerCounts.setFlags(Qt.ItemIsEditable)

                self.tableSurvey.setItem(row, 3, itemAnswerCounts)
                self.tableSurvey.setRowHeight(row, 50)

            self.tableSurvey.resizeColumnsToContents()
            self.tableSurvey.setColumnWidth(0, 60)
            self.tableSurvey.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
            self.tableSurvey.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.tableSurvey.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
            self.tableSurvey.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)

            self.labelSurvey.setVisible(False)
            self.tableSurvey.setVisible(True)

        else:
            self.tableSurvey.setVisible(False)
            self.labelSurvey.setVisible(True)

    def handleButtonTitleClick(self):
        widgetTitle = self.sender()
        uuid = widgetTitle.uuid
        self.central.realtimeDB.setSurveyView(self.central.clientId, uuid)
        self.central.mainForm.navBar.setSurveyWidget(uuid)
