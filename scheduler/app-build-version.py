from public.window import Window
from PyQt5.QtWidgets import QApplication
from sys import argv


if __name__ == "__main__":
    app = QApplication(argv)
    window = Window()
    window.show()
    app.exec_()
