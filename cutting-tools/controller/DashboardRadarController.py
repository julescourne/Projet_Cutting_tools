import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go


class DashboardRadarController:
    """
    Classe qui contient les méthodes necessaire à l'utilisation du Dashboard. Le dashboard est une interface plotly
    dash permettant de visualiser les données issues d'une expérience de la base de données.
    """

    def __init__(self, app, dashboard_radar):

        self.dashboard = dashboard_radar
        self.app = app

        # conteneur des paramètres remplis par l'utilisateur
        self.user_data = self.dashboard.data_usr
        self.data_exp = self.dashboard.data

        # nombre initial de dropdown pour le chart radar
        self.nb_drop = 4

        self.cmpt_add_click_radar = 0
        self.cmpt_del_click_radar = 0

        # contenu des dropdown servant pour le radar chart
        self.df_radar = {
            'dropdown1': None,
            'dropdown2': None,
            'dropdown3': None,
            'dropdown4': None,
            'dropdown5': None,
            'dropdown6': None,
            'dropdown7': None,
            'dropdown8': None
        }

        self.update_dropdown_radar_callbacks()
        self.update_dropdown_i_radar_callback(5)
        self.update_dropdown_i_radar_callback(6)
        self.update_dropdown_i_radar_callback(7)
        self.update_dropdown_i_radar_callback(8)
        self.update_radar_callbacks()

    def update_dropdown_radar_callbacks(self):
        @self.app.callback(
            Output('var-radar', 'children'),
            Input('btn-add-var-radar', 'n_clicks'),
            Input('btn-del-var-radar', 'n_clicks'),
            State('var-radar', 'children'),
            Input('dropdown1', 'value'),
            Input('dropdown2', 'value'),
            Input('dropdown3', 'value'),
            Input('dropdown4', 'value')
        )
        def update_dropdown(add_clicks, del_clicks, children, drop_1, drop_2, drop_3, drop_4):
            """
            Méthode permettant à l'utilisateur d'ajouter ou effacer des dropdowns pour la partie chart radar.
            :param add_clicks: nombre de cliques du boutton ajouter
            :param del_clicks: nombre de cliques du boutton Effacer
            :param children: Conteneur des dropdowns
            :param drop_1: valeur du dropdown 1
            :param drop_2: valeur du dropdown 2
            :param drop_3: valeur du dropdown 3
            :param drop_4: valeur du dropdown 4
            :return: Conteneur des dropdowns
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # Ajout d'un dropdown
            if button_id == 'btn-add-var-radar':

                # s'il n'y a pas plus de 8 dropdowns (et 3 bouttons)
                if len(children) < 11:

                    # numero et index du dernier dropdown
                    drop_num = add_clicks + 4 - del_clicks - self.cmpt_add_click_radar + self.cmpt_del_click_radar
                    index_add = drop_num - 1

                    # Creation du dropdown a ajouter
                    new_dropdown = dbc.Col(
                        dcc.Dropdown(id='dropdown{}'.format(drop_num), options=self.dashboard.dropdown_values,
                                     style={'background-color': '#ECECEC', 'border-color': 'black',
                                            'font-size': '12px'}),
                        width=2)

                    # insertion du dropdown a l'index dans le conteneur parent
                    children.insert(index_add, new_dropdown)

                    return children

                # S'il y a deja 8 dropdown
                else:
                    self.cmpt_add_click_radar += 1
                    print('Maximum number of dropdowns reached.')

            # Suppression d'un dropdown
            elif button_id == 'btn-del-var-radar':

                # S'il y a plus de 4 dropdowns
                if len(children) >= 8:

                    # numero et index du dropdown a supprimer
                    drop_num = add_clicks + 5 - del_clicks - self.cmpt_add_click_radar + self.cmpt_del_click_radar
                    index_del = drop_num - 1

                    # suppression du dropdown a l'index
                    children.pop(index_del)

                    # On efface les valeurs associé à ce dropdown
                    self.df_radar['dropdown{}'.format(drop_num)] = None

                    return children

                # S'il y a 4 dropdown
                else:
                    self.cmpt_del_click_radar += 1
                    print('No dropdowns to remove.')

            elif button_id == 'dropdown1':
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop_1), None)
                if option:
                    self.df_radar['dropdown1'] = option

            elif button_id == 'dropdown2':
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop_2), None)
                if option:
                    self.df_radar['dropdown2'] = option

            elif button_id == 'dropdown3':
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop_3), None)
                if option:
                    self.df_radar['dropdown3'] = option

            elif button_id == 'dropdown4':
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop_4), None)
                if option:
                    self.df_radar['dropdown4'] = option

            return children

    def update_dropdown_i_radar_callback(self, index):
        @self.app.callback(
            Output('dropdown{}'.format(index), 'value'),
            [Input('dropdown{}'.format(index), 'value')]
        )
        def update(drop):
            """
            Met à jour les dropdowns 5 à 8 pour la partie chart radar. Ces dropdowns peuvent ne pas exister.
            :param drop: la valeur du dropdown cliquer par l'utilisateur
            :return: drop: la valeur du dropdown cliquer par l'utilisateur
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'dropdown{}'.format(index):
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop), None)
                if option:
                    self.df_radar['dropdown{}'.format(index)] = option

            return drop

    def update_radar_callbacks(self):
        @self.app.callback(
            Output('total-value', 'children'),
            Output('near-value', 'children'),
            Output('far-value', 'children'),
            Output('radar-chart', 'style'),
            Output('radar-chart', 'figure'),
            Input('btn-val-var-radar', 'n_clicks')
        )
        def update_graph(val_click):
            """
            Construit le chart radar et met a jour les informations sur ce graphe
            :param val_click: nombre de cliques du boutton valider
            :return: le pourcentage total, la distance la plus courte et la plus eloigné
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # intialisation de la figure
            fig = go.Figure()

            # Si on clique sur valider
            if button_id == 'btn-val-var-radar' and val_click > 0:

                # initialisation des liste de valeurs
                labels_exp = []  # valeurs des labels des paramètres
                vals_exp = []  # valeurs des paramètres de l'experience
                vals_usr = []  # valeurs des paramètres voulus par l'utilisateur
                usr_df = []  # valeurs normées des paramètres voulus par l'utilisateur
                exp_df = []  # valeurs normées des paramètres de l'experience
                hover_data_exp = []
                hover_data_usr = []

                # initialisation des variables pour les informations du chart radar
                near_value = 99999999  # contient la valeur la plus proche entre experience et utilisateur
                str_near = ''
                far_value = 0  # contient la valeur la plus eloigne entre experience et utilisateur
                str_far = ''
                total_value = 0  # contient le total de ressemblance entre experience et utilisateur

                # pour tous les valeurs de dropdowns
                for i in range(1, len(self.df_radar)):
                    index = 'dropdown{}'.format(i)
                    # Si le dropdown a un selection
                    if self.df_radar[index] is not None and self.df_radar[index]['value'] is not None:
                        # Si la selection du dropdown est un choix utilisateur
                        label = self.map_datas(self.df_radar[index]['label'])
                        if label in self.user_data.keys():
                            if label == 'contraintes_residuelles':
                                hover_data_exp.append('Contraintes résiduelles max = ' + str(
                                    float(self.df_radar[index]['value'])) + ' MPa')
                                hover_data_usr.append('Contraintes résiduelles max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' MPa')
                            if label == 'durete':
                                hover_data_exp.append(
                                    'Dureté max = ' + str(float(self.df_radar[index]['value'])) + ' Hv')
                                hover_data_usr.append('Dureté max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' Hv')
                            if label == 'fatigue':
                                hover_data_exp.append(
                                    'Fatigue max = ' + str(float(self.df_radar[index]['value'])) + ' MPa')
                                hover_data_usr.append('Fatigue max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' MPa')
                            if label == 'rugosite':
                                hover_data_exp.append(
                                    'Rugosité max = ' + str(float(self.df_radar[index]['value'])) + ' µm')
                                hover_data_usr.append('Rugosité max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' µm')
                            if label == 'fx':
                                hover_data_exp.append('Effort Fx max à la dent = ' + str(
                                    float(self.df_radar[index]['value'])) + ' Newton')
                                hover_data_usr.append('Effort Fx max à la dent = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' Newton')
                            if label == 'fy':
                                hover_data_exp.append('Effort Fy max à la dent = ' + str(
                                    float(self.df_radar[index]['value'])) + ' Newton')
                                hover_data_usr.append('Effort Fy max à la dent = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' Newton')
                            if label == 'fz':
                                hover_data_exp.append('Effort Fz max à la dent = ' + str(
                                    float(self.df_radar[index]['value'])) + ' Newton')
                                hover_data_usr.append('Effort Fz max à la dent = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' Newton')
                            if label == 'temperature':
                                hover_data_exp.append(
                                    'Température max à la pièce = ' + str(float(self.df_radar[index]['value'])) + ' °C')
                                hover_data_usr.append('Température max à la pièce = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' °C')
                            if label == 'longueur_usine':
                                hover_data_exp.append(
                                    'Longueur usiné = ' + str(float(self.df_radar[index]['value'])) + ' mm')
                                hover_data_usr.append('Longueur usiné = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' mm')
                            if label == 'amplitude':
                                hover_data_exp.append(
                                    'Amplitude de fréquence max = ' + str(float(self.df_radar[index]['value'])))
                                hover_data_usr.append('Amplitude de fréquence max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])))

                            labels_exp.append(self.df_radar[index]['label'])
                            vals_exp.append(float(self.df_radar[index]['value']))
                            vals_usr.append(float(self.user_data[self.map_datas(self.df_radar[index]['label'])]))

                # On norme chaque valeur
                for i, j in zip(vals_usr, vals_exp):
                    if (i + j) != 0:
                        usr_df.append(i / (i + j))
                        exp_df.append(j / (i + j))
                    else:
                        usr_df.append(0)
                        exp_df.append(0)

                # On calcul la variable eloigne
                for i, j, p in zip(usr_df, exp_df, vals_exp):
                    if i > j:
                        if far_value < i - j:
                            far_value = i - j
                            str_far = labels_exp[vals_exp.index(p)]
                    if i < j:
                        if far_value < j - i:
                            far_value = j - i
                            str_far = labels_exp[vals_exp.index(p)]

                # On calcul la variable la plus proche
                for i, j, p in zip(usr_df, exp_df, vals_exp):
                    if i > j:
                        if near_value > i - j:
                            near_value = i - j
                            str_near = labels_exp[vals_exp.index(p)]
                    if i < j:
                        if near_value > j - i:
                            near_value = j - i
                            str_near = labels_exp[vals_exp.index(p)]

                # On calcul le total
                for i, j in zip(usr_df, exp_df):
                    if i > j:
                        if i != 0:
                            total_value += j / i
                        else:
                            total_value += 0
                    elif i < j:
                        if j != 0:
                            total_value += i / j
                        else:
                            total_value += 0
                    else:
                        total_value += 1

                if len(usr_df) != 0:
                    total_value = abs(total_value)
                    total_value /= len(usr_df)
                    total_value = round(total_value * 100, 2)
                else:
                    total_value = 0

                # creation de la trace experience
                fig.add_trace(go.Scatterpolar(
                    r=exp_df,
                    theta=labels_exp,
                    fill='toself',
                    name='Expérience proche',
                    customdata=hover_data_exp
                ))

                # creation de la trace utilisateur
                fig.add_trace(
                    go.Scatterpolar(
                        r=usr_df,
                        theta=labels_exp,
                        fill='toself',
                        name='Choix utilisateur',
                        customdata=hover_data_usr
                    )
                )

                fig.update_traces(
                    hovertemplate='%{customdata}'
                )

                # mis a jour du layout
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                        )),
                    showlegend=True
                )

                return html.P(f'{total_value}%', style={'margin': '0px', 'display': 'inline-block'}), \
                       html.P(f'{str_near}', style={'margin': '0px', 'display': 'inline-block'}), \
                       html.P(f'{str_far}', style={'margin': '0px', 'display': 'inline-block'}), \
                       {'width': '70vh', 'height': '60vh', 'display': 'flex'}, fig

            return html.P('', style={'margin': '0px', 'display': 'inline-block'}), \
                   html.P('', style={'margin': '0px', 'display': 'inline-block'}), \
                   html.P('', style={'margin': '0px', 'display': 'inline-block'}), \
                   {'width': '70vh', 'height': '60vh', 'display': 'none'}, fig

    def map_datas(self, label):
        """
        Fonction qui mappe le label des dropdowns avec le label des valeurs rempli par l'utilisateur
        :param label: label du dropdown
        :return: string représentant le label
        """
        if label == 'Contraintes max':
            return 'contraintes_residuelles'
        if label == 'Dureté max':
            return 'durete'
        if label == 'Fatigue max':
            return 'fatigue'
        if label == 'Ra max':
            return 'rugosite'
        if label == 'Fx dent max':
            return 'fx'
        if label == 'Fy dent max':
            return 'fy'
        if label == 'Fz dent max':
            return 'fz'
        if label == 'Température pièce max':
            return 'temperature'
        if label == 'Longueur usinée':
            return 'longueur_usine'
        if label == 'Amplitude':
            return 'amplitude'
        return None
