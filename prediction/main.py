import plotly.express as px
from dash import dcc, Dash, html
from dash.dependencies import Input, Output
import pandas as pd
from operations import CORRELATION_INPUT_DF, prediction_operation
import plotly.graph_objects as go


def dropdown_options(data_frame: pd.DataFrame, query: str) -> list:
    """
    makes a list of the unique items in a specified dataframe series.
    Args:
        data_frame: the dataframe whose series we are getting unique values
        query: the name of the column we are looking tpo get unique values from
    Return:
        a list of unique values from the column
    """
    options = [{'label': item, 'value': item} for item in data_frame[query].unique()]
    return options


app = Dash(__name__)

source_label = html.Label(['Select a Source'],
                          style={'font-weight': 'bold', "text-align": "right", "offset": 1})

source_options = dropdown_options(CORRELATION_INPUT_DF, 'Source')

source_selector = dcc.Dropdown(id='source', options=source_options,
                               value=source_options[0]['value'])

state_label = html.Label(['Select a State'],
                         style={'font-weight': 'bold', "text-align": "right", "offset": 1})

state_options = dropdown_options(CORRELATION_INPUT_DF, 'State')

state_selector = dcc.Dropdown(id='state', options=state_options,
                              value=state_options[0]['value'])
indicator_label = html.Label(['Select an Indicator'],
                                       style={'font-weight': 'bold', "text-align": "right", "offset": 1})

indicator_options = dropdown_options(CORRELATION_INPUT_DF, 'Indicator')

indicator_selector = dcc.Dropdown(id='indicator', options=indicator_options,
                                  value=indicator_options[0]['value'])

# make this a multi selectable dropdown list starting from 2018
year_selector = dcc.RangeSlider(id='year', min=2018, max=2026,
                                value=[2018, 2023],
                                step=1,
                                tooltip={'always_visible': True, 'placement': 'bottom'}
                                )

graph = dcc.Graph(id='graph', figure={})

app.layout = html.Div(children=[
    source_label,
    source_selector,
    state_label,
    state_selector,
    indicator_label,
    indicator_selector,
    year_selector,
    graph
])


@app.callback(
    Output('graph', 'figure'),
    Input('source', 'value'),
    Input('state', 'value'),
    Input('indicator', 'value'),
    Input('year', 'value')
)
def cb(source, state, indicator, year):
    # make a list of the year range selected so you can pass it into the prediction operation
    years = [i + 1 for i in range(year[0] - 1, year[-1])]
    df = prediction_operation(dataframe=CORRELATION_INPUT_DF,
                              indicator_column='Indicator',
                              indicator_query=indicator,
                              state_column='State',
                              state_query=state,
                              source_column='Source',
                              source_query=source,
                              columns_to_drop=['Indicator', 'State', 'LGA', 'Source'],
                              period_column='Period',
                              values_column='Value',
                              forecast_years=years
                              )
    df = [item for item in df]
    if not df:
        print("Dataframe is empty")
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching data found",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }
    else:
        df = pd.concat(df)
        print(df.tail())

    # fig = go.Figure()
    # return fig.add_scatter(x=df.index, y=df['Value'], mode='lines', name='Predictionss)

    return px.line(df, x=df.index, y=df['Value'])


if __name__ == "__main__":
    app.run_server(debug=True)
