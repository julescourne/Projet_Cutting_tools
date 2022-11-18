import numpy as np
import pandas as pd
from tkinter.messagebox import showerror, showinfo
import plotly.express as px
from sklearn.decomposition import PCA

from sources.Constants import *
from sources.model.Piece import Piece
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model.EffortCoupe import EffortCoupe
from sources.model.Experience import Experience
from sources.model.Outil import Outil
from sources.model.Rugosite import Rugosite
from sources.model.Temperature import Temperature
from sources.model import session

from sources.utils import get_distance

VARIABLE_LIST = [DUREE_VIE_OUTIL, TYPE_MAT_PIECE, TYPE_FAB_PIECE, DURETE, CONTRAINTES_RESIDUELLES, RUGOSITE,
                 TYPE_LUBRIFIANT, VITESSE_COUPE, VITESSE_AVANCE, PROFONDEUR_PASSE, EFFORT_COUPE_FX, EFFORT_COUPE_FY,
                 EFFORT_COUPE_FZ, TEMPERATURE]

def display_fig(fig):
    """Affiche la figure sur le navigateur"""

    if fig is not None:
        fig.show()
    else:
        showerror(title="Erreur", message="La figure est vide")

class ChoixOutilCoupant:
    """Classe qui contient les méthodes nécéssaire au choix de l'outil coupant"""

    def __init__(self):
        self.ids = None
        self.exp_nouns = None
        self.pca = None
        self.components = None
        self.classes_df = None
        self.fig_2d = None
        self.fig_3d = None
        self.features = None
        self.loadings = None
        self.total_var = None
        self.form_datas = None

    def create_pca_dataframes(self, form_datas):
        """Méthode créant et retournant le tableau utile afin de réaliser l'ACP

        Parameters:
            -form_datas: dictionnaire contentant les informations remplises par l'utilsateur lors de la page
                            choix outil coupant

        Returns:
            -dataframe: contient le tableau pour faire l'acp
        """

        # Requeter le base de données et prendre que les infos nécéssaires
        # Récuperer les id d'expériences correspondant au champs requis pour l'ACP
        # (type fabrication pièce + matérieau pièce).
        self.form_datas = form_datas

        self.ids = [x[0] for x in session.query(Piece.id_experience).filter(
            Piece.type_fabrication == self.form_datas[TYPE_FAB_PIECE],
            Piece.materiau == self.form_datas[TYPE_MAT_PIECE])
            .distinct(Piece.id_experience)]
        print("ids, ", self.ids)

        if not self.ids:
            showerror(title="Erreur", message="Aucune expérience correspondant au couple "
                                              + "(" + self.form_datas[TYPE_FAB_PIECE] + "/"
                                              + self.form_datas[TYPE_MAT_PIECE] + ")"
                                              + " est recensée dans la base de données")

        # Récup&ration des noms des expériences en vu d'un éventuel affichage
        self.exp_nouns = [x for x in session.query(Experience.id, Experience.nom
                                                   ).filter(Experience.id.in_(self.ids))]

        # Requetes des variables non dépendantes du temps
        # VC, FZ, AP et Type lubrifiant (string)
        info_cc_no_time_df = self.get_info_cc()

        # Requetes des variables dépendantes du temps
        info_effort_coupe_max_df = self.get_info_effort_coupe_max_df()
        info_rugosite_mean_df = self.get_info_rugosite_mean_df()
        info_temp_mean_df = self.get_info_temp_mean_df()
        info_piece_mean_df = self.get_info_piece_mean_df()
        info_outil_mean_df = self.get_info_outil_mean_df()

        session.close()

        # création du point référence
        choix_user = self.get_user_df()

        # Concaténation des tableaux et ajout du point référence
        data_db_df = pd.concat([info_cc_no_time_df, info_effort_coupe_max_df, info_piece_mean_df, info_outil_mean_df,
                               info_rugosite_mean_df, info_temp_mean_df], axis=1, sort=False)

        print("data_db_df", data_db_df)
        pca_df = pd.concat([data_db_df.drop(columns=["ID", TYPE_LUBRIFIANT]), choix_user], ignore_index=True, sort=False)

        # On centre les données
        for column in pca_df:
            # Soustraire la moyenne de chaque colonne à chaque valeur : centrer les valeurs
            pca_df[column] = pca_df[column].astype('float').sub(pca_df[column].astype('float').mean())

        # On change les NaN pour des zéros
        pca_df = pca_df.replace(np.nan, 0)

        # Création des classes
        self.classes_df = data_db_df[TYPE_LUBRIFIANT].to_frame()
        self.classes_df = self.classes_df.append({TYPE_LUBRIFIANT: "{}POINT EXPERIENCE".format(
                                                "{} : ".format(form_datas[TYPE_LUBRIFIANT])
                                                if TYPE_LUBRIFIANT in form_datas else "")}, ignore_index=True)

        return pca_df

    def compute_pca(self, form_datas):
        """ Fonction calculant l'ACP

        tab: list contenant les informations principales des éxpériences les plus proches
        """
        pca_df = self.create_pca_dataframes(form_datas)

        print('pca df', pca_df)
        # 2D si deux variables/individus ou moins, 3D sinon
        n_components = min(len(pca_df.columns) - 1, len(pca_df))
        self.pca = PCA(n_components=n_components)
        self.components = self.pca.fit_transform(pca_df)  # coordonnées des points de l'acp
        self.loadings = self.pca.components_.T * np.sqrt(self.pca.explained_variance_)
        self.features = [col_name for col_name in pca_df.columns]  # nom des variables prises en comptes pour l'acp

        return self.compute_closest_experiences()

    def create_and_display_fig_2d(self, with_variable=False):
        """ Créé la modèlisation de l'ACP en 2d avec ou sans les variables

        Parameters:
            with_variable: Boolean pour savoir si on doit ajouter les variables au graph"""

        if TYPE_LUBRIFIANT in self.classes_df:
            # On calcule le taux d'information contenu dans le graphique 2
            self.total_var = self.pca.explained_variance_ratio_[:2].sum() * 100
            self.fig_2d = px.scatter(
                self.components, x=0, y=1, color=self.classes_df[TYPE_LUBRIFIANT],
                title=f'Total Explained Variance: {self.total_var:.2f}%',
                labels={'0': "Factorial axe n°1: {}% ".format(round(self.pca.explained_variance_ratio_[0] * 100, 2)),
                        '1': "Factorial axe n°2: {}% ".format(round(self.pca.explained_variance_ratio_[1] * 100, 2))}
            )
        if with_variable:
            for i, feature in enumerate(self.features):
                self.fig_2d.add_shape(
                    type='line',
                    x0=0, y0=0,
                    x1=self.loadings[i, 0],
                    y1=self.loadings[i, 1]
                )
                self.fig_2d.add_annotation(
                    x=self.loadings[i, 0],
                    y=self.loadings[i, 1],
                    ax=0, ay=0,
                    xanchor="center",
                    yanchor="bottom",
                    text=feature,
                )
        display_fig(self.fig_2d)

    def create_and_display_fig_3d(self):
        """ Créé la modèlisation de l'ACP en 3d"""

        if self.pca.n_components < 3:
            showinfo(title="Info", message="L'ACP ne contient pas assez de composantes pour être affichée en 3D")
        else:
            if not self.fig_2d:
                # On calcule le taux d'information contenu dans le graphique 3
                self.total_var = self.pca.explained_variance_ratio_[:3].sum() * 100
                self.fig_3d = px.scatter_3d(
                    self.components, x=0, y=1, z=2, color=self.classes_df[TYPE_LUBRIFIANT],
                    title=f'Total Explained Variance: {self.total_var:.2f}%',
                    labels={'0': "Factorial axe n°1: {}% ".format(round(self.pca.explained_variance_ratio_[0] * 100, 2)),
                            '1': "Factorial axe n°2: {}% ".format(round(self.pca.explained_variance_ratio_[1] * 100, 2)),
                            '2': "Factorial axe n°3: {}% ".format(round(self.pca.explained_variance_ratio_[2] * 100, 2))}
                )
            display_fig(self.fig_3d)

    def compute_closest_experiences(self):
        """Fonction qui calcule le tableau récapitulant les expériences les plus proches

        Returns:
            tab: list contenant les informations principales des éxpériences les plus proches"""

        tab = []
        exp_user = self.components[-1]  # Les coordonées du point de l'utilisateur sont toujours en dernier

        dist = []
        for exp_coord in self.components[:-1]:
            dist.append(get_distance(exp_user, exp_coord, self.pca.explained_variance_ratio_))

        dist = np.array(dist)

        sorted_dist = dist.argsort()
        nb_rows = len(sorted_dist) if len(sorted_dist) < 10 else 10

        for index in sorted_dist[:nb_rows]:
            tab.append((self.ids[index], self.exp_nouns[index][1], round(dist[index], 3), self.classes_df[TYPE_LUBRIFIANT][index]))

        return tab

    def get_max_per_exp(self, info_multi_row_per_exp_df):
        """Fonction qui renvoie le maximum en valeur absolue sur chaque colonne du dataframe par id d'expérience

        Params: info_multi_row_per_exp_df: dataframe

        Returns: dataframe"""

        dataframes = []
        for id in self.ids:
            sub_df = info_multi_row_per_exp_df.query('ID == {}'.format(id))
            dataframes.append(sub_df.abs().max().to_frame().T)

        return pd.concat(dataframes, ignore_index=True, sort=False)

    def get_mean_per_exp(self, info_multi_row_per_exp_df):
        """Fonction qui renvoie la moyenne sur chaque colonne du dataframe par id d'expérience

        Params: info_multi_row_per_exp_df: dataframe

        Returns: dataframe"""

        dataframes = []
        for id in self.ids:
            sub_df = info_multi_row_per_exp_df.query('ID == {}'.format(id))
            dataframes.append(sub_df.mean().to_frame().T)

        return pd.concat(dataframes, ignore_index=True, sort=False)

    def get_info_effort_coupe_max_df(self):
        """Renvoie le dataframe associé aux efforts maximals de chaque compsosantes de chaque expérience

        Returns: dataframe or None"""

        if any(key in self.form_datas for key in [EFFORT_COUPE_FX, EFFORT_COUPE_FY, EFFORT_COUPE_FZ]):
            info_effort_coupe = [x for x in session.query(ConditionsCoupe.id_experience,
                                                          EffortCoupe.fx if EFFORT_COUPE_FX in self.form_datas else None,
                                                          EffortCoupe.fy if EFFORT_COUPE_FY in self.form_datas else None,
                                                          EffortCoupe.fz if EFFORT_COUPE_FZ in self.form_datas else None,
                                                          ).join(ConditionsCoupe).filter(
                ConditionsCoupe.id_experience.in_(self.ids))]
            # Déduire les variables supplémentaire de l'ACP (Max/min/mean)
            info_effort_coupe_df = pd.DataFrame(info_effort_coupe, columns=["ID",
                                                                            EFFORT_COUPE_FX if EFFORT_COUPE_FX in self.form_datas else None,
                                                                            EFFORT_COUPE_FY if EFFORT_COUPE_FY in self.form_datas else None,
                                                                            EFFORT_COUPE_FZ if EFFORT_COUPE_FZ in self.form_datas else None])
            info_effort_coupe_max_df = self.get_max_per_exp(info_effort_coupe_df.dropna(axis=1, how='all').replace(np.nan, 0))

            return info_effort_coupe_max_df
        return None

    def get_info_rugosite_mean_df(self):
        """Calcul les informations de la table Rugoisté en faisant une moyenne par expérience

        Returns:
            dataframe or None"""

        if RUGOSITE in self.form_datas:
            info_rugosite = [x for x in session.query(Piece.id_experience,
                                                      Rugosite.valeur).join(Piece)
                                                      .filter(Piece.id_experience.in_(self.ids))]
            # Déduire les variables supplémentaire de l'ACP (Max/min/mean)
            info_rugosite_df = pd.DataFrame(info_rugosite, columns=["ID", RUGOSITE])
            info_rugosite_max_df = self.get_mean_per_exp(info_rugosite_df)

            return info_rugosite_max_df
        return None

    def get_info_temp_mean_df(self):
        """Calcul les informations de la table Temperature en faisant une moyenne par expérience

        Returns:
            dataframe or None"""

        if TEMPERATURE in self.form_datas:
            info_temp = [x for x in session.query(ConditionsCoupe.id_experience,
                                                  Temperature.valeur).join(ConditionsCoupe)
                                                  .filter(ConditionsCoupe.id_experience.in_(self.ids))]
            # Déduire les variables supplémentaire de l'ACP (Max/min/mean)
            info_temp_df = pd.DataFrame(info_temp, columns=["ID", TEMPERATURE])
            info_temp_max_df = self.get_mean_per_exp(info_temp_df)

            return info_temp_max_df
        return None

    def get_info_piece_mean_df(self):
        """Calcul les informations de la table Piece en faisant une moyenne par expérience

        Returns:
            dataframe or None"""

        if any(key in self.form_datas for key in [CONTRAINTES_RESIDUELLES, DURETE]):
            info_piece = [x for x in session.query(Piece.id_experience,
                                                   Piece.contraintes_residuelles if CONTRAINTES_RESIDUELLES in self.form_datas else None,
                                                   Piece.durete if DURETE in self.form_datas else None,
                                                   ).filter(Piece.id_experience.in_(self.ids))]
            # Déduire les variables supplémentaire de l'ACP (Max/min/mean)
            info_piece_df = pd.DataFrame(info_piece, columns=["ID",
                                                              CONTRAINTES_RESIDUELLES if CONTRAINTES_RESIDUELLES in self.form_datas else None,
                                                              DURETE if DURETE in self.form_datas else None])
            info_piece_max_df = self.get_mean_per_exp(info_piece_df.dropna(axis=1, how='all').replace(np.nan, 0))

            return info_piece_max_df
        return None

    def get_info_outil_mean_df(self):
        """Calcul les informations de la table Outil en faisant une moyenne par expérience

        Returns:
            dataframe or None"""

        if DUREE_VIE_OUTIL in self.form_datas:
            info_outil = [x for x in session.query(Outil.id_experience, Outil.duree_de_vie
                                                   ).filter(Outil.id_experience.in_(self.ids))]
            # Déduire les variables supplémentaire de l'ACP (Max/min/mean)
            info_outil_df = pd.DataFrame(info_outil, columns=["ID", DUREE_VIE_OUTIL])
            info_outil_max_df = self.get_mean_per_exp(info_outil_df)

            return info_outil_max_df
        return None

    def get_info_cc(self):
        """Renvoie les informations sur les conditions de coupe des expériences

        Returns:
            dataframe"""

        info_cc_no_time = [x for x in session.query(ConditionsCoupe.id_experience,
                                  ConditionsCoupe.vitesse_coupe if VITESSE_COUPE in self.form_datas else None,
                                  ConditionsCoupe.vitesse_avance if VITESSE_AVANCE in self.form_datas else None,
                                  ConditionsCoupe.profondeur_passe if PROFONDEUR_PASSE in self.form_datas else None,
                                  ConditionsCoupe.type_lubrifiant,
                                  ).filter(ConditionsCoupe.id_experience.in_(self.ids)).distinct(
            ConditionsCoupe.id_experience)]
        info_cc_no_time_df = pd.DataFrame(info_cc_no_time,
                                          columns=["ID", VITESSE_COUPE if VITESSE_COUPE in self.form_datas else None,
                                                   VITESSE_AVANCE if VITESSE_AVANCE in self.form_datas else None,
                                                   PROFONDEUR_PASSE if PROFONDEUR_PASSE in self.form_datas else None,
                                                   TYPE_LUBRIFIANT])
        print(info_cc_no_time_df)
        return info_cc_no_time_df.dropna(axis=1, how='all').replace(np.nan, 0)

    def get_user_df(self):
        """Renvoie le dataframe correspondant aux choix du l'utilisteur dans le formulaire

        Returns:
            dataframe"""

        user_df = pd.DataFrame(self.form_datas, index=[0])

        # Supprimer les colonnes non utiles à l'acp:
        if TYPE_LUBRIFIANT in self.form_datas:
            user_df.drop(
                columns=[TYPE_FAB_PIECE, TYPE_MAT_PIECE, TYPE_LUBRIFIANT],
                inplace=True,
            )
        else:
            user_df.drop(
                columns=[TYPE_FAB_PIECE, TYPE_MAT_PIECE],
                inplace=True,
            )

        return user_df
