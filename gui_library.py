from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import QTimer, Qt

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