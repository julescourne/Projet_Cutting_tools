from sources.model.EffortCoupe import EffortCoupe
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model import session


class EffortCoupeController:
    """Classe qui gère l'ajout d'un objet effort de coupe dans la base de données"""

    def __init__(self):
        """Constructeur de la classe effortcoupecontroller"""
        self.effort_coupe = EffortCoupe()

    def create_effort_coupe(self, fx, fy, fz, type_lubrifiant_conditions_coupe):
        """fonction qui ajoute un effort de coupe à la base de données

        Parameters
        ----------
        fx : float
            La composante fx de l'effort de coupe
        fy : float
            La composante fy de l'effort de coupe
        fz : float
            La composante fz de l'effort de coupe
        type_lubrifiant_conditions_coupe : str
            Le type de lubrifiant de l'objet conditions de coupe en lien avec l'effort de coupe

        """
        self.effort_coupe.fx = fx
        self.effort_coupe.fy = fy
        self.effort_coupe.fz = fz

        if type_lubrifiant_conditions_coupe != "":
            conditions_coupe = session.query(ConditionsCoupe).filter_by(type_lubrifiant=type_lubrifiant_conditions_coupe).all()
            if len(conditions_coupe) != 0:
                self.effort_coupe.conditions_coupe = conditions_coupe[-1]
        else:
            self.effort_coupe.conditions_coupe = None

        session.add(self.effort_coupe)
        session.commit()
        session.close()
