import dash
import dash_html_components as html
import dash_core_components as dcc

markdown_text = '''
### Some references
- [Dash HTML Components](https://dash.plotly.com/dash-html-components)
- [Dash Core Components](https://dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/)  
'''

app = dash.Dash(__name__, title="2021 Dash Python App")

app.layout = html.Div([
    html.H1(app.title),
    dcc.Markdown(markdown_text)
])

if __name__ == '__main__':
    app.server.run(debug=True)