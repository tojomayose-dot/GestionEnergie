from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QMessageBox
)
from controllers.energie_controller import EnergieController
from datetime import datetime, timedelta

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = EnergieController()
        self.setWindowTitle("Gestion intelligente de l'énergie")
        self.setGeometry(100, 100, 600, 400)

        central = QWidget()
        self.layout = QVBoxLayout()

        # Consommation
        self.label_conso = QLabel("Consommation du jour : 0 kWh")
        self.layout.addWidget(self.label_conso)

        # Bouton actualiser
        btn_refresh = QPushButton("Actualiser")
        btn_refresh.clicked.connect(self.actualiser)
        self.layout.addWidget(btn_refresh)

        # Bouton alertes
        btn_alertes = QPushButton("Voir alertes")
        btn_alertes.clicked.connect(self.afficher_alertes)
        self.layout.addWidget(btn_alertes)

        # Bouton coupure
        btn_coupure = QPushButton("Simuler coupure JIRAMA")
        btn_coupure.clicked.connect(self.simuler_coupure)
        self.layout.addWidget(btn_coupure)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        btn_graph = QPushButton("Afficher graphique")
        btn_graph.clicked.connect(self.afficher_graphique)
        self.layout.addWidget(self.canvas)

        self.label_score = QLabel("Efficacite energetique : ---")
        self.layout.addWidget(self.label_score)

        central.setLayout(self.layout)
        self.setCentralWidget(central)

    def actualiser(self):
        total = self.controller.consommation_cumulee("jour")
        self.label_conso.setText(f"Consommation du jour : {total} kWh")

    def afficher_alertes(self):
        alertes = self.controller.alertes_consommation(seuil_kwh=50)

        if not alertes:
            QMessageBox.information(self, "Alertes", "Aucune anomalie détectée")
            return

        message = "Anomalies détectées :\n\n"
        for a in alertes:
            message += f"{a['nom']} : {a['total']} kWh\n"

        QMessageBox.warning(self, "Alertes énergétiques", message)

    def simuler_coupure(self):
        debut = datetime.now() - timedelta(hours=2)
        fin = datetime.now()
        self.controller.enregistrer_coupure(debut, fin)
        QMessageBox.information(self, "Coupure", "Coupure JIRAMA enregistrée")

    def afficher_graphique(self):
        data = self.controller.consommation_par_source_graph()

        noms = [row["nom"] for row in data]
        valeurs = [row["total"] for row in data]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(noms, valeurs)
        ax.set_title("Consommation par source (kWh)")
        ax.set_ylabel("kWh")

        self.canvas.draw()

        score = self.controller.score_efficacite()
        self.label_score.setText(f"Efficacité énergétique : {score}")
