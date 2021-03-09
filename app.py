import dash
from dash.dependencies import Input, Output, State

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

app = dash.Dash(__name__, title="2021 Dash Python App")

import pandas as pd

df_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
df = pd.read_csv(df_url)

df_vore = df['vore'].dropna().sort_values().unique()
opt_vore = [{'label': x + 'vore', 'value': x} for x in df_vore]

markdown_text = '''
### Some references
- [Dash HTML Components](https://dash.plotly.com/dash-html-components)
- [Dash Core Components](https://dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/) 
- [Dash DataTable](https://dash.plotly.com/datatable)  
'''

table_tab = dash_table.DataTable(
                id='my-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data= df.to_dict("records")
            )
graph_tab = dcc.Graph(id="graph",
                figure={"data":[
                        {"x":[1,2,3], "y":[4,2,1], "type": "bar", "name": "DF"},
                        {"x":[1,2,3], "y":[2,4,5], "type": "bar", "name": u'Montréal'}
                        ]}
            )

app.layout= html.Div([
    html.Div([html.H1(app.title, className="app-header--title")],
        className= "app-header",
    ),
    html.Div([  
        dcc.Markdown(markdown_text),
        html.Label(["Select types of feeding strategies:", 
            dcc.Dropdown('my-dropdown', options= opt_vore, value= [opt_vore[0]['value']], multi=True)
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
     Input('my-dropdown', 'value'))
def update_data(values):
    filter = df['vore'].isin(values)
    return df[filter].to_dict("records")


if __name__ == '__main__':
    app.server.run(debug=True)