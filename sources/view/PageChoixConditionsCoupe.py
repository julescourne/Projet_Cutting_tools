from tkinter import Frame, Button, StringVar, Radiobutton, LEFT, Label, RAISED, Entry, Canvas
from sources.Constants import GRAPH2D, GRAPH3D
from PIL import ImageTk, Image


class PageChoixConditionsCoupe:
    """Classe qui gère la vue de la page Choix Conditions de Coupe"""

    def __init__(self, window, background_image):
        """Constructeur de la page choix conditions de coupe

        Parameters
        ----------
        window : Tk
            La fenêtre principale de l'application
        background_image: PhotoImage
            L'objet qui prend une image en argument
        """
        # liste des checkbuttons
        self.list_cb_ab = []
        self.list_cb_or = []
        self.list_cb_co = []

        # creer la frame principale
        self.frame_choix_cond = Frame(window)

        # création du canvas
        self.canvas_choix_cond = Canvas(self.frame_choix_cond, width=1080, height=720)
        self.canvas_choix_cond.pack(fill="both", expand=True)

        self.canvas_choix_cond.create_image(0, 0, image=background_image, anchor="nw")

        # ajout logos
        self.logo_univ = ImageTk.PhotoImage(
            Image.open("../images/UnivTours-Logo horizontal.jpg").resize((138, 50), Image.ANTIALIAS))
        self.label_logo_univ = Label(self.canvas_choix_cond, image=self.logo_univ)
        self.label_logo_univ.place(relx=1.0, rely=0.0, anchor="ne")
        self.logo_ceroc = ImageTk.PhotoImage(
            Image.open("../images/Ceroc logo 2020.jpg").resize((153, 50), Image.ANTIALIAS))
        self.label_logo_ceroc = Label(self.canvas_choix_cond, image=self.logo_ceroc)
        self.label_logo_ceroc.place(relx=1.0, rely=0.09, anchor="ne")

        # création frame téléchargement
        self.frame_telechargement = Frame(self.canvas_choix_cond)
        self.butt_telechargement = Button(self.frame_telechargement, text="Télécharger le gabarit excel type",
                                          font=("Arial", 20),
                                          bg='white',
                                          fg='black')
        self.butt_telechargement.pack()
        self.frame_telechargement.pack(pady=10)

        # création frame sélectionner fichier
        self.frame_selectionner_fichier = Frame(self.canvas_choix_cond)
        self.butt_selectionner_fichier = Button(self.frame_selectionner_fichier,
                                                text="Sélectionner un fichier d'une expérience d'usinage",
                                                font=("Arial", 20), bg='white',
                                                fg='black')
        self.butt_selectionner_fichier.pack()
        self.frame_selectionner_fichier.pack(pady=10)

        # ajout des checbox pour le choix d'un graphique en 2D ou en 3D
        self.frame_cb = Frame(self.canvas_choix_cond)
        self.type_graphique = StringVar(value=GRAPH2D)

        self.button_2d = Radiobutton(self.frame_cb, text=GRAPH2D, variable=self.type_graphique,
                                     value=GRAPH2D)
        self.button_2d.pack(side=LEFT)
        self.button_3d = Radiobutton(self.frame_cb, text=GRAPH3D, variable=self.type_graphique,
                                     value=GRAPH3D)
        self.button_3d.pack(side=LEFT)
        self.frame_cb.pack(pady=20)

        # frame qui permet à l'utilisateur de choisir un nuage de point ou une courbe dans le cas 2D
        self.frame_type_graph_2D = Frame(self.canvas_choix_cond)
        self.type_graphique_2D = StringVar(value="nuage de points")

        self.button_points = Radiobutton(self.frame_type_graph_2D, text="nuage de points",
                                         variable=self.type_graphique_2D,
                                         value="nuage de points")
        self.button_courbe = Radiobutton(self.frame_type_graph_2D, text="courbe", variable=self.type_graphique_2D,
                                         value="courbe")
        self.frame_type_graph_2D.pack(pady=10)

        # frame sélection des axes
        self.frame_label_abscisse = Frame(self.canvas_choix_cond)
        self.frame_label_abscisse.pack()
        self.label_selectionner_abscisse = Label(self.frame_label_abscisse, font=("Arial", 20),
                                                 text="Sélectionner axe x",
                                                 relief=RAISED)

        # creer la frame des checkbox abscisse
        self.frame_cb_abscisse = Frame(self.canvas_choix_cond)
        self.frame_cb_abscisse.pack()

        self.list_texts = ["temps", "vitesse de coupe", "vitesse d'avance", "profondeur de passe", "géométrie outil",
                           "type lubrifiant",
                           "type fabrication pièce", "contraintes résiduelles", "durée de vie outil",
                           "dureté",
                           "effort de coupe fx", "effort de coupe fy", "effort de coupe fz", "rugosité", "température"]

        self.list_res = ["temps", "vitesse_coupe", "vitesse_avance", "profondeur_passe", "geometrie_outil",
                         "type_lubrifiant",
                         "type_fabrication_piece", "contraintes_residuelles", "duree_vie_outil",
                         "durete",
                         "effort_coupe_fx", "effort_coupe_fy", "effort_coupe_fz", "rugosite", "temperature"]

        self.var_abscisse = StringVar(value=self.list_res[0])
        self.var_ordonnee = StringVar(value=self.list_res[0])
        self.var_cote = StringVar(value=self.list_res[0])

        # ajout des checks button pour l'abscisse
        for i in range(len(self.list_texts)):
            self.list_cb_ab.append(
                Radiobutton(self.frame_cb_abscisse, text=self.list_texts[i], variable=self.var_abscisse,
                            value=self.list_res[i]))

        self.frame_label_ordonnee = Frame(self.canvas_choix_cond)
        self.frame_label_ordonnee.pack()
        self.label_selectionner_ordonnee = Label(self.frame_label_ordonnee, font=("Arial", 20),
                                                 text="Sélectionner axe y",
                                                 relief=RAISED)

        # creer la frame des checkbox ordonnees
        self.frame_cb_ordonne = Frame(self.canvas_choix_cond)
        self.frame_cb_ordonne.pack()

        # ajout des checks button pour l'ordonnée
        for i in range(len(self.list_texts)):
            self.list_cb_or.append(
                Radiobutton(self.frame_cb_ordonne, text=self.list_texts[i], variable=self.var_ordonnee,
                            value=self.list_res[i]))

        # frame axe z
        self.frame_label_cote = Frame(self.canvas_choix_cond)
        self.frame_label_cote.pack()
        self.label_selectionner_cote = Label(self.frame_label_cote, font=("Arial", 20), text="Sélectionner axe z",
                                             relief=RAISED)

        # creer la frame des checkbox cote
        self.frame_cb_cote = Frame(self.canvas_choix_cond)
        self.frame_cb_cote.pack()

        # ajout des checks button pour la cote
        for i in range(len(self.list_texts)):
            self.list_cb_co.append(Radiobutton(self.frame_cb_cote, text=self.list_texts[i], variable=self.var_cote,
                                               value=self.list_res[i]))

        # creer la frame des textbox pour les fonctions des variables
        self.frame_func_var = Frame(self.canvas_choix_cond)
        self.frame_func_var.pack()

        self.frame_text_abscisse = Frame(self.frame_func_var)
        self.frame_text_abscisse.pack()

        self.frame_text_ordonnee = Frame(self.frame_func_var)
        self.frame_text_ordonnee.pack()

        self.frame_text_cote = Frame(self.frame_func_var)
        self.frame_text_cote.pack()

        self.label_abscisse = Label(self.frame_text_abscisse, text="fonction X")
        self.entry_abscisse = Entry(self.frame_text_abscisse)
        self.label_ordonnee = Label(self.frame_text_ordonnee, text="fonction Y")
        self.entry_ordonnee = Entry(self.frame_text_ordonnee)
        self.label_cote = Label(self.frame_text_cote, text="fonction Z")
        self.entry_cote = Entry(self.frame_text_cote)

        self.frame_aide = Frame(self.canvas_choix_cond)
        self.frame_aide.pack()
        self.button_aide = Button(self.frame_aide, text="Aide", bg='white', fg='black')

        # creer la frame des boutons du bas
        self.frame_south = Frame(self.canvas_choix_cond)
        self.frame_south.pack(pady=10)

        self.butt_accueil = Button(self.frame_south, text="Accueil", font=("Arial", 20), bg='white', fg='black')
        self.butt_accueil.pack(side=LEFT)

        self.butt_valider = Button(self.frame_south, text="Valider", font=("Arial", 20), bg='white', fg='black')
