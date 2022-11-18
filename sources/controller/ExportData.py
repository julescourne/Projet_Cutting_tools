import os
from pathlib import Path
from tkinter.messagebox import askokcancel
from xlsxwriter import Workbook
from sources.Constants import CONTRAINTES_RESIDUELLES, DUREE_VIE_OUTIL, DURETE, EFFORT_COUPE, RUGOSITE, TEMPERATURE, COMPLET, VITESSE_COUPE, VITESSE_AVANCE, PROFONDEUR_PASSE, GEOMETRIE_OUTIL, TYPE_LUBRIFIANT, \
    TYPE_FAB_PIECE, TYPE_MAT_PIECE, TEMPS, EFFORT_COUPE_FX, EFFORT_COUPE_FY, EFFORT_COUPE_FZ, VITESSE_COUPE_U, PROFONDEUR_PASSE_U, VITESSE_AVANCE_U, \
    CONTRAINTES_RESIDUELLES_U, TEMPS_U, DURETE_U, EFFORT_COUPE_FX_U, EFFORT_COUPE_FY_U, EFFORT_COUPE_FZ_U, RUGOSITE_U, \
    TEMPERATURE_U

class ExportData:
    """Classe qui gère le téléchargement des gabarits excel"""

    def __init__(self, type_experience):
        """Constructeur"""
        self.type_experience = type_experience

    def export_data(self, check):
        """fonction qui permet de télécharger un gabarit excel type

        Parameters
        ----------
        check : Boolean
            booléen qui permet de savoir si une fenêtre de confirmation de l'action est à afficher

        """
        xlsx_file = Workbook(
            os.path.join(str(os.path.join(Path.home(), "Downloads")), "gabarit_" + self.type_experience + ".xlsx"))
        # creation de la feuille
        sheet1 = xlsx_file.add_worksheet("Feuil1")
        sheet1.write("A1", VITESSE_COUPE_U)
        sheet1.write("A2", VITESSE_AVANCE_U)
        sheet1.write("A3", PROFONDEUR_PASSE_U)
        sheet1.write("A4", GEOMETRIE_OUTIL)
        sheet1.write("A5", TYPE_LUBRIFIANT)
        sheet1.write("A6", TYPE_FAB_PIECE)
        sheet1.write("A7", TYPE_MAT_PIECE)
        sheet1.write("A9", TEMPS_U)

        if self.type_experience == CONTRAINTES_RESIDUELLES:
            sheet1.write("B9", CONTRAINTES_RESIDUELLES_U)

        elif self.type_experience == DUREE_VIE_OUTIL:
            sheet1.write("B9", DUREE_VIE_OUTIL)

        elif self.type_experience == DURETE:
            sheet1.write("B9", DURETE_U)

        elif self.type_experience == EFFORT_COUPE:
            sheet1.write("B9", EFFORT_COUPE_FX_U)
            sheet1.write("C9", EFFORT_COUPE_FY_U)
            sheet1.write("D9", EFFORT_COUPE_FZ_U)

        elif self.type_experience == RUGOSITE:
            sheet1.write("B9", RUGOSITE_U)

        elif self.type_experience == TEMPERATURE:
            sheet1.write("B9", TEMPERATURE_U)

        elif self.type_experience == COMPLET:
            sheet1.write("B9", EFFORT_COUPE_FX_U)
            sheet1.write("C9", EFFORT_COUPE_FY_U)
            sheet1.write("D9", EFFORT_COUPE_FZ_U)
            sheet1.write("E9", CONTRAINTES_RESIDUELLES_U)
            sheet1.write("F9", DUREE_VIE_OUTIL)
            sheet1.write("G9", DURETE_U)
            sheet1.write("H9", RUGOSITE_U)
            sheet1.write("I9", TEMPERATURE_U)

        if check:
            res = askokcancel(title="Télécharger",
                              message="Voulez vous télécharger le fichier " + self.type_experience + ".xlsx ?")
            if res:
                xlsx_file.close()
        else:
            xlsx_file.close()
