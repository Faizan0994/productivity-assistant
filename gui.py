import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QSizePolicy, QScrollArea
from PyQt5.QtGui import QGuiApplication, QFontDatabase, QFont, QPen, QColor, QIcon
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QSize
from gui_library import SmartScrollArea, FixedAxis, CustomGridViewBox, LineDrawer
from gui_data import *

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
        self.dashboardButton.setCursor(Qt.PointingHandCursor)
        self.limitsTabButton = QPushButton("App Limits", self.tabs)
        self.limitsTabButton.setCursor(Qt.PointingHandCursor)
        self.settingsButton = QPushButton("Settings", self.tabs)
        self.settingsButton.setCursor(Qt.PointingHandCursor)
        self.contentArea = QWidget(centralWidget)
        self.contentArea.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.contentArea.adjustSize()
        self.scroller = SmartScrollArea()
        self.scroller.setFrameShape(QScrollArea.NoFrame)

        self.dashboardButton.clicked.connect(self.renderDashboard)
        self.limitsTabButton.clicked.connect(self.renderLimitsTab)
        self.settingsButton.clicked.connect(self.renderSettingsTab)

        self.title.setStyleSheet(f"""background-color: transparent;
                                     color: {self.textColor};
                                     border: none;
                                     font-size: {int(3.4*self.vw)}px;
                                     font-weight: 500;
                                     """)
        self.defaultTabButtonStyle = f"""
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
        """
        self.activeTabButtonStyle = f"""
            color: {self.primaryColor};
            border-color: {self.primaryColor};
        """
        self.tabs.setStyleSheet(self.defaultTabButtonStyle)
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

        self.activeTabButton = None  # Track the currently active tab button
        self.renderDashboard()


    def resetTabButtonStyles(self):
        if self.activeTabButton:
            self.activeTabButton.setStyleSheet(self.defaultTabButtonStyle)


    def renderDashboard(self):
        # Cleaning up the content area and buttons
        self.resetTabButtonStyles()  # Reset the previous button's style
        self.activeTabButton = self.dashboardButton  # Update the active button
        self.dashboardButton.setStyleSheet(self.activeTabButtonStyle)
        self.clearContentArea()

        dashboardLayout = QVBoxLayout()
        cardsLayout = QHBoxLayout()
        todayLayout = QVBoxLayout()
        thisWeekLayout = QVBoxLayout()
        mostUsedAppLayout = QVBoxLayout()
        graphLayout = QHBoxLayout()
        appInfoHeadingLayout = QVBoxLayout()
        self.appInfoDataLayout = QVBoxLayout()
        self.appInfoLayout = QVBoxLayout()
        
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
        self.todayUsage = QLabel(screenTimeToday, self.todayCard)
        self.lastDayRef = QLabel(lastDayComparisonString, self.todayCard)
        todayLayout.addWidget(self.todayText)
        todayLayout.addWidget(self.todayUsage)
        todayLayout.addWidget(self.lastDayRef)
        self.todayCard.setLayout(todayLayout)

        self.thisWeekText = QLabel("This week", self.thisWeekCard)
        self.thisWeekUsage = QLabel(screenTimeThisWeek, self.thisWeekCard)
        self.lastWeekRef = QLabel(lastWeekComparisonString, self.thisWeekCard)
        thisWeekLayout.addWidget(self.thisWeekText)
        thisWeekLayout.addWidget(self.thisWeekUsage)
        thisWeekLayout.addWidget(self.lastWeekRef)
        self.thisWeekCard.setLayout(thisWeekLayout)

        self.mostUsedText = QLabel("Most Used App", self.mostUsedAppCard)
        self.mostUsedAppName = QLabel(mostUsedApp, self.mostUsedAppCard)
        mostUsedAppLayout.addWidget(self.mostUsedText, 1)
        mostUsedAppLayout.addWidget(self.mostUsedAppName, 2)
        mostUsedAppLayout.setSpacing(1*self.vw)
        self.mostUsedAppCard.setLayout(mostUsedAppLayout)

        # The Graph
        dayLabels = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }
        xAxisItem = FixedAxis(labels = dayLabels, orientation='bottom')
        yAxisItem = FixedAxis(orientation = 'left')
        self.graph = pg.PlotWidget(self.graphSection, axisItems={'bottom': xAxisItem, 'left': yAxisItem}, viewBox = CustomGridViewBox(color = self.mutedColor))
        graphLayout.addWidget(self.graph)
        self.graphSection.setLayout(graphLayout)
        self.graphSection.setObjectName("graphSection")
        myPen = pg.mkPen(color = self.primaryColor, width = int(0.25*self.vw))
        gridPen = QPen(QColor(self.mutedColor))
        days = xPoints
        usageTime = yPoints
        padding = 0.1 # padding both sides of x-axis so that Labels are not cut off
        x_min = days[0] - padding
        x_max = days[-1] + padding
        graphStyles = {"color": f"{self.textColor}", "font-size": f"{int(1.5*self.vw)}px"}
        self.graph.setXRange(x_min, x_max)
        self.graph.setTitle("Screen Time", color = self.textColor, size = f"{int(1.5*self.vw)}pt")
        self.graph.showGrid(x = False, y = True)
        self.graph.setMouseEnabled(x=False, y=False)
        self.graph.plot(days, usageTime, pen = myPen, symbol = "o", symbolBrush = self.accentColor)
        xAxis = self.graph.getAxis('bottom')
        yAxis = self.graph.getAxis('left')
        xAxis.setTextPen(QPen(QColor(self.mutedColor)))
        xAxis.setTickFont(QFont("inter", int(0.8*self.vw)))
        yAxis.setTextPen(QPen(QColor(self.mutedColor)))
        yAxis.setTickFont(QFont("inter", int(0.8*self.vw)))
        self.graph.setLabel("left", "Hours", **graphStyles) # Dictionary unpacking operator is necessary

        # App info Section
        self.appInfoHeader = QWidget(self.appInfoSection)
        self.appInfoTitle = QLabel("App Usage", self.appInfoHeader)
        self.appInfoLine = LineDrawer(color = self.mutedColor, strokeWidth = int(0.2*self.vw), direction = "horizontal")
        self.appInfoLine.setMinimumWidth(200)
        self.appInfoLine.setMinimumHeight(int(0.2*self.vw))
        appInfoHeadingLayout.addWidget(self.appInfoTitle)
        appInfoHeadingLayout.addWidget(self.appInfoLine)
        appInfoHeadingLayout.setContentsMargins(0,0,0,0)
        self.appInfoHeader.setLayout(appInfoHeadingLayout)
        self.appInfoLayout.addWidget(self.appInfoHeader)
        self.appInfoLayout.setSpacing(1*self.vw)
        self.displayAppUsageInfo(appUsageList)
        self.appInfoSection.setLayout(self.appInfoLayout)

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
  
    

    def displayAppUsageInfo(self, appUsageList): # Display the app usage info in the app info section
        usageInfoLayout = QVBoxLayout()
        usageInfoContainer = QWidget(self.appInfoSection)
        for info in appUsageList:
            appInfoLayout = QHBoxLayout()
            cardLayout = QHBoxLayout()
            card = QWidget(usageInfoContainer)
            appInfo = QWidget(card)
            appTitle = QLabel(info[0], appInfo)
            appTitle.setAlignment(Qt.AlignVCenter)
            appTime = QLabel(info[1], card)
            appTime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            appIcon = QSvgWidget("./assets/app-icon.svg", appInfo)
            appIcon.setFixedSize(int(3*self.vw), int(3*self.vw))
            appIcon.setStyleSheet("color: black;")
            appInfoLayout.addWidget(appIcon)
            appInfoLayout.addWidget(appTitle)
            appInfoLayout.setContentsMargins(0,0,0,0)
            appInfo.setLayout(appInfoLayout)
            cardLayout.addWidget(appInfo)
            cardLayout.addWidget(appTime)
            margin = int(0.5*self.vw)
            cardLayout.setContentsMargins(margin*2, margin, margin*2, margin)
            card.setLayout(cardLayout)
            usageInfoLayout.addWidget(card)

            card.setStyleSheet(f"""
                                border: 1px solid {self.cardOutlineColor};
                                background-color: {self.cardBgColor};
                                border-radius: 8px;
                            """)
            appInfo.setStyleSheet(f"""
                                border: none;
                                border-radius: 0px;
                                font-size: {int(1.6*self.vw)}px;
                                """)
            appTime.setStyleSheet(f"""
                                border: none;
                                border-radius: 0px;
                                font-size: {int(1.4*self.vw)}px;
                                font-weight: 500;
                                """)
        usageInfoLayout.setContentsMargins(0,0,0,0)
        usageInfoLayout.setSpacing(int(0.8*self.vw))
        usageInfoContainer.setLayout(usageInfoLayout)
        self.appInfoLayout.addWidget(usageInfoContainer)


    def renderLimitsTab(self):
        self.resetTabButtonStyles()
        self.activeTabButton = self.limitsTabButton
        self.limitsTabButton.setStyleSheet(self.activeTabButtonStyle)
        self.clearContentArea()
        self.title.setText("Usage Limits")

        limitsTabLayout = QVBoxLayout()
        self.limitedAppsLayout = QVBoxLayout()
        blockedAppsLayout = QVBoxLayout()

        self.limitsSection = QWidget(self.contentArea)
        self.blockingSection = QWidget(self.contentArea)
        
        # Title and info
        self.limitedApps = QWidget(self.limitsSection)
        self.limitedAppsTitle = QLabel("Limited Apps", self.limitsSection)
        self.limitedAppsLine = LineDrawer(color = self.mutedColor, strokeWidth = int(0.2*self.vw), direction = "horizontal")
        self.limitedAppsLine.setMinimumWidth(200)
        self.limitedAppsLine.setMinimumHeight(int(0.2*self.vw))
        self.limitedAppsLayout.addWidget(self.limitedAppsTitle)
        self.limitedAppsLayout.addWidget(self.limitedAppsLine)
        self.limitedAppsLayout.setContentsMargins(0,0,0,0)
        self.displayLimits([("Code", "4h 3m 13s", "9h 30m")]) # Display the app limits info

        # Button for adding new limits
        self.limitsButtonContainer = QWidget(self.limitsSection)
        limitsButtonLayout = QHBoxLayout()
        limitsButtonLayout.setContentsMargins(0,0,0,0)
        self.limitsPlusButton = QPushButton("+", self.limitsButtonContainer)
        self.limitsPlusButton.setFont(QFont("Segoe UI", int(2.5 * self.vw), QFont.Bold))
        self.limitsPlusButton.setFixedSize(int(8.5*self.vw), int(2.5*self.vw))
        limitsButtonLayout.addWidget(self.limitsPlusButton, alignment= Qt.AlignVCenter | Qt.AlignRight)
        self.limitsPlusButton.setCursor(Qt.PointingHandCursor)
        self.limitsButtonContainer.setLayout(limitsButtonLayout)
        self.limitedAppsLayout.addWidget(self.limitsButtonContainer)
        self.limitsSection.setLayout(self.limitedAppsLayout)

        self.limitedAppsTitle.setStyleSheet(f"""
                                        font-size: {int(1.4*self.vw)}px;
                                        font-weight: 400;
                                        """)
        self.limitsPlusButton.setStyleSheet(f"""
                                        color: {self.cardBgColor};
                                        font-size: {int(2.5*self.vw)}px;
                                        font-weight: 300;
                                        padding-bottom: {int(0.5*self.vw)}px;
                                        border: none;
                                        border-radius: 8px;
                                        background-color: {self.primaryColor};
                                        """)

        limitsTabLayout.addWidget(self.limitsSection)
        limitsTabLayout.addWidget(self.blockingSection)
        self.contentArea.setLayout(limitsTabLayout)


    def renderSettingsTab(self):
        self.resetTabButtonStyles()
        self.activeTabButton = self.settingsButton
        self.settingsButton.setStyleSheet(self.activeTabButtonStyle)
        self.clearContentArea()
    

    def displayLimits(self, limitedAppUsageToday = []): # Display the app limits info
        limitsBlockLayout = QVBoxLayout()
        limitsBlockContainer = QWidget(self.limitsSection)
        for info in limitedAppUsageToday:
            appInfoLayout = QHBoxLayout()
            cardLayout = QHBoxLayout()
            card = QWidget(limitsBlockContainer)
            appInfo = QWidget(card)
            appTitle = QLabel(info[0], appInfo)
            appTitle.setAlignment(Qt.AlignVCenter)
            appTime = QLabel(info[1] + " / " + info[2], card)
            appTime.setAlignment(Qt.AlignCenter)
            appIcon = QSvgWidget("./assets/app-icon.svg", appInfo)
            appIcon.setFixedSize(int(3*self.vw), int(3*self.vw))
            appIcon.setStyleSheet(f"color: {self.textColor};")
            buttonContainer = QWidget(card)
            buttonContainer.setStyleSheet("border: none;")
            containerLayout = QHBoxLayout()
            containerLayout.setContentsMargins(0,0,0,0)
            deletelimitButton = QPushButton(buttonContainer)
            deletelimitButton.setIcon(QIcon("./assets/delete-icon.svg"))
            deletelimitButton.setIconSize(QSize(int(2*self.vw), int(2*self.vw)))
            deletelimitButton.setCursor(Qt.PointingHandCursor)
            containerLayout.addWidget(deletelimitButton, alignment= Qt.AlignVCenter | Qt.AlignRight)
            buttonContainer.setLayout(containerLayout)
            appInfoLayout.addWidget(appIcon)
            appInfoLayout.addWidget(appTitle)
            appInfoLayout.setContentsMargins(0,0,0,0)
            appInfo.setLayout(appInfoLayout)
            cardLayout.addWidget(appInfo)
            cardLayout.addWidget(appTime)
            cardLayout.addWidget(buttonContainer)
            margin = int(0.5*self.vw)
            cardLayout.setContentsMargins(margin*2, margin, margin*2, margin)
            card.setLayout(cardLayout)
            limitsBlockLayout.addWidget(card)

            card.setStyleSheet(f"""
                                border: 1px solid {self.cardOutlineColor};
                                background-color: {self.cardBgColor};
                                border-radius: 8px;
                            """)
            appInfo.setStyleSheet(f"""
                                border: none;
                                border-radius: 0px;
                                font-size: {int(1.6*self.vw)}px;
                                """)
            appTime.setStyleSheet(f"""
                                border: none;
                                border-radius: 0px;
                                font-size: {int(1.4*self.vw)}px;
                                font-weight: 500;
                                """)
            deletelimitButton.setStyleSheet(f"""
                                            color: {self.textColor};
                                            border: none
                                            """)
        limitsBlockLayout.setContentsMargins(0,0,0,0)
        limitsBlockLayout.setSpacing(int(0.8*self.vw))
        limitsBlockContainer.setLayout(limitsBlockLayout)
        self.limitedAppsLayout.addWidget(limitsBlockContainer)
    
    
    def clearContentArea(self): # Wipe out everything except the header
        for child in self.contentArea.findChildren(QWidget):
            child.setParent(None)
            child.deleteLater()
        if self.contentArea.layout() is not None:
            self.contentArea.layout().deleteLater()
            # To delete a layout, you must assign it to a temporary widget first
            # and then delete the temporary widget
            temp = QWidget()
            temp.setLayout(self.contentArea.layout())
            temp.setParent(None)
            temp.deleteLater()


def main():
    app = QApplication(sys.argv) # consider sys.argv a placeholder
    window = MainWindow()
    window.show()
    app.exec_() # starts the event loop

main()