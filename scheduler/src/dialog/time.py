from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

TASK_OPTIONS = {
    "회의": "0",
    "교육/훈련": "1",
    "기타업무": "2",
    "사업관리": "3",
    "기술업무": "4"
}


class DialogTime(QDialog):
    def __init__(self, schedule, row, col):
        QDialog.__init__(self, schedule.central.window)

        self.setObjectName("TimeDialog")
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.schedule = schedule

        header = self.schedule.tableTime.horizontalHeaderItem(col).text()
        taskValues = self.schedule.tableTask.item(row, 2).taskValues
        self.oldTime = self.schedule.tableTime.item(row, col).text()

        taskOptionKey = TASK_OPTIONS[taskValues[3]]
        timeSource = [header[:2], header[3:5], taskValues[0], taskOptionKey]
        self.key = '-'.join(timeSource)

        self.labelDate = QLabel()
        self.labelDate.setObjectName("TimeLabel-date")
        self.labelDate.setAlignment(Qt.AlignCenter)
        self.labelDate.setText(f"{self.schedule.currentYear}/{timeSource[0]}/{timeSource[1]}")

        self.labelTaskName = QLabel()
        self.labelTaskName.setObjectName("TimeLabel-taskName")
        self.labelTaskName.setAlignment(Qt.AlignCenter)
        self.labelTaskName.setText(f"{taskValues[1]}")

        self.labelTaskOption = QLabel()
        self.labelTaskOption.setObjectName("TimeLabel-taskOption")
        self.labelTaskOption.setAlignment(Qt.AlignCenter)
        self.labelTaskOption.setText(f"# {taskValues[3]}")

        self.inputTime = QLineEdit()
        self.inputTime.setObjectName("TimeInput")
        self.inputTime.setAlignment(Qt.AlignCenter)
        self.inputTime.setText(self.oldTime)
        self.inputTime.textChanged.connect(self.handleInputTimeChange)

        self.btnOk = QPushButton()
        self.btnOk.setObjectName("TimeButton")
        self.btnOk.setText("저장")
        self.btnOk.setCursor(Qt.PointingHandCursor)
        self.btnOk.clicked.connect(self.handleBtnOkClick)

        layout = QVBoxLayout()
        layout.addWidget(self.labelDate, alignment=Qt.AlignCenter)
        layout.addWidget(self.labelTaskName, alignment=Qt.AlignCenter)
        layout.addWidget(self.labelTaskOption, alignment=Qt.AlignCenter)
        layout.addWidget(self.inputTime, alignment=Qt.AlignCenter)
        layout.addWidget(self.btnOk, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def handleInputTimeChange(self, time):
        try:
            time = round(float(time), 2)
            if time == 24:
                self.schedule.central.window.showMessage("밤새 일하면 수명이 줄어듭니다.", "확인")

            elif time > 24:
                self.schedule.central.window.showMessage("지구인들의 하루는 24시간인데, 혹시 외계인이세요?", "확인")
                self.inputTime.setText("24")
        except:
            self.inputTime.setText(time[:-1])

    def handleBtnOkClick(self):
        newTime = self.inputTime.text()
        if newTime != self.oldTime:
            newTime = float(newTime) if newTime else 0.0
            self.schedule.central.realTimeDB.setTime(self.schedule.currentYear, self.key, newTime)
            self.schedule.setListUser()
            self.schedule.setTableTimeAndTotal()
        self.close()
