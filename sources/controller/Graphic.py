from tkinter.messagebox import showerror

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sources.controller.Switcher import Switcher
from sources.Constants import GRAPH3D, GRAPH2D
from math import *


class Graphic:
    """Classe qui gère la création du graphique de qualité de surface"""

    def __init__(self, frame_graphic, var_abscisse, var_ordonnee, var_cote, type_graphique, entry_abscisse,
                 entry_ordonnee, entry_cote, type_graphique_2D):
        """Constructeur qui ajoute le graphique de qualité de surface à une frame

        Parameters
        ----------
        frame_graphic : frame
            La frame qui va contenir le graphique
        var_abscisse : str
            La variable de l'axe des abscisses
        var_ordonnee : str
            La variable de l'axe des ordonnées
        var_cote : str
            La variable de l'axe des cotes
        type_graphique : str
            Le type de graphique (2D ou 3D)
        entry_abscisse : str
            La fonction à appliquer sur la variable abcsisse
        entry_ordonnee : str
            La fonction à appliquer sur la variable ordonnée
        entry_cote : str
            La fonction à appliquer sur la variable cote
        type_graphique_2D : str
            Le type de graphique 2D (nuage de points ou courbe)

        """
        self.switcher = Switcher()

        # cas aucune expérience dans la base de données
        if self.switcher.experience is None:
            showerror(title="Erreur", message="Aucune expérience dans la base de données")
            self.error_syntax_abscisse = True
            self.error_syntax_ordonnee = True
            self.error_syntax_cote = True
            return

        self.list_abscisse = self.switcher.indirect(var_abscisse)
        self.list_ordonnee = self.switcher.indirect(var_ordonnee)
        self.error_syntax_abscisse = False
        self.error_syntax_ordonnee = False
        self.error_syntax_cote = False

        # cas graphique 3D
        if type_graphique == GRAPH3D:
            self.list_cote = self.switcher.indirect(var_cote)

        # tracer le graphique
        self.fig = Figure()
        self.plot_data(frame_graphic, var_abscisse, var_ordonnee, var_cote, type_graphique, entry_abscisse,
                       entry_ordonnee, entry_cote, type_graphique_2D)

    def plot_data(self, frame_graphic, var_abscisse, var_ordonnee, var_cote, type_graphique, entry_abscisse,
                  entry_ordonnee, entry_cote, type_graphique_2D):
        """fonction qui trace le graphique

        Parameters
        ----------
        frame_graphic : frame
            La frame qui va contenir le graphique
        var_abscisse : str
            La variable de l'axe des abscisses
        var_ordonnee : str
            La variable de l'axe des ordonnées
        var_cote : str
            La variable de l'axe des cotes
        type_graphique : str
            Le type de graphique (2D ou 3D)
        entry_abscisse : str
            La fonction à appliquer sur la variable abcsisse
        entry_ordonnee : str
            La fonction à appliquer sur la variable ordonnée
        entry_cote : str
            La fonction à appliquer sur la variable cote
        type_graphique_2D : str
            Le type de graphique 2D (nuage de points ou courbe)

        """
        # application des fonctions sur les variables
        if entry_abscisse.find("X") != -1 and type(self.list_abscisse[-1]) != str:
            for i in range(len(self.list_abscisse)):
                try:
                    self.list_abscisse[i] = eval(entry_abscisse.replace("X", str(self.list_abscisse[i])))
                except (SyntaxError, NameError, ValueError):
                    self.error_syntax_abscisse = True

        if self.error_syntax_abscisse:
            showerror(title="Erreur", message="Erreur de syntaxe dans la fonction de la variable X")

        if entry_ordonnee.find("Y") != -1 and type(self.list_ordonnee[-1]) != str:
            for i in range(len(self.list_ordonnee)):
                try:
                    self.list_ordonnee[i] = eval(entry_ordonnee.replace("Y", str(self.list_ordonnee[i])))
                except (SyntaxError, NameError, ValueError):
                    self.error_syntax_ordonnee = True

        if self.error_syntax_ordonnee:
            showerror(title="Erreur", message="Erreur de syntaxe dans la fonction de la variable Y")

        # cas 2D
        if type_graphique == GRAPH2D:
            a = self.fig.add_subplot()

            # cas courbe
            if type_graphique_2D == "courbe":
                a.plot(self.list_abscisse, self.list_ordonnee, color='blue')
            # cas nuage de points
            elif type_graphique_2D == "nuage de points":
                a.scatter(self.list_abscisse, self.list_ordonnee, color='blue')

            if entry_abscisse.find("X") != -1 and type(
                    self.list_abscisse[-1]) != str and not self.error_syntax_abscisse:
                a.set_xlabel(entry_abscisse.replace("X", self.change_name_axes(var_abscisse)))
            else:
                a.set_xlabel(self.change_name_axes(var_abscisse), fontsize=14)
            if entry_ordonnee.find("Y") != -1 and type(
                    self.list_ordonnee[-1]) != str and not self.error_syntax_ordonnee:
                a.set_ylabel(entry_ordonnee.replace("Y", self.change_name_axes(var_ordonnee)))
            else:
                a.set_ylabel(self.change_name_axes(var_ordonnee), fontsize=14)

        # cas 3D
        else:
            self.error_syntax_cote = False
            if entry_cote.find("Z") != -1 and type(self.list_cote[-1]) != str:
                for i in range(len(self.list_cote)):
                    try:
                        self.list_cote[i] = eval(entry_cote.replace("Z", str(self.list_cote[i])))
                    except (SyntaxError, NameError, ValueError):
                        self.error_syntax_cote = True

            if self.error_syntax_cote:
                showerror(title="Erreur", message="Erreur de syntaxe dans la fonction de la variable Z")

            # gestion des cas où il y a au moins une variable de type string
            if type(self.list_abscisse[-1]) == str:
                self.error_syntax_abscisse = True
                showerror(title="Erreur", message="La variable X n'est pas quantitative")
                return
            if type(self.list_ordonnee[-1]) == str:
                self.error_syntax_ordonnee = True
                showerror(title="Erreur", message="La variable Y n'est pas quantitative")
                return
            if type(self.list_cote[-1]) == str:
                self.error_syntax_cote = True
                showerror(title="Erreur", message="La variable Z n'est pas quantitative")
                return

            ax = self.fig.add_subplot(projection='3d')
            # cas surface
            try:
                ax.plot_trisurf(self.list_abscisse, self.list_ordonnee, self.list_cote)
            except (RuntimeError, ValueError):
                ax.plot3D(self.list_abscisse, self.list_ordonnee, self.list_cote, color='blue')

            if entry_abscisse.find("X") != -1 and type(
                    self.list_abscisse[-1]) != str and not self.error_syntax_abscisse:
                ax.set_xlabel(entry_abscisse.replace("X", self.change_name_axes(var_abscisse)))
            else:
                ax.set_xlabel(self.change_name_axes(var_abscisse), fontsize=14)
            if entry_ordonnee.find("Y") != -1 and type(
                    self.list_ordonnee[-1]) != str and not self.error_syntax_ordonnee:
                ax.set_ylabel(entry_ordonnee.replace("Y", self.change_name_axes(var_ordonnee)))
            else:
                ax.set_ylabel(self.change_name_axes(var_ordonnee), fontsize=14)
            if entry_cote.find("Z") != -1 and type(self.list_cote[-1]) != str and not self.error_syntax_cote:
                ax.set_zlabel(entry_cote.replace("Z", self.change_name_axes(var_cote)))
            else:
                ax.set_zlabel(self.change_name_axes(var_cote), fontsize=14)

        canvas = FigureCanvasTkAgg(self.fig, master=frame_graphic)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def change_name_axes(self, text):
        """fonction qui traduit un texte en anglais et ajoute l'unité

        Parameters
        ----------
        text : str
            Le texte à traduire

        Returns
        -------
        str
            Le nom anglais du texte avec son unité

        """
        if text == "temps":
            return "Time (s)"
        elif text == "vitesse_coupe":
            return "Cutting speed (m/min)"
        elif text == "vitesse_avance":
            return "Feed of cut (mm/min)"
        elif text == "profondeur_passe":
            return "Depth of cut (mm)"
        elif text == "geometrie_outil":
            return "Tool geometry"
        elif text == "type_lubrifiant":
            return "Lubricant type"
        elif text == "type_fabrication_piece":
            return "Type of part manufacture"
        elif text == "contraintes_residuelles":
            return "Residual stresses (Pa)"
        elif text == "duree_vie_outil":
            return "Tool life (min)"
        elif text == "durete":
            return "Hardness (HV)"
        elif text == "effort_coupe_fx":
            return "Cutting force Fx (N)"
        elif text == "effort_coupe_fy":
            return "Cutting force Fy (N)"
        elif text == "effort_coupe_fz":
            return "Cutting force Fz (N)"
        elif text == "rugosite":
            return "Roughness (µm)"
        elif text == "temperature":
            return "Temperature (°C)"
