from tkinter import Toplevel, Label, StringVar, Radiobutton, Button
from sources.controller.ExportData import ExportData
from sources.Constants import CONTRAINTES_RESIDUELLES, DUREE_VIE_OUTIL, DURETE, EFFORT_COUPE, RUGOSITE, TEMPERATURE, COMPLET


class MessageBoxTelechargerGabarit:
    """Classe qui gère la fenêtre de téléchargement des gabarits"""

    def __init__(self, parent):
        """Constructeur de la fenêtre Téléchargement des gabarits

        Parameters
        ----------
        parent : frame
            La frame parent

        """
        top = self.top = Toplevel(parent)
        self.title = Label(top, text="Sélectionner le type d'expérience")
        self.title.pack()
        type_experience = StringVar(value=CONTRAINTES_RESIDUELLES)
        self.button_contraintes_residuelles = Radiobutton(top, text=CONTRAINTES_RESIDUELLES, variable=type_experience, value=CONTRAINTES_RESIDUELLES)
        self.button_contraintes_residuelles.pack()
        self.button_duree_vie_outil = Radiobutton(top, text=DUREE_VIE_OUTIL, variable=type_experience, value=DUREE_VIE_OUTIL)
        self.button_duree_vie_outil.pack()
        self.button_durete = Radiobutton(top, text=DURETE, variable=type_experience, value=DURETE)
        self.button_durete.pack()
        self.button_effort_coupe = Radiobutton(top, text=EFFORT_COUPE, variable=type_experience, value=EFFORT_COUPE)
        self.button_effort_coupe.pack()
        self.button_rugosite = Radiobutton(top, text=RUGOSITE, variable=type_experience, value=RUGOSITE)
        self.button_rugosite.pack()
        self.button_temperature = Radiobutton(top, text=TEMPERATURE, variable=type_experience, value=TEMPERATURE)
        self.button_temperature.pack()
        self.button_complet = Radiobutton(top, text=COMPLET, variable=type_experience, value=COMPLET)
        self.button_complet.pack()
        self.button_submit = Button(top, text='Télécharger', command=lambda: self.send(type_experience.get()))
        self.button_submit.pack()

    def send(self, experience):
        """Fonction qui appelle la fonction pour télécharger le fichier excel

        Parameters
        ----------
        experience : str
            Le type du gabarit à télécharger

        """
        self.top.destroy()
        export = ExportData(experience)
        export.export_data(True)
