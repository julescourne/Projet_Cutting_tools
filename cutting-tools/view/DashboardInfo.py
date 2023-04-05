from dash import html, dcc
import dash_bootstrap_components as dbc


class DashboardInfo:
    """class contenant la vue du Dashboard"""

    def __init__(self, data_exp):

        self.data = data_exp

        # Affichage des données du procede
        self.info_procede = dbc.Row([
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Type de procédé", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[2], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='type-procede'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Type d'opération", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[3], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='type-operation'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Assistance", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[4], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='assistance'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Débit mql (ml/h)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[5], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='debit-mql'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Débit cryo (ml/h)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[6], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='debit-cryo'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Emulsion HP (bar)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[7], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='emulsion'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Vc (mm/min)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[8], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='vc'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("fz (mm/dent)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[9], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='fz_mm'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Ap (mm)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[10], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='ap'),
                ], style={"marginRight": "10px", "border-radius": "10px", "background-color": '#ECECEC',
                          'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Engagement (%)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[11], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='engagement'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
        ], style={"display": "flex", 'overflow-y': 'scroll', "white-space": "nowrap", 'height': '110px'})

        # Affichage des données de l'entree à la piece
        self.info_piece = dbc.Row([

            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Type de Matière", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[12], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='type-matiere-piece'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Matière", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[13], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='matiere-piece'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Procédé d'élaboration", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[14], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='procede-elab'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Impression 3D", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[15], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='imp-3d'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Longueur usinée (mm)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[16], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='lg-usine'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Numéro de passe", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[17], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='num-passe'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
        ], style={"display": "flex", "overflow-x": "hidden", "white-space": "nowrap", 'height': '110px'})

        # Affichage des données de l'entree à l'outil'
        self.info_outil = dbc.Row([
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Code produit", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P("", style={'text-align': 'center', 'font-size': '18px',
                                      'font-weight': 'bold'}, id='code-outil'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Type d'outil", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[26], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='type-outil'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Matière outil", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[27], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='matiere-outil'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Diamètre outil", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[28], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='diametre-outil'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Dents utilisées", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[29], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='dents'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Revêtement", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[30], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='revet'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            )
        ], style={"display": "flex", "overflow-x": "hidden", "white-space": "nowrap", 'height': '110px'})

        self.content = html.Div([
            html.Div(
                style={
                    'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'
                },
                children=[
                    html.H2(id='info-title', children="Expérience \'" + self.data[1] + "\'"),
                    html.Div(
                        style={'display': 'flex', 'align-items': 'center', 'margin-right': '30px',
                               "border-radius": "10px",
                               'border': '1px solid #000000', "background-color": '#ECECEC',
                               'width': '20vh', 'height': '10vh',
                               'justify-content': 'center'},
                        children=[
                            html.P("Distance", style={'font-weight': 'bold', 'margin-right': '10px'}),
                            html.P(self.data[len(self.data) - 1])
                        ]
                    )
                ],
            ),

            html.Legend("Procédé", style={'font-family': 'Abang', 'color': 'gray', 'padding': '20px',
                                          'font-size': '20px'}),
            html.Div(id="content-info-procede", children=[self.info_procede]),
            html.Legend("Pièce à usiner",
                        style={'font-family': 'Abang', 'color': 'gray', 'padding': '20px',
                               'font-size': '20px'}),
            html.Div(id="content-info-piece", children=[self.info_piece]),
            html.Legend("Outil d'usinage",
                        style={'font-family': 'Abang', 'color': 'gray', 'padding': '20px',
                               'font-size': '20px'}),
            html.Div(id="content-info-outil", children=[self.info_outil]),
            html.Button("Exporter experience", id="export", n_clicks=0)
        ], className='content', id='content_infos', style={'display': 'block', 'width': '80vh'})
