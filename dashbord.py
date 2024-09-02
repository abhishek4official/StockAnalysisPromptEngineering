import sqlite3
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd

from StockProcess import StockProcessor

# Connect to SQLite database and load data
def load_data():
    conn = sqlite3.connect('db/StockData.db')
    df = pd.read_sql_query("SELECT Symbol, Date, Uptrend, Downtrend, NeutralTrend, Markdown FROM PromptLog", conn)
    conn.close()
    return df

# Load data
df = load_data()

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container([
   
    dbc.Row([
        dbc.Col([
            
            dash_table.DataTable(
                id='data-table',
              
                columns=[
                    {'name': 'Symbol', 'id': 'Symbol'},
                    {'name': 'Date', 'id': 'Date'},
                    {'name': 'Uptrend', 'id': 'Uptrend'},
                    {'name': 'Downtrend', 'id': 'Downtrend'},
                    {'name': 'NeutralTrend', 'id': 'NeutralTrend'}
                ],
                data=df.to_dict('records'),
                row_selectable='single',
                filter_action='native',
                sort_action='native',
                
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
            ),
        ], width=6,),
        
        dbc.Col([
            dbc.Row([
                dbc.Input(id='input-text', type='text', placeholder='Enter text'),
                dbc.Button('Analyze', id='analyze-button', color='primary', className='ml-2')
            ],style={'margin-bottom': '20px'}),
            dbc.Row([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Uptrend'),
                    html.P(id='uptrend-card')
                ])
            ], className='col-4'),
            dbc.Card([
                dbc.CardBody([
                    html.H4('Downtrend'),
                    html.P(id='downtrend-card')
                ])
            ], className='col-4'),
            dbc.Card([
                dbc.CardBody([
                    html.H4('NeutralTrend'),
                    html.P(id='neutraltrend-card')
                ])
            ], className='col-4')
    ])], width=6)
    ],class_name=''),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Markdown'),
                    dcc.Markdown(id='markdown-content')
                ])
            ], className='mb-3')
        ], width=12)
    ])
])

# Callback to update cards and Markdown content based on selected row
@app.callback(
    [Output('uptrend-card', 'children'),
     Output('downtrend-card', 'children'),
     Output('neutraltrend-card', 'children'),
     Output('markdown-content', 'children'),
     Output('data-table', 'data')],
    [Input('data-table', 'selected_rows'),
     Input('analyze-button', 'n_clicks')],
    [dash.dependencies.State('data-table', 'data'),
     dash.dependencies.State('input-text', 'value')]
)
def update_cards(selected_rows, n_clicks, rows, input_text):
    
    if selected_rows:
        selected_row = rows[selected_rows[0]]
        return (selected_row['Uptrend'], selected_row['Downtrend'], selected_row['NeutralTrend'], selected_row['Markdown'], rows)
    elif n_clicks:
        if type(input_text)!=None and len(input_text) > 0:
            sp=StockProcessor()
            sp.process_stock_code(input_text)
            df=load_data()
        rows = df.to_dict('records')
        filtered_rows = [row for row in rows if row['Symbol'] == input_text]
        if filtered_rows:
            return (filtered_rows[0]['Uptrend'], filtered_rows[0]['Downtrend'], filtered_rows[0]['NeutralTrend'], filtered_rows[0]['Markdown'], rows)
    return ('', '', '', '', rows)

if __name__ == '__main__':
    app.run_server(debug=True)

# Callback to update cards and Markdown content based on selected row
@app.callback(
    [Output('uptrend-card', 'children'),
     Output('downtrend-card', 'children'),
     Output('neutraltrend-card', 'children'),
     Output('markdown-content', 'children')],
    [Input('data-table', 'selected_rows')],
    [dash.dependencies.State('data-table', 'data')]
)
def update_cards(selected_rows, rows):
    df = load_data()  # Reload the data from SQL
    if selected_rows:
        selected_row = rows[selected_rows[0]]
        return (selected_row['Uptrend'], selected_row['Downtrend'], selected_row['NeutralTrend'], selected_row['Markdown'])
    return ('', '', '', '')

if __name__ == '__main__':
    app.run_server(debug=True)