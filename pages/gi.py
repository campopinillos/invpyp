from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash
import base64
import io
import pandas as pd
from firestore_upload import consulta_empresas, cargue, delete_collection, base_final
from google.cloud import storage
from google.cloud import firestore

dash.register_page(__name__)

# Inicializa el servicio de almacenamiento (Firebase Storage) con el nombre de tu bucket
storage_client = storage.Client.from_service_account_json("serviceAccountKey.json")
bucket = storage_client.get_bucket("inversionpyp-7db7c.appspot.com")

# Inicializa el servicio de almacenamiento (Firestore Database) con el nombre del proyecto
db = firestore.Client(project="inversionpyp-7db7c")
empresas = None

programa = "gi_"

texto ="""
1. Asignación y atención por investigación de AT.
"""

sucursales = [
    "AMAZONAS", "ANTIOQUIA", "ARAUCA", 
    "ATLANTICO", "BOGOTA", "BOLIVAR", "BOYACA", "CALDAS", 
    "CAQUETA", "CASANARE", "CAUCA", "CESAR", "CHOCO",
    "CORDOBA", "CUNDINAMARCA", "GUAINIA", "GUAVIARE", 
    "HUILA", "LA GUAJIRA", "MAGDALENA", "META", "NARIÑO", 
    "NORTE SANTANDER", "PUTUMAYO", "QUINDIO", "RISARALDA",
    "SAN ANDRES", "SANTANDER", "SUCRE", "TOLIMA", "VALLE", 
    "VAUPES", "VICHADA"]

tab1_content = html.Div([
    html.Br(),
    html.H1("Atención Directa", style={'textAlign': 'center', 'font-family': 'Muli', 'color': '#ff7500'}),
    html.Hr(),
    html.H3("Descargar Plantilla", style={'textAlign': 'center', 'font-family': 'Muli', 'color': '#ff7500'}),
    # Botón para descargar la plantilla
    dcc.Link(html.Button("Descargar", id="url-button", style={
        'width': '98%',
        'height': '55px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'bold',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'font-family': 'Muli',
        'font-size': '18px'
    }), href="https://firebasestorage.googleapis.com/v0/b/inversionpyp-7db7c.appspot.com/o/REPORTE_PLANTILLA.xlsx?alt=media&token=eb69b535-27fc-486e-b0af-a5a09dcb244d&_gl=1*s6zata*_ga*MTgyODYxOTA3OC4xNjk2MzAwMDYw*_ga_CW55HF8NVT*MTY5NjQzOTY5OC43LjAuMTY5NjQzOTY5OC42MC4wLjA.",
    target="_blank"),
    
    html.Br(),

    html.H2("Cargue Masivo", style={'textAlign': 'center', 'font-family': 'Muli', 'color': '#ff7500'}),
    
    # Componente de carga masiva en la primera pestaña
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'ARRASTRA O ',
            html.A('SELECCIONA PLANTILLA DILIGENCIADA.')
        ]),
        style={
            'width': '98%',
            'height': '55px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'font-family': 'Muli',
            'font-size': '18px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Hr(),
    html.Div([
        html.Button("Notas", id="toggle-button", 
        style={
            'width': '98%',
            'height': '55px',
            'lineHeight': '50px',
            'borderWidth': '1px',
            'borderStyle': 'solid',  # Change to 'solid' for border style
            'borderColor': '#0d6efd',    # Border color
            'backgroundColor': '#0d6efd',  # Background color (blue)
            'color': 'white',         # Text color (white)
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'fontFamily': 'Muli',    # Change to 'fontFamily'
            'fontSize': '18px' 
        }
        ),
        html.Br(),
        html.Div(id="collapse-output-gi")]),
    html.Hr(),
    html.Div(id='output-data-upload-tab1-gi'),
    dash_table.DataTable(
        id='data-table-gi',
        columns=[],  # Se actualizará en la función display_contents
        data=[],     # Se actualizará en la función display_contents
        style_table={'overflowX': 'scroll'},
        style_header={'textAlign': 'center',
                      'fontWeight': 'bold'},
    )
])

# Define el contenido de la segunda pestaña
tab2_content = html.Div([
    html.Br(),
    html.H1("Distribución Recursos PyP", style={'textAlign': 'center', 'font-family': 'Muli', 'color': '#ff7500'}),
    html.H6("Recurso propio para gestión y atención de empresas (Administrativo)", style={'textAlign': 'center', 'font-family': 'Muli', 'color': '#ff7500'}),
    html.Hr(),
    # Botón para descargar la plantilla
    html.H3("Descargar Plantilla", style={'textAlign': 'center', 'font-family': 'Muli', 'color': '#ff7500'}),
    # Botón para descargar la plantilla
    dcc.Link(html.Button("Descargar", id="url-button_tab2", style={
        'width': '98%',
        'height': '55px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'bold',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'font-family': 'Muli',
        'font-size': '18px'
    }), href="https://firebasestorage.googleapis.com/v0/b/inversionpyp-7db7c.appspot.com/o/REPORTE_PLANTILLA_GRAN_MIPYIME.xlsx?alt=media&token=f1441b75-9ba2-4f32-925a-c49718847085",
    target="_blank"),
    
    html.Br(),
    html.Br(),
    html.H3("Ingrese los siguientes datos:", 
            style={
                'textAlign': 'center',
                'font-family': 'Muli',
                'color': '#ff7500'}),
    dcc.Dropdown(sucursales, id="input1", placeholder="Sucursal:",style={
        'width': '99%',
        'height': '55px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'bold',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '5px',
        'padding': '0',
        'font-family': 'Muli',
        'font-size': '18px',
        'padding': '0',  # Resetear el relleno
    }),
    dcc.Input(id="input2", type="number", placeholder="Valor de la Factura:", style={
        'width': '98%',
        'height': '55px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'bold',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'font-family': 'Muli',
        'font-size': '18px'
    }, debounce=True),
    dcc.Input(id="input3", type="text", placeholder="Descripción de la Inversión:", style={
        'width': '98%',
        'height': '55px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'bold',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px',
        'font-family': 'Muli',
        'font-size': '18px'
    }, debounce=True),

    html.H2("Cargue Masivo", style={'textAlign': 'center', 'font-family': 'Muli', 'color': '#ff7500'}),
    
    # Componente de carga masiva en la primera pestaña
    dcc.Upload(
        id='upload-data-tab2',
        children=html.Div([
            'ARRASTRA O ',
            html.A('SELECCIONA PLANTILLA DILIGENCIADA.')
        ]),
        style={
            'width': '98%',
            'height': '55px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'font-family': 'Muli',
            'font-size': '18px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),

    html.Div(id="output"),
    html.Div(id='output-data-upload-tab2-gi'),
    dash_table.DataTable(
        id='data-table-tab2',
        columns=[],  # Se actualizará en la función display_contents
        data=[],     # Se actualizará en la función display_contents
        style_table={'overflowX': 'scroll'},
        style_header={'textAlign': 'center',
                      'fontWeight': 'bold'}
    )
])

layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Atención Directa', children=tab1_content),
        dcc.Tab(label='Asignación Recursos', children=tab2_content),
    ])
])

def parse_contents(contents,tab_flag):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Lee el archivo XLSX y crea un DataFrame
        xls = pd.ExcelFile(io.BytesIO(decoded))
        sheet_names = xls.sheet_names
        appended_df = pd.DataFrame()  # DataFrame para appendear
        for sheet_name in sheet_names:
            df = pd.read_excel(xls, sheet_name)
            df['Programa'] = programa
            df['Tipo Atención'] = sheet_name
            appended_df = pd.concat([appended_df, df], ignore_index=True)
        try:
            df_wide =  appended_df.pivot(index=['Vigencia', 'Mes', 'Sucursal', 'Tipo Documento', 'No. Documento', 'Razón Social'], columns='Tipo Atención', values='Valor Total Ejecutado').reset_index()
            # Fill missing values with 0
            df_wide = df_wide.fillna(0)
            # Calculate the total sum of ValorTotalEjecutado for all sheets
            df_wide['Total'] = df_wide.iloc[:, 6:].sum(axis=1)
        except:
            return appended_df, tab_flag
        return df_wide, tab_flag
    except Exception as e:
        print(e)
        return html.Div([
            'Error procesando el archivo no corresponde a la plantilla xlsx.'
        ])

def generate_output_id(input1, input2, input3):
    return 'Sucursal: {input1}\nValor Factura: {input2}\nDescripción de la Inversión: {input3}'

@callback(
    Output("collapse-output-gi", "children"),
    Input("toggle-button", "n_clicks"),
)
def toggle_collapse(n_clicks):
    if n_clicks is None:
        return ""
    if n_clicks % 2 == 1:
        return dcc.Markdown(
            texto
        )
    else:
        return ""

# Función para mostrar los datos en la interfaz de usuario
@callback(Output('output-data-upload-tab1-gi', 'children'),
              Output('data-table-gi', 'columns'),
              Output('data-table-gi', 'data'),
              Input('upload-data', 'contents'))
def display_contents_tab1(contents):
    if contents is not None:
        dataframes, tab_flag = parse_contents(contents, "directa")
        collection = programa + tab_flag
        delete_collection(collect=collection)
        cargue(collect=collection, df=dataframes)
        base_final()
        if dataframes is not None:
            # Construir DataTable
            columns = [{'name': col, 'id': col} for col in dataframes.columns]
            data = dataframes.to_dict('records')
            return [html.H4('Consolidado por Empresa Archivo Excel:', style={
                'textAlign': 'center', 
                'font-family': 'Muli', 
                'color': '#ff7500'}),
                columns,
                data
            ]
    # Si no se ha cargado ningún archivo o ha ocurrido un error
    return html.Div(), [], []

# Función para mostrar los datos en la interfaz de usuario
@callback(
    Output('output-data-upload-tab2-gi', 'children'),
    Input("input1", "value"),
    Input("input2", "value"),
    Input("input3", "value"),
    Input('upload-data-tab2', 'contents'),
    State('upload-data-tab2', 'filename'),
    State('upload-data-tab2', 'last_modified'),
    prevent_initial_call=True)
def display_contents_tab_2(input1, input2, input3, contents, filename, last_modified):
    if contents is not None:
        global empresas 
        empresas = consulta_empresas()
        dataframes, tab_flag = parse_contents(contents, "indirecta")
        dataframes = dataframes.merge(empresas,
                                      on=['Vigencia', 'Mes', 'Sucursal', 'Tipo Documento', 'No. Documento', 'Razón Social'],
                                      how='left')
        dataframes['Programa'] = programa
        dataframes['Sucursal_2'] = input1
        dataframes['Valor'] = input2
        dataframes['Descripción'] = input3
        suma_prima_total = dataframes['Prima'].sum()
        dataframes['Total_inv_pyp'] = ((dataframes['Prima'] / suma_prima_total)) * dataframes['Valor']
        collection = programa + tab_flag
        delete_collection(collect=collection)
        cargue(collect=collection, df=dataframes)
        base_final()
        if dataframes is not None:
            # Construir DataTable
            columns = [{'name': col, 'id': col} for col in dataframes.columns]
            data = dataframes.to_dict('records')
            return html.Div([
                html.Div(id=generate_output_id(input1, input2, input3)),
                html.Hr(),
                html.H5('Empresas Atendidas:', 
                        style={
                            'textAlign': 'center',
                            'font-family': 'Muli',
                            'color': '#ff7500'}),
                dash_table.DataTable(
                    id='data-table-tab2',
                    columns=columns,
                    data=data,
                    style_table={
                        'overflowX': 'scroll'},
                    style_header={
                        'textAlign': 'center',
                        'fontWeight': 'bold'}
                ),
            ])
    # Si no se ha cargado ningún archivo o ha ocurrido un error
    return html.Div() 
