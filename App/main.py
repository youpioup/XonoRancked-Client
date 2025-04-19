import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import subprocess


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.join_button = QPushButton("Join")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.join_button)
        self.centralWidget.setLayout(self.layout)

        self.join_button.clicked.connect(self.join_game)
    
    def join_game(self):
        subprocess.run(["xonotic-sdl-wrapper", "+connect 192.168.1.155:26000"])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())