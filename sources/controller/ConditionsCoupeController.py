from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model.Temperature import Temperature
from sources.model.EffortCoupe import EffortCoupe
from sources.model.Experience import Experience
from sources.model import session

class ConditionsCoupeController:
    """Classe qui gère l'ajout d'un objet conditons de coupe dans la base de données"""

    def __init__(self):
        """Constructeur de la classe conditionscoupecontroller"""
        self.conditions_coupe = ConditionsCoupe()

    def create_conditions_coupe(self, type_lubrifiant, vitesse_coupe, vitesse_avance, profondeur_passe, temps, effort_coupe_valeur, temperature_valeur, nom_experience):
        """fonction qui ajoute une condition de coupe à la base de données

        Parameters
        ----------
        type_lubrifiant : str
            Le type de lubrifiant de la condition de coupe
        vitesse_coupe : float
            La vitesse de coupe de la condition de coupe
        vitesse_avance : float
            La vitesse d'avance de la condition de coupe
        profondeur_passe : float
            La profondeur de passe de la condition de coupe
        temps : float
            L'instant auquel est liée la condition de coupe
        effort_coupe_valeur : list
            La liste des valeurs de l'objet effort de coupe en lien avec la condition de coupe
        temperature_valeur : float
            La valeur de l'objet température en lien avec la condition de coupe
        nom_experience : str
            Le nom de l'expérience en lien avec la condition de coupe

        """
        self.conditions_coupe.type_lubrifiant = type_lubrifiant
        self.conditions_coupe.vitesse_coupe = vitesse_coupe
        self.conditions_coupe.vitesse_avance = vitesse_avance
        self.conditions_coupe.profondeur_passe = profondeur_passe
        self.conditions_coupe.temps = temps

        if len(effort_coupe_valeur) == 3:
            if effort_coupe_valeur[0] is not None and effort_coupe_valeur[1] is not None and effort_coupe_valeur[2] is not None:
                efforts_coupe = session.query(EffortCoupe).filter_by(fx=effort_coupe_valeur[0], fy=effort_coupe_valeur[1], fz=effort_coupe_valeur[2]).all()
                if len(efforts_coupe) != 0:
                    self.conditions_coupe.effort_coupe = efforts_coupe[-1]
        else:
            self.conditions_coupe.effort_coupe = None

        if temperature_valeur is not None:
            temperatures = session.query(Temperature).filter_by(valeur=temperature_valeur).all()
            if len(temperatures) != 0:
                self.conditions_coupe.temperature = temperatures[-1]
        else:
            self.conditions_coupe.temperature = None

        if nom_experience != "":
            experience = session.query(Experience).filter_by(nom=nom_experience).all()
            if len(experience) != 0:
                self.conditions_coupe.experience = experience[-1]
        else:
            self.conditions_coupe.experience = None

        session.add(self.conditions_coupe)
        session.commit()
        session.close()

    def get_lubrication_types(self):
        """Renvoie une liste des différents types de lubrifiants présents dans la base de données cutting

        Returns:
            type_lub : liste des type de lubrifiant différent"""

        type_lubs = [type_lub[0] for type_lub in session.query(ConditionsCoupe.type_lubrifiant).distinct()]
        session.close()
        return type_lubs
