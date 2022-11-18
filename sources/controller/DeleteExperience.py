from tkinter.messagebox import showinfo

from sources.model import session, mydb
from sources.model.Experience import Experience


class DeleteExperience:
    """Classe qui gère la suppression d'une expérience de la base de données"""

    def __init__(self):
        """Constructeur"""
        self.mycursor = mydb.cursor()

    def delete_experience(self):
        """fonction qui supprime la dernière expérience ajoutée à la base de données"""
        id_exp = None
        self.mycursor.execute("""select * from experience order by id desc limit 1""")
        experience = self.mycursor.fetchall()
        for x in experience:
            id_exp = x[0]

        if id_exp is not None:
            sql1 = """select * from conditionscoupe where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (id_exp,))
            conditions_coupes = self.mycursor.fetchall()
            for x in conditions_coupes:
                sql2 = """delete from effortcoupe where id_conditions_coupe = %s"""
                self.mycursor.execute(sql2, (x[0],))
                sql3 = """delete from temperature where id_conditions_coupe = %s"""
                self.mycursor.execute(sql3, (x[0],))
                sql4 = """delete from conditionscoupe where id = %s"""
                self.mycursor.execute(sql4, (x[0],))

            sql5 = """select * from piece where id_experience = %s order by id"""
            self.mycursor.execute(sql5, (id_exp,))
            pieces = self.mycursor.fetchall()

            for x in pieces:
                sql6 = """delete from rugosite where id_piece = %s"""
                self.mycursor.execute(sql6, (x[0],))
                sql7 = """delete from piece where id = %s"""
                self.mycursor.execute(sql7, (x[0],))

            sql8 = """select * from outil where id_experience = %s order by id"""
            self.mycursor.execute(sql8, (id_exp,))
            outils = self.mycursor.fetchall()
            for x in outils:
                sql9 = """delete from outil where id = %s"""
                self.mycursor.execute(sql9, (x[0],))

            sql10 = """delete from experience where id = %s"""
            self.mycursor.execute(sql10, (id_exp,))
            mydb.commit()

            showinfo(title=None, message="Expérience supprimée")
        else:
            showinfo(title=None, message="Il n'y a aucune expérience dans la base de données")
