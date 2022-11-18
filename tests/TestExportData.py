import os
from pathlib import Path
import unittest
import pandas as pd

from sources.controller.ExportData import ExportData


class TestExportData(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if os.path.isfile(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                       "gabarit_" + self.export.type_experience + ".xlsx")):
            os.remove(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                   "gabarit_" + self.export.type_experience + ".xlsx"))

    @classmethod
    def setUpClass(cls):
        cls.export = ExportData("contraintes résiduelles")
        cls.check = True

    def test_export_file_is_exist(self):
        """test pour savoir si le fichier résultat existe dans le dossier download"""
        self.export.export_data(self.check)
        self.assertEqual(os.path.isfile(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                                     "gabarit_" + self.export.type_experience + ".xlsx")), True)

    def test_export_file_is_exist_with_wrong_experience_name(self):
        """test pour savoir si le fichier résultat existe dans le dossier download avec un type d'expérience qui
        n'existe pas """
        self.export.type_experience = "mauvais_nom"
        self.export.export_data(self.check)
        self.assertEqual(os.path.isfile(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                                     "gabarit_" + self.export.type_experience + ".xlsx")), True)

    def test_export_file_exist_without_check(self):
        """test pour vérifier que le fichier résultat existe dans le dossier download avec check = False"""
        self.check = False
        self.export.type_experience = "température"
        self.export.export_data(self.check)
        self.assertEqual(os.path.isfile(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                                     "gabarit_" + self.export.type_experience + ".xlsx")), True)

    def test_file_not_exist(self):
        """test pour vérifier que le fichier n'existe pas dans le dossier download"""
        self.check = True
        self.export.type_experience = "température"
        self.export.export_data(self.check)
        self.assertEqual(os.path.isfile(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                                     "gabarit_" + self.export.type_experience + ".xlsx")), False)

    def test_data_correctly_write_gabarit_temperature(self):
        """test pour vérifier que les données sont bonnes pour le gabarit température"""
        self.check = False
        self.export.type_experience = "température"
        self.export.export_data(self.check)
        data = pd.read_excel(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                          "gabarit_" + self.export.type_experience + ".xlsx"))
        self.assertEqual(list(data.columns), ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type "
                                                                                                               "fabrication "
                                                                                                               "pièce",
                                              "matériau pièce", "température"])

    def test_data_correctly_write_gabarit_effort_coupe(self):
        """test pour vérifier que les données sont bonnes pour le gabarit effort coupe"""
        self.check = False
        self.export.type_experience = "effort de coupe"
        self.export.export_data(self.check)
        data = pd.read_excel(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                          "gabarit_" + self.export.type_experience + ".xlsx"))
        self.assertEqual(list(data.columns), ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type "
                                                                                                               "fabrication "
                                                                                                               "pièce",
                                              "matériau pièce", "effort de coupe fx", "effort de coupe fy", "effort "
                                                                                                            "de coupe"
                                                                                                            " fz"])

    def test_data_correctly_write_gabarit_mauvais_nom(self):
        """test pour vérifier que les données sont bonnes pour un mauvais gabarit"""
        self.check = False
        self.export.type_experience = "mauvais nom"
        self.export.export_data(self.check)
        data = pd.read_excel(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                          "gabarit_" + self.export.type_experience + ".xlsx"))
        self.assertEqual(list(data.columns),
                         ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type "
                                                                                           "fabrication "
                                                                                           "pièce",
                          "matériau pièce"])

    def test_data_not_correctly_write_column_name_error(self):
        """test pour vérifier que la dernière colonne contient une erreur de nom"""
        self.check = False
        self.export.type_experience = "contraintes résiduelles"
        self.export.export_data(self.check)
        data = pd.read_excel(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                          "gabarit_" + self.export.type_experience + ".xlsx"))
        self.assertNotEqual(list(data.columns),
                            ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type "
                                                                                              "fabrication "
                                                                                              "pièce",
                             "matériau pièce", "contrainte résiduelles"])

    def test_data_not_correctly_write_column_exchanges_columns(self):
        """test pour vérifier que deux colonnes sont échangées"""
        self.check = False
        self.export.type_experience = "contraintes résiduelles"
        self.export.export_data(self.check)
        data = pd.read_excel(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                          "gabarit_" + self.export.type_experience + ".xlsx"))
        self.assertNotEqual(list(data.columns),
                            ["vc", "temps", "fz", "ap", "géométrie outil", "type lubrifiant", "type "
                                                                                              "fabrication "
                                                                                              "pièce",
                             "matériau pièce", "contraintes résiduelles"])

    def test_data_not_correctly_write_column_extra_column(self):
        """test pour vérifier qu'il y a une colonne en trop'"""
        self.check = False
        self.export.type_experience = "contraintes résiduelles"
        self.export.export_data(self.check)
        data = pd.read_excel(os.path.join(str(os.path.join(Path.home(), "Downloads")),
                                          "gabarit_" + self.export.type_experience + ".xlsx"))
        self.assertNotEqual(list(data.columns),
                            ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type "
                                                                                              "fabrication "
                                                                                              "pièce",
                             "matériau pièce", "contraintes résiduelles", "colonne"])
