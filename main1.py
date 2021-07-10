from login import *

def main():
    app = QApplication([])
    app.setWindowIcon(QIcon('picture/logo_car.jpeg'))
    status = Status()
    status.ui.show()
    app.exec()

if __name__ == '__main__':
    main()