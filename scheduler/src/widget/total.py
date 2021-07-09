from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from src.widget.totalUser import TotalUser
from src.widget.totalYear import TotalYear


class Total(QWidget):
    def __init__(self, central=None):
        QWidget.__init__(self, central)
        self.central = central

        self.totalUser = TotalUser(self)
        self.totalYear = TotalYear(self)

        self.tabTotal = QTabWidget()
        self.tabTotal.setObjectName("TotalTab")
        self.tabTotal.addTab(self.totalYear, "연도별 집계")
        self.tabTotal.addTab(self.totalUser, "부서원별 집계")

        layout = QVBoxLayout()
        layout.addWidget(self.tabTotal)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)