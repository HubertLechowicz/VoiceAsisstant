import sys

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
)

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


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grażyna 2000")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QGridLayout()

        self.b1 = QPushButton("Słuchaj")
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
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())