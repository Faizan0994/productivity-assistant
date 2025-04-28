import os
import sys
import winshell
from win32com.client import Dispatch
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt

class DigitalClock(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Digital Clock")
        self.resize(300, 100)

        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setStyleSheet("font-size:40px; color:#2E8B57;")

        layout = QVBoxLayout()
        layout.addWidget(self.clock_label)
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

        # Do NOT show the window automatically
        self.hide()

    def update_time(self):
        self.clock_label.setText(QTime.currentTime().toString("hh:mm:ss"))

def install_startup():
    exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(_file_)
    startup_dir = winshell.startup()
    shortcut = os.path.join(startup_dir, "DigitalClock.lnk")

    if not os.path.exists(shortcut):
        shell = Dispatch('WScript.Shell').CreateShortCut(shortcut)
        shell.TargetPath = exe_path
        shell.Arguments = ""  # No arguments needed
        shell.WorkingDirectory = os.path.dirname(exe_path)
        shell.IconLocation = exe_path
        shell.save()

def main():
    install_startup()
    app = QApplication(sys.argv)
    clock = DigitalClock()
    # Do NOT call clock.show() anywhere to keep it hidden completely
    sys.exit(app.exec_())

if _name_ == "_main_":
    main()