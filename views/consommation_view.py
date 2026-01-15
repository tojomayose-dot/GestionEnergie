from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QDoubleSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QDateEdit
)
from PyQt6.QtCore import QDate
from controllers.consommation_controller import ConsommationController


class ConsommationView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ConsommationController()
        layout = QVBoxLayout()

        # ---- Formulaire ----
        form = QHBoxLayout()

        self.cb_equipement = QComboBox()
        self.cb_source = QComboBox()

        self.spin_kwh = QDoubleSpinBox()
        self.spin_kwh.setSuffix(" kWh")
        self.spin_kwh.setMaximum(10000)

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        btn_add = QPushButton("Ajouter")

        form.addWidget(self.cb_equipement)
        form.addWidget(self.cb_source)
        form.addWidget(self.spin_kwh)
        form.addWidget(self.date_edit)
        form.addWidget(btn_add)

        layout.addLayout(form)

        # ---- Tableau ----
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Équipement", "Source", "kWh", "Date"]
        )
        layout.addWidget(self.table)

        btn_del = QPushButton("Supprimer")
        btn_del.clicked.connect(self.supprimer)
        btn_add.clicked.connect(self.ajouter)
        layout.addWidget(btn_del)

        self.setLayout(layout)

        self.charger_combobox()
        self.charger_table()

    def charger_combobox(self):
        self.cb_equipement.clear()
        self.cb_source.clear()

        for e in self.controller.equipements():
            self.cb_equipement.addItem(e["nom"], e["id"])

        for s in self.controller.sources():
            self.cb_source.addItem(s["nom"], s["id"])

    def charger_table(self):
        data = self.controller.liste()
        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(row["equipement"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["source"]))
            self.table.setItem(i, 3, QTableWidgetItem(str(row["kwh"])))
            self.table.setItem(i, 4, QTableWidgetItem(row["date"]))

    def ajouter(self):
        self.controller.ajouter(
            self.cb_equipement.currentData(),
            self.cb_source.currentData(),
            self.spin_kwh.value(),
            self.date_edit.date().toString("yyyy-MM-dd")
        )
        self.charger_table()

    def supprimer(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Sélection requise")
            return

        id_ = int(self.table.item(row, 0).text())
        self.controller.supprimer(id_)
        self.charger_table()
