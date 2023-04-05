import dash
from dash.dependencies import Input, Output
from controller.ExportExperience import ExportExperience


class DashboardInfoController:
    """
    Classe qui contient les méthodes necessaire à l'utilisation du Dashboard. Le dashboard est une interface plotly
    dash permettant de visualiser les données issues d'une expérience de la base de données.
    """

    def __init__(self, app, dashboard_info):

        self.dashboard_info = dashboard_info
        self.app = app
        self.export_to_excel()

    def export_to_excel(self):
        @self.app.callback(
            Output('export', 'n_clicks'),
            [Input('export', 'n_clicks')]
        )
        def export_to_excel(n_clicks):
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = 'btn-info'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'export':
                export = ExportExperience(self.data_exp[0])

            return n_clicks
