from PyQt5.QtWidgets import QScrollArea, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPen, QColor, QPainter
import pyqtgraph as pg

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