import dash_core_components as dcc
import dash_html_components as html
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div([
    dcc.Interval(id='interval1', interval=1000, n_intervals=0),
    html.H1(id='label1', children=''),
    dcc.Graph(id='game_area')
])


@app.callback(dash.dependencies.Output('label1', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    return 'Intervals Passed: ' + str(n)

@app.callback(
    Output('game_area', 'figure'),
    [dash.dependencies.Input('interval1', 'n_intervals')]
)
def update_figure(interval):
    print(interval)
    df = pd.DataFrame(dict(entity=["drop1", "drop2"], xpos=[2,4], ypos=[0+interval*0.2, 3]))
    fig = px.scatter(df, x="xpos", y="ypos", range_x=[0, 5], range_y=[0, 5])
    return fig

app.run_server(debug=False, port=8050)
