from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QTabWidget, QPushButton, QHBoxLayout, QLabel, QTableWidget, \
    QVBoxLayout, QTableWidgetItem, QFileDialog, QListWidgetItem, QHeaderView


class TotalYear(QWidget):
    def __init__(self, total):
        QWidget.__init__(self)
        self.total = total
        self.central = total.central

        self.totalSource = None

        self.listSettingYear = QListWidget()
        self.listSettingYear.setObjectName("TotalList")

        self.listSettingTask = QListWidget()
        self.listSettingTask.setObjectName("TotalList")

        self.listSettingUser = QListWidget()
        self.listSettingUser.setObjectName("TotalList")

        self.tabListSetting = QTabWidget()
        self.tabListSetting.setObjectName("TotalTab-setting")
        self.tabListSetting.addTab(self.listSettingYear, "연도 선택")
        self.tabListSetting.addTab(self.listSettingTask, "사업 선택")
        self.tabListSetting.addTab(self.listSettingUser, "부서원 선택")

        self.buttonRun = QPushButton()
        self.buttonRun.setObjectName("TotalButton-run")
        self.buttonRun.setText("집계 산출")
        self.buttonRun.setCursor(Qt.PointingHandCursor)
        self.buttonRun.clicked.connect(self.handleButtonRunClick)

        self.buttonExcel = QPushButton()
        self.buttonExcel.setObjectName("TotalButton-excel")
        self.buttonExcel.setText("엑셀 저장")
        self.buttonExcel.setCursor(Qt.PointingHandCursor)
        self.buttonExcel.clicked.connect(self.handleButtonExcelClick)

        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.buttonRun)
        layoutBtn.addWidget(QLabel(" "), 10)
        layoutBtn.addWidget(self.buttonExcel)
        layoutBtn.setContentsMargins(0, 0, 0, 0)

        self.tableTotal = QTableWidget()
        self.tableTotal.setObjectName("TotalTable")
        self.tableTotal.verticalHeader().setVisible(False)

        layoutTotal = QVBoxLayout()
        layoutTotal.addLayout(layoutBtn, stretch=0)
        layoutTotal.addWidget(self.tableTotal, stretch=10)
        layoutTotal.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.addWidget(self.tabListSetting)
        layout.addLayout(layoutTotal)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self.setListYear()
        self.setListTask()
        self.setListUser()

    def setListYear(self):
        for year in self.central.realTimeDB.getYearList():
            item = QListWidgetItem()
            item.setText(year)
            item.setCheckState(Qt.Checked)
            self.listSettingYear.addItem(item)

    def setListTask(self):
        for uuid, name, visible in self.central.realTimeDB.getTaskList():
            item = QListWidgetItem()
            item.uuid = uuid
            item.setText(name)
            if visible:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.listSettingTask.addItem(item)

    def setListUser(self):
        for userId, name, status in self.central.realTimeDB.getUserList():
            item = QListWidgetItem()
            item.userId = userId
            item.setText(name)
            if status == "재직":
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.listSettingUser.addItem(item)

    def handleButtonRunClick(self):
        years = []
        for row in range(self.listSettingYear.count()):
            item = self.listSettingYear.item(row)
            if item.checkState():
                years.append(item.text())

        tasks = []
        taskInfo = {}
        for row in range(self.listSettingTask.count()):
            item = self.listSettingTask.item(row)
            if item.checkState():
                tasks.append(item.uuid)
                taskInfo[item.uuid] = item.text()

        users = []
        for row in range(self.listSettingUser.count()):
            item = self.listSettingUser.item(row)
            if item.checkState():
                users.append(item.userId)

        self.totalSource = self.central.realTimeDB.getTotalYear(years, tasks, taskInfo, users)
        self.setTableTotal()

    def handleButtonExcelClick(self):
        if self.totalSource:
            savePath = QFileDialog.getSaveFileName(self, "파일 저장", "연도별 시간 집계", "*.xlsx")[0]
            if savePath:
                self.central.realTimeDB.toExcelTotalYear(savePath, self.totalSource)

    def setTableTotal(self):
        self.tableTotal.clear()
        self.tableTotal.setColumnCount(len(self.totalSource.columns))
        self.tableTotal.setHorizontalHeaderLabels(self.totalSource.columns)
        self.tableTotal.setRowCount(0)

        for row, line in enumerate(self.totalSource.values):
            self.tableTotal.insertRow(row)

            for col, value in enumerate(line):

                item = QTableWidgetItem()

                if col == 0:
                    item.setText(value)

                else:
                    item.setText(format(value, ","))
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                item.setFlags(Qt.ItemIsEditable)
                self.tableTotal.setItem(row, col, item)

        self.tableTotal.resizeColumnsToContents()

        for col in range(1, self.tableTotal.columnCount()):
            self.tableTotal.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
