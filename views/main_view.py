from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QMessageBox,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from controllers.energie_controller import EnergieController
from datetime import datetime, timedelta
from views.equipement_view import EquipementView
from views.consommation_view import ConsommationView


class MainView(QMainWindow):

    def __init__(self):
        super().__init__()

        # ===== STYLE GLOBAL =====
        self.setStyleSheet("""
        QMainWindow { 
            background-color: #f4f6f8; 
        }
        QLabel { 
            font-size: 13px; 
        }
        QTabWidget::pane { 
            background: white; 
        }
        QTabBar::tab { 
            padding:8px;
            background:#ddd; 
            color:black;
        }
        QTabBar::tab:selected { 
            background:#2ecc71; color:white; font-weight:bold; 
        }
        QPushButton {
            background:#3498db; color:white;
            border-radius:6px; padding:6px 12px;
        }
        QPushButton:hover { 
            background:#2980b9; 
        }
        """)

        self.controller = EnergieController()

        self.setWindowTitle("Gestion intelligente de l’énergie – Madagascar")
        self.setGeometry(100, 100, 1000, 600)

        central = QWidget()
        main_layout = QVBoxLayout()

        # ===== TITRE =====
        titre = QLabel("Tableau de bord énergétique")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setStyleSheet("font-size:20px; font-weight:bold;")
        main_layout.addWidget(titre)

        # ===== ONGLETS =====
        self.tabs = QTabWidget()
        self.tabs.addTab(self.dashboard_tab(), "Dashboard")
        self.tabs.addTab(self.historique_tab(), "Historique coupures")
        self.tabs.addTab(self.info_tab(), "Informations")
        self.tabs.addTab(EquipementView(), "Équipements")
        self.tabs.addTab(ConsommationView(), "Consommation")
        main_layout.addWidget(self.tabs)

        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # Actualiser le dashboard au démarrage
        self.actualiser()

    # ===== CREER CARTE KPI =====
    def creer_carte(self, texte, couleur):
        label = QLabel(texte)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"""
            background-color:{couleur};
            color:white;
            font-size:16px;
            font-weight:bold;
            border-radius:12px;
            padding:20px;
        """)
        return label

    # ===== DASHBOARD =====
    def dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # --- KPI ---
        kpi_layout = QHBoxLayout()
        self.label_conso = self.creer_carte("Consommation : 0 kWh", "#3498db")
        self.label_score = self.creer_carte("Efficacité : ---", "#2ecc71")
        kpi_layout.addWidget(self.label_conso)
        kpi_layout.addWidget(self.label_score)
        layout.addLayout(kpi_layout)

        # --- Boutons ---
        btn_layout = QHBoxLayout()
        btn_refresh = QPushButton("Actualiser")
        btn_refresh.clicked.connect(self.actualiser)
        btn_refresh.setToolTip("Actualiser le dashboard")
        btn_layout.addWidget(btn_refresh)

        btn_alert = QPushButton("Voir alertes")
        btn_alert.clicked.connect(self.afficher_alertes)
        btn_alert.setToolTip("Voir les anomalies de consommation")
        btn_layout.addWidget(btn_alert)

        btn_coupure = QPushButton("Simuler coupure JIRAMA")
        btn_coupure.clicked.connect(self.simuler_coupure)
        btn_coupure.setToolTip("Simuler une coupure JIRAMA")
        btn_layout.addWidget(btn_coupure)

        layout.addLayout(btn_layout)

        # --- Graphique ---
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        tab.setLayout(layout)
        return tab

    # ===== HISTORIQUE =====
    def historique_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Début", "Fin", "Durée (h)"])
        layout.addWidget(self.table)

        btn = QPushButton("Actualiser l’historique")
        btn.clicked.connect(self.charger_historique_coupures)
        layout.addWidget(btn)

        tab.setLayout(layout)
        self.charger_historique_coupures()
        return tab

    def charger_historique_coupures(self):
        data = self.controller.historique_coupures()
        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(row["debut"])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row["fin"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(round(row["duree"], 2))))

    # ===== INFO =====
    def info_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel(
            "Application de gestion intelligente de l’énergie\n\n"
            "• Suivi de consommation\n"
            "• Comparaison des sources\n"
            "• Alertes automatiques\n"
            "• Historique des coupures\n\n"
            "Adaptée au contexte énergétique de Madagascar"
        )
        layout.addWidget(label)
        tab.setLayout(layout)
        return tab

    # ===== LOGIQUE =====
    def actualiser(self):
        total = self.controller.consommation_cumulee()
        score = self.controller.score_efficacite()

        # Carte consommation
        self.label_conso.setText(f"Consommation : {total} kWh")

        # Carte efficacité avec couleur dynamique
        if "Très" in score:
            couleur = "#2ecc71"
        elif "Moyenne" in score:
            couleur = "#f39c12"
        else:
            couleur = "#e74c3c"

        self.label_score.setStyleSheet(f"""
            background-color:{couleur};
            color:white;
            font-size:16px;
            font-weight:bold;
            border-radius:12px;
            padding:20px;
        """)
        self.label_score.setText(f"Efficacité : {score}")

        # Mettre à jour graphique
        self.afficher_graphique()

    def afficher_alertes(self):
        alertes = self.controller.alertes_consommation(25)
        if not alertes:
            QMessageBox.information(self, "Alertes", "Aucune anomalie détectée")
            return

        msg = "Équipements gourmands :\n\n"
        for a in alertes:
            msg += f"- {a['nom']} : {a['total']} kWh\n"
        QMessageBox.warning(self, "Alertes", msg)

    def simuler_coupure(self):
        debut = datetime.now() - timedelta(hours=2)
        fin = datetime.now()
        self.controller.enregistrer_coupure(debut, fin)
        self.charger_historique_coupures()
        QMessageBox.information(self, "Coupure", "Coupure simulée avec succès")

    def afficher_graphique(self):
        data = self.controller.consommation_par_source_graph()
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if data:
            data_dict = {r["nom"]: r["total"] for r in data}

            ordre = ["JIRAMA", "Groupe", "Solaire"]

            sources = []
            valeurs = []
            for nom in ordre:
                sources.append(nom)
                valeurs.append(data_dict.get(nom, 0))

            couleurs = ['#e74c3c', '#3498db', '#f1c40f']

            bars = ax.bar(sources, valeurs, color=couleurs)
            ax.set_title("Consommation par source")
            ax.set_ylabel("kWh")
            ax.grid(axis="y", linestyle="--", alpha=0.5)

            for bar, val in zip(bars, valeurs):
                ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, str(val),
                        ha='center', va='bottom', fontsize=10)
        else:
            ax.text(0.5, 0.5, "Aucune donnée", ha="center", fontsize=12)

        self.canvas.draw()
