import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QSizePolicy, QScrollArea
from PyQt5.QtGui import QGuiApplication, QFontDatabase, QFont, QPen, QColor
from PyQt5.QtCore import Qt
from gui_library import SmartScrollArea, FixedAxis, CustomGridViewBox, LineDrawer

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
        centralWidget.setStyleSheet(f"""
                                    background-color: {self.bgColor};
                                    font-family: inter
                                    """)

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

        self.renderDashboard()


    def renderDashboard(self):
        dashboardLayout = QVBoxLayout()
        cardsLayout = QHBoxLayout()
        todayLayout = QVBoxLayout()
        thisWeekLayout = QVBoxLayout()
        mostUsedAppLayout = QVBoxLayout()
        graphLayout = QHBoxLayout()
        appInfoLayout = QVBoxLayout()
        
        self.cardsSection = QWidget(self.contentArea)
        self.graphSection = QWidget(self.contentArea)
        self.appInfoSection = QWidget(self.contentArea)

        # Cards Section
        self.todayCard = QWidget(self.cardsSection)
        self.thisWeekCard = QWidget(self.cardsSection)
        self.mostUsedAppCard = QWidget(self.cardsSection)
        cardsLayout.addWidget(self.todayCard)
        cardsLayout.addWidget(self.thisWeekCard)
        cardsLayout.addWidget(self.mostUsedAppCard)
        cardsLayout.setSpacing(5*self.vw)
        self.cardsSection.setLayout(cardsLayout)

        # Cards
        self.todayText = QLabel("Today", self.todayCard)
        self.todayUsage = QLabel("8h 20m 03s", self.todayCard)
        self.lastDayRef = QLabel("6h more than yesterday")
        todayLayout.addWidget(self.todayText)
        todayLayout.addWidget(self.todayUsage)
        todayLayout.addWidget(self.lastDayRef)
        self.todayCard.setLayout(todayLayout)

        self.thisWeekText = QLabel("This week", self.thisWeekCard)
        self.thisWeekUsage = QLabel("56h 31m 40s", self.thisWeekCard)
        self.lastWeekRef = QLabel("1h less than last week", self.thisWeekCard)
        thisWeekLayout.addWidget(self.thisWeekText)
        thisWeekLayout.addWidget(self.thisWeekUsage)
        thisWeekLayout.addWidget(self.lastWeekRef)
        self.thisWeekCard.setLayout(thisWeekLayout)

        self.mostUsedText = QLabel("Most Used", self.mostUsedAppCard)
        self.mostUsedAppName = QLabel("Firefox", self.mostUsedAppCard)
        mostUsedAppLayout.addWidget(self.mostUsedText, 1)
        mostUsedAppLayout.addWidget(self.mostUsedAppName, 2)
        mostUsedAppLayout.setSpacing(1*self.vw)
        self.mostUsedAppCard.setLayout(mostUsedAppLayout)

        # The Graph
        dayLabels = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'
        }
        xAxisItem = FixedAxis(labels = dayLabels, orientation='bottom')
        yAxisItem = FixedAxis(orientation = 'left')
        self.graph = pg.PlotWidget(self.graphSection, axisItems={'bottom': xAxisItem, 'left': yAxisItem}, viewBox = CustomGridViewBox(color = self.mutedColor))
        graphLayout.addWidget(self.graph)
        self.graphSection.setLayout(graphLayout)
        self.graphSection.setObjectName("graphSection")
        myPen = pg.mkPen(color = self.primaryColor, width = int(0.25*self.vw))
        gridPen = QPen(QColor(self.mutedColor))
        days = [1, 2, 3, 4, 5, 6, 7]
        usageTime = [2, 3, 4, 4, 2, 1, 5]
        graphStyles = {"color": f"{self.textColor}", "font-size": f"{int(1.5*self.vw)}px"}
        self.graph.setTitle("Screen Time", color = self.textColor, size = f"{int(1.5*self.vw)}pt")
        self.graph.showGrid(x = False, y = True)
        self.graph.setMouseEnabled(x=False, y=False)
        self.graph.plot(days, usageTime, pen = myPen, symbol = "o", symbolBrush = self.accentColor)
        xAxis = self.graph.getAxis('bottom')
        yAxis = self.graph.getAxis('left')
        xAxis.setTextPen(QPen(QColor(self.mutedColor)))
        xAxis.setTickFont(QFont("inter", 10))
        yAxis.setTextPen(QPen(QColor(self.mutedColor)))
        yAxis.setTickFont(QFont("inter", 10))
        self.graph.setLabel("left", "Hours", **graphStyles) # Dictionary unpacking operator is necessary

        # App info Section
        self.appInfoHeader = QWidget(self.appInfoSection)
        self.appInfoTitle = QLabel("App Usage", self.appInfoSection)
        self.appInfoLine = LineDrawer(color = self.mutedColor, strokeWidth = int(0.2*self.vw), direction = "horizontal")
        self.appInfoLine.setMinimumWidth(200)
        self.appInfoLine.setMinimumHeight(int(0.2*self.vw))
        appInfoLayout.addWidget(self.appInfoTitle)
        appInfoLayout.addWidget(self.appInfoLine)
        appInfoLayout.setContentsMargins(0,0,0,0)
        self.appInfoSection.setLayout(appInfoLayout)

        # Fixed size for cards and graph section
        self.cardsSection.setFixedHeight(12*self.vw)
        self.graphSection.setFixedHeight(30*self.vw)

        # Styling
        self.graph.setBackground(self.cardBgColor)
        for card in [self.todayCard, self.thisWeekCard, self.mostUsedAppCard]:
            card.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.cardBgColor};
                    border: 2px solid {self.cardOutlineColor};
                    border-radius: 8px;
                    padding-left: {1*self.vw}px;
                }}
                QLabel {{
                    background: none;
                    border: none;
                }}
            """)
        self.todayText.setStyleSheet(f"""
                                     font-size: {int(1.1*self.vw)}px;
                                     font-weight: bold;
                                     """)
        self.todayUsage.setStyleSheet(f"""
                                     font-size: {3*self.vw}px;
                                     font-weight: 500;
                                     margin-left: -{int(0.8*self.vw)}px;
                                     """)
        self.lastDayRef.setStyleSheet(f"""
                                     font-size: {int(1.1*self.vw)}px;
                                     color: {self.mutedColor};
                                     """)
        self.thisWeekText.setStyleSheet(f"""
                                     font-size: {int(1.1*self.vw)}px;
                                     font-weight: bold;
                                     """)
        self.thisWeekUsage.setStyleSheet(f"""
                                     font-size: {3*self.vw}px;
                                     font-weight: 500;
                                     margin-left: -{int(0.8*self.vw)}px;
                                     """)
        self.lastWeekRef.setStyleSheet(f"""
                                     font-size: {int(1.1*self.vw)}px;
                                     color: {self.mutedColor};
                                     """)
        self.mostUsedText.setStyleSheet(f"""
                                     font-size: {int(1.1*self.vw)}px;
                                     font-weight: bold;
                                     margin-top: {int(0.3*self.vw)}px;
                                     """)
        self.mostUsedAppName.setStyleSheet(f"""
                                     font-size: {3*self.vw}px;
                                     font-weight: 500;
                                     margin-left: -{int(0.8*self.vw)}px;
                                     margin-bottom: {int(2*self.vw)}px;
                                     """)
        self.graphSection.setStyleSheet(f"""
            #graphSection {{
                background-color: {self.cardBgColor};
                border: 2px solid {self.cardOutlineColor};
                border-radius: 8px;
                padding: {int(1*self.vw)}px;
            }}
        """)
        self.appInfoTitle.setStyleSheet(f"""
                                        font-size: {int(1.4*self.vw)}px;
                                        font-weight: 400;
                                        """)

        dashboardLayout.addWidget(self.cardsSection)
        dashboardLayout.addWidget(self.graphSection)
        dashboardLayout.addWidget(self.appInfoSection)
        dashboardLayout.setSpacing(4*self.vw)
        self.contentArea.setLayout(dashboardLayout)
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.contentArea)
  
    

    def clearContentArea(self): # Wipe out everything except the header
        for child in self.contentArea.findChildren(QWidget):
            child.setParent(None)
            child.deleteLater()


def main():
    app = QApplication(sys.argv) # consider sys.argv a placeholder
    window = MainWindow()
    window.show()
    app.exec_() # starts the event loop

main()