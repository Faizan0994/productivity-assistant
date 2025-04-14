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
        windowWidth = 1200
        windowHeight = 768
        centeringVertex = ((screen.width() - windowWidth) // 2, (screen.height() - windowHeight) // 2)
        self.setWindowTitle("Productivity Assistant")
        self.setFixedSize(windowWidth, windowHeight)
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
        self.contentArea.setMinimumHeight(1200)
        self.scroller = SmartScrollArea()
        self.scroller.setWidget(self.contentArea)
        self.scroller.setFrameShape(QScrollArea.NoFrame)

        self.title.setStyleSheet(f"""background-color: transparent;
                                     color: {self.textColor};
                                     border: none;
                                     font-size: 36px;
                                     font-weight: 500;
                                     """)

        self.tabs.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                margin-top: 16px;
                border: none;
                outline: none;
                color: {self.textColor};
                font-size: 16px;
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
                width: 6px;
                margin: 0px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.scrollBarColor};
                min-height: 30px;
                border-radius: 3px;
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
        mainLayout.setContentsMargins(64,0,64,0) # Padding to the right and left

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