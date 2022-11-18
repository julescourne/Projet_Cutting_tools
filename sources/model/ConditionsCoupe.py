from sqlalchemy.orm import relationship
from sources.model.__init__ import Base
from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey


class ConditionsCoupe(Base):
    """Classe du modèle représentant les conditions de coupe"""
    __tablename__ = 'ConditionsCoupe'

    id = Column(Integer, primary_key=True)
    type_lubrifiant = Column(VARCHAR(15))
    vitesse_coupe = Column(Float)
    vitesse_avance = Column(Float)
    profondeur_passe = Column(Float)
    temps = Column(Float)
    effort_coupe = relationship("EffortCoupe", uselist=False, back_populates="conditions_coupe", cascade="all, delete")
    temperature = relationship("Temperature", uselist=False, back_populates="conditions_coupe", cascade="all, delete")
    id_experience = Column(Integer, ForeignKey('Experience.id'))
    experience = relationship("Experience", back_populates="conditions_coupe", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe conditions de coupe"""
        if not len(args) == 0:
            self.type_lubrifiant = args[0]
            self.vitesse_coupe = args[1]
            self.vitesse_avance = args[2]
            self.profondeur_passe = args[3]
            self.temps = args[4]
            self.effort_coupe = args[5]
            self.temperature = args[6]
            self.experience = args[7]

    def __eq__(self, other):
        """Fonction qui compare deux objets conditions de coupe

        Parameters
        ----------
        other : ConditionsCoupe
            L'objet conditions de coupe à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.experience is None and self.effort_coupe is None and self.temperature is None:
            return self.type_lubrifiant == other.type_lubrifiant and self.vitesse_coupe == other.vitesse_coupe and self.vitesse_avance == other.vitesse_avance and self.profondeur_passe == other.profondeur_passe and self.temps == other.temps and other.experience is None and other.effort_coupe is None and other.temperature is None
        elif self.experience is None and self.effort_coupe is None and self.temperature is not None:
            return self.type_lubrifiant == other.type_lubrifiant and self.vitesse_coupe == other.vitesse_coupe and self.vitesse_avance == other.vitesse_avance and self.profondeur_passe == other.profondeur_passe and self.temps == other.temps and self.temperature.valeur == other.temperature.valeur and other.experience is None and other.effort_coupe is None
        elif self.experience is None and self.effort_coupe is not None and self.temperature is None:
            return self.type_lubrifiant == other.type_lubrifiant and self.vitesse_coupe == other.vitesse_coupe and self.vitesse_avance == other.vitesse_avance and self.profondeur_passe == other.profondeur_passe and self.temps == other.temps and self.effort_coupe.fx == other.effort_coupe.fx and self.effort_coupe.fy == other.effort_coupe.fy and self.effort_coupe.fz == other.effort_coupe.fz and other.experience is None and other.temperature is None
        elif self.experience is not None and self.effort_coupe is None and self.temperature is None:
            return self.type_lubrifiant == other.type_lubrifiant and self.vitesse_coupe == other.vitesse_coupe and self.vitesse_avance == other.vitesse_avance and self.profondeur_passe == other.profondeur_passe and self.temps == other.temps and self.experience.nom == other.experience.nom and other.effort_coupe is None and other.temperature is None
        elif self.experience is None and self.effort_coupe is not None and self.temperature is not None:
            return self.type_lubrifiant == other.type_lubrifiant and self.vitesse_coupe == other.vitesse_coupe and self.vitesse_avance == other.vitesse_avance and self.profondeur_passe == other.profondeur_passe and self.temps == other.temps and self.effort_coupe.fx == other.effort_coupe.fx and self.effort_coupe.fy == other.effort_coupe.fy and self.effort_coupe.fz == other.effort_coupe.fz and self.temperature.valeur == other.temperature.valeur and other.experience is None
        elif self.experience is not None and self.effort_coupe is None and self.temperature is not None:
            return self.type_lubrifiant == other.type_lubrifiant and self.vitesse_coupe == other.vitesse_coupe and self.vitesse_avance == other.vitesse_avance and self.profondeur_passe == other.profondeur_passe and self.temps == other.temps and self.experience.nom == other.experience.nom and self.temperature.valeur == other.temperature.valeur and other.effort_coupe is None
        elif self.experience is not None and self.effort_coupe is not None and self.temperature is None:
            return self.type_lubrifiant == other.type_lubrifiant and self.vitesse_coupe == other.vitesse_coupe and self.vitesse_avance == other.vitesse_avance and self.profondeur_passe == other.profondeur_passe and self.temps == other.temps and self.experience.nom == other.experience.nom and self.effort_coupe.fx == other.effort_coupe.fx and self.effort_coupe.fy == other.effort_coupe.fy and self.effort_coupe.fz == other.effort_coupe.fz and other.temperature is None
        else:
            return self.type_lubrifiant == other.type_lubrifiant and self.vitesse_coupe == other.vitesse_coupe and self.vitesse_avance == other.vitesse_avance and self.profondeur_passe == other.profondeur_passe and self.temps == other.temps and self.experience.nom == other.experience.nom and self.effort_coupe.fx == other.effort_coupe.fx and self.effort_coupe.fy == other.effort_coupe.fy and self.effort_coupe.fz == other.effort_coupe.fz and self.temperature.valeur == other.temperature.valeur

    def __str__(self):
        return "type lubrifiant " + self.type_lubrifiant + " vitesse de coupe " + str(
            self.vitesse_coupe) + " vitesse d'avance " + str(self.vitesse_avance) + " profondeur de passe " + str(
            self.profondeur_passe) + " effort de coupe " + self.effort_coupe + " température " + self.temperature + " expérience " + self.experience

    @property
    def __type_lubrifiant__(self):
        return self.type_lubrifiant

    @__type_lubrifiant__.setter
    def __type_lubrifiant__(self, type_lubrifiant):
        self.type_lubrifiant = type_lubrifiant

    @property
    def __vitesse_coupe__(self):
        return self.vitesse_coupe

    @__vitesse_coupe__.setter
    def __vitesse_coupe__(self, vitesse_coupe):
        self.vitesse_coupe = vitesse_coupe

    @property
    def __vitesse_avance__(self):
        return self.vitesse_avance

    @__vitesse_avance__.setter
    def __vitesse_avance__(self, vitesse_avance):
        self.vitesse_avance = vitesse_avance

    @property
    def __profondeur_passe__(self):
        return self.profondeur_passe

    @__profondeur_passe__.setter
    def __profondeur_passe__(self, profondeur_passe):
        self.profondeur_passe = profondeur_passe

    @property
    def __temps__(self):
        return self.temps

    @__temps__.setter
    def __temps__(self, temps):
        self.temps = temps

    @property
    def __effort_coupe__(self):
        return self.effort_coupe

    @__effort_coupe__.setter
    def __effort_coupe__(self, effort_coupe):
        self.effort_coupe = effort_coupe

    @property
    def __temperature__(self):
        return self.temperature

    @__temperature__.setter
    def __temperature__(self, temperature):
        self.temperature = temperature

    @property
    def __experience__(self):
        return self.experience

    @__experience__.setter
    def __experience__(self, experience):
        self.experience = experience
