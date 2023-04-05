import threading
import dash
import webbrowser
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from model import mydb
from view.Dashboard import Dashboard
from controller.DashboardBarController import DashboardBarController
from controller.DashboardRadarController import DashboardRadarController
from controller.DashboardInfoController import DashboardInfoController
from controller.DashboardNuageController import DashboardNuageController

class DashboardController:
    """
    Classe qui contient les méthodes necessaire à l'utilisation du Dashboard. Le dashboard est une interface plotly
    dash permettant de visualiser les données issues d'une expérience de la base de données.
    """

    def __init__(self, treeview, datas_usr):
        """
        Constructeur de la classe DashboardController
        :param treeview: Objet treeview contenant les données d'une expérience de la base de données
        :param datas_usr: Paramètres d'usinage remplis par l'utilisateur
        """
        # Données du treeview associés au dashboard
        self.treeview = treeview

        # id de l'expérience associé au dashboard
        self.item_id = None
        self.data_exp = None
        self.effort_piece = None
        self.effort_outil = None
        self.dashboard = None
        self.radar_controller = None
        self.info_controller = None
        self.bar_controller = None
        self.nuage_controller = None

        self.user_data = datas_usr

        # Initialisation de l'application dash
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

        # Ensemble des méthodes utilisant le décorateur @self.app.callback
        self.visibility()
        self.color_callbacks()

    def visibility(self):
        @self.app.callback(
            Output('content_infos', 'style'),
            Output('content_radar', 'style'),
            Output('content_bar', 'style'),
            Output('content_nuage', 'style'),
            Input('btn-info', 'n_clicks'),
            Input('btn-radar', 'n_clicks'),
            Input('btn-bar', 'n_clicks'),
            Input('btn-nuage', 'n_clicks')
        )
        def display_page_infos(n_info_clicks, n_radar_clicks, n_bar_clicks, n_nuage_clicks):
            """
            Méthode permettant de gérer l'affichage de chaque partie en fonction des cliques de l'utilisateur
            :param n_info_clicks: nombre de click sur l'item 'Informations generales'
            :param n_radar_clicks: nombre de click sur l'item 'Graphique en radar'
            :param n_bar_clicks: nombre de click sur l'item 'Visualisation en bar'
            :return: style des conteneurs de la partie droite du dashboard
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = 'btn-info'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'btn-info':
                return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

            elif button_id == 'btn-radar':
                return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

            elif button_id == 'btn-bar':
                return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}

            elif button_id == 'btn-nuage':
                return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}

    def color_callbacks(self):
        @self.app.callback(
            Output('btn-info', 'style'),
            Output('btn-radar', 'style'),
            Output('btn-bar', 'style'),
            Output('btn-nuage', 'style'),
            Input('btn-info', 'n_clicks'),
            Input('btn-radar', 'n_clicks'),
            Input('btn-bar', 'n_clicks'),
            Input('btn-nuage', 'n_clicks'),
        )
        def update_button_colors(info_clicks, radar_clicks, courbe_clicks, nuage_clicks):
            """
            Fonction qui color le bouton cliqué en dernier par l'utilisateur
            :param info_clicks: nombre de click sur l'item 'Informations generales'
            :param radar_clicks: nombre de click sur l'item 'Graphique en radar'
            :param bar_clicks: nombre de click sur l'item 'Visualisation en bar'
            :return: style des trois items
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = 'btn-info'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'btn-info':
                return {'color': 'white', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}
            elif button_id == 'btn-radar':
                return {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': 'white', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}
            elif button_id == 'btn-bar':
                return {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': 'white', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}
            elif button_id == 'btn-nuage':
                return {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': 'white', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}



    def get_needed_data(self):
        """
        Recupere les efforts et les données de l'experience
        """
        self.data_exp = self.treeview.item(self.item_id)['values']
        mycursor = mydb.cursor()
        sql1 = """select id_entree_piece from entree_piece where id_experience=%s"""
        mycursor.execute(sql1, (self.treeview.item(self.item_id)['values'][0],))
        piece = mycursor.fetchall()

        sql2 = """select * from effort_piece where id_entree_piece=%s"""
        mycursor.execute(sql2, (piece[0][0],))
        self.effort_piece = mycursor.fetchall()

        sql3 = """select id_entree_outil from entree_outil where id_experience=%s"""
        mycursor.execute(sql3, (self.treeview.item(self.item_id)['values'][0],))
        outil = mycursor.fetchall()

        sql4 = """select * from effort_outil where id_entree_outil=%s"""
        mycursor.execute(sql4, (outil[0][0],))
        self.effort_outil = mycursor.fetchall()
        mycursor.close()

    def open_browser(self):
        """
        Ouvre l'application dash sur une page web
        """
        webbrowser.open_new("http://localhost:{}".format(8050))

    def ouvrir_dash_interface(self, event):
        """
        Lance l'application dash
        :param event: evenement de clique de la souris
        """
        self.item_id = self.treeview.identify_row(event.y)
        self.get_needed_data()
        self.dashboard = Dashboard(self.app, self.data_exp, self.user_data)
        self.radar_controller = DashboardRadarController(self.app, self.dashboard.dashboard_radar)
        self.bar_controller = DashboardBarController(self.app, self.dashboard.dashboard_bar, self.effort_piece,
                                                     self.effort_outil)
        self.info_controller = DashboardInfoController(self.app, self.dashboard.dashboard_info)
        self.nuage_controller = DashboardNuageController(self.app, self.dashboard.dashboard_bar, self.effort_piece,
                                                     self.effort_outil)
        t1 = threading.Thread(target=self.app.run, kwargs={'debug': True, 'port': 8050, 'use_reloader': False})
        t1.start()
        self.open_browser()
