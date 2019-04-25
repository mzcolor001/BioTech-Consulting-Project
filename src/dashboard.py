'''
this file is to display the hdf5 info. in a csv dash format 
'''

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
# import h5py
# import numpy as np

with pd.HDFStore('wgs11N.hdf5') as hf:
#     print(hf.keys())
    keys = list(hf.keys())
    print(keys)
    data_frames = [hf[key] for key in keys]
    print(data_frames)

df = data_frames[0]
# print(df)
# print(df.head())


def generate_table(dataframe, max_rows=10):
	return html.Table(

        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div(children=[
	html.H4(children='Persephone Demo'),
	dcc.Dropdown(id='dropdown', options=[
    {'label': i , 'value': i} for i in df.Sample.unique()
    ], multi=True, placeholder='Filter by Sample'),
    html.Div(id='table-container')
])

@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])

def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(df)

    diff = df[df.Sample.str.contains('|'.join(dropdown_value))]
    return generate_table(diff)


if __name__ == '__main__':
	app.run_server(debug=True)
