'''
this file is to display the hdf5 info. in a csv dash format 
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go 


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
mgr_options = df["Sample"].unique()

# Create the app
app = dash.Dash()

# Populate the layout with HTML and graph components
app.layout = html.Div([
    html.H2("Persephone Demo Sample classified_percent"),
    html.Div(
        [
            dcc.Dropdown(
                id="Sample",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value='All Samples'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])

# Add the callbacks to support the interactive componets
@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Sample', 'value')])

def update_graph(Sample):
    if Sample == "All Samples":
        df_plot = df.copy()
    else:
        df_plot = df[df['Sample'] == Sample]

    pv = pd.pivot_table(
        df_plot,
        index=['name'],
        columns=["level"],
        values=['classified_percent'],
        # aggfunc=sum,
        fill_value=0)

    trace = go.Bar(x=pv.index, y= pv.values)


    return {
        'data': [trace],
        'layout':
        go.Layout(
            title='Classified percentage for Sample {}'.format(Sample),
            barmode='stack')
    }


if __name__ == '__main__':
	app.run_server(debug=True)
