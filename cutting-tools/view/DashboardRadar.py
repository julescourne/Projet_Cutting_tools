from dash import html, dcc
import dash_bootstrap_components as dbc


class DashboardRadar:
    """class contenant la vue du Dashboard"""

    def __init__(self, data_exp, data_usr):

        self.data = data_exp

        self.data_usr = data_usr

        # valeurs des dropdown pour le chart radar
        self.dropdown_values = []

        if 'contraintes_residuelles' in data_usr and eval(self.data[25]) is not None:
            self.dropdown_values.append({'label': 'Contraintes max', 'value': self.data[25]})
        if 'durete' in data_usr and eval(self.data[23]) is not None:
            self.dropdown_values.append({'label': 'Dureté max', 'value': self.data[23]})
        if 'fatigue' in data_usr and eval(self.data[24]) is not None:
            self.dropdown_values.append({'label': 'Fatigue max', 'value': self.data[24]})
        if 'rugosite' in data_usr and eval(self.data[22]) is not None:
            self.dropdown_values.append({'label': 'Ra max', 'value': self.data[22]})
        if 'fx' in data_usr and eval(self.data[31]) is not None:
            self.dropdown_values.append({'label': 'Fx dent max', 'value': self.data[31]})
        if 'fy' in data_usr and eval(self.data[32]) is not None:
            self.dropdown_values.append({'label': 'Fy dent max', 'value': self.data[32]})
        if 'fz' in data_usr and eval(self.data[33]) is not None:
            self.dropdown_values.append({'label': 'Fz dent max', 'value': self.data[33]})
        if 'temperature' in data_usr and eval(self.data[21]) is not None:
            self.dropdown_values.append({'label': 'Température pièce max', 'value': self.data[21]})
        if 'longueur_usine' in data_usr and eval(self.data[16]) is not None:
            self.dropdown_values.append({'label': 'Longueur usinée', 'value': self.data[16]})
        if 'amplitude' in data_usr and eval(self.data[len(self.data) - 2]) is not None:
            self.dropdown_values.append({'label': 'Amplitude', 'value': self.data[len(self.data) - 2]})

        # dropdowns pour le radar chart
        self.radar_var = dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='dropdown1', options=self.dropdown_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(
                dcc.Dropdown(id='dropdown2', options=self.dropdown_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(
                dcc.Dropdown(id='dropdown3', options=self.dropdown_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(
                dcc.Dropdown(id='dropdown4', options=self.dropdown_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(dbc.Button('Ajouter', id='btn-add-var-radar', n_clicks=0, outline=True, className='mr-2',
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button('Effacer', id='btn-del-var-radar', n_clicks=0, outline=True, className='mr-2',
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button("Valider", id='btn-val-var-radar', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1)
        ], justify='left', id='var-radar')

        self.content = html.Div([
            html.H2(id='title', children="Visualisation en radar", style={'margin-bottom': '20px'}),
            html.H2(id='sub-title-radar', children="Choix des paramètres", style={'font-size': '12px'}),
            html.Div(id="content-radar-container", children=[self.radar_var]),
            dcc.Graph(id='radar-chart', style={'width': '70vh', 'height': '50vh', 'display': 'none'}),
            html.Div([
                html.Div([
                    html.P("Total:", style={'font-weight': 'bold', 'display': 'inline-block'}),
                    html.P(id='total-value', style={'margin': '0px', 'display': 'inline-block', 'padding-left': '10px'})
                ]),
                html.Div([
                    html.P("Variable proche:", style={'font-weight': 'bold', 'display': 'inline-block'}),
                    html.P(id='near-value', style={'margin': '0px', 'display': 'inline-block', 'padding-left': '10px'})
                ]),
                html.Div([
                    html.P("Variable éloigné:", style={'font-weight': 'bold', 'display': 'inline-block'}),
                    html.P(id='far-value', style={'margin': '0px', 'display': 'inline-block', 'padding-left': '10px'})
                ])
            ], id='info-radar', style={
                'position': 'absolute',
                'top': '30vh',
                'right': '20vh',
                'height': '40vh',
                'width': '50vh',
                'padding': '20px',
                'background-color': '#f9f9f9',
                'border': '1px solid #d3d3d3',
                'border-radius': '5px'
            })
        ], className='content', id='content_radar', style={'display': 'none'})
