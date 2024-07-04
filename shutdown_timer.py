import os
import sys

from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QColor, QPainterPath, QPalette, QRegion
from PyQt5.QtWidgets import (QApplication, QDial, QDialog, QDialogButtonBox,
                             QHBoxLayout, QLabel, QMainWindow, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)


class CustomTitleBar(QWidget):
    def __init__(self, parent=None, title="", color="#121212"):
        super(CustomTitleBar, self).__init__(parent)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(color))
        self.setPalette(palette)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #BB86FC;")

        self.minimize_button = QPushButton('-')
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet(
            "background-color: #6200EE; color: white; border: none; border-radius: 5px;")
        self.minimize_button.clicked.connect(self.minimize)

        self.close_button = QPushButton('x')
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet(
            "background-color: #6200EE; color: white; border: none; border-radius: 5px;")
        self.close_button.clicked.connect(self.close)

        layout = QHBoxLayout()
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def minimize(self):
        self.window().showMinimized()

    def close(self):
        self.window().close()

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.window().move(event.globalPos() - self.start)

    def mouseReleaseEvent(self, event):
        self.pressing = False


class CustomMessageBox(QDialog):
    def __init__(self, title, message, parent=None):
        super(CustomMessageBox, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)

        layout = QVBoxLayout()
        self.title_bar = CustomTitleBar(self, title, "#1E1E1E")
        layout.addWidget(self.title_bar)

        self.label = QLabel(message)
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.buttonBox.button(QDialogButtonBox.Yes).setText('Yes')
        self.buttonBox.button(QDialogButtonBox.No).setText('No')
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
                color: #ffffff;
                border-radius: 10px;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #6200EE;
                color: #ffffff;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3700B3;
            }
        """)

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        super().resizeEvent(event)

    @staticmethod
    def showMessage(title, message, parent=None):
        dialog = CustomMessageBox(title, message, parent)
        result = dialog.exec_()
        return result == QDialog.Accepted


class CountdownMessageBox(QDialog):
    def __init__(self, title, message, countdown_seconds=15, parent=None):
        super(CountdownMessageBox, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.countdown_seconds = countdown_seconds

        layout = QVBoxLayout()
        self.title_bar = CustomTitleBar(self, title, "#1E1E1E")
        layout.addWidget(self.title_bar)

        self.label = QLabel(message)
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        self.countdown_label = QLabel(
            f"Shutting down in {self.countdown_seconds} seconds...")
        self.countdown_label.setStyleSheet("color: #BB86FC;")
        layout.addWidget(self.countdown_label)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setText('Ok')
        self.buttonBox.button(QDialogButtonBox.Cancel).setText('Cancel')
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
                color: #ffffff;
                border-radius: 10px;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #6200EE;
                color: #ffffff;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3700B3;
            }
        """)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateCountdown)
        self.timer.start(1000)

    def updateCountdown(self):
        self.countdown_seconds -= 1
        self.countdown_label.setText(
            f"Shutting down in {self.countdown_seconds} seconds...")
        if self.countdown_seconds <= 0:
            self.timer.stop()
            self.accept()

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        super().resizeEvent(event)

    @staticmethod
    def showMessage(title, message, countdown_seconds=15, parent=None):
        dialog = CountdownMessageBox(title, message, countdown_seconds, parent)
        result = dialog.exec_()
        return result == QDialog.Accepted


class ShutdownTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Shutdown Timer')
        self.setGeometry(300, 300, 400, 300)  # Increased the size

        # Remove default title bar and set custom one
        self.setWindowFlag(Qt.FramelessWindowHint)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Apply rounded corners to the main window
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

        self.title_bar = CustomTitleBar(self, "Shutdown Timer")
        self.setMenuWidget(self.title_bar)

        # Set the dark theme palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.WindowText, QColor("#ffffff"))
        central_widget.setPalette(palette)
        central_widget.setAutoFillBackground(True)

        # Set the dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow {
                border-radius: 10px;
                border: 1px solid white;
            }
            QLabel {
                color: #ffffff;
            }
            QDial {
                background: #333333;
                border: none;
            }
            QPushButton {
                background-color: #6200EE;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3700B3;
            }
        """)

        layout = QVBoxLayout()

        self.label = QLabel('Set shutdown time (minutes):', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        dial_layout = QHBoxLayout()
        dial_layout.addStretch()
        self.dial = QDial(self)
        self.dial.setRange(1, 120)  # 1 to 120 minutes
        self.dial.setValue(30)  # Default to 30 minutes
        self.dial.setNotchesVisible(True)
        self.dial.setFixedSize(120, 120)  # Increased size of the dial
        self.dial.valueChanged.connect(self.updateLabel)

        # Apply a custom stylesheet for the QDial to set the color
        self.dial.setStyleSheet("""
            QDial {
                background-color: #333333;
                border: none;
            }
            QDial::groove:horizontal {
                border: 1px solid #BB86FC;
                background: #BB86FC;
                width: 10px;
                border-radius: 5px;
            }
            QDial::handle {
                background: #BB86FC;
                border: 1px solid #BB86FC;
                width: 10px;
                height: 10px;
                border-radius: 5px;
                margin: -5px 0; /* half the width of the handle */
            }
        """)

        dial_layout.addWidget(self.dial)
        dial_layout.addStretch()
        layout.addLayout(dial_layout)

        self.timeLabel = QLabel('30 minutes', self)
        self.timeLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timeLabel)

        self.button = QPushButton('Start Timer', self)
        self.button.clicked.connect(self.setShutdownTimer)
        layout.addWidget(self.button)

        central_widget.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDial)

    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        super().resizeEvent(event)

    def updateLabel(self, value):
        self.timeLabel.setText(f'{value} minutes')

    def setShutdownTimer(self):
        self.time_remaining = self.dial.value() * 60  # time remaining in seconds
        result = CustomMessageBox.showMessage(
            'Confirm Shutdown', f'Are you sure you want to shut down the PC in {self.time_remaining // 60} minutes?', self)

        if result:
            self.timer.start(1000)  # start the timer to update every second
            QTimer.singleShot(self.time_remaining * 1000,
                              self.showCountdownMessageBox)

    def showCountdownMessageBox(self):
        result = CountdownMessageBox.showMessage(
            'Shutdown Warning', 'The PC will shut down in 15 seconds. Click OK to shut down immediately or Cancel to abort.', 15, self)

        if result:
            self.shutdownPC()
        else:
            self.timer.stop()

    def updateDial(self):
        if self.time_remaining > 0:
            # update remaining time based on dial value
            self.time_remaining = self.dial.value() * 60
            self.time_remaining -= 1
            remaining_minutes = self.time_remaining // 60
            self.updateLabel(remaining_minutes)
        else:
            self.timer.stop()

    def shutdownPC(self):
        if sys.platform == 'win32':
            os.system('shutdown /s /t 0')
        else:
            CustomMessageBox.showMessage(
                'Error', 'This function is only supported on Windows.', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShutdownTimerApp()
    ex.show()
    sys.exit(app.exec_())
