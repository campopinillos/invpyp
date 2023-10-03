import dash
from dash import Dash, html, dcc
import firebase_admin
from firebase_admin import credentials


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
# Especifica la ruta al archivo JSON de las credenciales de servicio
cred = credentials.Certificate("./serviceAccountKey.json")
# Inicializa Firebase Admin SDK con la credencial
firebase_admin.initialize_app(cred)

app.layout = html.Div([dash.page_container])

if __name__ == '__main__':
    app.run(debug=True)
