import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QSizePolicy, QScrollArea
from PyQt5.QtGui import QGuiApplication, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from gui_library import SmartScrollArea

class MainWindow(QMainWindow):
    # This will be changed later
    bgColor = "#EDF1F5"
    primaryColor = "#3B82F6"
    accentColor = "#38BDF8"
    textColor = "#1E293B"
    mutedColor = "#878E97"
    cardOutlineColor = "#8199B7"
    cardBgColor = "#E2E8F0"
    scrollBarColor = "#94A3B8"

    def __init__(self):
        super().__init__()
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.windowWidth = int(screen.width() * 0.7)  # 70% of screen width
        self.windowHeight = int(self.windowWidth * 0.64)   # To keep the width to height ratio same for all screens
        
        # To replicate CSS vw and vh units
        self.vw = self.windowWidth // 100
        self.vh = self.windowHeight // 100

        centeringVertex = ((screen.width() - self.windowWidth) // 2, (screen.height() - self.windowHeight) // 2)
        self.setWindowTitle("Productivity Assistant")
        self.setFixedSize(self.windowWidth, self.windowHeight)
        self.move(centeringVertex[0], centeringVertex[1]) # the center of screen
        self.initUI()


    def initUI(self): # Builds the basic structure
        centralWidget = QWidget() # The window must have a central widget
        centralWidget.setStyleSheet(f"""background-color: {self.bgColor};""")

        fontId = QFontDatabase.addApplicationFont("./assets/inter.ttf")
        interFontFamily = QFontDatabase.applicationFontFamilies(fontId)[0] # first element is the font we want to use
        interFont = QFont(interFontFamily, 1)
        centralWidget.setFont(interFont)

        self.header = QWidget(centralWidget)
        self.title = QLabel("Dashboard", self.header)
        self.tabs = QWidget(self.header)
        self.dashboardButton = QPushButton("Dashboard", self.tabs)
        self.limitsTabButton = QPushButton("App Limits", self.tabs)
        self.settingsButton = QPushButton("Settings", self.tabs)
        self.contentArea = QWidget(centralWidget)
        self.contentArea.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.contentArea.adjustSize()
        self.scroller = SmartScrollArea()
        self.scroller.setFrameShape(QScrollArea.NoFrame)

        self.title.setStyleSheet(f"""background-color: transparent;
                                     color: {self.textColor};
                                     border: none;
                                     font-size: {int(3.4*self.vw)}px;
                                     font-weight: 500;
                                     """)

        self.tabs.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                margin-top: {int(1.2*self.vw)}px;
                border: none;
                outline: none;
                color: {self.textColor};
                font-size: {int(1.4*self.vw)}px;
                border-bottom: 1px solid {self.accentColor};
                padding: 0px;
                width: auto;
                font-weight: 400;
            }}
            QPushButton:hover {{
                color: {self.accentColor};
                border-color: {self.primaryColor};
            }}
        """)
        self.scroller.setStyleSheet(f"""
            QScrollBar:vertical {{
                background: {self.cardBgColor};
                width: {int(0.5*self.vw)}px;
                margin: 0px;
                border-radius: {int(0.3*self.vw)}px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.scrollBarColor};
                min-height: {int(2.4*self.vw)}px;
                border-radius: {int(0.3*self.vw)};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)
        self.dashboardButton.setStyleSheet(f"""
                                            color: {self.primaryColor};
                                            border-color: {self.primaryColor};
                                            """)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.header, 1)
        mainLayout.addWidget(self.scroller, 7)
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(5*self.vw,0,5*self.vw,0) # Padding to the right and left

        headerLayout = QHBoxLayout()
        headerLayout.addWidget(self.title, 2)
        headerLayout.addWidget(self.tabs, 1)
        self.header.setLayout(headerLayout)

        tabsLayout = QHBoxLayout()
        tabsLayout.addWidget(self.dashboardButton)
        tabsLayout.addWidget(self.limitsTabButton)
        tabsLayout.addWidget(self.settingsButton)
        tabsLayout.setSpacing(0)
        self.tabs.setLayout(tabsLayout)

        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    



def main():
    app = QApplication(sys.argv) # consider sys.argv a placeholder
    window = MainWindow()
    window.show()
    app.exec_() # starts the event loop

main()