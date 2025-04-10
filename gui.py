import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Productivity Assistant")

def main():
    app = QApplication(sys.argv) # consider sys.argv a placeholder
    window = MainWindow()
    window.show()
    app.exec_() # starts the event loop

main()