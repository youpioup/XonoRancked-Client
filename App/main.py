import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
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
        self.timer = QTimer()

        self.join_button.clicked.connect(self.start_search)
        self.timer.timeout.connect(self.join)
    
    def start_search(self):
        self.join_button.setText("Wait for a game")
        self.timer.start(5000)


    def join(self):
        if self.slots_avalible() > 0:
            self.join_game(self.get_server())
            self.timer.stop()
            self.join_button.setText("Join")

    def get_server(self):
        url = "http://127.0.0.1:8000/server/0"
        res = requests.get(url)
        if res.status_code == 200:
            port = res.json()["port"]
            return port
        else:
            print(f"error:{res.status_code}")
        


    def slots_avalible(self):
        r = requests.get("http://127.0.0.1:8000/server_status/0")
        if r.status_code == 200:
            slots = r.json()["slot_free"]
            return slots
        else:
            print (f"error:{r.status_code}")


    def join_game(self, port:int):

        subprocess.run(["xonotic-sdl-wrapper", f"+connect 192.168.1.155:{port}"])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())