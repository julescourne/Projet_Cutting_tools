from tkinter import Frame, Label, Entry, Button, LEFT, RIGHT, Canvas, Checkbutton, BooleanVar, ttk, LabelFrame, \
    StringVar
from tkinter.constants import *
from tkinter.ttk import Treeview

from PIL import ImageTk, Image

from sources.Constants import DURETE_U, VITESSE_COUPE_U, VITESSE_AVANCE_U, PROFONDEUR_PASSE_U, \
    EFFORT_COUPE_FX_U, EFFORT_COUPE_FY_U, EFFORT_COUPE_FZ_U, TEMPERATURE_U, TYPE_LUBRIFIANT, RUGOSITE_U, \
    CONTRAINTES_RESIDUELLES_U, TYPE_FAB_PIECE, TYPE_MAT_PIECE, DUREE_VIE_OUTIL
from sources.controller.ConditionsCoupeController import ConditionsCoupeController
from sources.controller.PieceController import PieceController


class PageResultatsChoixOutilCoupant:
    """Classe qui gère la vue de la page des résultats du choix  de l'outil coupant"""

    def __init__(self, window):
        """Constructeur de la page des résultats du choix  de l'outil coupant

        Parameters
        ----------
        window : Tk
            La fenêtre principale de l'application
        """

        # creer la frame principale
        self.frame_resultats = Frame(window)

        # TOP
        self.frame_top = Frame(self.frame_resultats)
        self.frame_top_left = Frame(self.frame_top)
        self.frame_top_right = Frame(self.frame_top)
        self.frame_top.pack(side=TOP)
        self.frame_top_left.pack(side=LEFT, padx=40)
        self.frame_top_right.pack(side=RIGHT, padx=40)

        # BOTTOM
        self.frame_bot = Frame(self.frame_resultats)
        self.frame_bot_right = LabelFrame(self.frame_bot, text="Listes des expériences les plus similaires", font=("Arial", 15))
        self.frame_bot_left = Frame(self.frame_bot)
        self.frame_bot.pack(side=BOTTOM)
        self.frame_bot_left.pack(side=LEFT, padx=40)
        self.frame_bot_right.pack(side=RIGHT, padx=40)

        self.n_components_str = StringVar()
        self.label_componnets = Label(self.frame_top_left, textvariable=self.n_components_str)
        self.label_componnets.pack()

        self.butt_acp_2d = Button(self.frame_top_left, text="Afficher l'ACP en 2D", font=("Arial", 15),
                                      bg='white', fg='black')
        self.butt_acp_2d.pack(pady=50)

        self.butt_acp_3d = Button(self.frame_top_left, text="Afficher l'ACP en 3D", font=("Arial", 15),
                                  bg='white', fg='black')
        self.butt_acp_3d.pack(pady=50)

        self.butt_acp_params = Button(self.frame_top_right, text="Afficher l'ACP (2D) avec les variables", font=("Arial", 15),
                                      bg='white', fg='black')
        self.butt_acp_params.pack(pady=50)

        self.butt_accueil = Button(self.frame_bot_left, text="Accueil", font=("Arial", 15),
                                  bg='white', fg='black')
        self.butt_accueil.pack(side=LEFT)

        self.butt_retour = Button(self.frame_bot_left, text="Retour", font=("Arial", 15),
                                  bg='white', fg='black')
        self.butt_retour.pack(side=RIGHT)

        self.tableau = Treeview(self.frame_bot_right, columns=('id', 'nom', 'dist', 'type_lub'))
        self.tableau.heading('id', text='ID Expérience')
        self.tableau.heading('nom', text="Nom de l'expérience")
        self.tableau.heading('dist', text='Distance')
        self.tableau.heading('type_lub', text='Type de lubrifiant')
        self.tableau.pack(pady=50)
