from models.equipement_model import EquipementModel

class EquipementController:
    def __init__(self):
        self.model = EquipementModel()

    def liste(self):
        return self.model.get_all()

    def ajouter(self, nom):
        self.model.create(nom)

    def modifier(self, id_, nom):
        self.model.update(id_, nom)

    def supprimer(self, id_):
        self.model.delete(id_)
