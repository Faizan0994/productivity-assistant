import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QGuiApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        screen = QGuiApplication.primaryScreen().availableGeometry()
        windowWidth = 1280
        windowHeight = 768
        centeringVertex = ((screen.width() - windowWidth) // 2, (screen.height() - windowHeight) // 2)
        self.setWindowTitle("Productivity Assistant")
        self.setGeometry(centeringVertex[0], centeringVertex[1], windowWidth, windowHeight) # window's size and placement

def main():
    app = QApplication(sys.argv) # consider sys.argv a placeholder
    window = MainWindow()
    window.show()
    app.exec_() # starts the event loop

main()