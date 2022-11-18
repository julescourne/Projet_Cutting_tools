from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey
from sources.model.__init__ import Base


class Piece(Base):
    """Classe du modèle représentant une pièce"""
    __tablename__ = 'Piece'

    id = Column(Integer, primary_key=True)
    materiau = Column(VARCHAR(15))
    type_fabrication = Column(VARCHAR(15))
    fatigue = Column(Float)
    durete = Column(Float)
    contraintes_residuelles = Column(Float)
    temps = Column(Float)
    rugosite = relationship("Rugosite", uselist=False, back_populates="piece", cascade="all, delete")
    id_experience = Column(Integer, ForeignKey('Experience.id'))
    experience = relationship("Experience", back_populates="piece", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe piece"""
        if not len(args) == 0:
            self.materiau = args[0]
            self.type_fabrication = args[1]
            self.fatigue = args[2]
            self.durete = args[3]
            self.contraintes_residuelles = args[4]
            self.temps = args[5]
            self.rugosite = args[6]
            self.experience = args[7]

    def __eq__(self, other):
        """Fonction qui compare deux objets piece

        Parameters
        ----------
        other : Piece
            L'objet pièce à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.experience is None and self.rugosite is None:
            return self.materiau == other.materiau and self.type_fabrication == other.type_fabrication and self.fatigue == other.fatigue and self.durete == other.durete and self.contraintes_residuelles == other.contraintes_residuelles and self.temps == other.temps and other.experience is None and other.rugosite is None
        elif self.experience is not None and self.rugosite is None:
            return self.materiau == other.materiau and self.type_fabrication == other.type_fabrication and self.fatigue == other.fatigue and self.durete == other.durete and self.contraintes_residuelles == other.contraintes_residuelles and self.temps == other.temps and self.experience.nom == other.experience.nom and other.rugosite is None
        elif self.experience is None and self.rugosite is not None:
            return self.materiau == other.materiau and self.type_fabrication == other.type_fabrication and self.fatigue == other.fatigue and self.durete == other.durete and self.contraintes_residuelles == other.contraintes_residuelles and self.temps == other.temps and other.experience is None and self.rugosite.valeur == other.rugosite.valeur
        else:
            return self.materiau == other.materiau and self.type_fabrication == other.type_fabrication and self.fatigue == other.fatigue and self.durete == other.durete and self.contraintes_residuelles == other.contraintes_residuelles and self.experience.nom == other.experience.nom and self.rugosite.valeur == other.rugosite.valeur

    @property
    def __materiau__(self):
        return self.materiau

    @__materiau__.setter
    def __materiau__(self, materiau):
        self.materiau = materiau

    @property
    def __type_fabrication__(self):
        return self.type_fabrication

    @__type_fabrication__.setter
    def __type_fabrication__(self, type_fabrication):
        self.type_fabrication = type_fabrication

    @property
    def __fatigue__(self):
        return self.fatigue

    @__fatigue__.setter
    def __fatigue__(self, fatigue):
        self.fatigue = fatigue

    @property
    def __durete__(self):
        return self.durete

    @__durete__.setter
    def __durete__(self, durete):
        self.durete = durete

    @property
    def __contraintes_residuelles__(self):
        return self.contraintes_residuelles

    @__contraintes_residuelles__.setter
    def __contraintes_residuelles__(self, contraintes_residuelles):
        self.contraintes_residuelles = contraintes_residuelles

    @property
    def __temps__(self):
        return self.temps

    @__temps__.setter
    def __temps__(self, temps):
        self.temps = temps

    @property
    def __rugosite__(self):
        return self.rugosite

    @__rugosite__.setter
    def __rugosite__(self, rugosite):
        self.rugosite = rugosite

    @property
    def __experience__(self):
        return self.experience

    @__experience__.setter
    def __experience__(self, experience):
        self.experience = experience
