from PIL import ImageTk, Image
import PIL
from tkinter import BOTH, YES, LEFT, RIGHT, Tk
import os
from pathlib import Path
from tkinter.messagebox import showinfo, showerror

from sources.controller.DeleteExperience import DeleteExperience
from sources.controller.Graphic import Graphic
from sources.controller.ImportData import ImportData
from sources.controller.ChoixOutilCoupant import ChoixOutilCoupant
from sources.model import session
from sources.model.Experience import Experience
from sources.view.MenuView import MenuView
from sources.view.PageChoixConditionsCoupe import PageChoixConditionsCoupe
from sources.view.PageResultats import PageResultats
from sources.view.MessageBoxTelechargerGabarit import MessageBoxTelechargerGabarit
from sources.view.MenuAide import MenuAide
from sources.view.PageChoixOutilCoupant import PageChoixOutilCoupant
from sources.view.PageResultatsChoixOutilCoupant import PageResultatsChoixOutilCoupant
from sources.Constants import GRAPH2D, GRAPH3D, CONTRAINTES_RESIDUELLES, DUREE_VIE_OUTIL, DURETE, EFFORT_COUPE, RUGOSITE,\
                        TEMPERATURE, COMPLET, TYPE_MAT_PIECE, TYPE_FAB_PIECE, TYPE_LUBRIFIANT, VITESSE_COUPE, \
                        VITESSE_AVANCE, PROFONDEUR_PASSE, EFFORT_COUPE_FX, EFFORT_COUPE_FY, EFFORT_COUPE_FZ


def back_to_home(new_frame, old_frame):
    """fonction qui permet de changer de page

    Parameters
    ----------
    new_frame : frame
        La frame à afficher
    old_frame : frame
        La frame à enlever

    """
    old_frame.forget()
    new_frame.pack(fill=BOTH, expand=YES)


class MainController:
    """Classe MainController: classe centrale qui appelle les autres classes de l'application"""

    def __init__(self):
        """Constructeur de la classe MainController"""

        # creation fenetre
        self.window = Tk()

        # image
        self.image = PIL.Image.open("../images/theme.jpg")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image.resize((self.window.winfo_width(), self.window.winfo_height())))

        # liste des vues
        self.experiences = session.query(Experience).all()
        self.menu_view = MenuView(self.window, self.background_image)
        self.menu_view.frame_menu.bind('<Configure>', self.resize_image_menu)
        self.page_choix_conditions_coupe = PageChoixConditionsCoupe(self.window, self.background_image)
        self.page_choix_conditions_coupe.frame_choix_cond.bind('<Configure>', self.resize_image_page_choix_conditions_coupe)
        self.page_resultats = PageResultats(self.window, self.background_image)
        self.page_resultats.frame_resultats.bind('<Configure>', self.resize_image_page_resultats)
        self.page_choix_outil_coupant = PageChoixOutilCoupant(self.window)
        self.page_resultats_choix_outil_coupant = PageResultatsChoixOutilCoupant(self.window)

        self.graphic = None
        self.delete = None
        self.import_data_object = ImportData()
        self.controller_choix_outil_coupant = ChoixOutilCoupant()  # On veut que le controller change à chaque ACP
        self.form_datas = {}  # données du formulaire choix outil coupant

        # configuration action bouton
        self.menu_view.butt_import.config(
            command=lambda: self.import_file(False))
        self.menu_view.butt_conditions.config(
            command=self.display_page_conditions_coupe)
        self.menu_view.butt_outil.config(command=self.display_page_choix_outil_coupant)
        self.configure_action_buttons_page_choix_conditions_coupe()
        self.configure_action_button_page_resultats()
        self.configure_action_buttons_page_choix_outil_coupant()
        self.configure_action_buttons_page_resultats_choix_outil_coupant()

        # afficher fenetre
        self.window.mainloop()

    def resize_image(self, event):
        """fonction qui ajuste l'image en fonction de la taille de l'application"""
        self.image = self.img_copy.resize(
            (event.width, event.height), Image.ANTIALIAS)

        self.background_image = ImageTk.PhotoImage(
            self.image.resize((self.window.winfo_width(), self.window.winfo_height())))

    def resize_image_menu(self, event):
        """fonction qui ajuste la taille de l'image du background en fonction de la taille de la fenetre d'accueil"""
        self.resize_image(event)
        self.menu_view.canvas_menu.create_image(0, 0, image=self.background_image, anchor="nw")

    def resize_image_page_choix_conditions_coupe(self, event):
        """fonction qui ajuste la taille de l'image du background en fonction de la taille
                de la page choix conditions de coupe"""
        self.resize_image(event)
        self.page_choix_conditions_coupe.canvas_choix_cond.create_image(0, 0, image=self.background_image, anchor="nw")

    def resize_image_page_resultats(self, event):
        """fonction qui ajuste la taille de l'image du background en fonction de la taille de la page résultats"""
        self.resize_image(event)
        self.page_resultats.canvas_resultats.create_image(0, 0, image=self.background_image, anchor="nw")

    def display_page_conditions_coupe(self):
        """fonction qui affiche la page choix conditions coupe"""
        # titre fenetre
        self.window.title("Choix conditions de coupe")
        self.menu_view.frame_menu.forget()
        self.page_choix_conditions_coupe.frame_choix_cond.pack(fill=BOTH, expand=YES)
        self.page_choix_conditions_coupe.frame_choix_cond.bind('<Configure>', self.resize_image_page_choix_conditions_coupe)

    def display_page_resultats(self):
        """fonction qui affiche la page résultats"""
        # titre fenetre
        self.window.title("Résultats (qualité de surface)")
        self.page_choix_conditions_coupe.frame_choix_cond.forget()
        self.graphic = Graphic(self.page_resultats.frame_graphic,
                               str(self.page_choix_conditions_coupe.var_abscisse.get()),
                               str(self.page_choix_conditions_coupe.var_ordonnee.get()),
                               str(self.page_choix_conditions_coupe.var_cote.get()),
                               str(self.page_choix_conditions_coupe.type_graphique.get()),
                               self.page_choix_conditions_coupe.entry_abscisse.get(),
                               self.page_choix_conditions_coupe.entry_ordonnee.get(),
                               self.page_choix_conditions_coupe.entry_cote.get(),
                               self.page_choix_conditions_coupe.type_graphique_2D.get())
        self.page_resultats.frame_resultats.pack(fill=BOTH, expand=YES)
        self.page_resultats.frame_resultats.bind('<Configure>', self.resize_image_page_resultats)
        if self.graphic.error_syntax_abscisse or self.graphic.error_syntax_ordonnee or self.graphic.error_syntax_cote:
            self.back_from_page_resultats_to_page_conditions_coupe()

    def display_aide(self):
        """fonction qui affiche l'aide pour les formules"""
        MenuAide(self.page_choix_conditions_coupe.frame_choix_cond)

    def display_page_choix_outil_coupant(self):
        """fonction qui affiche la page choix outil coupant"""
        # titre fenetre
        self.window.title("Choix outil coupant")
        self.menu_view.frame_menu.forget()
        self.page_choix_outil_coupant.frame_choix_outil.pack(fill=BOTH, expand=YES)
    
    def validate_page_resultats_choix_outil_coupant_form(self):
        """fonction qui vérifie si le formulaire a été correctement rempli
        avant d'afficher la page des résultats du choix de l'outil coupant"""

        self.determine_checked_attributes()
        # vérifier s'il y a suffisament de données pour réaliser l'ACP.
        copy_data_without_combobox = self.form_datas.copy()
        if TYPE_LUBRIFIANT in self.form_datas:
            del copy_data_without_combobox[TYPE_LUBRIFIANT]
        if TYPE_FAB_PIECE in self.form_datas:
            del copy_data_without_combobox[TYPE_FAB_PIECE]
        if TYPE_MAT_PIECE in self.form_datas:
            del copy_data_without_combobox[TYPE_MAT_PIECE]
        if len(copy_data_without_combobox) < 3:
            showerror(title="Erreur",
                      message="Le formulaire doit contenir au moins 3 attributs afin de réaliser une ACP"
                              + "\nHors champs requis et le type de lubrifiant")
            self.form_datas.clear()
            return
        # vérifier caractère numérique de tous les champs:
        for key, value in self.form_datas.items():
            # on ne teste pas les comboboxs
            if "Type" in key:
                continue
            try:
                value_f = float(value)
            except ValueError:
                showerror(title="Erreur",
                          message="Tous les champs remplis doivent contenir uniquement des valeurs numériques."
                          + "\nNB: On utilise le point pour les nombres à virgule."
                          + "\nExemple: 0.5"
                          + "\n\n{} : {}".format(key, value))
                # Erreur, on vide le dictionnaire et l'utilisateur devra re-essayer
                self.form_datas.clear()
                return

        # si les champs requis ne sont pas renseignés:
        if not self.page_choix_outil_coupant.combobox_type_materiau_piece.get() or not self.page_choix_outil_coupant.combobox_type_fab_piece.get():
            showerror(title="Erreur",
                      message="Vous devez absolument renseigner les champs "
                              "'Matériau pièce' et 'Type fabrication pièce'")
        else:
            self.display_page_resultats_choix_outil_coupant()

    def display_page_resultats_choix_outil_coupant(self):
        """fonction qui affiche la page des résulats choix outil coupant"""

        # titre fenetre
        self.window.title("Résultats Choix outil coupant")

        # Calcul de l'ACP, on retourne les tableau contenant des informations sur les expériences les plus proches
        tab = self.controller_choix_outil_coupant.compute_pca(self.form_datas)  # time consumming

        # Mise à jour du label
        n_components_str = "Nombre de composantes : {}".format(self.controller_choix_outil_coupant.pca.n_components)
        self.page_resultats_choix_outil_coupant.n_components_str.set(n_components_str)

        # Affichage du tableau
        for element in tab:
            self.page_resultats_choix_outil_coupant.tableau.insert('', 'end', values=element)

        self.page_choix_outil_coupant.frame_choix_outil.forget()
        self.page_resultats_choix_outil_coupant.frame_resultats.pack(fill=BOTH, expand=YES)

    def determine_checked_attributes(self):
        """Méthode déterminant les variables cochées pendant la page choix outil coupant"""

        if self.page_choix_outil_coupant.bool_duree_vie_outil.get():
            self.form_datas[DUREE_VIE_OUTIL] = self.page_choix_outil_coupant.entry_duree_vie_outil.get()
        if self.page_choix_outil_coupant.combobox_type_materiau_piece.get():
            self.form_datas[TYPE_MAT_PIECE] = self.page_choix_outil_coupant.combobox_type_materiau_piece.get()
        if self.page_choix_outil_coupant.combobox_type_fab_piece.get():
            self.form_datas[TYPE_FAB_PIECE] = self.page_choix_outil_coupant.combobox_type_fab_piece.get()
        if self.page_choix_outil_coupant.bool_durete.get():
            self.form_datas[DURETE] = self.page_choix_outil_coupant.entry_durete.get()
        if self.page_choix_outil_coupant.bool_cr.get():
            self.form_datas[CONTRAINTES_RESIDUELLES] = self.page_choix_outil_coupant.entry_cr.get()
        if self.page_choix_outil_coupant.bool_rugosite.get():
            self.form_datas[RUGOSITE] = self.page_choix_outil_coupant.entry_rugosite.get()
        if self.page_choix_outil_coupant.bool_type_lub.get():
            self.form_datas[TYPE_LUBRIFIANT] = self.page_choix_outil_coupant.combobox_type_lub.get()
        if self.page_choix_outil_coupant.bool_vc.get():
            self.form_datas[VITESSE_COUPE] = self.page_choix_outil_coupant.entry_vc.get()
        if self.page_choix_outil_coupant.bool_fz.get():
            self.form_datas[VITESSE_AVANCE] = self.page_choix_outil_coupant.entry_fz.get()
        if self.page_choix_outil_coupant.bool_ap.get():
            self.form_datas[PROFONDEUR_PASSE] = self.page_choix_outil_coupant.entry_ap.get()
        if self.page_choix_outil_coupant.bool_effort_x.get():
            self.form_datas[EFFORT_COUPE_FX] = self.page_choix_outil_coupant.entry_effort_x.get()
        if self.page_choix_outil_coupant.bool_effort_y.get():
            self.form_datas[EFFORT_COUPE_FY] = self.page_choix_outil_coupant.entry_effort_y.get()
        if self.page_choix_outil_coupant.bool_effort_z.get():
            self.form_datas[EFFORT_COUPE_FZ] = self.page_choix_outil_coupant.entry_effort_z.get()
        if self.page_choix_outil_coupant.bool_tmp.get():
            self.form_datas[TEMPERATURE] = self.page_choix_outil_coupant.entry_tmp.get()

    def open_download_dialog(self):
        """fonction pour afficher la boite de dialogue de téléchargement de gabarit"""
        input_dialog = MessageBoxTelechargerGabarit(self.page_choix_conditions_coupe.frame_choix_cond)
        self.page_choix_conditions_coupe.frame_choix_cond.wait_window(input_dialog.top)

    def remove_experience(self):
        """fonction permettant de retirer la dernière expérience de la base de données"""
        self.delete = DeleteExperience()
        self.delete.delete_experience()
        session.commit()

    def back_from_page_choix_conditions_coupe_to_menu_view(self):
        """fonction permettant de passer de la page choix conditions coupe au menu"""
        self.window.title("Accueil")
        back_to_home(self.menu_view.frame_menu, self.page_choix_conditions_coupe.frame_choix_cond)
        self.page_choix_conditions_coupe.__init__(self.window, self.background_image)
        self.configure_action_buttons_page_choix_conditions_coupe()
        self.page_choix_conditions_coupe.frame_choix_cond.bind('<Configure>', self.resize_image_page_choix_conditions_coupe)
        self.menu_view.canvas_menu.create_image(0, 0, image=self.background_image, anchor="nw")

    def back_from_page_resultats_to_menu_view(self):
        """fonction permettant de passer de la page résultats au menu"""
        self.window.title("Accueil")
        back_to_home(self.menu_view.frame_menu, self.page_resultats.frame_resultats)
        self.page_resultats.__init__(self.window, self.background_image)
        self.configure_action_button_page_resultats()
        self.page_resultats.frame_resultats.bind('<Configure>', self.resize_image_page_resultats)
        self.menu_view.canvas_menu.create_image(0, 0, image=self.background_image, anchor="nw")

        self.page_choix_conditions_coupe.__init__(self.window, self.background_image)
        self.configure_action_buttons_page_choix_conditions_coupe()
        self.page_choix_conditions_coupe.frame_choix_cond.bind('<Configure>',
                                                               self.resize_image_page_choix_conditions_coupe)

    def back_from_page_resultats_to_page_conditions_coupe(self):
        """fonction permettant de passer de la page résultats à la page choix conditions coupe"""
        self.back_from_page_resultats_to_menu_view()
        self.display_page_conditions_coupe()

    def back_from_page_choix_outil_coupant_to_menu_view(self):
        """fonction permettant de passer de la page choix outil coupant au menu"""
        self.window.title("Accueil")
        back_to_home(self.menu_view.frame_menu, self.page_choix_outil_coupant.frame_choix_outil)
        self.page_choix_outil_coupant.__init__(self.window)
        self.configure_action_buttons_page_choix_outil_coupant()
        self.menu_view.canvas_menu.create_image(0, 0, image=self.background_image, anchor="nw")

    def back_from_resultats_page_choix_outil_coupant_to_menu_view(self):
        """fonction permettant de passer de la page resultat choix outil coupant au menu"""
        self.window.title("Accueil")
        back_to_home(self.menu_view.frame_menu, self.page_resultats_choix_outil_coupant.frame_resultats)
        self.page_resultats_choix_outil_coupant.__init__(self.window)

        # Reset de calcul de l'ACP
        self.controller_choix_outil_coupant = ChoixOutilCoupant()
        self.form_datas.clear()

        self.configure_action_buttons_page_resultats_choix_outil_coupant()
        self.menu_view.canvas_menu.create_image(0, 0, image=self.background_image, anchor="nw")

    def back_from_resultats_page_choix_outil_coupant_to_page_choix_outil_coupant(self):
        """fonction permettant de passer de la page resultat choix outil coupant à un nouveau choix de l'outil coupant"""

        self.back_from_resultats_page_choix_outil_coupant_to_menu_view()
        self.display_page_choix_outil_coupant()

    def export_image(self):
        """fonction permettant d'exporter le graphique résultat en image"""
        # cas 2D
        if str(self.page_choix_conditions_coupe.type_graphique.get()) == GRAPH2D:
            self.graphic.fig.savefig(os.path.join(str(os.path.join(Path.home(), "Downloads")), str(
                self.page_choix_conditions_coupe.type_graphique.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_abscisse.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_ordonnee.get()) + ".png"))
            showinfo(title=None, message=str(self.page_choix_conditions_coupe.type_graphique.get()) + " " + str(
                self.page_choix_conditions_coupe.var_abscisse.get()) + " " + str(
                self.page_choix_conditions_coupe.var_ordonnee.get()) + " téléchargé")
        # cas 3D
        else:
            self.graphic.fig.savefig(os.path.join(str(os.path.join(Path.home(), "Downloads")), str(
                self.page_choix_conditions_coupe.type_graphique.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_abscisse.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_ordonnee.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_cote.get()) + ".png"))
            showinfo(title=None, message=str(self.page_choix_conditions_coupe.type_graphique.get()) + " " + str(
                self.page_choix_conditions_coupe.var_abscisse.get()) + " " + str(
                self.page_choix_conditions_coupe.var_ordonnee.get()) + " " + str(
                self.page_choix_conditions_coupe.var_cote.get()) + " téléchargé")

    def export_pdf(self):
        """fonction permettant d'exporter le graphique résultat en pdf"""
        # cas 2D
        if str(self.page_choix_conditions_coupe.type_graphique.get()) == GRAPH2D:
            self.graphic.fig.savefig(os.path.join(str(os.path.join(Path.home(), "Downloads")), str(
                self.page_choix_conditions_coupe.type_graphique.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_abscisse.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_ordonnee.get()) + ".pdf"))
            showinfo(title=None, message=str(self.page_choix_conditions_coupe.type_graphique.get()) + " " + str(
                self.page_choix_conditions_coupe.var_abscisse.get()) + " " + str(
                self.page_choix_conditions_coupe.var_ordonnee.get()) + " téléchargé")
        # cas 3D
        else:
            self.graphic.fig.savefig(os.path.join(str(os.path.join(Path.home(), "Downloads")), str(
                self.page_choix_conditions_coupe.type_graphique.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_abscisse.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_ordonnee.get()) + "_" + str(
                self.page_choix_conditions_coupe.var_cote.get()) + ".pdf"))
            showinfo(title=None, message=str(self.page_choix_conditions_coupe.type_graphique.get()) + " " + str(
                self.page_choix_conditions_coupe.var_abscisse.get()) + " " + str(
                self.page_choix_conditions_coupe.var_ordonnee.get()) + " " + str(
                self.page_choix_conditions_coupe.var_cote.get()) + " téléchargé")

    def configure_action_buttons_page_choix_conditions_coupe(self):
        """fonction qui configure les actions des boutons de la page choix conditions coupe"""
        self.page_choix_conditions_coupe.butt_telechargement.config(command=self.open_download_dialog)
        self.page_choix_conditions_coupe.butt_selectionner_fichier.config(
            command=lambda: self.import_file(True))
        self.page_choix_conditions_coupe.butt_accueil.config(
            command=self.back_from_page_choix_conditions_coupe_to_menu_view)
        self.page_choix_conditions_coupe.butt_valider.config(command=self.display_page_resultats)
        self.page_choix_conditions_coupe.button_aide.config(command=self.display_aide)

    def configure_action_button_page_resultats(self):
        """fonction qui configure les actions des boutons de la page résultats"""
        self.page_resultats.butt_accueil.config(command=self.back_from_page_resultats_to_menu_view)
        self.page_resultats.butt_supprimer_experience.config(command=self.remove_experience)
        self.page_resultats.butt_choix_conditions_coupe.config(
            command=self.back_from_page_resultats_to_page_conditions_coupe)
        self.page_resultats.butt_export_image.config(command=self.export_image)
        self.page_resultats.butt_export_pdf.config(command=self.export_pdf)

    def configure_action_buttons_page_choix_outil_coupant(self):
        """fonction qui configure les actions des boutons de la page choix outil coupant"""
        # Boutons
        self.page_choix_outil_coupant.button_accueil.config(command=self.back_from_page_choix_outil_coupant_to_menu_view)
        self.page_choix_outil_coupant.button_valider.config(command=self.validate_page_resultats_choix_outil_coupant_form)

    def configure_action_buttons_page_resultats_choix_outil_coupant(self):
        """fonction qui configure les actions des boutons de la page résultats choix outil coupant"""
        # Boutons
        self.page_resultats_choix_outil_coupant.butt_acp_2d.config(command=self.controller_choix_outil_coupant.create_and_display_fig_2d)
        self.page_resultats_choix_outil_coupant.butt_acp_3d.config(command=self.controller_choix_outil_coupant.create_and_display_fig_3d)
        self.page_resultats_choix_outil_coupant.butt_acp_params.config(command= lambda:
                                                        self.controller_choix_outil_coupant.create_and_display_fig_2d(with_variable=True))
        self.page_resultats_choix_outil_coupant.butt_accueil.config(command=self.back_from_resultats_page_choix_outil_coupant_to_menu_view)
        self.page_resultats_choix_outil_coupant.butt_retour.config(command=self.back_from_resultats_page_choix_outil_coupant_to_page_choix_outil_coupant)

    def import_file(self, check):
        """fonction qui importe les données d'un fichier excel et qui affiche les éléments graphiques correspondant

        Parameters
        ----------
        check : Boolean
            booléen qui permet de savoir s'il faut afficher les widgets après l'importation d'un fichier excel
        """
        self.import_data_object.import_data()

        # gestion affichage des checkbox
        # s'il n'y a pas d'erreurs
        if self.import_data_object.errors == "" and check and self.import_data_object.rep_file is not None:
            # affichage checkbox
            self.initialize_checkbox()

            # contraintes résiduelles
            if self.import_data_object.type_file == CONTRAINTES_RESIDUELLES:
                self.display_experience_checkbox([True, False, False, False, False, False, False, False])

            # durée de vie outil
            elif self.import_data_object.type_file == DUREE_VIE_OUTIL:
                self.display_experience_checkbox([False, True, False, False, False, False, False, False])

            # dureté
            elif self.import_data_object.type_file == DURETE:
                self.display_experience_checkbox([False, False, True, False, False, False, False, False])

            # effort de coupe
            elif self.import_data_object.type_file == EFFORT_COUPE:
                self.display_experience_checkbox([False, False, False, True, True, True, False, False])

            # rugosité
            elif self.import_data_object.type_file == RUGOSITE:
                self.display_experience_checkbox([False, False, False, False, False, False, True, False])

            # température
            elif self.import_data_object.type_file == TEMPERATURE:
                self.display_experience_checkbox([False, False, False, False, False, False, False, True])

            # complet
            elif self.import_data_object.type_file == COMPLET:
                self.display_experience_checkbox([True, True, True, True, True, True, True, True])

            if self.import_data_object.type_file == COMPLET:
                # affichage des radiobuttons sur 2 lignes pour le gabarit complet
                for i in range(len(self.page_choix_conditions_coupe.list_texts)):
                    self.page_choix_conditions_coupe.list_cb_ab[i].config(height=2,
                                                                          text=self.page_choix_conditions_coupe.list_texts[
                                                                              i].replace(" ", "\n", 1))
                    self.page_choix_conditions_coupe.list_cb_or[i].config(height=2,
                                                                          text=self.page_choix_conditions_coupe.list_texts[
                                                                              i].replace(" ", "\n", 1))
                    self.page_choix_conditions_coupe.list_cb_co[i].config(height=2,
                                                                          text=self.page_choix_conditions_coupe.list_texts[
                                                                              i].replace(" ", "\n", 1))
            else:
                # affichage des radiobuttons sur 1 ligne pour les autres gabarits
                for i in range(len(self.page_choix_conditions_coupe.list_texts)):
                    self.page_choix_conditions_coupe.list_cb_ab[i].config(height=1,
                                                                          text=
                                                                          self.page_choix_conditions_coupe.list_texts[
                                                                              i].replace("\n", " ", 1))
                    self.page_choix_conditions_coupe.list_cb_or[i].config(height=1,
                                                                          text=
                                                                          self.page_choix_conditions_coupe.list_texts[
                                                                              i].replace("\n", " ", 1))
                    self.page_choix_conditions_coupe.list_cb_co[i].config(height=1,
                                                                          text=
                                                                          self.page_choix_conditions_coupe.list_texts[
                                                                              i].replace("\n", " ", 1))

    def initialize_checkbox(self):
        """fonction qui initialise les checkbox communes à toutes les expériences"""
        for i in range(7):
            self.page_choix_conditions_coupe.list_cb_ab[i].pack(side=LEFT)
            self.page_choix_conditions_coupe.list_cb_or[i].pack(side=LEFT)
            if str(self.page_choix_conditions_coupe.type_graphique.get()) == GRAPH3D:
                self.page_choix_conditions_coupe.list_cb_co[i].pack(side=LEFT)
            else:
                self.page_choix_conditions_coupe.list_cb_co[i].pack_forget()
        if self.page_choix_conditions_coupe.butt_valider is not None:
            self.page_choix_conditions_coupe.butt_valider.pack(side=RIGHT, padx=50)

        self.page_choix_conditions_coupe.label_selectionner_abscisse.pack()
        self.page_choix_conditions_coupe.label_selectionner_ordonnee.pack()
        # cas graph 3D
        if str(self.page_choix_conditions_coupe.type_graphique.get()) == GRAPH3D:
            self.page_choix_conditions_coupe.label_selectionner_cote.pack()
            self.page_choix_conditions_coupe.label_abscisse.pack(side=LEFT)
            self.page_choix_conditions_coupe.entry_abscisse.pack(side=RIGHT)
            self.page_choix_conditions_coupe.label_ordonnee.pack(side=LEFT)
            self.page_choix_conditions_coupe.entry_ordonnee.pack(side=RIGHT)
            self.page_choix_conditions_coupe.label_cote.pack(side=LEFT)
            self.page_choix_conditions_coupe.entry_cote.pack(side=RIGHT)
            self.page_choix_conditions_coupe.frame_text_cote.pack()
            self.page_choix_conditions_coupe.button_points.pack_forget()
            self.page_choix_conditions_coupe.button_courbe.pack_forget()
        # cas graph 2D
        else:
            self.page_choix_conditions_coupe.label_selectionner_cote.pack_forget()
            self.page_choix_conditions_coupe.label_abscisse.pack(side=LEFT)
            self.page_choix_conditions_coupe.entry_abscisse.pack(side=RIGHT)
            self.page_choix_conditions_coupe.label_ordonnee.pack(side=LEFT)
            self.page_choix_conditions_coupe.entry_ordonnee.pack(side=RIGHT)
            self.page_choix_conditions_coupe.label_cote.pack_forget()
            self.page_choix_conditions_coupe.entry_cote.pack_forget()
            self.page_choix_conditions_coupe.frame_text_cote.pack_forget()
            self.page_choix_conditions_coupe.button_points.pack(side=LEFT)
            self.page_choix_conditions_coupe.button_courbe.pack(side=LEFT)

        self.page_choix_conditions_coupe.button_aide.pack()

    def display_experience_checkbox(self, list_bool):
        """fonction qui affiche la checkbox correspondant au type d'experience

        Parameters
        ----------
        list_bool : list
            La liste de booléens pour savoir quel widget afficher en fonction du type d'expérience importée
        """
        for i in range(len(list_bool)):
            if list_bool[i]:
                self.page_choix_conditions_coupe.list_cb_ab[i + 7].pack(side=LEFT)
                self.page_choix_conditions_coupe.list_cb_or[i + 7].pack(side=LEFT)
                if str(self.page_choix_conditions_coupe.type_graphique.get()) == GRAPH3D:
                    self.page_choix_conditions_coupe.list_cb_co[i + 7].pack(side=LEFT)
                else:
                    self.page_choix_conditions_coupe.list_cb_co[i + 7].pack_forget()
            else:
                self.page_choix_conditions_coupe.list_cb_ab[i + 7].pack_forget()
                self.page_choix_conditions_coupe.list_cb_or[i + 7].pack_forget()
                if str(self.page_choix_conditions_coupe.type_graphique.get()) == GRAPH2D:
                    self.page_choix_conditions_coupe.list_cb_co[i + 7].pack_forget()
