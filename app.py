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

nbr_revs_df = pd.read_csv("notebooks/top_difficult.tsv", sep="\t")
all_revs_df = pd.read_csv("notebooks/all_reviews.tsv", sep="\t")

fig = px.bar(
    nbr_revs_df,
    x="character",
    y="reviews",
    title="Jakob's most reviewed characters")

app.layout = html.Div(children=[
    html.H1('Anki Dash'),
    dcc.Slider(id='input_slider', min=1, max=100, value=10),
    dcc.Graph(id='mainplot'),
    dcc.Dropdown(id='char_select',
                 value=nbr_revs_df.head(5).character,
                 options=[{'label':i,'value':i} for i in nbr_revs_df.character],
                 multi=True,
                 placeholder='A placeholder..'),
    dcc.Graph(id='charplot')
    ]
)
# 一
@app.callback(
    Output('mainplot', 'figure'),
    [Input('input_slider', 'value')]
)
def update_figure(show_count):
    filter_df = nbr_revs_df.head(show_count)
    my_fig = px.bar(filter_df, x="character", y="reviews", title="Jakob's most reviewed characters")
    return my_fig

@app.callback(
    Output('charplot', 'figure'),
    [Input('char_select', 'value')]
)
def character_graph(characters):

    if len(characters) > 1:
        revs_to_plot = all_revs_df[all_revs_df['character'].isin(characters)]
    else:
        revs_to_plot = all_revs_df[all_revs_df['character'] == characters]

    my_fig = px.line(revs_to_plot, y="duration", color="character")
    # my_fig.update_layout(yaxis_type="log")

    return my_fig


if __name__ == '__main__':
    app.run_server()


