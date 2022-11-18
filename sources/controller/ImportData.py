import csv
import os
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showerror, showinfo, askyesno
import pandas as pd
from sqlalchemy import event, text

from sources.model import session, mydb, engine
from sources.controller.ConditionsCoupeController import ConditionsCoupeController
from sources.controller.EffortCoupeController import EffortCoupeController
from sources.controller.ExperienceController import ExperienceController
from sources.controller.ExportData import ExportData
from sources.controller.OutilController import OutilController
from sources.controller.PieceController import PieceController
from sources.controller.RugositeController import RugositeController
from sources.controller.TemperatureController import TemperatureController
from sources.Constants import DURETE, CONTRAINTES_RESIDUELLES, DUREE_VIE_OUTIL, EFFORT_COUPE, RUGOSITE, TEMPERATURE, \
    COMPLET, TEMPS_U, VITESSE_AVANCE_U, PROFONDEUR_PASSE_U, GEOMETRIE_OUTIL, \
    TYPE_LUBRIFIANT, VITESSE_COUPE_U, TYPE_MAT_PIECE, TYPE_FAB_PIECE, VITESSE_COUPE, VITESSE_AVANCE, PROFONDEUR_PASSE, CONTRAINTES_RESIDUELLES_U, \
    DURETE_U, EFFORT_COUPE_FX_U, EFFORT_COUPE_FY_U, EFFORT_COUPE_FZ_U, RUGOSITE_U, TEMPERATURE_U
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model.EffortCoupe import EffortCoupe
from sources.model.Outil import Outil
from sources.model.Piece import Piece
from sources.model.Temperature import Temperature
from sources.model.Rugosite import Rugosite

class ImportData:
    """Classe qui permet d'importer les données d'une expérience d'usinage dans la base de données"""

    def __init__(self):
        """Constructeur"""

        self.rep_file = None
        self.exp_controller = ExperienceController()
        self.ou_controller = OutilController()
        self.con_coupe_controller = ConditionsCoupeController()
        self.eff_coupe_controller = EffortCoupeController()
        self.pie_controller = PieceController()
        self.ru_controller = RugositeController()
        self.temp_controller = TemperatureController()

        self.chemin = ""

        # nom des colonnes des fichiers excels par défaut
        self.column_names = [TEMPS_U]

        # nom des lignes fixes des fichiers excels par défaut
        self.fixe_line_names = [VITESSE_COUPE_U, VITESSE_AVANCE_U, PROFONDEUR_PASSE_U, GEOMETRIE_OUTIL, TYPE_LUBRIFIANT, TYPE_FAB_PIECE, TYPE_MAT_PIECE]

        # en tête des colonnes
        self.column_headers = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

        self.errors = ""
        self.type_file = ""

        self.bad_columns = list()
        self.columns_not_provided = list()

        self.numerical_values = list()
        self.required_fields = list()

        self.vc = None
        self.fz = None
        self.ap = None
        self.geometrie_outil = None
        self.type_lubrifiant = None
        self.type_fabrication_piece = None
        self.materiau_piece = None

        # éléments dans la colonne dureté
        self.list_durete = []
        # éléments dans la colonne contraintes résiduelles
        self.list_contraintes_residuelles = []
        # éléments dans la colonne durée de vie outil
        self.list_duree_vie_outil = []
        # éléments dans les colonnes effort de coupe
        self.list_effort_coupe = []
        # éléments de la colonne temps
        self.list_temps = []
        # éléments de la colonne rugosité
        self.list_rugosite = []
        # éléments de la colonne température
        self.list_temperature = []

        self.set_vc = set()
        self.set_fz = set()
        self.set_ap = set()
        self.set_geometrie_outil = set()
        self.set_type_lubrifiant = set()
        self.set_type_fabrication_piece = set()
        self.set_materiau_piece = set()
        self.set_durete = set()
        self.set_contraintes_residuelles = set()
        self.set_duree_vie_outil = set()

        self.number_lines = -1

    def error_column(self):
        """fonction qui vérifie s'il y a des erreurs de colonnes parmi les colonnes prévues"""
        if len(self.bad_columns) > 0:
            self.errors = self.errors + "Mauvaises colonnes : "
            for i in range(len(self.bad_columns)):
                self.errors = self.errors + "L'en-tête de la colonne " + self.bad_columns[i][2] + " est " + \
                              self.bad_columns[i][
                                  0] + " alors qu'il devrait être " + self.bad_columns[i][1] + "\n"
            self.errors = self.errors + "\n" + "\n"

    def extra_column(self):
        """fonction qui vérifie s'il y des colonnes non prévues (en trop)"""
        if len(self.columns_not_provided) > 0:
            self.errors = self.errors + "Colonnes non prévues : "
            for i in self.columns_not_provided:
                self.errors = self.errors + str(i) + ", "
            self.errors = self.errors[0:-2] + "\n" + "\n"

    def expected_numerical_value(self):
        """fonction qui vérifie si une valeur numérique est présente là où elle est attendue"""
        if len(self.numerical_values) > 0:
            self.errors = self.errors + "Valeurs numériques attendues : "
            for i in self.numerical_values:
                error = "\n" + "Ligne : "
                for j in i:
                    error = error + str(j) + ", colonne : "
                self.errors = self.errors + error[0:-12] + " "
            self.errors = self.errors + "\n" + "\n"

    def missing_value(self):
        """fonction qui vérifie s'il y a un champ manquant (pour les colonnes qui ne doivent avoir aucune case de vide)"""
        if len(self.required_fields) > 0:
            self.errors = self.errors + "Champs obligatoires "
            for i in self.required_fields:
                error = "\n" + "Ligne "
                for j in i:
                    error = error + str(j) + ", colonne : "
                self.errors = self.errors + error[0:-12] + " "
            self.errors = self.errors + "\n" + "\n"

    def empty_column(self):
        """fonction qui vérifie si une colonne est vide ou si elle contient au moins 2 valeurs différentes"""
        # si la colonne vc est vide
        if self.vc is None:
            self.errors = self.errors + "La colonne " + VITESSE_COUPE + " est vide " + "\n"

        # si la colonne fz est vide
        if self.fz is None:
            self.errors = self.errors + "La colonne " + VITESSE_AVANCE + " est vide " + "\n"

        # si la colonne ap est vide
        if self.ap is None:
            self.errors = self.errors + "La colonne " + PROFONDEUR_PASSE + " est vide " + "\n"

        # si la colonne géométrie outil est vide
        if self.geometrie_outil is None:
            self.errors = self.errors + "La colonne " + GEOMETRIE_OUTIL + " est vide " + "\n"

        # si la colonne type lubrifiant est vide
        if self.type_lubrifiant is None:
            self.errors = self.errors + "La colonne " + TYPE_LUBRIFIANT + " est vide " + "\n"

        # si la colonne type fabrication pièce est vide
        if self.type_fabrication_piece is None:
            self.errors = self.errors + "La colonne " + TYPE_FAB_PIECE + " est vide " + "\n"

        # si la colonne matériau pièce est vide
        if self.materiau_piece is None:
            self.errors = self.errors + "La colonne " + TYPE_MAT_PIECE + " est vide " + "\n"

        if self.type_file == DURETE or self.type_file == COMPLET:
            # si la colonne dureté est vide
            if len(self.set_durete) == 0:
                self.errors = self.errors + "La colonne " + DURETE + " est vide " + "\n"
            elif len(self.set_durete) > 1 and len(self.list_durete) != self.number_lines:
                self.errors = self.errors + "La colonne " + DURETE + " a des cases vides " + "\n"

        if self.type_file == CONTRAINTES_RESIDUELLES or self.type_file == COMPLET:
            # si la colonne contraintes résiduelles est vide
            if len(self.set_contraintes_residuelles) == 0:
                self.errors = self.errors + "La colonne " + CONTRAINTES_RESIDUELLES + " est vide " + "\n"
            elif len(self.set_contraintes_residuelles) > 1 and len(
                    self.list_contraintes_residuelles) != self.number_lines:
                self.errors = self.errors + "La colonne " + CONTRAINTES_RESIDUELLES + " a des cases vides " + "\n "

        if self.type_file == DUREE_VIE_OUTIL or self.type_file == COMPLET:
            # si la colonne durée de vie outil est vide
            if len(self.set_duree_vie_outil) == 0:
                self.errors = self.errors + "La colonne " + DUREE_VIE_OUTIL + " est vide " + "\n"
            elif len(self.set_duree_vie_outil) > 1 and len(self.list_duree_vie_outil) != self.number_lines:
                self.errors = self.errors + "La colonne " + DUREE_VIE_OUTIL + " a des cases vides " + "\n"

    def check_experience_type(self, row):
        """fonction qui vérifie quel est le type de l'expérience

        Parameters
        ----------
        row : list
            La liste des en têtes de colonne
        """
        # cas gabarit total (contient tous les éléments)
        if CONTRAINTES_RESIDUELLES_U in row and DUREE_VIE_OUTIL in row and DURETE_U in row and EFFORT_COUPE_FX_U in row and EFFORT_COUPE_FY_U in row and EFFORT_COUPE_FZ_U in row and RUGOSITE_U in row and TEMPERATURE_U in row:
            self.type_file = COMPLET
            self.column_names = [TEMPS_U, EFFORT_COUPE_FX_U, EFFORT_COUPE_FY_U, EFFORT_COUPE_FZ_U,
                                 CONTRAINTES_RESIDUELLES_U, DUREE_VIE_OUTIL, DURETE_U, RUGOSITE_U, TEMPERATURE_U]
            return

        # autres cas
        for colonne in range(len(row)):
            if row[colonne] == CONTRAINTES_RESIDUELLES_U:
                self.type_file = CONTRAINTES_RESIDUELLES
                self.column_names.append(CONTRAINTES_RESIDUELLES_U)
                break
            elif row[colonne] == DUREE_VIE_OUTIL:
                self.type_file = DUREE_VIE_OUTIL
                self.column_names.append(DUREE_VIE_OUTIL)
                break
            elif row[colonne] == DURETE:
                self.type_file = DURETE
                self.column_names.append(DURETE)
                break
            elif row[colonne] == EFFORT_COUPE_FX_U or row[colonne] == EFFORT_COUPE_FY_U \
                    or row[colonne] == EFFORT_COUPE_FZ_U:
                self.type_file = EFFORT_COUPE
                self.column_names.append(EFFORT_COUPE_FX_U)
                self.column_names.append(EFFORT_COUPE_FY_U)
                self.column_names.append(EFFORT_COUPE_FZ_U)
                break
            elif row[colonne] == RUGOSITE_U:
                self.type_file = RUGOSITE
                self.column_names.append(RUGOSITE_U)
                break
            elif row[colonne] == TEMPERATURE_U:
                self.type_file = TEMPERATURE
                self.column_names.append(TEMPERATURE_U)
                break

    def check_numerical_value(self, row, i):
        """fonction qui vérifie que les colonnes avec des chiffres contiennent bien des chiffres

        Parameters
        ----------
        row : list
            La liste des valeurs d'une ligne du fichier excel
        i : int
            Le numéro de ligne analysée du fichier excel

        """
        if row[0] != "":
            try:
                float(row[0])
            except ValueError:
                self.numerical_values.append([i + 1, self.column_names[0]])

        if self.type_file == EFFORT_COUPE:
            if row[1] != "":
                try:
                    float(row[1])
                except ValueError:
                    self.numerical_values.append([i + 1, self.column_names[1]])

            if row[2] != "":
                try:
                    float(row[2])
                except ValueError:
                    self.numerical_values.append([i + 1, self.column_names[2]])
            if row[3] != "":
                try:
                    float(row[3])
                except ValueError:
                    self.numerical_values.append([i + 1, self.column_names[3]])

        # cas gabarit complet
        if self.type_file == COMPLET:
            for colonne in range(2, 9):
                if row[colonne] != "":
                    try:
                        float(row[colonne])
                    except ValueError:
                        self.numerical_values.append([i + 1, self.column_names[colonne]])

    def clean_data(self):
        """fonction qui ajoute les données manquantes pour les listes concernées"""

        if self.type_file == DURETE or self.type_file == COMPLET:
            if len(self.set_durete) == 1:
                new_list = list(self.set_durete)
                self.list_durete = []
                for i in range(self.number_lines):
                    self.list_durete.append(new_list[0])

        if self.type_file == CONTRAINTES_RESIDUELLES or self.type_file == COMPLET:
            if len(self.set_contraintes_residuelles) == 1:
                new_list = list(self.set_contraintes_residuelles)
                self.list_contraintes_residuelles = []
                for i in range(self.number_lines):
                    self.list_contraintes_residuelles.append(new_list[0])

        if self.type_file == DUREE_VIE_OUTIL or self.type_file == COMPLET:
            if len(self.set_duree_vie_outil) == 1:
                new_list = list(self.set_duree_vie_outil)
                self.list_duree_vie_outil = []
                for i in range(self.number_lines):
                    self.list_duree_vie_outil.append(new_list[0])

    def persist_data(self):
        """fonction qui ajoute les objets créés dans la base de données"""
        self.exp_controller.create_experience(os.path.basename(self.chemin)[0:-5])

        mycursor = mydb.cursor()
        id_exp = None
        mycursor.execute("""select * from experience order by id desc limit 1""")
        experience = mycursor.fetchall()
        for x in experience:
            id_exp = x[0]

        if self.type_file == DUREE_VIE_OUTIL or self.type_file == COMPLET:
            data = pd.DataFrame({
                'nom': ['o1' for i in range(len(self.list_temps))],
                'materiau': ['' for i in range(len(self.list_temps))],
                'geometrie': [self.geometrie_outil for i in range(len(self.list_temps))],
                'duree_de_vie': self.list_duree_vie_outil,
                'temps': self.list_temps,
                'id_experience': [id_exp for i in range(len(self.list_temps))]
            })

        else:
            data = pd.DataFrame({
                'nom': ['o1' for i in range(len(self.list_temps))],
                'materiau': ['' for i in range(len(self.list_temps))],
                'geometrie': [self.geometrie_outil for i in range(len(self.list_temps))],
                'duree_de_vie': [None for i in range(len(self.list_temps))],
                'temps': self.list_temps,
                'id_experience': [id_exp for i in range(len(self.list_temps))]
            })

        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True

        data.to_sql('outil', engine, index=False, if_exists="append")

        if self.type_file == CONTRAINTES_RESIDUELLES:
            data = pd.DataFrame({
                'materiau': [self.materiau_piece for i in range(len(self.list_temps))],
                'type_fabrication': [self.type_fabrication_piece for i in range(len(self.list_temps))],
                'fatigue': [0 for i in range(len(self.list_temps))],
                'durete': [None for i in range(len(self.list_temps))],
                'contraintes_residuelles': self.list_contraintes_residuelles,
                'temps': self.list_temps,
                'id_experience': [id_exp for i in range(len(self.list_temps))]
            })

        elif self.type_file == DURETE:
            data = pd.DataFrame({
                'materiau': [self.materiau_piece for i in range(len(self.list_temps))],
                'type_fabrication': [self.type_fabrication_piece for i in range(len(self.list_temps))],
                'fatigue': [0 for i in range(len(self.list_temps))],
                'durete': self.list_durete,
                'contraintes_residuelles': [None for i in range(len(self.list_temps))],
                'temps': self.list_temps,
                'id_experience': [id_exp for i in range(len(self.list_temps))]
            })

        elif self.type_file == COMPLET:
            data = pd.DataFrame({
                'materiau': [self.materiau_piece for i in range(len(self.list_temps))],
                'type_fabrication': [self.type_fabrication_piece for i in range(len(self.list_temps))],
                'fatigue': [0 for i in range(len(self.list_temps))],
                'durete': self.list_durete,
                'contraintes_residuelles': self.list_contraintes_residuelles,
                'temps': self.list_temps,
                'id_experience': [id_exp for i in range(len(self.list_temps))]
            })

        else:
            data = pd.DataFrame({
                'materiau': [self.materiau_piece for i in range(len(self.list_temps))],
                'type_fabrication': [self.type_fabrication_piece for i in range(len(self.list_temps))],
                'fatigue': [0 for i in range(len(self.list_temps))],
                'durete': [None for i in range(len(self.list_temps))],
                'contraintes_residuelles': [None for i in range(len(self.list_temps))],
                'temps': self.list_temps,
                'id_experience': [id_exp for i in range(len(self.list_temps))]
            })

        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True

        data.to_sql('piece', engine, index=False, if_exists="append")

        if self.type_file == RUGOSITE or self.type_file == COMPLET:
            id_piece = None

            piece = engine.execute(text("select * from piece order by id desc limit 1"))
            for row in piece:
                id_piece = row['id']

            id_piece = id_piece - len(self.list_temps) + 1

            data = pd.DataFrame({
                'valeur': self.list_rugosite,
                'id_piece': [i for i in range(id_piece, id_piece + len(self.list_temps))]
            })

            @event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                if executemany:
                    cursor.fast_executemany = True

            data.to_sql('rugosite', engine, index=False, if_exists="append")

        data = pd.DataFrame({
            'type_lubrifiant':[self.type_lubrifiant for i in range(len(self.list_temps))],
            'vitesse_coupe': [self.vc for i in range(len(self.list_temps))],
            'vitesse_avance': [self.fz for i in range(len(self.list_temps))],
            'profondeur_passe': [self.ap for i in range(len(self.list_temps))],
            'temps': self.list_temps,
            'id_experience': [id_exp for i in range(len(self.list_temps))]
        })

        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True

        data.to_sql('conditionscoupe', engine, index=False, if_exists="append")

        id_cond = None

        cond = engine.execute(text("select * from conditionscoupe order by id desc limit 1"))
        for row in cond:
            id_cond = row['id']

        id_cond = id_cond - len(self.list_temps) + 1

        if self.type_file == EFFORT_COUPE or self.type_file == COMPLET:
            data = pd.DataFrame({
                'fx': [self.list_effort_coupe[i][0] for i in range(len(self.list_temps))],
                'fy': [self.list_effort_coupe[i][1] for i in range(len(self.list_temps))],
                'fz': [self.list_effort_coupe[i][2] for i in range(len(self.list_temps))],
                'id_conditions_coupe': [i for i in range(id_cond, id_cond + len(self.list_temps))]
            })

            @event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                if executemany:
                    cursor.fast_executemany = True

            data.to_sql('effortcoupe', engine, index=False, if_exists="append")

        if self.type_file == TEMPERATURE or self.type_file == COMPLET:
            data = pd.DataFrame({
                'valeur': self.list_temperature,
                'id_conditions_coupe': [i for i in range(id_cond, id_cond + len(self.list_temps))]
            })

            @event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                if executemany:
                    cursor.fast_executemany = True

            data.to_sql('temperature', engine, index=False, if_exists="append")

        mydb.commit()

    def check_header(self, row):
        """fonction qui vérifie analyse l'en tête des colonnes

        Parameters
        ----------
        row : list
            La liste des valeurs d'une ligne du fichier excel

        """
        # vérification type d'expérience
        self.check_experience_type(row)

        # cas ou le fichier ne correspond à aucun type d'expérience
        if self.type_file == "":
            showerror(title="Erreur", message="Le fichier ne correspond à aucun type d'expérience")

        # première ligne du fichier
        # vérification en tete colonnes
        for j in range(len(self.column_names)):
            if row[j] != "" and self.column_names[j] != row[j]:
                self.bad_columns.append([row[j], self.column_names[j], self.column_headers[j]])
            elif row[j] == "":
                self.bad_columns.append(["", self.column_names[j], self.column_headers[j]])

        for l in range(len(row)):
            if not row[l] in self.column_names and row[l] != "" and l > len(self.column_names) - 1:
                self.columns_not_provided.append(row[l])

    def check_lines(self, row, i):
        """fonction qui analyse les lignes du fichier excel (autres que l'en-tête)

        Parameters
        ----------
        row : list
            La liste des valeurs d'une ligne du fichier excel
        i : int
            Le numéro de ligne analysée du fichier excel

        """
        # vérifier que les colonnes avec des chiffres contiennent bien des chiffres
        self.check_numerical_value(row, i)

        # vérifier si les champs requis sont présents
        if row[0] == "":
            self.required_fields.append([i + 1, self.column_names[0]])
        else:
            self.list_temps.append(row[0])

        if self.type_file == DURETE:
            if row[1] != "":
                self.list_durete.append(row[1])
        elif self.type_file == CONTRAINTES_RESIDUELLES:
            if row[1] != "":
                self.list_contraintes_residuelles.append(row[1])
        elif self.type_file == DUREE_VIE_OUTIL:
            if row[1] != "":
                self.list_duree_vie_outil.append(row[1])
        elif self.type_file == EFFORT_COUPE:
            if row[1] == "":
                self.required_fields.append([i + 1, self.column_names[1]])
            if row[2] == "":
                self.required_fields.append([i + 1, self.column_names[2]])
            if row[3] == "":
                self.required_fields.append([i + 1, self.column_names[3]])
            if row[1] != "" and row[2] != "" and row[3] != "":
                self.list_effort_coupe.append([row[1], row[2], row[3]])
        elif self.type_file == COMPLET:
            if row[1] == "":
                self.required_fields.append([i + 1, self.column_names[1]])
            if row[2] == "":
                self.required_fields.append([i + 1, self.column_names[2]])
            if row[3] == "":
                self.required_fields.append([i + 1, self.column_names[3]])
            if row[1] != "" and row[2] != "" and row[3] != "":
                self.list_effort_coupe.append([row[1], row[2], row[3]])
            if row[4] != "":
                self.list_contraintes_residuelles.append(row[4])
            if row[5] != "":
                self.list_duree_vie_outil.append(row[5])
            if row[6] != "":
                self.list_durete.append(row[6])
            if row[7] == "":
                self.required_fields.append([i + 1, self.column_names[7]])
            else:
                self.list_rugosite.append(row[7])
            if row[8] == "":
                self.required_fields.append([i + 1, self.column_names[8]])
            else:
                self.list_temperature.append(row[8])
        else:
            if row[1] == "":
                self.required_fields.append([i + 1, self.column_names[1]])
            else:
                if self.type_file == RUGOSITE:
                    self.list_rugosite.append(row[1])
                elif self.type_file == TEMPERATURE:
                    self.list_temperature.append(row[1])

    def manage_errors(self):
        """fonction qui affiche les erreurs contenues dans le fichier excel"""
        # s'il y a des erreurs
        if self.errors != "":
            if self.type_file != "":
                if askyesno(title="Erreur",
                            message=self.errors + "\n" + "\n" + "Voulez-vous télécharger le "
                                                                "gabarit de "
                                                                "l'expérience " + self.type_file + " ? "):
                    export = ExportData(self.type_file)
                    export.export_data(False)
            else:
                showerror(title="Erreur", message=self.errors)

        else:
            # ajuster les données
            self.clean_data()

            # enregistrer les données dans la base de données
            self.persist_data()

            showinfo(title="", message="Importation réussie")

    def add_general_data(self, row, i):
        """
        fonction qui ajoute les éléments fixes (non dépendants du temps) aux attributs de l'expérience
        row: colonne du csv
        i: indice de la ligne
        """

        if i == 0:
            # Vitesse de coupe
            try:
                float(row[1])
            except ValueError:
                self.numerical_values.append([i + 1, self.fixe_line_names[i]])
            self.vc = row[1]
        elif i == 1:
            # Vitesse d'avance
            try:
                float(row[1])
            except ValueError:
                self.numerical_values.append([i + 1, self.fixe_line_names[i]])
            self.fz = row[1]
        elif i == 2:
            # Profondeur de passe
            try:
                float(row[1])
            except ValueError:
                self.numerical_values.append([i + 1, self.fixe_line_names[i]])
            self.ap = row[1]
        elif i == 3:
            # Géometrie Outil
            self.geometrie_outil = str(row[1])
        elif i == 4:
            # type_lubrifiant
            self.type_lubrifiant = str(row[1])
        elif i == 5:
            # type fabrication piece
            self.type_fabrication_piece = str(row[1])
        elif i == 6:
            # materiau_piece
            self.materiau_piece = str(row[1])
        else:
            raise Exception("Erreur " + str(i) + " n'est pas un nombre interpretable")

    def import_data(self):
        """fonction qui importe les données d'un fichier excel dans la base de données"""
        self.__init__()
        # ouverture de la boite de dialogue pour selection du fichier rep_file
        self.rep_file = askopenfile(mode="r", filetypes=[("Fichiers excel", ".xlsx")], defaultextension=".xlsx",
                                    title="Lire un fichier excel")
        if self.rep_file is None:  # si appuie sur annuler
            pass
        else:
            # recuperation du nom de fichier complet
            self.chemin = os.path.abspath(self.rep_file.name)

            # convertir fichier excel en csv (le fichier excel doit contenir une seule feuille)
            xlsx_file = pd.read_excel(self.chemin, index_col=None)
            xlsx_file.to_csv(self.chemin.replace("xlsx", "csv"), encoding='utf-8', index=False)

            # lire le fichier csv
            with open(self.chemin.replace("xlsx", "csv"), newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                i = 0
                for row in csv_reader:
                    if i < 7:
                        # Ajouts des attributs fixes
                        self.add_general_data(row, i)
                    if i == 8:
                        # vérifier du header
                        self.number_lines = self.number_lines + 1
                        self.check_header(row)

                    elif i > 8 and len(self.bad_columns) == 0 and len(self.columns_not_provided) == 0:
                        # vérification des autres lignes
                        self.number_lines = self.number_lines + 1
                        self.check_lines(row, i)

                    i = i + 1

            # erreurs de colonnes parmi les colonnes prévues
            self.error_column()

            # colonne pas prévue (en trop)
            self.extra_column()

            # erreur: valeur numérique attendue
            self.expected_numerical_value()

            # erreur : champ manquant (pour les colonnes qui ne doivent avoir aucune case de vide)
            self.missing_value()

            # erreur colonne vide (pour les colonnes qui doivent avoir une seule case non vide)
            if len(self.bad_columns) == 0 and len(self.columns_not_provided) == 0:
                self.set_durete = set(self.list_durete)
                self.set_contraintes_residuelles = set(self.list_contraintes_residuelles)
                self.set_duree_vie_outil = set(self.list_duree_vie_outil)

                # erreur aucune valeur ou plusieurs valeurs
                self.empty_column()

            # gestion des erreurs
            self.manage_errors()

            # suppression du fichier .csv
            if os.path.isfile(self.chemin.replace("xlsx", "csv")):
                os.remove(self.chemin.replace("xlsx", "csv"))
