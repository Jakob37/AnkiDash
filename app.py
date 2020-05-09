#!/usr/bin/env python3

import plotly.graph_objects as go
fig = go.Figure()

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server()


