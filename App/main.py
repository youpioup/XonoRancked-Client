import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtCore import QTimer
import subprocess
import requests

xonotic_process = None

class MainWindow(QMainWindow):
    def __init__(self):
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
        url = f"http://127.0.0.1:8000/server/{id}"
        res = requests.get(url)
        if res.status_code == 200:
            print(res.json())
            return res.json()
        else:
            print(f"error:{res.status_code}")
        

    def slots_avalible(self, server_id):
        url = f"http://127.0.0.1:8000/server_status/{server_id}"
        r = requests.get(url)
        print(f"Réponse brute de l'API : {r.text}")  # Affiche la réponse brute
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"Réponse JSON : {data}")  # Affiche la réponse JSON
                slots = data["available_slots"]
                if isinstance(slots, int):
                    return slots
                else:
                    return 0
            except KeyError:
                print("La clé 'available_slots' est absente de la réponse JSON.")
                return 0
            except ValueError:
                print("La réponse n'est pas un JSON valide.")
                return 0
        else:
            print(f"Erreur HTTP : {r.status_code}")
            return 0

    def join_game(self, ip_address: str, port:int):
        global xonotic_process

        if xonotic_process:
            xonotic_process.terminate()
            xonotic_process.wait(timeout=30)
            xonotic_process = subprocess.Popen([self.launch_commande.text(), f"+connect {ip_address}:{port}"])
        else:
            xonotic_process = subprocess.Popen([self.launch_commande.text(), f"+connect {ip_address}:{port}"])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())