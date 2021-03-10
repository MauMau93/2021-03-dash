import dash
from dash.dependencies import Input, Output, State

import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table

app = dash.Dash(__name__, title="2021 Dash Python App")

import pandas as pd

df_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
df = pd.read_csv(df_url).dropna(subset = ['vore'])

df_vore = df['vore'].sort_values().unique()
opt_vore = [{'label': x + 'vore', 'value': x} for x in df_vore]
# Discrete Colors in Python
# https://plotly.com/python/discrete-color/
col_vore = {x: px.colors.qualitative.G10[i] for i,x in enumerate(df_vore)}

min_bodywt = min(df['bodywt'].dropna())
max_bodywt = max(df['bodywt'].dropna())

markdown_text = '''
### Some references
- [Dash HTML Components](https://dash.plotly.com/dash-html-components)
- [Dash Core Components](https://dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/) 
- [Dash DataTable](https://dash.plotly.com/datatable)  
'''

table_tab = dash_table.DataTable(
                id='my-table',
                columns=[{"name": i, "id": i} for i in df.columns]
            )

graph_tab = dcc.Graph(id="my-graph")

app.layout= html.Div([
    html.Div([html.H1(app.title, className="app-header--title")],
        className= "app-header",
    ),
    html.Div([  
        dcc.Markdown(markdown_text),
        html.Label(["Select types of feeding strategies:", 
            dcc.Dropdown('my-dropdown', options= opt_vore, value= [opt_vore[0]['value']], multi=True)
        ]),
        html.Label(["Range of values for body weight:", 
                 dcc.RangeSlider(
                     max= max_bodywt,
                     min= min_bodywt,
                     step= (max_bodywt - min_bodywt)/10,
                     marks= {'{}'.format(min_bodywt + (max_bodywt - min_bodywt)/10 * i): '{}'.format(round(min_bodywt + (max_bodywt - min_bodywt)/10 * i,2)) for i in range(10)},
                     value= [min_bodywt,max_bodywt],
                 )
        ]),
        dcc.Tabs(id="tabs", value='tab-t', children=[
            dcc.Tab(label='Table', value='tab-t'),
            dcc.Tab(label='Graph', value='tab-g'),
        ]),
        html.Div(id='tabs-content')
    ],
    className= "app-body")
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-t':
        return table_tab
    elif tab == 'tab-g':
        return graph_tab

@app.callback(
     Output('my-table', 'data'),
     Input('my-dropdown', 'value'),
     State('tabs', 'value'))
def update_table(values, tab):
    if tab != 'tab-t':
        return None
    filter = df['vore'].isin(values)
    return df[filter].to_dict("records")

@app.callback(
     Output('my-graph', 'figure'),
     Input('my-dropdown', 'value'),
     State('tabs', 'value'))
def update_graph(values, tab):
    if tab != 'tab-g':
        return None
    filter = df['vore'].isin(values)
    print(col_vore)
    return px.scatter(df[filter], x="bodywt", y="sleep_total", color="vore",
    #color_discrete_sequence=px.colors.qualitative.G10
    color_discrete_map=col_vore)

if __name__ == '__main__':
    app.server.run(debug=True)