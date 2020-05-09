import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

app = dash.Dash(__name__)
server = app.server
app.title = "Anki Dash"

df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp", title="Life expectancy in Canada")

########### Set up the layout
app.layout = html.Div(children=[
    html.H1('Anki Dash'),
        dcc.Graph(
            id = 'mainplot',
            figure = fig
        )
    ]
)

if __name__ == '__main__':
    app.run_server()
