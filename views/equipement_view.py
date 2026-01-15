from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox
)
from controllers.equipement_controller import EquipementController


class EquipementView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = EquipementController()

        layout = QVBoxLayout()

        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Nom de l’équipement")
        layout.addWidget(self.input_nom)

        btn_add = QPushButton("Ajouter")
        btn_add.clicked.connect(self.ajouter)
        layout.addWidget(btn_add)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "Nom"])
        layout.addWidget(self.table)

        btns = QHBoxLayout()
        btn_del = QPushButton("Supprimer")
        btn_del.clicked.connect(self.supprimer)
        btns.addWidget(btn_del)

        layout.addLayout(btns)
        self.setLayout(layout)

        self.charger()

    def charger(self):
        data = self.controller.liste()
        self.table.setRowCount(len(data))

        for i, e in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(e["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(e["nom"]))

    def ajouter(self):
        nom = self.input_nom.text()
        if not nom:
            QMessageBox.warning(self, "Erreur", "Nom requis")
            return
        self.controller.ajouter(nom)
        self.input_nom.clear()
        self.charger()

    def supprimer(self):
        row = self.table.currentRow()
        if row < 0:
            return
        id_ = int(self.table.item(row, 0).text())
        self.controller.supprimer(id_)
        self.charger()
