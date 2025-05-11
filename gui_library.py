from PyQt5.QtWidgets import QScrollArea, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTimeEdit
from PyQt5.QtCore import QTimer, Qt, QTime, pyqtSignal
from PyQt5.QtGui import QPen, QColor, QPainter
from gui_data import appNames
import pyqtgraph as pg

lightColors = {
    "bgColor": "#EDF1F5",
    "primaryColor": "#3B82F6",
    "accentColor": "#38BDF8",
    "textColor": "#1E293B",
    "mutedColor": "#878E97",
    "cardOutlineColor": "#8199B7",
    "cardBgColor": "#E2E8F0",
    "scrollBarColor": "#94A3B8"
}

darkColors = {
    "bgColor": "#1F2937",
    "primaryColor": "#60A5FA",
    "accentColor": "#F472B6",
    "textColor": "#F9FAFB",
    "mutedColor": "#4B5563",
    "cardOutlineColor": "#334155",
    "cardBgColor": "#1E293B",
    "scrollBarColor": "#4B5563"
}

class SmartScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Start hidden

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hideScrollbar)

        # Enable mouse tracking
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)

    def wheelEvent(self, event):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Show scrollbar
        self.timer.start(1500)  # Hide after 1.5 sec of inactivity
        super().wheelEvent(event)

    def hideScrollbar(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

class FixedAxis(pg.AxisItem): # Tweaking the axes a little
    def __init__(self, labels=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.labels = labels or {}

    def tickStrings(self, values, scale, spacing): # Overriding the tickStrings method
        return [self.labels.get(int(val) % 7, str(int(val))) for val in values]
    
    def tickValues(self, minVal, maxVal, size): # Overriding the tickValues method, to remove subticks
        majorTicks = [(i, 0) for i in range(int(minVal), int(maxVal) + 1)]
        return [(1, [i for i, _ in majorTicks])]
    
class CustomGridViewBox(pg.ViewBox): # Allows changing grid color
    def __init__(self, color = "black", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gridPen = QPen(QColor(color))
        self.gridPen.setWidth(1)
        self.gridPen.setStyle(Qt.DotLine)
        self.enableAutoRange()

class LineDrawer(QWidget):
    def __init__(self, color = "black", direction = "horizontal", strokeWidth = 1):
        super().__init__()
        self.color = color
        self.direction = direction
        self.strokeWidth = strokeWidth
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(self.color), self.strokeWidth)
        painter.setPen(pen)

        if self.direction == "horizontal":
            painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)
        
        if self.direction == "vertical":
            painter.drawLine(self.width() // 2, 0, self.width() // 2, self.height())


class addLimitDialogBox(QWidget):
    closeSignal = pyqtSignal(int)
    def __init__(self, limitButtonAction, title="Add Limit", sizeUnits=1, theme="light"):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(35*sizeUnits, 25*sizeUnits)
        centeringheight = (self.screen().availableGeometry().height() - self.height()) // 2
        centeringwidth = (self.screen().availableGeometry().width() - self.width()) // 2
        self.move(centeringwidth, centeringheight)
        self.limitButtonAction = limitButtonAction

        if theme == "light":
            self.colors = lightColors
        else:
            self.colors = darkColors

        dialogLayout = QVBoxLayout()
        buttonsLayout = QHBoxLayout()
        self.dialogText = QLabel("Select an app")

        self.combo = QComboBox()
        self.combo.addItems(appNames)

        self.timeText = QLabel("Select a time limit")

        self.timeSelect = QTimeEdit()
        self.timeSelect.setDisplayFormat("hh:mm")
        self.timeSelect.setTime(QTime(0, 60))

        buttonsContainer = QWidget()
        setLimitButton = QPushButton("Set Limit")
        setLimitButton.setCursor(Qt.PointingHandCursor)
        setLimitButton.setFixedSize(12*sizeUnits, 3*sizeUnits)
        setLimitButton.clicked.connect(self.applyLimit)
        cancelButton = QPushButton("Cancel")
        cancelButton.setCursor(Qt.PointingHandCursor)
        cancelButton.clicked.connect(self.close)
        cancelButton.setFixedSize(12*sizeUnits, 3*sizeUnits)


        dialogLayout.addWidget(self.dialogText)
        dialogLayout.addWidget(self.combo)
        dialogLayout.addWidget(self.timeText)
        dialogLayout.addWidget(self.timeSelect)
        buttonsLayout.addWidget(setLimitButton)
        buttonsLayout.addWidget(cancelButton)
        buttonsContainer.setLayout(buttonsLayout)
        dialogLayout.addWidget(buttonsContainer)
        dialogLayout.setSpacing(1*sizeUnits)
        self.setLayout(dialogLayout)


        self.setStyleSheet(f"""
            background-color: {self.colors['bgColor']};
            color: {self.colors['textColor']};
            font-size: {2*sizeUnits}px;
            font-family: 'Inter', sans-serif;
        """)
        self.dialogText.setStyleSheet(f"""
            color: {self.colors['textColor']};
            font-size: {1.5*sizeUnits}px;
            margin: 0px;
            padding: 0px;
        """)
        self.timeText.setStyleSheet(f"""
            color: {self.colors['textColor']};
            font-size: {int(1.5*sizeUnits)}px;
            margin: 0px;
            padding: 0px;
        """)
        self.timeSelect.setStyleSheet(f"""
            QTimeEdit {{
                color: {self.colors['textColor']};
                font-size: {int(1.5*sizeUnits)}px;
                background-color: {self.colors['cardBgColor']};
                border: 1px solid {self.colors['cardOutlineColor']};
                border-radius: 5px;
            }}
            QTimeEdit::up-button, QTimeEdit::down-button {{
                width: 0px;
                height: 0px;
                border: none;
            }}
        """)
        self.combo.setStyleSheet(f"""
            QComboBox {{
                color: {self.colors['textColor']};
                font-size: {int(1.5*sizeUnits)}px;
                background-color: {self.colors['cardBgColor']};
                border: 1px solid {self.colors['cardOutlineColor']};
                border-radius: 5px;
            }}
        """)
        setLimitButton.setStyleSheet(f"""
            background-color: {self.colors['primaryColor']};
            color: {self.colors['bgColor']};
            border: none;
            border-radius: 8px;
        """)
        cancelButton.setStyleSheet(f"""
            background-color: transparent;
            color: {self.colors['textColor']};
            border: 1px solid {self.colors['cardOutlineColor']};
            border-radius: 8px;
        """)

    def applyLimit(self):
        appName = self.combo.currentText()
        timeLimit = self.timeSelect.time().hour() * 60 + self.timeSelect.time().minute() # Time in minutes
        self.limitButtonAction(appName, timeLimit)
        self.close()
        self.closeSignal.emit(1)