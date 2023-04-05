from dash import html, dcc
import dash_bootstrap_components as dbc
from view.DashboardInfo import DashboardInfo
from view.DashboardRadar import DashboardRadar
from view.DashboardBar import DashboardBar
from view.DashboardNuage import DashboardNuage


class Dashboard:
    """class contenant la vue du Dashboard"""

    def __init__(self, app, data_exp, data_usr):
        """Constructeur de la classe Dashboard"""

        # attribut contenant l'application Dash
        self.app = app

        # valeurs associees à une experience de la base de données
        self.data = data_exp

        self.data_usr = data_usr

        self.dashboard_info = DashboardInfo(self.data)

        self.dashboard_radar = DashboardRadar(self.data, self.data_usr)

        self.dashboard_bar = DashboardBar(self.data)

        self.dashboard_nuage = DashboardNuage(self.data)

        # Menu vertical à gauche
        self.menu = html.Div([
            html.H2('Dashboard',
                    style={'color': 'white', 'background-color': '#363740', 'padding': '10px', 'font-family': 'Abang',
                           'text-align': 'center'}),
            html.Button('Informations générales', id='btn-info', n_clicks=0,
                        style={'color': 'white', 'margin-bottom': '10px', 'padding': '10px',
                               'width': '100%',
                               'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}),
            html.Button('Visualisation en radar', id='btn-radar', n_clicks=0,
                        style={'color': 'white', 'margin-bottom': '10px', 'padding': '10px',
                               'width': '100%',
                               'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}),
            html.Button('Visualisation en bar', id='btn-bar', n_clicks=0,
                        style={'color': 'white', 'margin-bottom': '10px', 'padding': '10px',
                               'width': '100%',
                               'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}),
            html.Button('Nuage de points', id='btn-nuage', n_clicks=0,
                        style={'color': 'white', 'margin-bottom': '10px', 'padding': '10px',
                               'width': '100%',
                               'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'})
        ], className='menu', style={'backgroundColor': '#363740', 'height': '100%', 'width': '200px'})

        # Définition du layout de l'application
        self.app.layout = html.Div([
            dbc.Row([
                dbc.Col([
                    self.menu,
                ], width=2),
                dbc.Col([
                    dbc.Row([
                        self.dashboard_info.content,
                        self.dashboard_radar.content,
                        self.dashboard_bar.content,
                        self.dashboard_nuage.content
                    ])
                ], style={'padding-top': '20px', 'padding-bottom': '20px'}),
            ], className='wrapper', style={'height': '100vh'})
        ], style={'overflow-x': 'hidden'})
