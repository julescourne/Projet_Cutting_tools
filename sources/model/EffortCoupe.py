from sqlalchemy.orm import relationship
from sources.model.__init__ import Base
from sqlalchemy import Column, Integer, Float, ForeignKey


class EffortCoupe(Base):
    """Classe du modèle représentant un effort de coupe"""
    __tablename__ = 'EffortCoupe'

    id = Column(Integer, primary_key=True)
    fx = Column(Float)
    fy = Column(Float)
    fz = Column(Float)
    id_conditions_coupe = Column(Integer, ForeignKey('ConditionsCoupe.id'))
    conditions_coupe = relationship("ConditionsCoupe", back_populates="effort_coupe", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe effort de coupe"""
        if not len(args) == 0:
            self.fx = args[0]
            self.fy = args[1]
            self.fz = args[2]
            self.conditions_coupe = args[3]

    def __eq__(self, other):
        """Fonction qui compare deux objets effort de coupe

        Parameters
        ----------
        other : EffortCoupe
            L'objet effort de coupe à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        try:
            if self.conditions_coupe is None:
                return self.fx == other.fx and self.fy == other.fy and self.fz == other.fz and other.conditions_coupe is None
            else:
                return self.fx == other.fx and self.fy == other.fy and self.fz == other.fz and self.conditions_coupe.type_lubrifiant == other.conditions_coupe.type_lubrifiant and self.conditions_coupe.vitesse_coupe == other.conditions_coupe.vitesse_coupe and self.conditions_coupe.vitesse_avance == other.conditions_coupe.vitesse_avance and self.conditions_coupe.profondeur_passe == other.conditions_coupe.profondeur_passe and self.conditions_coupe.temps == other.conditions_coupe.temps
        except AttributeError:
            return False

    @property
    def __fx__(self):
        return self.fx

    @__fx__.setter
    def __fx__(self, fx):
        self.fx = fx

    @property
    def __fy__(self):
        return self.fy

    @__fy__.setter
    def __fy__(self, fy):
        self.fy = fy

    @property
    def __fz__(self):
        return self.fz

    @__fz__.setter
    def __fz__(self, fz):
        self.fz = fz

    @property
    def __conditions_coupe__(self):
        return self.conditions_coupe

    @__conditions_coupe__.setter
    def __conditions_coupe__(self, conditions_coupe):
        self.conditions_coupe = conditions_coupe
