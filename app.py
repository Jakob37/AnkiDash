import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server
app.title = "Anki Dash"

df = pd.read_csv("notebooks/top_difficult.tsv", sep="\t")
fig = px.bar(df, x="character", y="reviews", title="Jakob's most reviewed characters")

app.layout = html.Div(children=[
    html.H1('Anki Dash'),
    dcc.Slider(id='input_slider', min=1, max=100, value=10),
    dcc.Graph(id = 'mainplot')
    ]
)

@app.callback(
    Output('mainplot', 'figure'),
    [Input('input_slider', 'value')]
)
def update_figure(show_count):
    filter_df = df.head(show_count)
    fig = px.bar(filter_df, x="character", y="reviews", title="Jakob's most reviewed characters")
    return fig



if __name__ == '__main__':
    app.run_server()


