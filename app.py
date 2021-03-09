import dash
import dash_html_components as html

app = dash.Dash(__name__, title="2021 Dash Python App")

app.layout = html.H1(app.title) 

if __name__ == '__main__':
    app.server.run()