# What is API?
# -> Frontend/UI/Website/Mobile App ekhathe toh jinish gulo visually dekhte pai. But ekhane
# jokhon login koren ei kajgulo kothay hoy, kuno ekta server e hoy. Eije calculation operation
# kisher maddhome hoy. Eigula backend er maddhome hoy. So ekhane script gula lekha thake. 
# Sheikhan theke mane backend theke response ashle sei response gula amra hocche website e 
# dekhte pari. Apni jokhon ekta login korben, apnar website backend er website e hit kore 
# okhane jeye apnar credential match kore jodi credential thikthak thake, tokhon website e 
# ekta response jay it is success. So erokom tinta planform holo FastAPI Flask Django Python
# er jonne.

# Django, Flask, FastAPI --> API bananor jonno use hoy

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df_csv = pd.read_csv("smoothie sales.csv", parse_dates=["Date"])

df_static = pd.DataFrame({
    "Smoothie": ["Banana", "Mango", "Berry", "Papaya", "Mango", "Banana"],
    "Sales": [150, 200, 180, 90, 220, 170],
    "Day": ["Mon", "Mon", "Mon", "Mon", "Tue", "Tue"]
})

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Smoothie Dashboard", style={'textAlign': 'center'}),

    html.H2("CSV-based Sales Over Time", style={'marginTop': '30px'}),
    dcc.Dropdown(
      id='csv-smoothie-filter',
      options=[{'label': smoothie, 'value': smoothie} for
                smoothie in df_csv['Smoothie'].unique()],
    value='Mango'
    ),
    dcc.Graph(id='csv-sales-over-time'),
    html.Br(),

    dcc.Graph(
        id="csv-total-sales-bar",
        figure=px.bar(
            df_csv.groupby("Smoothie").sum(numeric_only=True).reset_index(),
            x="Smoothie", y="Sales", color="Smoothie", 
            title="Total Sales by Smoothie (csv)"
        )
    ),
    html.H2("Static Smoothie sales by Day", style={'marginTop': '30px'}),
    dcc.Dropdown(
      id='static-smoothie-dropdown',
      options=[{'label': smoothie, 'value': smoothie} for
                smoothie in df_csv['Smoothie'].unique()],
    value='Mango'
    ),
    dcc.Graph(id="static-sales-graph")
])


@app.callback(
    Output("csv-sales-over-time", 'figure'),
    Input('csv-smoothie-filter', 'value')
)
def update_csv_time_series(selected_smoothie):
    filtered_df = df_csv[df_csv['Smoothie']==selected_smoothie]
    fig = px.line(filtered_df, x="Date", y="Sales",
                  title=f"{selected_smoothie} sales over time(csv)")
    return fig


@app.callback(
    Output('static-sales-graph', 'figure'),
    Input('static-smoothie-dropdown', 'value')
)
def update_static_graph(selected_smoothie):
    filtered_df = df_static[df_static['Smoothie']==selected_smoothie]
    fig = px.bar(filtered_df, x="Day", y="Sales",
                  title=f"{selected_smoothie} Sales by Day(Static)")
    return fig


if __name__ == '__main__':
    app.run(debug=True)