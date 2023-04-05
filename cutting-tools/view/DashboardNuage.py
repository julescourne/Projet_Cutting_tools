from dash import html, dcc
import dash_bootstrap_components as dbc


class DashboardNuage:
    """class contenant la vue du Dashboard"""

    def __init__(self, data_exp):
        self.data_exp = data_exp

        # valeurs du dropdown pour l'abscisse pour le line chart
        self.abscisse_values = [
            {'label': 'Temps (s)', 'value': 1},
            {'label': 'Fx pièce (N)', 'value': 2},
            {'label': 'Fy pièce (N)', 'value': 3},
            {'label': 'Fz pièce (N)', 'value': 4},
            {'label': 'Fx outil (N)', 'value': 5},
            {'label': 'Fy outil (N)', 'value': 6},
            {'label': 'Fz outil (N)', 'value': 7}
        ]

        # valeurs des dropdowns pour l'ordonnée pour le line chart
        self.ord_values = [
            {'label': 'Fx pièce (N)', 'value': 1},
            {'label': 'Fy pièce (N)', 'value': 2},
            {'label': 'Fz pièce (N)', 'value': 3},
            {'label': 'Fx outil (N)', 'value': 4},
            {'label': 'Fy outil (N)', 'value': 5},
            {'label': 'Fz outil (N)', 'value': 6}
        ]

        self.nuage_abs_var = dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='dropdown-abs-nuage', options=self.abscisse_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2)
        ], justify='left', id='var-nuage-abs')

        self.nuage_ord_var = dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='dropdown-nuage-ord1', options=self.ord_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(dbc.Button("Ajouter", id='btn-add-var-nuage-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button("Effacer", id='btn-del-var-nuage-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button("Valider", id='btn-val-var-nuage-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1)
        ], justify='left', id='var-nuage-ord')

        self.content = html.Div([
            html.H2(id='Nuage-title', children="Visualisation en Nuage de points", style={'margin-bottom': '20px'}),
            html.H2(id='sub-title-abs-nuage', children="Choix de l'abscisse", style={'font-size': '12px'}),
            html.Div(id="content-nuage-container-abs", children=[self.nuage_abs_var], style={'margin-bottom': '20px'}),
            html.H2(id='sub-title-ord-nuage', children="Choix des ordonnées", style={'font-size': '12px'}),
            html.Div(id="content-nuage-container-ord", children=[self.nuage_ord_var], style={'margin-bottom': '20px'}),
            dcc.Graph(id='nuage-chart', style={'width': '100%'}),
        ], className='content', id='content_nuage', style={'display': 'none', 'height': '140vh'})
