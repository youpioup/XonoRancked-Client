import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtCore import QTimer
import subprocess
import requests
import os

def load_config():
    if not os.path.exists("config.txt"):
        with open("config.txt", "w") as f:
            f.write("backend_ip=127.0.0.1\n")
            f.write("backend_port=8000\n")
        print("fichier de config crée avec des valeurs par défaut.")

    with open("config.txt", "r") as f:
        lines = f.readlines()

    config = {}
    for line in lines:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)
            config[key] = value
    return config


class MainWindow(QMainWindow):
    def __init__(self):
        self.xonotic_process = None
        super().__init__()
        self.setWindowTitle("XonoRanked")

        self.join_button = QPushButton("Join")
        self.launch_commande = QLineEdit("xonotic-sdl-wrapper")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.launch_commande)
        self.layout.addWidget(self.join_button)
        self.centralWidget.setLayout(self.layout)
        self.timer = QTimer()
        self.server_check_timer = QTimer()

        self.join_button.clicked.connect(self.start_search)
        self.timer.timeout.connect(self.join)
        self.server_check_timer.timeout.connect(self.server_check)
    
    def start_search(self):
        self.join_game(self.get_server(0)["ip_address"], self.get_server(0)["port"])
        self.join_button.setText("Wait for a game")
        self.timer.start(5000)

    def server_check(self):
        if self.slots_avalible(1) < 2:
            self.join_game(self.get_server(0)["ip_address"], self.get_server(0)["port"])
            self.start_search()

    def join(self):
        if self.slots_avalible(1) > 0:
            self.join_game(self.get_server(1)["ip_address"], self.get_server(1)["port"])
            self.timer.stop()
            self.server_check_timer.start(5000)
            self.join_button.setText("Join")

    def get_server(self, id):
        backend_ip = load_config()["backend_ip"]
        backend_port = load_config()["backend_port"]
        url = f"http://{backend_ip}:{backend_port}/server/{id}"
        res = requests.get(url)
        if res.status_code == 200:
            print(res.json())
            return res.json()
        else:
            print(f"error:{res.status_code}")
        

    def slots_avalible(self, server_id):
        backend_ip = load_config()["backend_ip"]
        backend_port = load_config()["backend_port"]
        url = f"http://{backend_ip}:{backend_port}/server_status/{server_id}"
        r = requests.get(url)
        if r.status_code == 200:
            try:
                data = r.json()
                slots = data["available_slots"]
                if isinstance(slots, int):
                    return slots
                else:
                    return 0
            except KeyError:
                return 0
            except ValueError:
                return 0
        else:
            print(f"error HTTP : {r.status_code}")
            return 0

    def join_game(self, ip_address: str, port:int):

        if self.xonotic_process:
            self.xonotic_process.terminate()
            self.xonotic_process.wait(timeout=30)
            self.xonotic_process = subprocess.Popen([self.launch_commande.text(), f"+connect {ip_address}:{port}"])
        else:
            self.xonotic_process = subprocess.Popen([self.launch_commande.text(), f"+connect {ip_address}:{port}"])



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())