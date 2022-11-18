from sqlalchemy import Column, Integer, Float, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sources.model.__init__ import Base


class Outil(Base):
    """Classe du modèle représentant un outil"""
    __tablename__ = 'Outil'

    id = Column(Integer, primary_key=True)
    nom = Column(VARCHAR(15))
    materiau = Column(VARCHAR(15))
    geometrie = Column(VARCHAR(15))
    duree_de_vie = Column(Float)
    temps = Column(Float)
    id_experience = Column(Integer, ForeignKey('Experience.id'))
    experience = relationship("Experience", back_populates="outil", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe outil"""
        if not len(args) == 0:
            self.nom = args[0]
            self.materiau = args[1]
            self.geometrie = args[2]
            self.duree_de_vie = args[3]
            self.temps = args[4]
            self.experience = args[5]

    def __eq__(self, other):
        """Fonction qui compare deux objets outil

        Parameters
        ----------
        other : Outil
            L'objet outil à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.experience is None:
            return self.nom == other.nom and self.materiau == other.materiau and self.geometrie == other.geometrie and self.duree_de_vie == other.duree_de_vie and self.temps == other.temps and other.experience is None
        else:
            return self.nom == other.nom and self.materiau == other.materiau and self.geometrie == other.geometrie and self.duree_de_vie == other.duree_de_vie and self.temps == other.temps and self.experience.nom == other.experience.nom

    @property
    def __nom__(self):
        return self.nom

    @__nom__.setter
    def __nom__(self, nom):
        self.nom = nom

    @property
    def __materiau__(self):
        return self.materiau

    @__materiau__.setter
    def __materiau__(self, materiau):
        self.materiau = materiau

    @property
    def __geometrie__(self):
        return self.geometrie

    @__geometrie__.setter
    def __geometrie__(self, geometrie):
        self.geometrie = geometrie

    @property
    def __duree_de_vie__(self):
        return self.duree_de_vie

    @__duree_de_vie__.setter
    def __duree_de_vie__(self, duree_de_vie):
        self.duree_de_vie = duree_de_vie

    @property
    def __temps__(self):
        return self.temps

    @__temps__.setter
    def __temps__(self, temps):
        self.temps = temps

    @property
    def __experience__(self):
        return self.experience

    @__experience__.setter
    def __experience__(self, experience):
        self.experience = experience
