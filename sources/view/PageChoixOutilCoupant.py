from tkinter import Frame, Label, Entry, Button, LEFT, RIGHT, Canvas, Checkbutton, BooleanVar, ttk, LabelFrame
from tkinter.constants import *

from PIL import ImageTk, Image

from sources.Constants import DURETE_U, VITESSE_COUPE_U, VITESSE_AVANCE_U, PROFONDEUR_PASSE_U, \
    EFFORT_COUPE_FX_U, EFFORT_COUPE_FY_U, EFFORT_COUPE_FZ_U, TEMPERATURE_U, TYPE_LUBRIFIANT, RUGOSITE_U, \
    CONTRAINTES_RESIDUELLES_U, TYPE_FAB_PIECE, TYPE_MAT_PIECE, DUREE_VIE_OUTIL
from sources.controller.ConditionsCoupeController import ConditionsCoupeController
from sources.controller.PieceController import PieceController


class PageChoixOutilCoupant:
    """Classe qui gère la vue de la page Choix Outil Coupant"""

    def __init__(self, window):
        """Constructeur de la page choix outil coupant

        Parameters
        ----------
        window : Tk
            La fenêtre principale de l'application
        """

        # Déclaration des controllers nécéssaires
        self.pie_controller = PieceController()
        self.con_coupe_controller = ConditionsCoupeController()

        # creer la frame principale
        self.frame_choix_outil = Frame(window)
        self.frame_left = Frame(self.frame_choix_outil)
        self.frame_right = LabelFrame(self.frame_choix_outil, text="Conditions sur l'expérience", font=("Arial", 15))
        self.frame_left.pack(side=LEFT, padx=40)
        self.frame_right.pack(side=RIGHT, padx=40, pady=20)

        self.frame_left_top = LabelFrame(self.frame_left, text="Conditions sur l'outil et la pièce", font=("Arial", 15))
        self.frame_left_top.pack(side=TOP)

        self.frame_left_bot = Frame(self.frame_left)
        self.frame_left_bot.pack(side=BOTTOM)

        self.frame_left_top_top = LabelFrame(self.frame_left_top, text="Requis", font=("Arial", 13))
        self.frame_left_top_top.pack(side=TOP, padx=5, pady=10)

        self.frame_left_top_bot = Frame(self.frame_left_top)
        self.frame_left_top_bot.pack(side=BOTTOM)

        """
        self.canvas_choix_outil = Canvas(self.frame_choix_outil, width=1080, height=720)
        self.canvas_choix_outil.pack(fill="both", expand=True)

        self.canvas_choix_outil.create_image(0, 0, image=background_image, anchor="nw")

        # ajout logos
        self.logo_univ = ImageTk.PhotoImage(
            Image.open("../images/UnivTours-Logo horizontal.jpg").resize((138, 50), Image.ANTIALIAS))
        self.label_logo_univ = Label(self.frame_choix_outil, image=self.logo_univ)
        self.label_logo_univ.place(relx=0.0, rely=1.0, anchor="ne")
        self.logo_ceroc = ImageTk.PhotoImage(
            Image.open("../images/Ceroc logo 2020.jpg").resize((153, 50), Image.ANTIALIAS))
        self.label_logo_ceroc = Label(self.frame_choix_outil, image=self.logo_ceroc)
        self.label_logo_ceroc.place(relx=0.0, rely=1.09, anchor="ne")
        """
        # FRAME LEFT

        # durée de vie outil
        self.bool_duree_vie_outil = BooleanVar()
        self.frame_duree_vie_outil = Frame(self.frame_left_top_bot, borderwidth=2, relief=RAISED)
        self.frame_duree_vie_outil.pack(pady=40)
        self.checkbox_duree_vie_outil = Checkbutton(self.frame_duree_vie_outil, variable=self.bool_duree_vie_outil)
        self.checkbox_duree_vie_outil.pack(side=RIGHT)
        self.label_duree_vie_outil = Label(self.frame_duree_vie_outil, text=DUREE_VIE_OUTIL, font=("Arial", 15))
        self.label_duree_vie_outil.pack(side=LEFT)
        self.entry_duree_vie_outil = Entry(self.frame_duree_vie_outil)
        self.entry_duree_vie_outil.pack(side=RIGHT)

        # type matériau pièce
        self.frame_type_materiau_piece = Frame(self.frame_left_top_top, borderwidth=2, relief=RAISED)
        self.frame_type_materiau_piece.pack(pady=40)
        self.label_type_materiau_piece = Label(self.frame_type_materiau_piece, text=TYPE_MAT_PIECE, font=("Arial", 15))
        self.label_type_materiau_piece.pack(side=LEFT)
        self.combobox_type_materiau_piece = ttk.Combobox(self.frame_type_materiau_piece, values=self.pie_controller.get_materials_types())
        self.combobox_type_materiau_piece.pack(side=RIGHT, padx=5)

        # type fabrication pièce
        self.frame_type_fab_piece = Frame(self.frame_left_top_top, borderwidth=2, relief=RAISED)
        self.frame_type_fab_piece.pack(pady=15)
        self.label_type_fab_piece = Label(self.frame_type_fab_piece, text=TYPE_FAB_PIECE, font=("Arial", 15))
        self.label_type_fab_piece.pack(side=LEFT, padx=5)
        self.combobox_type_fab_piece = ttk.Combobox(self.frame_type_fab_piece, values=self.pie_controller.get_manufacturing_types())
        self.combobox_type_fab_piece.pack(side=RIGHT, padx=5)

        # dureté
        self.bool_durete = BooleanVar()
        self.frame_durete = Frame(self.frame_left_top_bot, borderwidth=2, relief=RAISED)
        self.frame_durete.pack(pady=15)
        self.checkbox_durete = Checkbutton(self.frame_durete, variable=self.bool_durete)
        self.checkbox_durete.pack(side=RIGHT)
        self.label_durete = Label(self.frame_durete, text=DURETE_U, font=("Arial", 15))
        self.label_durete.pack(side=LEFT, padx=5)
        self.entry_durete = Entry(self.frame_durete)
        self.entry_durete.pack(side=RIGHT, padx=5)

        # Contraintes résiduelles
        self.bool_cr = BooleanVar()
        self.frame_cr = Frame(self.frame_left_top_bot, borderwidth=2, relief=RAISED)
        self.frame_cr.pack(pady=15)
        self.checkbox_cr = Checkbutton(self.frame_cr, variable=self.bool_cr)
        self.checkbox_cr.pack(side=RIGHT)
        self.label_cr = Label(self.frame_cr, text=CONTRAINTES_RESIDUELLES_U, font=("Arial", 15))
        self.label_cr.pack(side=LEFT, padx=5)
        self.entry_cr = Entry(self.frame_cr)
        self.entry_cr.pack(side=RIGHT, padx=5)

        # rugosité
        self.bool_rugosite = BooleanVar()
        self.frame_rugosite = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_rugosite.pack(pady=15)
        self.checkbox_rugosite = Checkbutton(self.frame_rugosite, variable=self.bool_rugosite)
        self.checkbox_rugosite.pack(side=RIGHT)
        self.label_rugosite = Label(self.frame_rugosite, text=RUGOSITE_U, font=("Arial", 15))
        self.label_rugosite.pack(side=LEFT, padx=5)
        self.entry_rugosite = Entry(self.frame_rugosite)
        self.entry_rugosite.pack(side=RIGHT, padx=5)

        # fatigue pièce (pas pris en compte encore)
        """
        self.frame_fatigue = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_fatigue.pack(pady=15)
        self.checkbox_fatigue = Checkbutton(self.frame_fatigue)
        self.checkbox_fatigue.pack(side=RIGHT)
        self.label_fatigue = Label(self.frame_fatigue, text=PROFONDEUR_PASSE_U, font=("Arial", 15))
        self.label_fatigue.pack(side=LEFT, padx=5)
        self.entry_fatigue = Entry(self.frame_fatigue)
        self.entry_fatigue.pack(side=RIGHT, padx=5)
        """

        # Right FRAME

        # type lubrifiant
        self.bool_type_lub = BooleanVar()
        self.frame_type_lub = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_type_lub.pack(pady=15)
        self.checkbox_type_lub = Checkbutton(self.frame_type_lub, variable=self.bool_type_lub)
        self.checkbox_type_lub.pack(side=RIGHT)
        self.label_type_lub = Label(self.frame_type_lub, text=TYPE_LUBRIFIANT, font=("Arial", 15))
        self.label_type_lub.pack(side=LEFT, padx=5)
        self.combobox_type_lub = ttk.Combobox(self.frame_type_lub, values=self.con_coupe_controller.get_lubrication_types())
        self.combobox_type_lub.pack(side=RIGHT, padx=5)

        # vitesse de coupe
        self.bool_vc = BooleanVar()
        self.frame_vc = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_vc.pack(pady=15)
        self.checkbox_vc = Checkbutton(self.frame_vc, variable=self.bool_vc)
        self.checkbox_vc.pack(side=RIGHT)
        self.label_vc = Label(self.frame_vc, text=VITESSE_COUPE_U, font=("Arial", 15))
        self.label_vc.pack(side=LEFT, padx=5)
        self.entry_vc = Entry(self.frame_vc)
        self.entry_vc.pack(side=RIGHT, padx=5)

        # vitesse d'avance
        self.bool_fz = BooleanVar()
        self.frame_fz = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_fz.pack(pady=15)
        self.checkbox_fz = Checkbutton(self.frame_fz, variable=self.bool_fz)
        self.checkbox_fz.pack(side=RIGHT)
        self.label_fz = Label(self.frame_fz, text=VITESSE_AVANCE_U, font=("Arial", 15))
        self.label_fz.pack(side=LEFT, padx=5)
        self.entry_fz = Entry(self.frame_fz)
        self.entry_fz.pack(side=RIGHT, padx=5)

        # profondeur de passe
        self.bool_ap = BooleanVar()
        self.frame_ap = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_ap.pack(pady=15)
        self.checkbox_ap = Checkbutton(self.frame_ap, variable=self.bool_ap)
        self.checkbox_ap.pack(side=RIGHT)
        self.label_ap = Label(self.frame_ap, text=PROFONDEUR_PASSE_U, font=("Arial", 15))
        self.label_ap.pack(side=LEFT, padx=5)
        self.entry_ap = Entry(self.frame_ap)
        self.entry_ap.pack(side=RIGHT, padx=5)

        # Effort Fx
        self.bool_effort_x = BooleanVar()
        self.frame_effort_x = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_effort_x.pack(pady=15)
        self.checkbox_effort_x = Checkbutton(self.frame_effort_x, variable=self.bool_effort_x)
        self.checkbox_effort_x.pack(side=RIGHT)
        self.label_effort_x = Label(self.frame_effort_x, text=EFFORT_COUPE_FX_U+" Maximum", font=("Arial", 15))
        self.label_effort_x.pack(side=LEFT, padx=5)
        self.entry_effort_x = Entry(self.frame_effort_x)
        self.entry_effort_x.pack(side=RIGHT, padx=5)

        # Effort Fy
        self.bool_effort_y = BooleanVar()
        self.frame_effort_y = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_effort_y.pack(pady=15)
        self.checkbox_effort_y = Checkbutton(self.frame_effort_y, variable=self.bool_effort_y)
        self.checkbox_effort_y.pack(side=RIGHT)
        self.label_effort_y = Label(self.frame_effort_y, text=EFFORT_COUPE_FY_U+" Maximum", font=("Arial", 15))
        self.label_effort_y.pack(side=LEFT, padx=5)
        self.entry_effort_y = Entry(self.frame_effort_y)
        self.entry_effort_y.pack(side=RIGHT, padx=5)

        # Effort Fz
        self.bool_effort_z = BooleanVar()
        self.frame_effort_z = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_effort_z.pack(pady=15)
        self.checkbox_effort_z = Checkbutton(self.frame_effort_z, variable=self.bool_effort_z)
        self.checkbox_effort_z.pack(side=RIGHT)
        self.label_effort_z = Label(self.frame_effort_z, text=EFFORT_COUPE_FZ_U+" Maximum", font=("Arial", 15))
        self.label_effort_z.pack(side=LEFT, padx=5)
        self.entry_effort_z = Entry(self.frame_effort_z)
        self.entry_effort_z.pack(side=RIGHT, padx=5)

        # température
        self.bool_tmp = BooleanVar()
        self.frame_tmp = Frame(self.frame_right, borderwidth=2, relief=RAISED)
        self.frame_tmp.pack(pady=15)
        self.checkbox_tmp = Checkbutton(self.frame_tmp, variable=self.bool_tmp)
        self.checkbox_tmp.pack(side=RIGHT)
        self.label_tmp = Label(self.frame_tmp, text=TEMPERATURE_U + " Moyenne", font=("Arial", 15))
        self.label_tmp.pack(side=LEFT, padx=5)
        self.entry_tmp = Entry(self.frame_tmp)
        self.entry_tmp.pack(side=RIGHT, padx=5)

        # frame des boutons du bas
        self.frame_south = Frame(self.frame_left_bot)
        self.frame_south.pack(side=BOTTOM, pady=70)
        self.button_accueil = Button(self.frame_south, text="Accueil", font=("Arial", 20), bg='white', fg='black')
        self.button_accueil.pack(side=LEFT)
        self.button_valider = Button(self.frame_south, text="Valider", font=("Arial", 20), bg='white', fg='black')
        self.button_valider.pack(side=RIGHT)

        # Liste

        self.entries = [self.entry_tmp, self.entry_vc, self.entry_ap, self.entry_fz, self.entry_cr,
                        self.entry_duree_vie_outil, self.entry_durete, self.entry_effort_x,
                        self.entry_effort_y, self.entry_effort_z, self.entry_rugosite]
