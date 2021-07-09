from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *


# t = QTextEdit()
# s = t.document().size().toSize()
# t.setFixedHeight(s.height() + 3)
from src.widget.navbar import NavBar


class MainForm(QWidget):
    def __init__(self, central=None):
        QWidget.__init__(self, central)
        self.central = central
        
        # >> 운영 방안 :: 관리자, 개발자만 수정 가능
        # >> 설문 목록 생성
        # >> uuid, 설문 제목, 생성 일자, 생성자(비밀), 참여자 수(카운트) :: 생성자, 관리자, 개발자만 삭제 가능

        # 좌측 메뉴 :: 홈, 목록, 로그아웃
        # 홈 클릭 시 :: 화사 로고
        # 목록 아이템 클릭 시 :: 해당 설문으로 이동(좌측 설문 내용 / 우측 설문 답글)

        self.navBar = NavBar(central)

        self.vLine = QFrame()
        self.vLine.setObjectName("MainFormVLine")
        self.vLine.setFrameShape(QFrame.VLine)
        self.vLine.setFrameShadow(QFrame.Sunken)

        layout = QHBoxLayout()
        layout.addWidget(self.navBar)
        layout.addWidget(self.vLine)
        layout.addWidget(QLabel(" "), 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

