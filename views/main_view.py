from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from controllers.energie_controller import EnergieController
from datetime import datetime, timedelta


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = EnergieController()

        self.setWindowTitle("Gestion intelligente de l’énergie – Madagascar")
        self.setGeometry(100, 100, 1000, 600)

        # ===== Widget central =====
        central = QWidget()
        self.main_layout = QVBoxLayout()

        # ===== Titre =====
        titre = QLabel("Tableau de bord énergétique")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setStyleSheet("font-size:20px; font-weight:bold;")
        self.main_layout.addWidget(titre)

        # ===== Onglets =====
        self.tabs = QTabWidget()
        self.tabs.addTab(self.dashboard_tab(), "Dashboard")
        self.tabs.addTab(self.historique_tab(), "Historique des coupures")
        self.tabs.addTab(self.info_tab(), "Informations")
        self.main_layout.addWidget(self.tabs)

        central.setLayout(self.main_layout)
        self.setCentralWidget(central)

        # Dessiner le graphe au démarrage
        self.afficher_graphique()
        self.actualiser()

    # ONGLET DASHBOARD
    def dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # ---- Indicateurs (KPI) ----
        kpi_layout = QHBoxLayout()

        self.label_conso = QLabel("Consommation totale : 0 kWh")
        self.label_conso.setStyleSheet("font-size:14px;")
        kpi_layout.addWidget(self.label_conso)

        self.label_score = QLabel("Efficacité énergétique : ---")
        self.label_score.setStyleSheet("font-size:14px;")
        kpi_layout.addWidget(self.label_score)

        layout.addLayout(kpi_layout)

        # ---- Boutons ----
        btn_layout = QHBoxLayout()

        btn_refresh = QPushButton("Actualiser")
        btn_refresh.clicked.connect(self.actualiser)
        btn_layout.addWidget(btn_refresh)

        btn_alertes = QPushButton("Voir alertes")
        btn_alertes.clicked.connect(self.afficher_alertes)
        btn_layout.addWidget(btn_alertes)

        btn_coupure = QPushButton("Simuler coupure JIRAMA")
        btn_coupure.clicked.connect(self.simuler_coupure)
        btn_layout.addWidget(btn_coupure)

        layout.addLayout(btn_layout)

        # ---- Graphique ----
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        tab.setLayout(layout)
        return tab

    # ONGLET INFO
    def info_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        texte = QLabel(
            "Application de gestion intelligente de l’énergie\n\n"
            "Fonctionnalités :\n"
            "- Suivi de consommation\n"
            "- Comparaison des sources (JIRAMA / Groupe / Solaire)\n"
            "- Détection d’anomalies\n"
            "- Simulation de coupures\n\n"
            "Conçue pour le contexte énergétique de Madagascar."
        )
        texte.setStyleSheet("font-size:13px;")
        layout.addWidget(texte)

        tab.setLayout(layout)
        return tab
    
    # HISTORIQUE
    def historique_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.table_coupures = QTableWidget()
        self.table_coupures.setColumnCount(3)
        self.table_coupures.setHorizontalHeaderLabels(
            ["Début", "Fin", "Durée (h)"]
        )

        layout.addWidget(self.table_coupures)

        btn_refresh = QPushButton("Actualiser l’historique")
        btn_refresh.clicked.connect(self.charger_historique_coupures)
        layout.addWidget(btn_refresh)

        tab.setLayout(layout)

        # Charger dès l'ouverture
        self.charger_historique_coupures()
        return tab
    
    def charger_historique_coupures(self):
        data = self.controller.historique_coupures()

        self.table_coupures.setRowCount(len(data))

        for i, row in enumerate(data):
            self.table_coupures.setItem(i, 0, QTableWidgetItem(str(row["debut"])))
            self.table_coupures.setItem(i, 1, QTableWidgetItem(str(row["fin"])))
            self.table_coupures.setItem(i, 2, QTableWidgetItem(str(round(row["duree"], 2))))



    # LOGIQUE IHM
    def actualiser(self):
        total = self.controller.consommation_cumulee()
        self.label_conso.setText(f"Consommation totale : {total} kWh")

        score = self.controller.score_efficacite()
        self.label_score.setText(f"Efficacité énergétique : {score}")

    def afficher_alertes(self):
        alertes = self.controller.alertes_consommation(seuil_kwh=50)

        if not alertes:
            QMessageBox.information(self, "Alertes", "Aucune anomalie détectée")
            return

        message = "⚠️ Anomalies détectées :\n\n"
        for a in alertes:
            message += f"- {a['nom']} : {a['total']} kWh\n"

        QMessageBox.warning(self, "Alertes énergétiques", message)

    def simuler_coupure(self):
        debut = datetime.now() - timedelta(hours=2)
        fin = datetime.now()
        self.controller.enregistrer_coupure(debut, fin)
        self.charger_historique_coupures()

        QMessageBox.information(
            self,
            "Coupure JIRAMA",
            "Coupure simulée et enregistrée avec succès."
        )

    def afficher_graphique(self):
        data = self.controller.consommation_par_source_graph()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not data:
            ax.text(0.5, 0.5, "Aucune donnée disponible",
                    ha="center", va="center", fontsize=12)
        else:
            sources = [row["nom"] for row in data]
            valeurs = [row["total"] for row in data]
            ax.bar(sources, valeurs)
            ax.set_title("Consommation par source d’énergie")
            ax.set_ylabel("kWh")

        self.canvas.draw()
