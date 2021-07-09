from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout

ICON_PATH = "images/menu.png"


class Header(QLabel):
    def __init__(self, central):
        QLabel.__init__(self)
        self.central = central

        self.setObjectName("Header")
        self.setFixedHeight(80)

        self.btnNavBar = QPushButton()
        self.btnNavBar.setIcon(QIcon(QPixmap(ICON_PATH)))
        self.btnNavBar.setObjectName("HeaderButton-menu")
        self.btnNavBar.setCursor(Qt.PointingHandCursor)
        self.btnNavBar.clicked.connect(self.handleBtnNavBarClick)

        self.labelContents = QLabel()
        self.labelContents.setObjectName("HeaderLabel-contents")
        self.labelContents.setText(" ")

        self.btnProfile = QPushButton()
        self.btnProfile.setText("내 정보")
        self.btnProfile.setObjectName("HeaderButton-profile")
        self.btnProfile.setCursor(Qt.PointingHandCursor)
        self.btnProfile.clicked.connect(self.handleBtnProfileClick)

        self.btnLogout = QPushButton()
        self.btnLogout.setText("로그아웃")
        self.btnLogout.setObjectName("HeaderButton-logout")
        self.btnLogout.setCursor(Qt.PointingHandCursor)
        self.btnLogout.clicked.connect(self.handleBtnLogoutClick)

        layout = QHBoxLayout()
        layout.addWidget(self.btnNavBar, alignment=Qt.AlignLeft)
        layout.addWidget(self.labelContents, alignment=Qt.AlignLeft)
        layout.addWidget(QLabel(" "), 10)
        layout.addWidget(self.btnProfile, alignment=Qt.AlignRight)
        layout.addWidget(self.btnLogout, alignment=Qt.AlignRight)
        layout.setContentsMargins(5, 0, 10, 0)

        self.setLayout(layout)

    def handleBtnNavBarClick(self):
        flag = self.central.mainForm.navBar.isVisible()
        self.central.mainForm.navBar.setVisible(not flag)

    def handleBtnProfileClick(self):
        self.central.mainForm.navBar.handlerItemClick(item=None, text=" 부서원 정보")
        self.central.mainForm.navBar.widget.accessByProfile()

    def handleBtnLogoutClick(self):
        self.central.setLayoutAuth()
