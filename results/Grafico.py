from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os

files = []
categories = []
pasta = 'results/coleta/'
for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        files.append(os.path.join(diretorio, arquivo))

for file in files:
    categories.append(os.path.basename(file))

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="values",
        options=[{'label': category, 'value': category} for category in categories],
        value=categories[0],
    ),
    dcc.Graph(id="graph")
])

@app.callback(
    Output("graph", "figure"),
    Input("values", "value")
)
def generate_chart(value):
    selected_file = os.path.join(pasta, value)
    arquivo = pd.read_excel(selected_file)
    
    colunas = arquivo.columns.tolist()
    
    fig = px.pie(arquivo,
        values= colunas[1],
        names= colunas[0],
        title="Categorias mais assistidas da Twitch",
        color_discrete_sequence=px.colors.sequential.Purples_r
    )

    return fig
if __name__ == "__main__":
    app.run_server(debug=True)


