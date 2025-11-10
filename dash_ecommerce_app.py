# dash_ecommerce_app.py
# Projeto final: Dashboard interativo com Dash
import os
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

POSSIBLE_PATHS = [
    'ecommerce_estatistica.csv',
    './ecommerce_estatistica.csv',
    '/mnt/data/ecommerce_estatistica.csv',
    '/mnt/data/ecommerce_estatistica (2).csv'
]

csv_path = next((p for p in POSSIBLE_PATHS if os.path.exists(p)), None)
if not csv_path:
    raise FileNotFoundError('Arquivo ecommerce_estatistica.csv não encontrado.')

df = pd.read_csv(csv_path)

app = Dash(__name__)
server = app.server

num_cols = df.select_dtypes(include=['number']).columns.tolist()
all_cols = df.columns.tolist()

app.layout = html.Div([
    html.H1('Dashboard Interativo - E-commerce', style={'textAlign': 'center'}),
    html.Div([
        html.Label('Eixo X:'),
        dcc.Dropdown(id='x-axis', options=[{'label': c, 'value': c} for c in all_cols], value=all_cols[0]),
        html.Label('Eixo Y:'),
        dcc.Dropdown(id='y-axis', options=[{'label': c, 'value': c} for c in num_cols], value=num_cols[0] if num_cols else all_cols[0]),
        html.Label('Tipo de gráfico:'),
        dcc.RadioItems(id='chart-type', options=[
            {'label': 'Dispersão', 'value': 'scatter'},
            {'label': 'Linha', 'value': 'line'},
            {'label': 'Barras', 'value': 'bar'},
            {'label': 'Histograma', 'value': 'hist'}
        ], value='scatter'),
        html.Label('Coluna de cor (opcional):'),
        dcc.Dropdown(id='color-col', options=[{'label': c, 'value': c} for c in all_cols], value=None, clearable=True)
    ], style={'width': '28%', 'display': 'inline-block', 'padding': '20px', 'verticalAlign': 'top', 'borderRight': '1px solid #ddd'}),
    html.Div([dcc.Graph(id='main-graph', style={'height': '600px'})],
             style={'width': '68%', 'display': 'inline-block', 'padding': '20px'}),
    html.Hr(),
    html.H3('Amostra dos dados carregados:'),
    html.Pre(id='data-preview', style={'backgroundColor': '#f9f9f9', 'padding': '10px', 'borderRadius': '8px'})
])

@app.callback(Output('main-graph', 'figure'), Input('x-axis', 'value'), Input('y-axis', 'value'),
              Input('chart-type', 'value'), Input('color-col', 'value'))
def update_graph(x, y, chart_type, color):
    if chart_type == 'scatter':
        fig = px.scatter(df, x=x, y=y, color=color, title='Gráfico de Dispersão')
    elif chart_type == 'line':
        fig = px.line(df, x=x, y=y, color=color, title='Gráfico de Linha')
    elif chart_type == 'bar':
        fig = px.bar(df, x=x, y=y, color=color, title='Gráfico de Barras')
    elif chart_type == 'hist':
        fig = px.histogram(df, x=y, title='Histograma')
    else:
        fig = px.scatter(df, x=x, y=y)
    fig.update_layout(template='plotly_white')
    return fig

@app.callback(Output('data-preview', 'children'), Input('x-axis', 'value'))
def show_preview(_):
    return df.head(10).to_string()

if __name__ == '__main__':
    print(f'Arquivo carregado: {csv_path}')
    app.run_server(debug=True, port=8050)
