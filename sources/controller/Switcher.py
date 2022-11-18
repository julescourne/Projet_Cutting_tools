from sources.model import session, mydb
from sources.model.Experience import Experience


class Switcher(object):
    """Classe qui gère l'association entre une chaîne de caractère et une liste de valeurs"""

    def __init__(self):
        """Constructeur"""
        self.mycursor = mydb.cursor()
        self.mycursor.execute("""select * from experience order by id desc limit 1""")
        experiences = self.mycursor.fetchall()
        self.experience = None
        for x in experiences:
            self.experience = x[0]

    def indirect(self, name):
        method_name = str(name)
        method = getattr(self, method_name, lambda: "")
        return method()

    def temps(self):
        """fonction qui associe le temps aux valeurs de temps de l'expérience

        Returns : list
            La liste des valeurs du temps
        """
        result = []
        if self.experience is not None:
            sql1 = """select temps from outil where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            temps = self.mycursor.fetchall()
            for x in temps:
                result.append(x[0])
        return result

    def vitesse_coupe(self):
        """fonction qui associe la vitesse de coupe aux valeurs de vitesse de coupe de l'expérience

        Returns : list
            La liste des vitesse de coupe
        """
        result = []
        if self.experience is not None:
            sql1 = """select vitesse_coupe from conditionscoupe where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            vitesse_coupe = self.mycursor.fetchall()
            for x in vitesse_coupe:
                result.append(x[0])
        return result

    def vitesse_avance(self):
        """fonction qui associe la vitesse d'avance aux valeurs de vitesse d'avance de l'expérience

        Returns : list
            La liste des vitesse d'avance
        """
        result = []
        if self.experience is not None:
            sql1 = """select vitesse_avance from conditionscoupe where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            vitesse_avance = self.mycursor.fetchall()
            for x in vitesse_avance:
                result.append(x[0])
        return result

    def profondeur_passe(self):
        """fonction qui associe la profondeur de passe aux valeurs de profondeur de passe de l'expérience

        Returns : list
            La liste des profondeurs de passe
        """
        result = []
        if self.experience is not None:
            sql1 = """select profondeur_passe from conditionscoupe where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            profondeur_passe = self.mycursor.fetchall()
            for x in profondeur_passe:
                result.append(x[0])
        return result

    def geometrie_outil(self):
        """fonction qui associe la géométrie de l'outil aux valeurs de géométrie de l'outil dans l'expérience

        Returns : list
            La liste des géométrie de l'outil
        """
        result = []
        if self.experience is not None:
            sql1 = """select geometrie from outil where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            geometrie = self.mycursor.fetchall()
            for x in geometrie:
                result.append(x[0])
        return result

    def type_lubrifiant(self):
        """fonction qui associe le type de lubrifiant aux valeurs du type de lubrifiant dans l'expérience

        Returns : list
            La liste des types de lubrifiant
        """
        result = []
        if self.experience is not None:
            sql1 = """select type_lubrifiant from conditionscoupe where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            type_lubrifiant = self.mycursor.fetchall()
            for x in type_lubrifiant:
                result.append(x[0])
        return result

    def type_fabrication_piece(self):
        """fonction qui associe le type de fabrication de pièce aux valeurs du type de fabrication de pièce dans
        l'expérience

        Returns : list
            La liste des types de fabrication de pièce
        """
        result = []
        if self.experience is not None:
            sql1 = """select type_fabrication from piece where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            type_fabrication = self.mycursor.fetchall()
            for x in type_fabrication:
                result.append(x[0])
        return result

    def contraintes_residuelles(self):
        """fonction qui associe les contraintes résiduelles aux valeurs de contraintes résiduelles de l'expérience

        Returns : list
            La liste des contraintes résiduelles
        """
        result = []
        if self.experience is not None:
            sql1 = """select contraintes_residuelles from piece where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            contraintes_residuelles = self.mycursor.fetchall()
            for x in contraintes_residuelles:
                result.append(x[0])
        return result

    def duree_vie_outil(self):
        """fonction qui associe la durée de vie aux valeurs de durée de vie de l'expérience

        Returns : list
            La liste des durées de vie de l'outil
        """
        result = []
        if self.experience is not None:
            sql1 = """select duree_de_vie from outil where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            duree_de_vie = self.mycursor.fetchall()
            for x in duree_de_vie:
                result.append(x[0])
        return result

    def durete(self):
        """fonction qui associe la dureté aux valeurs de dureté de l'expérience

        Returns : list
            La liste des duretés
        """
        result = []
        if self.experience is not None:
            sql1 = """select durete from piece where id_experience = %s"""
            self.mycursor.execute(sql1, (self.experience,))
            durete = self.mycursor.fetchall()
            for x in durete:
                result.append(x[0])
        return result

    def effort_coupe_fx(self):
        """fonction qui associe la composante fx aux valeurs de la composante fx de l'expérience

        Returns : list
            La liste des composantes fx de l'effort de coupe
        """
        result = []
        if self.experience is not None:
            sql1 = """select * from conditionscoupe where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (self.experience,))
            conditions_coupes = self.mycursor.fetchall()
            for i in conditions_coupes:
                sql2 = """select fx from effortcoupe where id_conditions_coupe = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fx = self.mycursor.fetchall()
                for x in fx:
                    result.append(x[0])
        return result

    def effort_coupe_fy(self):
        """fonction qui associe la composante fy aux valeurs de la composante fy de l'expérience

        Returns : list
            La liste des composantes fy de l'effort de coupe
        """
        result = []
        if self.experience is not None:
            sql1 = """select * from conditionscoupe where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (self.experience,))
            conditions_coupes = self.mycursor.fetchall()
            for i in conditions_coupes:
                sql2 = """select fy from effortcoupe where id_conditions_coupe = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fy = self.mycursor.fetchall()
                for x in fy:
                    result.append(x[0])
        return result

    def effort_coupe_fz(self):
        """fonction qui associe la composante fz aux valeurs de la composante fz de l'expérience

        Returns : list
            La liste des composantes fz de l'effort de coupe
        """
        result = []
        if self.experience is not None:
            sql1 = """select * from conditionscoupe where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (self.experience,))
            conditions_coupes = self.mycursor.fetchall()
            for i in conditions_coupes:
                sql2 = """select fz from effortcoupe where id_conditions_coupe = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fz = self.mycursor.fetchall()
                for x in fz:
                    result.append(x[0])
        return result

    def rugosite(self):
        """fonction qui associe la rugosité aux valeurs de rugosité de l'expérience

        Returns : list
            La liste des rugosités
        """
        result = []
        if self.experience is not None:
            sql1 = """select * from piece where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (self.experience,))
            pieces = self.mycursor.fetchall()
            for i in pieces:
                sql2 = """select valeur from rugosite where id_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                rugosite = self.mycursor.fetchall()
                for x in rugosite:
                    result.append(x[0])
        return result

    def temperature(self):
        """fonction qui associe la température aux valeurs de température de l'expérience

        Returns : list
            La liste des températures
        """
        result = []
        if self.experience is not None:
            sql1 = """select * from conditionscoupe where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (self.experience,))
            conditions_coupes = self.mycursor.fetchall()
            for i in conditions_coupes:
                sql2 = """select valeur from temperature where id_conditions_coupe = %s"""
                self.mycursor.execute(sql2, (i[0],))
                temperature = self.mycursor.fetchall()
                for x in temperature:
                    result.append(x[0])
        return result
