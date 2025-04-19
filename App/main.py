import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import subprocess
import requests


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
        url = "http://127.0.0.1:8000/server/0"

        res = requests.get(url)

        if res.status_code == 200:
            print(res.json())

        subprocess.run([f"xonotic-sdl-wrapper", "+connect 192.168.1.155:{res.json[port]}"])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())