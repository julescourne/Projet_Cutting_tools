import unittest
from sources.controller.ImportData import *


class TestImportData(unittest.TestCase):
    def setUp(self):
        self.import_data_object.__init__()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls.import_data_object = ImportData()
        cls.errors = ""
        cls.bad_columns = []
        cls.bad_columns_2 = [["test", "colonneA", "A"]]
        cls.bad_columns_3 = [["test", "colonneA", "A"], ["test", "colonneD", "D"]]

        cls.columns_not_provided = []
        cls.columns_not_provided_2 = ["colonne1"]
        cls.columns_not_provided_3 = ["colonne1", "colonne4"]

        cls.numerical_values = []
        cls.numerical_values_2 = [[2, "colonne D"]]
        cls.numerical_values_3 = [[3, "colonne C"], [6, "colonne A"]]

        cls.required_fields = []
        cls.required_fields_2 = [[1, "colonne A"]]
        cls.required_fields_3 = [[5, "colonne R"], [8, "colonne Z"]]

        cls.type_file = "contraintes résiduelles"
        cls.set_vc = set("3")
        cls.set_fz = set("a")
        cls.set_ap = set("b")
        cls.set_geometrie_outil = set("c")
        cls.set_type_lubrifiant = set("d")
        cls.set_type_fabrication_piece = set("e")
        cls.set_materiau_piece = set("f")
        cls.set_durete = set("g")
        cls.set_contraintes_residuelles = set("h")
        cls.set_duree_vie_outil = set("i")

        cls.row = []
        cls.column_names = ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type fabrication pièce",
                            "matériau pièce"]

        cls.exp_controller = ExperienceController()
        cls.ou_controller = OutilController()
        cls.pie_controller = PieceController()
        cls.ru_controller = RugositeController()
        cls.con_coupe_controller = ConditionsCoupeController()
        cls.eff_coupe_controller = EffortCoupeController()
        cls.temp_controller = TemperatureController()
        cls.chemin = "test/gab.xlsx"
        cls.list_temps = []
        cls.list_rugosite = []
        cls.list_effort_coupe = []
        cls.list_temperature = []

    def test_error_column_without_error(self):
        """test sans erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.bad_columns = self.bad_columns
        self.import_data_object.error_column()
        self.assertEqual(self.import_data_object.errors, "")

    def test_error_column_with_one_error(self):
        """test avec une seule erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.bad_columns = self.bad_columns_2
        self.import_data_object.error_column()
        self.assertEqual(self.import_data_object.errors,
                         "Mauvaises colonnes : L'en-tête de la colonne A est test alors "
                         "qu'il devrait être colonneA" + "\n" + "\n" +
                         "\n")

    def test_error_column_with_several_errors(self):
        """test avec plusieurs erreurs"""
        self.import_data_object.errors = self.errors
        self.import_data_object.bad_columns = self.bad_columns_3
        self.import_data_object.error_column()
        self.assertEqual(self.import_data_object.errors,
                         "Mauvaises colonnes : L'en-tête de la colonne A est test alors "
                         "qu'il devrait être colonneA" + "\n" + "L'en-tête de la colonne D est test alors qu'il "
                                                                "devrait être colonneD" + "\n" + "\n"
                                                                                                 "\n")

    def test_extra_column_without_error(self):
        """test sans erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.columns_not_provided = self.columns_not_provided
        self.import_data_object.extra_column()
        self.assertEqual(self.import_data_object.errors, "")

    def test_extra_column_with_one_error(self):
        """test avec une seule erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.columns_not_provided = self.columns_not_provided_2
        self.import_data_object.extra_column()
        self.assertEqual(self.import_data_object.errors,
                         "Colonnes non prévues : colonne1" + "\n" + "\n")

    def test_extra_column_with_several_errors(self):
        """test avec plusieurs erreurs"""
        self.import_data_object.errors = self.errors
        self.import_data_object.columns_not_provided = self.columns_not_provided_3
        self.import_data_object.extra_column()
        self.assertEqual(self.import_data_object.errors, "Colonnes non prévues : colonne1, "
                                                         "colonne4" + "\n" + "\n")

    def test_expected_numerical_value_without_error(self):
        """test sans erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.numerical_values = self.numerical_values
        self.import_data_object.expected_numerical_value()
        self.assertEqual(self.import_data_object.errors, "")

    def test_expected_numerical_value_with_one_error(self):
        """test avec une seule erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.numerical_values = self.numerical_values_2
        self.import_data_object.expected_numerical_value()
        self.assertEqual(self.import_data_object.errors, "Valeurs numériques "
                                                         "attendues : " + "\n" +
                         "Ligne : 2, colonne : colonne D " + "\n" + "\n")

    def test_expected_numerical_value_with_several_error(self):
        """test avec plusieurs erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.numerical_values = self.numerical_values_3
        self.import_data_object.expected_numerical_value()
        self.assertEqual(self.import_data_object.errors, "Valeurs numériques "
                                                         "attendues : " + "\n" +
                         "Ligne : 3, colonne : colonne C " + "\n" + "Ligne : 6, colonne : colonne A " + "\n" + "\n")

    def test_missing_value_without_error(self):
        """test sans erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.required_fields = self.required_fields
        self.import_data_object.missing_value()
        self.assertEqual(self.import_data_object.errors, "")

    def test_missing_value_with_one_error(self):
        """test avec une erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.required_fields = self.required_fields_2
        self.import_data_object.missing_value()
        self.assertEqual(self.import_data_object.errors,
                         "Champs obligatoires " + "\n" + "Ligne 1, colonne : colonne A " + "\n" + "\n")

    def test_missing_value_with_several_errors(self):
        """test avec plusieurs erreurs"""
        self.import_data_object.errors = self.errors
        self.import_data_object.required_fields = self.required_fields_3
        self.import_data_object.missing_value()
        self.assertEqual(self.import_data_object.errors,
                         "Champs obligatoires " + "\n" + "Ligne 5, colonne : colonne R " + "\n" + "Ligne 8, colonne : "
                                                                                                  "colonne Z " + "\n"
                         + "\n")

    def test_empty_column_without_error(self):
        """test sans erreur"""
        self.import_data_object.errors = self.errors
        self.import_data_object.type_file = self.type_file
        self.import_data_object.set_vc = self.set_vc
        self.import_data_object.set_fz = self.set_fz
        self.import_data_object.set_ap = self.set_ap
        self.import_data_object.set_geometrie_outil = self.set_geometrie_outil
        self.import_data_object.set_type_lubrifiant = self.set_type_lubrifiant
        self.import_data_object.set_type_fabrication_piece = self.set_type_fabrication_piece
        self.import_data_object.set_materiau_piece = self.set_materiau_piece
        self.import_data_object.set_durete = self.set_durete
        self.import_data_object.set_contraintes_residuelles = self.set_contraintes_residuelles
        self.import_data_object.set_duree_vie_outil = self.set_duree_vie_outil
        self.import_data_object.empty_column()
        self.assertEqual(self.import_data_object.errors, "")

    def test_empty_column_with_empty_column_vc(self):
        """test avec la colonne vc vide"""
        self.import_data_object.errors = self.errors
        self.import_data_object.type_file = self.type_file
        self.import_data_object.set_vc = set()
        self.import_data_object.set_fz = self.set_fz
        self.import_data_object.set_ap = self.set_ap
        self.import_data_object.set_geometrie_outil = self.set_geometrie_outil
        self.import_data_object.set_type_lubrifiant = self.set_type_lubrifiant
        self.import_data_object.set_type_fabrication_piece = self.set_type_fabrication_piece
        self.import_data_object.set_materiau_piece = self.set_materiau_piece
        self.import_data_object.set_durete = self.set_durete
        self.import_data_object.set_contraintes_residuelles = self.set_contraintes_residuelles
        self.import_data_object.set_duree_vie_outil = self.set_duree_vie_outil
        self.import_data_object.empty_column()
        self.assertEqual(self.import_data_object.errors,
                         "La colonne vc est vide " + "\n")

    def test_empty_column_with_empty_column_contraintes_residuelles_and_several_values_durete(self):
        """test avec la colonne contraintes résiduelles vide et la colonne dureté avec plusieurs valeurs"""
        self.import_data_object.errors = self.errors
        self.import_data_object.type_file = self.type_file
        self.import_data_object.set_contraintes_residuelles = set()
        self.import_data_object.set_materiau_piece = {"e1", "e2"}
        self.import_data_object.set_vc = self.set_vc
        self.import_data_object.set_fz = self.set_fz
        self.import_data_object.set_ap = self.set_ap
        self.import_data_object.set_geometrie_outil = self.set_geometrie_outil
        self.import_data_object.set_type_lubrifiant = self.set_type_lubrifiant
        self.import_data_object.set_type_fabrication_piece = self.set_type_fabrication_piece
        self.import_data_object.set_durete = self.set_durete
        self.import_data_object.set_duree_vie_outil = self.set_duree_vie_outil
        self.import_data_object.empty_column()
        self.assertEqual(self.import_data_object.errors,
                         "La colonne matériau pièce a des cases vides " + "\n" + "La colonne "
                                                                                                                        "contraintes "
                                                                                                                        "résiduelles est vide "
                                                                                                                        "" + "\n")

    def test_check_experience_type_none(self):
        """test avec aucun type d'expérience"""
        self.row = ["", "3", "contraintes"]
        self.import_data_object.type_file = ""
        self.import_data_object.column_names = ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant",
                                                "type fabrication pièce",
                                                "matériau pièce"]
        self.import_data_object.check_experience_type(self.row)
        self.assertEqual(self.import_data_object.type_file, "")
        self.assertEqual(self.import_data_object.column_names,
                         ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type fabrication pièce",
                          "matériau pièce"])

    def test_check_experience_type_duree_vie_outil(self):
        """test avec expérience de type durée de vie outil"""
        self.row = ["", "3", "durée de vie outil", "case"]
        self.import_data_object.type_file = ""
        self.import_data_object.column_names = ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant",
                                                "type fabrication pièce",
                                                "matériau pièce"]
        self.import_data_object.check_experience_type(self.row)
        self.assertEqual(self.import_data_object.type_file, "durée de vie outil")
        self.assertEqual(self.import_data_object.column_names,
                         ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type fabrication pièce",
                          "matériau pièce", "durée de vie outil"])

    def test_check_experience_type_contraintes_residuelles(self):
        """test avec expérience de type contraintes résiduelles"""
        self.row = ["", "contraintes résiduelles", "durée de vie outil", "case"]
        self.import_data_object.type_file = ""
        self.import_data_object.check_experience_type(self.row)
        self.assertEqual(self.import_data_object.type_file, "contraintes résiduelles")
        self.assertEqual(self.import_data_object.column_names,
                         ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type fabrication pièce",
                          "matériau pièce", "contraintes résiduelles"])

    def test_check_numerical_value_with_no_errors(self):
        """test avec aucune erreur"""
        self.row = [1.3, "3", -34, 9.4, 4.2, "attr2", "attr3", "attr4", 5.3]
        self.import_data_object.check_numerical_value(self.row, 5)
        self.assertEqual(self.import_data_object.numerical_values, [])

    def test_check_numerical_value_with_errors(self):
        """test avec 2 erreurs"""
        self.row = ["error1", "3", -34, 9.4, 4.2, "attr2", "attr3", "attr4", "error2"]
        self.import_data_object.column_names.append("contraintes résiduelles")
        self.import_data_object.check_numerical_value(self.row, 5)
        self.assertEqual(self.import_data_object.numerical_values,
                         [[6, "temps"], [6, "contraintes résiduelles"]])

    def test_check_numerical_value_with_type_effort_coupe(self):
        """test avec une expérience de type effort coupe"""
        self.row = [5.3, "3", -34, 9.4, 4.2, "attr2", "attr3", "attr4", 4, "4", "5"]
        self.import_data_object.type_file = "effort de coupe"
        self.import_data_object.check_numerical_value(self.row, 5)
        self.assertEqual(self.import_data_object.numerical_values, [])

    def test_check_header_error_extra_column(self):
        """test avec un fichier qui contient une colonne en trop"""
        self.import_data_object.check_header(
            ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type fabrication pièce",
             "matériau pièce", "température", "colonne1"])
        self.assertEqual(self.import_data_object.columns_not_provided, ["colonne1"])

    def test_check_header_error_wrong_column_name(self):
        """test avec un fichier a un mauvais nom de colonne"""
        self.import_data_object.check_header(
            ["temps", "vc", "fz", "app", "géométrie outil", "type lubrifiant", "type fabrication pièce",
             "matériau pièce", "température"])
        self.assertEqual(self.import_data_object.bad_columns, [["app", "ap", "D"]])

    # A CHANGER
    def test_check_header_error_wrong_column(self):
        """test avec un fichier a un mauvais"""
        self.import_data_object.check_header(
            ["temps", "vc", "fz", "ap", "géométrie outil", "type lubrifiant", "type fabrication pièce",
             "matériau pièce", "température", "vc"])
        self.assertEqual(self.import_data_object.columns_not_provided, [])

    def test_check_lines_without_error(self):
        """test sans erreur"""
        self.import_data_object.type_file = "contraintes résiduelles"
        self.import_data_object.check_lines(
            [1.5, 3, 67.3, 4.3, "geo_ou", "ty_lubri", "ty_fab_pie",
             "mat_pie", 0.3], 4)
        self.assertEqual(self.import_data_object.required_fields, [])
        self.assertEqual(self.import_data_object.list_contraintes_residuelles, [0.3])

    def test_check_lines_with_missing_fields(self):
        """test avec des valeurs manquantes"""
        self.import_data_object.type_file = "contraintes résiduelles"
        self.import_data_object.check_lines(
            ["", 3, 67.3, 4.3, "geo_ou", "ty_lubri", "ty_fab_pie",
             "mat_pie", 0.3], 4)
        self.assertEqual(self.import_data_object.required_fields, [[5, "temps"]])
