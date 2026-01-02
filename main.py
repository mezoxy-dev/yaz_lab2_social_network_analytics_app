import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print("Application starting...")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
