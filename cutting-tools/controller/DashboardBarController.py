import dash
import numpy as np
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd


class DashboardBarController:
    """
    Classe qui contient les méthodes necessaire à l'utilisation du Dashboard. Le dashboard est une interface plotly
    dash permettant de visualiser les données issues d'une expérience de la base de données.
    """

    def __init__(self, app, dashboard_bar, effort_piece, effort_outil):

        self.app = app
        self.dashboard = dashboard_bar
        self.effort_piece = effort_piece
        self.effort_outil = effort_outil

        # compteurs de clique sur les boutons add et del
        self.cmpt_add_click_bar = 0
        self.cmpt_del_click_bar = 0

        # mode d'affichage du graphique en bar
        self.mode_value = None

        # contenu des dropdown servant pour le chart bar
        self.df_bar = {
            'dropdown-abs': None,
            'dropdown1': None,
            'dropdown2': None,
            'dropdown3': None,
            'dropdown4': None,
            'dropdown5': None,
            'dropdown6': None
        }

        self.update_dropdown_bar_callbacks()
        self.update_dropdown_i_bar_callback(1)
        self.update_dropdown_i_bar_callback(2)
        self.update_dropdown_i_bar_callback(3)
        self.update_dropdown_i_bar_callback(4)
        self.update_dropdown_i_bar_callback(5)
        self.update_dropdown_i_bar_callback(6)
        self.graph_bar_callback()

    def update_dropdown_bar_callbacks(self):
        @self.app.callback(
            Output('var-bar-ord', 'children'),
            Output('dropdown-abs', 'value'),
            Input('btn-add-var-bar-ord', 'n_clicks'),
            Input('btn-del-var-bar-ord', 'n_clicks'),
            Input('dropdown-abs', 'value'),
            State('var-bar-ord', 'children'),
        )
        def update_dropdown(add_clicks, del_clicks, value, children):
            """
            Méthode permettant à l'utilisateur d'ajouter ou effacer des dropdowns pour la partie chart bar.
            :param add_clicks: nombre de cliques du boutton ajouter
            :param del_clicks: nombre de cliques du boutton effacer
            :param value: valeur du dropdown associé à l'abscisse
            :param children: conteneur des dropdowns associé à l'ordonnée.
            :return: children: conteneur des dropdowns associé à l'ordonnée.
            :return: value: valeur du dropdown associé à l'abscisse
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # Ajout d'un dropdown
            if button_id == 'btn-add-var-bar-ord':

                # S'il y a moins de 6 dropdowns (et 3 bouttons)
                if len(children) < 9:

                    # Numero et index du dropdown a ajouter
                    drop_num = add_clicks + 1 - del_clicks + self.cmpt_del_click_bar - self.cmpt_add_click_bar
                    index_add = drop_num - 1

                    # creation du nouveaux dropdown
                    new_dropdown = dbc.Col(
                        dcc.Dropdown(id='dropdown-ord{}'.format(drop_num), options=self.dashboard.ord_values,
                                     style={'background-color': '#ECECEC', 'border-color': 'black',
                                            'font-size': '12px'}),
                        width=2)

                    # Insertion dans le conteneur parent
                    children.insert(index_add, new_dropdown)

                # S'il y a deja 6 dropdowns
                else:
                    self.cmpt_add_click_bar += 1
                    print('Maximum number of dropdowns reached.')

            # Suppression d'un dropdown
            elif button_id == 'btn-del-var-bar-ord':

                # S'il y a au moins deux dropdowns (et 3 bouttons)
                if len(children) >= 5:

                    # Numero et index du dropdown a effacer
                    drop_num = add_clicks + 2 - del_clicks + self.cmpt_del_click_bar - self.cmpt_add_click_bar
                    index_del = drop_num - 1

                    # Mise a jour du conteneur parent
                    children.pop(index_del)

                    # Mise a jour des valeurs du dropdown
                    self.df_bar.update({'dropdown{}'.format(drop_num): None})

                # S'il y a un dropdown
                else:
                    self.cmpt_del_click_bar += 1
                    print('No dropdowns to remove.')

            # Mise a jour de la valeur de l'abscisse
            elif button_id == 'dropdown-abs':
                if value == 1:
                    drop = [t[1] for t in self.effort_piece]
                    self.df_bar['dropdown-abs'] = {'label': 'Temps (s)', 'value': drop}
                if value == 2:
                    drop = [t[2] for t in self.effort_piece]
                    self.df_bar['dropdown-abs'] = {'label': 'Fx pièce (N)', 'value': drop}
                if value == 3:
                    drop = [t[3] for t in self.effort_piece]
                    self.df_bar['dropdown-abs'] = {'label': 'Fy pièce (N)', 'value': drop}
                if value == 4:
                    drop = [t[4] for t in self.effort_piece]
                    self.df_bar['dropdown-abs'] = {'label': 'Fz pièce (N)', 'value': drop}
                if value == 5:
                    drop = [t[2] for t in self.effort_outil]
                    self.df_bar['dropdown-abs'] = {'label': 'Fx outil (N)', 'value': drop}
                if value == 6:
                    drop = [t[3] for t in self.effort_outil]
                    self.df_bar['dropdown-abs'] = {'label': 'Fy outil (N)', 'value': drop}
                if value == 7:
                    drop = [t[4] for t in self.effort_outil]
                    self.df_bar['dropdown-abs'] = {'label': 'Fz outil (N)', 'value': drop}

            return children, value

    def update_dropdown_i_bar_callback(self, index):
        @self.app.callback(
            Output('dropdown-ord{}'.format(index), 'value'),
            [Input('dropdown-ord{}'.format(index), 'value')]
        )
        def update(value):
            """
            Met à jour les dropdowns 2 à 6 pour la partie chart bar. Ces dropdowns peuvent ne pas exister.
            :param value: la valeur du dropdown cliquer par l'utilisateur
            :return: value: la valeur du dropdown cliquer par l'utilisateur
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'dropdown-ord{}'.format(index):
                if value == 1:
                    drop = [t[2] for t in self.effort_piece]
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fx pièce (N)', 'value': drop}})
                if value == 2:
                    drop = [t[3] for t in self.effort_piece]
                    self.df_bar['dropdown{}'.format(index)] = {'label': 'Fy pièce (N)', 'value': drop}
                if value == 3:
                    drop = [t[4] for t in self.effort_piece]
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fz pièce (N)', 'value': drop}})
                if value == 4:
                    drop = [t[2] for t in self.effort_outil]
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fx outil (N)', 'value': drop}})
                if value == 5:
                    drop = [t[3] for t in self.effort_outil]
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fy outil (N)', 'value': drop}})
                if value == 6:
                    drop = [t[4] for t in self.effort_outil]
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fz outil (N)', 'value': drop}})

            return value

    def graph_bar_callback(self):
        @self.app.callback(
            Output('bar-chart', 'style'),
            Output('bar-chart', 'figure'),
            Input('seg-value', 'value'),
            Input('mode-value', 'value'),
            Input('btn-val-var-bar-ord', 'n_clicks'),
            [Input('dropdown-abs', 'value')],
            [State('dropdown-abs', 'options')],
            State('formula', 'value')
        )
        def graph_bar(seg_value, mode_value, val_clicks, value, options, f_value):
            """
            Méthode permettant de créer le chart bar.
            :param mode_value: valeur du mode d'affichage du graphique
            :param val_clicks: nombre de clique sur le boutton valider
            :param value: valeur du dropdown de l'abscisse
            :param options: options pour le dropdown de l'abscisse
            :param f_value: valeur de la formule entrée par l'utilisateur
            :return: html_p : Objet hmtl.P contenant l'erreur associé à la formule
            :return: style : le style du plotly express bar a afficher
            :return: fig : plotly express bar a afficher
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # initialisation du chart bar
            fig = px.bar()

            # initialisation du conteneur de l'erreur associé a la formule
            html_p = html.P('', style={'font-weight': 'bold', 'display': 'inline-block'})

            # Si l'utilisateur clique sur valider
            if button_id == 'btn-val-var-bar-ord':
                # verification que l'utilisateur a bien cliquer sur valider
                if val_clicks > 0:

                    # on récupère le label du dropdown pour l'abscisse
                    label = [o['label'] for o in options if o['value'] == value][0]

                    # initialisation des tableaux qui contienent les données a afficher
                    abscissa = []  # valeurs du choix utilisateurs pour l'abscisse
                    fx_piece = []  # valeurs de l'effort fx a la piece
                    fy_piece = []  # valeurs de l'effort fy a la piece
                    fz_piece = []  # valeurs de l'effort fz a la piece
                    fx_outil = []  # valeurs de l'effort fx a l'outil
                    fy_outil = []  # valeurs de l'effort fy a l'outil
                    fz_outil = []  # valeurs de l'effort fz a l'outil
                    ord_name = ''  # nom de l'ordonnée

                    # Si l'utilisateur veut le temps en abscisse
                    if label == 'Temps (s)':
                        # ajout des valeurs du temps
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)

                    # Si l'utilisateur veut l'effort fx piece en abscisse
                    if label == 'Fx pièce (N)':
                        # ajout des valeurs de fx
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fx piece'

                    # Si l'utilisateur veut l'effort fy piece en abscisse
                    if label == 'Fy pièce (N)':
                        # ajout des valeurs de fy
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fy piece'

                    # Si l'utilisateur veut l'effort fz piece en abscisse
                    if label == 'Fz pièce (N)':
                        # ajout des valeurs de fz
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fz piece'

                    # Si l'utilisateur veut l'effort fx outil en abscisse
                    if label == 'Fx outil (N)':
                        # ajout des valeurs de fx
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fx outil'

                    # Si l'utilisateur veut l'effort fy outil en abscisse
                    if label == 'Fy outil (N)':
                        # ajout des valeurs de fy
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fy outil'

                    # Si l'utilisateur veut l'effort fz outil en abscisse
                    if label == 'Fz outil (N)':
                        # ajout des valeurs de fz
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fz outil'

                    # Pour tous les dropdowns
                    for i in range(1, 6):
                        # Si le dropdown i est associé à une valeur
                        if self.df_bar['dropdown{}'.format(i)] is not None:
                            # Si le dropdown i est associé aux efforts fx a la piece
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fx pièce (N)':
                                # ajout des valeurs fx a la piece
                                fx_piece = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fy a la piece
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fy pièce (N)':
                                # ajout des valeurs fy a la piece
                                fy_piece = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fz a la piece
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fz pièce (N)':
                                # ajout des valeurs fz a la piece
                                fz_piece = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fx a l'outil
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fx outil (N)':
                                # ajout des valeurs fx a l'outil
                                fx_outil = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fy a l'outil
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fy outil (N)':
                                # ajout des valeurs fy a l'outil
                                fy_outil = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fx a l'outil
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fz outil (N)':
                                # ajout des valeurs fz a l'outil
                                fz_outil = self.df_bar['dropdown{}'.format(i)]['value']

                    # nombre de valeurs de l'abscisse
                    size = len(abscissa)

                    # affectation des valeurs du temps
                    temps = [i[1] for i in self.effort_piece]

                    df = pd.DataFrame({})
                    # S'il y a au moins une valeur en abscisse
                    if size > 0:
                        # Si l'utilisateur est en mode moyenne des valeurs.
                        if mode_value == 1:
                            # Si l'abscisse est le temps
                            if label == 'Temps (s)':
                                # Si le nombre de valeurs de l'ordonnée est egale au nombre de valeurs de l'abscisse
                                # si l'ordonnee est fx piece
                                if len(fx_piece) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fx pour chaque seconde
                                    df['fx piece{}'.format(ord_name)] = self.get_mean(fx_piece, temps, seg_value)[0]
                                # si l'ordonnee est fy piece
                                if len(fy_piece) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fy pour chaque seconde
                                    df['fy piece{}'.format(ord_name)] = self.get_mean(fy_piece, temps, seg_value)[0]
                                # si l'ordonnee est fz piece
                                if len(fz_piece) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fz pour chaque seconde
                                    df['fz piece{}'.format(ord_name)] = self.get_mean(fz_piece, temps, seg_value)[0]
                                # si l'ordonnee est fx outil
                                if len(fx_outil) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fx pour chaque seconde
                                    df['fx outil{}'.format(ord_name)] = self.get_mean(fx_outil, temps, seg_value)[0]
                                # si l'ordonnee est fy outil
                                if len(fy_outil) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fy pour chaque seconde
                                    df['fy outil{}'.format(ord_name)] = self.get_mean(fy_outil, temps, seg_value)[0]
                                # si l'ordonnee est fz outil
                                if len(fz_outil) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fz pour chaque seconde
                                    df['fz outil{}'.format(ord_name)] = self.get_mean(fz_outil, temps, seg_value)[0]

                            # Si l'abscisse n'est pas le temps
                            else:
                                # si l'ordonnee est fx piece
                                if len(fx_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fx = [round(fx / abs, 4) for fx, abs in zip(fx_piece, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fx piece{}'.format(ord_name)] = self.get_mean(fx, temps, seg_value)[0]

                                # si l'ordonnee est fy piece
                                if len(fy_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fy = [round(fy / abs, 4) for fy, abs in zip(fy_piece, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fy piece{}'.format(ord_name)] = self.get_mean(fy, temps, seg_value)[0]

                                # si l'ordonnee est fz piece
                                if len(fz_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fz = [round(fz / abs, 4) for fz, abs in zip(fz_piece, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fz piece{}'.format(ord_name)] = self.get_mean(fz, temps, seg_value)[0]

                                # si l'ordonnee est fx outil
                                if len(fx_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fx = [round(fx / abs, 4) for fx, abs in zip(fx_outil, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fx outil{}'.format(ord_name)] = self.get_mean(fx, temps, seg_value)[0]

                                # si l'ordonnee est fy outil
                                if len(fy_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fy = [round(fy / abs, 4) for fy, abs in zip(fy_outil, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fy outil{}'.format(ord_name)] = self.get_mean(fy, temps, seg_value)[0]

                                # si l'ordonnee est fz outil
                                if len(fz_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fz = [round(fz / abs, 4) for fz, abs in zip(fz_outil, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fz outil{}'.format(ord_name)] = self.get_mean(fz, temps, seg_value)[0]

                        # si le mode est 'maximum'
                        elif mode_value == 2:
                            # Si l'abscisse est le temps
                            if label == 'Temps (s)':
                                # Si le nombre de valeurs de l'ordonnée est egale au nombre de valeurs de l'abscisse
                                # si l'ordonnee est fx piece
                                if len(fx_piece) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fx piece{}'.format(ord_name)] = self.get_max(fx_piece, temps, seg_value)[0]
                                # si l'ordonnee est fy piece
                                if len(fy_piece) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fy piece{}'.format(ord_name)] = self.get_max(fy_piece, temps, seg_value)[0]
                                # si l'ordonnee est fz piece
                                if len(fz_piece) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fz piece{}'.format(ord_name)] = self.get_max(fz_piece, temps, seg_value)[0]
                                # si l'ordonnee est fx outil
                                if len(fx_outil) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fx outil{}'.format(ord_name)] = self.get_max(fx_outil, temps, seg_value)[0]
                                # si l'ordonnee est fy outil
                                if len(fy_outil) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fy outil{}'.format(ord_name)] = self.get_max(fy_outil, temps, seg_value)[0]
                                # si l'ordonnee est fz outil
                                if len(fz_outil) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fz outil{}'.format(ord_name)] = self.get_max(fz_outil, temps, seg_value)[0]

                            # si l'abscisse n'est pas le temps
                            else:
                                # si l'ordonnee est fx piece
                                if len(fx_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fx = [round(fx / abs, 4) for fx, abs in zip(fx_piece, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fx piece{}'.format(ord_name)] = self.get_max(fx, temps, seg_value)[0]
                                # si l'ordonnee est fy piece
                                if len(fy_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fy = [round(fy / abs, 4) for fy, abs in zip(fy_piece, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fy piece{}'.format(ord_name)] = self.get_max(fy, temps, seg_value)[0]
                                # si l'ordonnee est fz piece
                                if len(fz_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fz = [round(fz / abs, 4) for fz, abs in zip(fz_piece, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fz piece{}'.format(ord_name)] = self.get_max(fz, temps, seg_value)[0]
                                # si l'ordonnee est fx outil
                                if len(fx_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fx = [round(fx / abs, 4) for fx, abs in zip(fx_outil, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fx outil{}'.format(ord_name)] = self.get_max(fx, temps, seg_value)[0]
                                # si l'ordonnee est fy outil
                                if len(fy_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fy = [round(fy / abs, 4) for fy, abs in zip(fy_outil, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fy outil{}'.format(ord_name)] = self.get_max(fy, temps, seg_value)[0]
                                # si l'ordonnee est fz outil
                                if len(fz_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fz = [round(fz / abs, 4) for fz, abs in zip(fz_outil, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fz outil{}'.format(ord_name)] = self.get_max(fz, temps, seg_value)[0]

                        # on stocke chaque seconde
                        df['temps'] = self.get_mean([1 for i in range(size)], temps, seg_value)[1]

                        # conteneur des nom des colonnes (abscisse et ordonnée)
                        traces = ['temps']
                        for col in df.columns:
                            if col != 'temps':
                                traces.append(col)

                        # Si la formule n'est pas vide ou egale à sa valeur initial
                        if f_value != '' and f_value != 'sqrt(y), ..':
                            try:
                                # pour toutes les colonnes
                                for tr in traces:
                                    result = []
                                    if tr != 'temps':
                                        # pour toutes les valeurs associé à la colonne
                                        for f in df[tr]:
                                            f = str(f)
                                            # on stocke le résultat de la formule avec la valeur
                                            result.append(eval(f_value.replace('(y', '(' + f)))
                                        df[tr] = result

                                # # Construction du chart abr
                                fig = px.bar(df, x='temps', y=traces)


                                # affectation des labels associés aux axes
                                fig.update_xaxes(title='Temps (s)')
                                fig.update_yaxes(title='Efforts (N)')

                                return {'width': '100%', 'display': 'flex'}, fig

                            except Exception as e:
                                # affichage de l'erreur

                                return {'width': '100%', 'display': 'flex'}, fig

                        # creation du bar chart
                        fig = px.bar(df, x='temps', y=traces)

                        fig.update_xaxes(title='Temps (s)')
                        fig.update_yaxes(title='Efforts (N)')

                return {'width': '100%', 'display': 'flex'}, fig
            return [{'width': '100%', 'display': 'None'}, fig]

    def get_mean(self, list_effort, list_temps, segment):
        """
        Calcul la moyenne des efforts pour une seconde. Permet d'avoir un graph lisible en vue du grand
        nombre de données.
        :param list_effort: liste des valeurs des efforts
        :param list_temps: liste des valeurs du temps
        :return: liste moyennes des efforts, liste de chaque secondes
        """
        temps = np.array(list_temps)
        effort = np.array(list_effort)

        if segment == 'second':
            int_temps = temps.astype(int)
            unique_temps, indices = np.unique(int_temps, return_inverse=True)
            effort_mean = np.bincount(indices, weights=effort) / np.bincount(indices)
        elif segment == 'decisecond':
            int_temps = (temps * 10).astype(int)
            unique_temps, indices = np.unique(int_temps, return_inverse=True)
            unique_temps = unique_temps / 10
            effort_mean = np.bincount(indices, weights=effort) / np.bincount(indices)
        elif segment == 'centisecond':
            int_temps = (temps * 100).astype(int)
            unique_temps, indices = np.unique(int_temps, return_inverse=True)
            unique_temps = unique_temps / 100
            effort_mean = np.bincount(indices, weights=effort) / np.bincount(indices)
        elif segment == 'millisecond':
            int_temps = (temps * 1000).astype(int)
            unique_temps, indices = np.unique(int_temps, return_inverse=True)
            unique_temps = unique_temps / 1000
            effort_mean = np.bincount(indices, weights=effort) / np.bincount(indices)
        return effort_mean.tolist(), unique_temps.tolist()

    def get_max(self, list_effort, list_temps, segment):
        """
        Calcul du max (ou min si abs(min) > abs(max)) des efforts pour une seconde.
        Permet d'avoir une courbe lisible en vue du grand nombre de données.
        :param list_effort: liste des valeurs des efforts
        :param list_temps: liste des valeurs du temps
        :return: liste max des efforts, liste de chaque secondes
        """
        temps = np.array(list_temps)
        effort = np.array(list_effort)
        unique_temps = None
        if segment == 'second':
            int_temps = temps.astype(int)
            temps_unique = np.unique(int_temps)
            effort_mean = np.zeros(len(temps_unique))
            for iu, t in enumerate(temps_unique):
                indices = np.where(int_temps == t)[0]
                effort_mean[iu] = np.max(effort[indices]) if abs(np.max(effort[indices])) > abs(
                    np.min(effort[indices])) else np.min(effort[indices])
        elif segment == 'decisecond':
            int_temps = (temps * 10).astype(int)
            unique_temps, indices = np.unique(int_temps, return_inverse=True)
            unique_temps = unique_temps / 10
            for iu, t in enumerate(unique_temps):
                indices = np.where(int_temps == t)[0]
                unique_temps[iu] = np.max(effort[indices]) if abs(np.max(effort[indices])) > abs(
                    np.min(effort[indices])) else np.min(effort[indices])
        elif segment == 'centisecond':
            int_temps = (temps * 100).astype(int)
            unique_temps, indices = np.unique(int_temps, return_inverse=True)
            unique_temps = unique_temps / 100
            for iu, t in enumerate(unique_temps):
                indices = np.where(int_temps == t)[0]
                unique_temps[iu] = np.max(effort[indices]) if abs(np.max(effort[indices])) > abs(
                    np.min(effort[indices])) else np.min(effort[indices])
        elif segment == 'millisecond':
            int_temps = (temps * 1000).astype(int)
            unique_temps, indices = np.unique(int_temps, return_inverse=True)
            unique_temps = unique_temps / 1000
            for iu, t in enumerate(unique_temps):
                indices = np.where(int_temps == t)[0]
                unique_temps[iu] = np.max(effort[indices]) if abs(np.max(effort[indices])) > abs(
                    np.min(effort[indices])) else np.min(effort[indices])

        return effort_mean.tolist(), temps_unique.tolist()
