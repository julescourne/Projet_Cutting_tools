from dash import html, dcc
import dash_bootstrap_components as dbc


class DashboardBar:
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

        self.modes_bar = [
            {'label': 'Moyenne', 'value': 1},
            {'label': 'Maximum', 'value': 2},
        ]

        self.segment = [
            {'label': 'second', 'value': 'second'},
            {'label': 'decisecond', 'value': 'decisecond'},
            {'label': 'centisecond', 'value': 'centisecond'},
            {'label': 'millisecond', 'value': 'millisecond'},
        ]

        # dropdown pour l'abscisse du line chart
        self.bar_abs_var = dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='dropdown-abs', options=self.abscisse_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2)
        ], justify='left', id='var-bar-abs')

        # dropdowns pour l'ordonnée du line chart
        self.bar_ord_var = dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='dropdown-ord1', options=self.ord_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(dbc.Button("Ajouter", id='btn-add-var-bar-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button("Effacer", id='btn-del-var-bar-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button("Valider", id='btn-val-var-bar-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1)
        ], justify='left', id='var-bar-ord')

        self.content = html.Div([
            html.H2(id='bar-title', children="Visualisation en Bar", style={'margin-bottom': '20px'}),
            html.H2(id='sub-title-abs', children="Choix de l'abscisse", style={'font-size': '12px'}),
            html.Div(id="content-bar-container-abs", children=[self.bar_abs_var], style={'margin-bottom': '20px'}),
            html.H2(id='sub-title-ord', children="Choix des ordonnées", style={'font-size': '12px'}),
            html.Div(id="content-bar-container-ord", children=[self.bar_ord_var], style={'margin-bottom': '20px'}),
            html.Div([
                html.Div([
                    html.P("Segmentation ", style={'font-weight': 'bold', 'display': 'inline-block'}),
                ]),
                html.Div([
                    dcc.Dropdown(id='seg-value', options=self.segment, style={'display': 'inline-block', 'padding-left': '2vh', 'width': '30vh'})
                ]),
                html.Div([
                    html.P("Mode ", style={'font-weight': 'bold', 'display': 'inline-block'}),
                ]),
                html.Div([
                    dcc.Dropdown(id='mode-value', options=self.modes_bar, style={'display': 'inline-block', 'padding-left': '2vh', 'width': '30vh'})
                ]),
                html.Div([
                    html.P("Formule", style={'font-weight': 'bold', 'display': 'inline-block'}),
                ]),
                html.Div([
                    dcc.Textarea(id='formula', value='sqrt(y), ..',style={'width': '40vh', 'display': 'inline-block', 'padding-left': '2vh'}),
                ])
            ], id='info-mode', style={
                'position': 'relative',
                'top': '10px',
                'height': '10vh',
                'width': '100%',
                'padding': '10px',
                'background-color': '#f9f9f9',
                'border': '1px solid #d3d3d3',
                'border-radius': '5px',
                'display': 'flex',
                'flex-direction': 'row',
                'justify-content': 'space-between',
                'align-items': 'center',
                'flex-wrap': 'wrap'
            }),
            dcc.Graph(id='bar-chart', style={'width': '100%'}),
            ], className='content', id='content_bar', style={'display': 'none', 'height': '140vh'})
