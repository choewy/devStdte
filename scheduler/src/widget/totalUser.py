from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QLabel, QListWidget, QTabWidget, QVBoxLayout, QPushButton, \
    QListWidgetItem, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView


class TotalUser(QWidget):
    def __init__(self, total):
        QWidget.__init__(self)
        self.total = total
        self.central = total.central

        self.totalSources = None

        self.labelYear = QLabel()
        self.labelYear.setObjectName("TotalLabel")
        self.labelYear.setText("  연도 선택 :")

        self.comboYear = QComboBox()
        self.comboYear.setObjectName("TotalCombo")

        layoutYear = QHBoxLayout()
        layoutYear.addWidget(self.labelYear, stretch=0, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        layoutYear.addWidget(self.comboYear, stretch=10, alignment=Qt.AlignCenter)
        layoutYear.setContentsMargins(0, 0, 0, 0)

        self.listSettingTask = QListWidget()
        self.listSettingTask.setObjectName("TotalList")

        self.listSettingUser = QListWidget()
        self.listSettingUser.setObjectName("TotalList")

        self.tabListSetting = QTabWidget()
        self.tabListSetting.setObjectName("TotalTab-setting")
        self.tabListSetting.addTab(self.listSettingTask, "사업 선택")
        self.tabListSetting.addTab(self.listSettingUser, "부서원 선택")

        layoutSetting = QVBoxLayout()
        layoutSetting.addLayout(layoutYear, stretch=0)
        layoutSetting.addWidget(self.tabListSetting, stretch=10)
        layoutSetting.setContentsMargins(0, 0, 0, 0)

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

        self.tabTotal = QTabWidget()
        self.tabTotal.setObjectName("TotalTabTables")

        layoutTotal = QVBoxLayout()
        layoutTotal.addLayout(layoutBtn, stretch=0)
        layoutTotal.addWidget(self.tabTotal, stretch=10)
        layoutTotal.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.addLayout(layoutSetting, stretch=0)
        layout.addLayout(layoutTotal, stretch=10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self.setComboYear()
        self.setListTask()
        self.setListUser()

    def setComboYear(self):
        years = self.central.realTimeDB.getYearList()
        years.sort(reverse=True)
        self.comboYear.addItems(years)

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
        year = self.comboYear.currentText()

        tasks = []
        taskInfo = {}
        for row in range(self.listSettingTask.count()):
            item = self.listSettingTask.item(row)
            if item.checkState():
                tasks.append(item.uuid)
                taskInfo[item.uuid] = item.text()

        users = []
        userInfo = {"전체": "전체"}
        for row in range(self.listSettingUser.count()):
            item = self.listSettingUser.item(row)
            if item.checkState():
                users.append(item.userId)
                userInfo[item.userId] = item.text()

        self.totalSources = self.central.realTimeDB.getTotalUser(year, tasks, taskInfo, users, userInfo)
        self.setTabTotal()

    def handleButtonExcelClick(self):
        if self.totalSources:
            savePath = QFileDialog.getSaveFileName(self, "파일 저장", "부서원별 시간 집계", "*.xlsx")[0]
            if savePath:
                self.central.realTimeDB.toExcelTotalUser(savePath, self.totalSources)

    def setTabTotal(self):
        self.tabTotal.clear()

        for key, totalSource in self.totalSources.items():
            tableTotal = QTableWidget()
            tableTotal.setObjectName("TotalTable")
            tableTotal.verticalHeader().setVisible(False)
            tableTotal.setColumnCount(len(totalSource.columns))
            tableTotal.setHorizontalHeaderLabels(totalSource.columns)

            for row, line in enumerate(totalSource.values):
                tableTotal.insertRow(row)

                for col, value in enumerate(line):

                    item = QTableWidgetItem()

                    if col == 0:
                        item.setText(value)
                    else:
                        item.setText(format(value, ","))
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    item.setFlags(Qt.ItemIsEditable)
                    tableTotal.setItem(row, col, item)
            tableTotal.resizeColumnsToContents()

            for col in range(1, tableTotal.columnCount()):
                tableTotal.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

            self.tabTotal.addTab(tableTotal, key)
