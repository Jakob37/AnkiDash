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

nbr_revs_df = pd.read_csv("parsed_data/top_difficult.tsv", sep="\t")
all_revs_df = pd.read_csv("parsed_data/all_reviews.tsv", sep="\t")

fig = px.bar(
    nbr_revs_df,
    x="character",
    y="reviews",
    title="Jakob's most reviewed characters")

axis_choices = [
    {'label': option, 'value': option} for option in ['avg_ease', 'reviews', 'curr_dur']]

app.layout = html.Div(children=[
    html.H1('Anki Dash'),
    dcc.Slider(id='input_slider', min=1, max=100, value=10),
    dcc.Graph(id='mainplot'),
    dcc.Dropdown(id='char_select',
                 value=nbr_revs_df.head(5).character,
                 options=[{'label': ch, 'value': ch} for ch in nbr_revs_df.character],
                 multi=True,
                 placeholder='A placeholder..'),
    dcc.Graph(id='charplot'),
    html.H3('Opacity'),
    dcc.Slider(id='scatter_opacity', min=0, max=1, value=0.6, step=0.05),
    html.H3('X-axis'),
    dcc.Dropdown(id='scatter_xaxis', options=axis_choices, value='reviews'),
    html.H3('Y-axis'),
    dcc.Dropdown(id='scatter_yaxis', options=axis_choices, value='avg_ease'),
    html.H3('Color'),
    dcc.Dropdown(id='scatter_color', options=axis_choices, value='curr_dur'),
    dcc.Graph(id='targethistplot')
    ]
)


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

    my_fig = px.line(revs_to_plot, x="nbr", y="duration", color="character")
    return my_fig


@app.callback(
    Output('targethistplot', 'figure'),
    [
        Input('scatter_opacity', 'value'),
        Input('scatter_xaxis', 'value'),
        Input('scatter_yaxis', 'value'),
        Input('scatter_color', 'value')
    ]
)
def target_hist(scatter_opacity, xaxis, yaxis, color):

    #color_map = {"ease_1": "red", "ease_2": "gray", "ease_3": "green", "ease_4": "blue"}

    my_fig = px.scatter(
        nbr_revs_df,
        x=xaxis,
        y=yaxis,
        color=color,
        log_y=False,
        color_continuous_scale=['red', 'lightgreen', 'blue'],
        #color_discrete_map=color_map,
        opacity=scatter_opacity,
        hover_name="character",
        title="Distribution of duration and review"
    )
    return my_fig


if __name__ == '__main__':
    app.run_server()


