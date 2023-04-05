import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

class DashboardNuageController:
    """
    Classe qui contient les méthodes necessaire à l'utilisation du Dashboard. Le dashboard est une interface plotly
    dash permettant de visualiser les données issues d'une expérience de la base de données.
    """

    def __init__(self, app, dashboard_nuage, effort_piece, effort_outil):

        self.app = app
        self.dashboard = dashboard_nuage
        self.effort_piece = effort_piece
        self.effort_outil = effort_outil

        self.cmpt_add_click_nuage = 0
        self.cmpt_del_click_nuage = 0

        self.df_nuage = {
            'dropdown-abs': None,
            'dropdown1': None,
            'dropdown2': None,
            'dropdown3': None,
            'dropdown4': None,
            'dropdown5': None,
            'dropdown6': None
        }

        self.update_dropdown_nuage_callbacks()
        self.update_dropdown_i_nuage_callback(1)
        self.update_dropdown_i_nuage_callback(2)
        self.update_dropdown_i_nuage_callback(3)
        self.update_dropdown_i_nuage_callback(4)
        self.update_dropdown_i_nuage_callback(5)
        self.update_dropdown_i_nuage_callback(6)

    def update_dropdown_nuage_callbacks(self):
        @self.app.callback(
            Output('var-nuage-ord', 'children'),
            Output('dropdown-abs-nuage', 'value'),
            Input('btn-add-var-nuage-ord', 'n_clicks'),
            Input('btn-del-var-nuage-ord', 'n_clicks'),
            Input('dropdown-abs-nuage', 'value'),
            State('var-nuage-ord', 'children'),
        )
        def update_dropdown(add_clicks, del_clicks, value, children):

            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # Ajout d'un dropdown
            if button_id == 'btn-add-var-nuage-ord':

                # S'il y a moins de 6 dropdowns (et 3 bouttons)
                if len(children) < 9:

                    # Numero et index du dropdown a ajouter
                    drop_num = add_clicks + 1 - del_clicks + self.cmpt_del_click_nuage - self.cmpt_add_click_nuage
                    index_add = drop_num - 1

                    # creation du nouveaux dropdown
                    new_dropdown = dbc.Col(
                        dcc.Dropdown(id='dropdown-nuage-ord{}'.format(drop_num), options=self.dashboard.ord_values,
                                     style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                        width=2)

                    # Insertion dans le conteneur parent
                    children.insert(index_add, new_dropdown)

                # S'il y a deja 6 dropdowns
                else:
                    self.cmpt_add_click_nuage += 1
                    print('Maximum number of dropdowns reached.')

            # Suppression d'un dropdown
            elif button_id == 'btn-del-var-nuage-ord':

                # S'il y a au moins deux dropdowns (et 3 bouttons)
                if len(children) >= 5:

                    # Numero et index du dropdown a effacer
                    drop_num = add_clicks + 2 - del_clicks + self.cmpt_del_click_nuage - self.cmpt_add_click_nuage
                    index_del = drop_num - 1

                    # Mise a jour du conteneur parent
                    children.pop(index_del)

                    # Mise a jour des valeurs du dropdown
                    self.df_nuage.update({'dropdown{}'.format(drop_num): None})

                # S'il y a un dropdown
                else:
                    self.cmpt_del_click_nuage += 1
                    print('No dropdowns to remove.')

            # Mise a jour de la valeur de l'abscisse
            elif button_id == 'dropdown-abs':
                if value == 1:
                    drop = [t[1] for t in self.effort_piece]
                    self.df_nuage['dropdown-abs'] = {'label': 'Temps (s)', 'value': drop}
                if value == 2:
                    drop = [t[2] for t in self.effort_piece]
                    self.df_nuage['dropdown-abs'] = {'label': 'Fx pièce (N)', 'value': drop}
                if value == 3:
                    drop = [t[3] for t in self.effort_piece]
                    self.df_nuage['dropdown-abs'] = {'label': 'Fy pièce (N)', 'value': drop}
                if value == 4:
                    drop = [t[4] for t in self.effort_piece]
                    self.df_nuage['dropdown-abs'] = {'label': 'Fz pièce (N)', 'value': drop}
                if value == 5:
                    drop = [t[2] for t in self.effort_outil]
                    self.df_nuage['dropdown-abs'] = {'label': 'Fx outil (N)', 'value': drop}
                if value == 6:
                    drop = [t[3] for t in self.effort_outil]
                    self.df_nuage['dropdown-abs'] = {'label': 'Fy outil (N)', 'value': drop}
                if value == 7:
                    drop = [t[4] for t in self.effort_outil]
                    self.df_nuage['dropdown-abs'] = {'label': 'Fz outil (N)', 'value': drop}

            return children, value

    def update_dropdown_i_nuage_callback(self, index):
        @self.app.callback(
            Output('dropdown-nuage-ord{}'.format(index), 'value'),
            [Input('dropdown-nuage-ord{}'.format(index), 'value')]
        )
        def update(value):
            """
            Met à jour les dropdowns 2 à 6 pour la partie chart . Ces dropdowns peuvent ne pas exister.
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
                    self.df_nuage.update({'dropdown{}'.format(index): {'label': 'Fx pièce (N)', 'value': drop}})
                if value == 2:
                    drop = [t[3] for t in self.effort_piece]
                    self.df_nuage['dropdown{}'.format(index)] = {'label': 'Fy pièce (N)', 'value': drop}
                if value == 3:
                    drop = [t[4] for t in self.effort_piece]
                    self.df_nuage.update({'dropdown{}'.format(index): {'label': 'Fz pièce (N)', 'value': drop}})
                if value == 4:
                    drop = [t[2] for t in self.effort_outil]
                    self.df_nuage.update({'dropdown{}'.format(index): {'label': 'Fx outil (N)', 'value': drop}})
                if value == 5:
                    drop = [t[3] for t in self.effort_outil]
                    self.df_nuage.update({'dropdown{}'.format(index): {'label': 'Fy outil (N)', 'value': drop}})
                if value == 6:
                    drop = [t[4] for t in self.effort_outil]
                    self.df_nuage.update({'dropdown{}'.format(index): {'label': 'Fz outil (N)', 'value': drop}})

            return value
