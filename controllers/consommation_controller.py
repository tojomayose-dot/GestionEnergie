from models.consommation_model import ConsommationModel
from models.equipement_model import EquipementModel
from models.source_model import SourceModel

class ConsommationController:
    def __init__(self):
        self.model = ConsommationModel()
        self.equipement_model = EquipementModel()
        self.source_model = SourceModel()

    def liste(self):
        return self.model.get_all()

    def ajouter(self, equipement_id, source_id, kwh, date):
        self.model.create(equipement_id, source_id, kwh, date)

    def supprimer(self, id_):
        self.model.delete(id_)

    def equipements(self):
        return self.equipement_model.get_all()

    def sources(self):
        return self.source_model.get_all()

    def liste_avec_cout(self, ordre="desc"):
        return self.model.get_all_with_cout(ordre=ordre)
