import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table

import pandas as pd

app = dash.Dash(__name__, title="2021 Dash Python App")

markdown_text = '''
### Some references
- [Dash HTML Components](https://dash.plotly.com/dash-html-components)
- [Dash Core Components](https://dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/)  
'''

df_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
df = pd.read_csv(df_url)

app.layout = html.Div([
    html.H1(app.title),
    dcc.Markdown(markdown_text),
    dash_table.DataTable(
        id='my-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data= df.to_dict("records")
        )
])

if __name__ == '__main__':
    app.server.run(debug=True)