import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()

app.layout = html.Div([
    html.H1('Hello, Dash'),
    dcc.Dropdown(id='dropdown', options=[{'label': i, 'value': i} for i in ['A', 'B', 'C']], value='A'),
    html.Div(id='output')
])

@app.callback(dash.dependencies.Output('output', 'children'), [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
