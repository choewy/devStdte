from PyQt5.QtWidgets import QApplication
from public.window import Window
from sys import argv


if __name__ == "__main__":
    print(1)
    app = QApplication(argv)
    window = Window()
    window.show()
    app.exec_()