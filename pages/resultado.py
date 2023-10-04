from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash
import pandas as pd
from firestore_upload import consulta_empresas

dash.register_page(__name__)

empresas = consulta_empresas(collect='resultado_pyp')

layout = html.Div([
    dash_table.DataTable(
        id='table_result',
        columns=[{'name': col, 'id': col} for col in empresas.columns],
        data=empresas.to_dict('records'),
        style_table={'overflowX': 'scroll'},
        style_header={'textAlign': 'center',
                      'fontWeight': 'bold'}
    )
])