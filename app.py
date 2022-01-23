import sys

from PyQt5.QtCore import QObject, QThread, pyqtSignal

from PyQt5 import QtCore, QtGui, QtWidgets

from main import voice_assistant, greet

class VoiceAssistantWorker(QObject):
    finished = pyqtSignal()
    greet_finished = pyqtSignal()

    def run(self):
        voice_assistant()
        self.finished.emit()
    
    def greet(self):
        greet()
        self.greet_finished.emit()
    
    def stop(self):
        self._isRunning = False


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grażyna 2000")
        self.setFixedWidth(500)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        p = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0, 500, 300, 0)
        gradient.setColorAt(0.0, QtGui.QColor(207,236,247))
        gradient.setColorAt(0.8, QtGui.QColor(98,193,229))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)

        self.b1 = QtWidgets.QPushButton("Słuchaj")
        QtGui.QFontDatabase.addApplicationFont("Rubik-Medium.ttf")
        self.b1.setStyleSheet("""QPushButton {
            background-color: #fcfcfc;
            border-radius: 4px;
            border-style: none;
            font-family: 'Rubik Medium', sans-serif;
            font-size: 16px;
            font-weight: 700;
            line-height: 1.5;
            margin: 0;
            max-width: none;
            min-height: 40px;
            min-width: 10px;
            outline: none;
            padding: 8px 16px 6px;
            position: relative;
            text-align: center;
            text-transform: none;
            width: 100%;
        }
        QPushButton:disabled {
            background-color: #db6a6a;
            color: #FFFFFF;
        }
        """)
        self.b1.setGeometry(200, 230, 100, 40)
        self.b1.setCheckable(True)
        self.b1.setEnabled(False)
        self.b1.clicked.connect(self.toggle_voice_assistant)

        layout.addWidget(self.b1, 1, 1)
        self.setLayout(layout)
        self.run_greet_task()
    
    def run_greet_task(self):
        self.thread = QThread()
        self.worker = VoiceAssistantWorker()
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.greet)
        self.worker.greet_finished.connect(self.thread.quit)
        self.worker.greet_finished.connect(lambda: self.b1.setEnabled(True))
        self.thread.start()

    def run_voice_assistant_task(self):
        self.thread = QThread()
        self.worker = VoiceAssistantWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(lambda: self.b1.setEnabled(True))
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
    
    def toggle_voice_assistant(self):
        self.b1.setEnabled(False)
        self.run_voice_assistant_task()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())