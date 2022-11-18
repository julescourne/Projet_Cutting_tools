from tkinter import Frame, Button, LEFT, Canvas, Label
from PIL import ImageTk, Image


class PageResultats:
    """Classe qui gère la vue de la page Résultats"""

    def __init__(self, window, background_image):
        """Constructeur de la page résultats (qualité de surface)

        Parameters
        ----------
        window : Tk
            La fenêtre principale de l'application
        background_image: PhotoImage
            L'objet qui prend une image en argument
        """
        # creer la frame principale
        self.frame_resultats = Frame(window)

        self.canvas_resultats = Canvas(self.frame_resultats, width=1080, height=720)
        self.canvas_resultats.pack(fill="both", expand=True)

        self.canvas_resultats.create_image(0, 0, image=background_image, anchor="nw")

        # ajout logos
        self.logo_univ = ImageTk.PhotoImage(
            Image.open("../images/UnivTours-Logo horizontal.jpg").resize((138, 50), Image.ANTIALIAS))
        self.label_logo_univ = Label(self.canvas_resultats, image=self.logo_univ)
        self.label_logo_univ.place(relx=1.0, rely=0.0, anchor="ne")
        self.logo_ceroc = ImageTk.PhotoImage(
            Image.open("../images/Ceroc logo 2020.jpg").resize((153, 50), Image.ANTIALIAS))
        self.label_logo_ceroc = Label(self.canvas_resultats, image=self.logo_ceroc)
        self.label_logo_ceroc.place(relx=1.0, rely=0.09, anchor="ne")

        # creer la frame du graphique
        self.frame_graphic = Frame(self.canvas_resultats)
        self.frame_graphic.pack()

        # creer la frame des boutons du bas
        self.frame_south = Frame(self.canvas_resultats)
        self.frame_south.pack(pady=50)

        self.butt_accueil = Button(self.frame_south, text="Accueil", font=("Arial", 15), bg='white', fg='black')
        self.butt_accueil.pack(side=LEFT, padx=25)

        self.butt_supprimer_experience = Button(self.frame_south, text="Supprimer l'expérience", font=("Arial", 15),
                                                bg='white',
                                                fg='black')
        self.butt_supprimer_experience.pack(side=LEFT,
                                            padx=25)

        self.butt_choix_conditions_coupe = Button(self.frame_south, text="Page précédente",
                                                  font=("Arial", 15),
                                                  bg='white',
                                                  fg='black')
        self.butt_choix_conditions_coupe.pack(side=LEFT, padx=25)

        self.butt_export_image = Button(self.frame_south, text="Exporter en image",
                                        font=("Arial", 15),
                                        bg='white',
                                        fg='black')
        self.butt_export_image.pack(side=LEFT, padx=25)

        self.butt_export_pdf = Button(self.frame_south, text="Exporter en pdf",
                                      font=("Arial", 15),
                                      bg='white',
                                      fg='black')
        self.butt_export_pdf.pack(side=LEFT, padx=25)
