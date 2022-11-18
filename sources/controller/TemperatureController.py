from sources.model.Temperature import Temperature
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model import session


class TemperatureController:
    """Classe qui gère l'ajout d'un objet température dans la base de données"""

    def __init__(self):
        """Constructeur de la classe temperaturecontroller"""
        self.temperature = Temperature()

    def create_temperature(self, valeur, type_lubrifiant_conditions_coupe):
        """fonction qui ajoute un objet température à la base de données

        Parameters
        ----------
        valeur : float
            La valeur de la température
        type_lubrifiant_conditions_coupe : str
            Le type de lubrifiant de la condition de coupe associée à la température

        """
        self.temperature.valeur = valeur

        if type_lubrifiant_conditions_coupe != "":
            conditions_coupe = session.query(ConditionsCoupe).filter_by(type_lubrifiant=type_lubrifiant_conditions_coupe).all()
            if len(conditions_coupe) != 0:
                self.temperature.conditions_coupe = conditions_coupe[-1]

        else:
            self.temperature.conditions_coupe = None

        session.add(self.temperature)
        session.commit()
        session.close()
