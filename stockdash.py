import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
import pandas as pd
import json

import yfinance as yf
from pytickersymbols import PyTickerSymbols, Statics

import datetime


# Initialize Application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


# Creating an instance of PyTickerSymbols
pytick = PyTickerSymbols()

# Grabbing US NASDAQ index code
index = Statics.Indices.US_NASDAQ

# Acquiring stock information through method call and formatting result into a DataFrame
stocks_df = pd.DataFrame.from_records(pytick.get_stocks_by_index(index=index)).set_index("symbol")

# Grabbing the ticker symbols from the DataFrame Index
tickers = stocks_df.index

# Helper Functions
def create_card(comp, founded, employees, invalid):

    employees = "N/A" if employees == '' else employees

    className = "invalid-card" if invalid else "valid-card"

    card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(comp, className="card-title"),
                        html.P(f"Est: {founded}", className="card-text")
                    ],

                    style=dict(
                        fontFamily="Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                            DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                            Helvetica, Arial, sans-serif"
                    )
                ),
                dbc.CardFooter(f"Employees: {employees}"),
            ],

            className=className,
            style=dict(
                width="18rem",
                margin="5px"
            )
        )

    return card


# Main application layout
app.layout = html.Div(
    [
        html.H1(
            "Stock Ticker Dashboard",

            style=dict(
                fontSize=80,
                fontFamily='Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                            DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                            Helvetica, Arial, sans-serif',
                color="white",
                fontWeight=100,
                textAlign="center"
            )
        ),

        html.Hr(
            style=dict(
                backgroundColor="white",
                marginBottom=30
            )
        ),

        # LEVEL 1 Div holding inner divs for both of our DCC and H3 components
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Select Stock Name",

                            style=dict(
                                fontSize=30,
                                fontFamily="Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                            DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                            Helvetica, Arial, sans-serif",
                                fontWeight=100,
                            ),
                            className="header-med"
                        ),

                        # DROPDOWN MENU TO SELECT STOCK INDEX

                        dcc.Dropdown(
                            id='stock-input',
                            options=[
                                dict(
                                    label=stocks_df.loc[symbol]["name"],
                                    value=symbol
                                ) for symbol in tickers
                            ],

                            value=['TSLA', 'AAPL'],
                            multi=True,
                            style=dict(
                                width="500px",
                                fontSize=24,
                                height="auto",
                                display="inline-block",
                                backgroundColor="black",
                                textAlign="center"
                            )

                        )
                    ],

                    style=dict(
                        # marginRight="10px",
                        # marginTop="5px",
                        # flexDirection="row"
                    )
                ),

                html.Div([
                    dbc.Button(
                        id="state-button",
                        children="Submit",
                        style=dict(
                            marginLeft="10px",
                            height="48px"
                        )
                    )
                ],
                style=dict(
                    display="flex",
                    alignItems = "center"

                )
                ),

                html.Div(
                    [
                        html.H3(
                            "Select Start and End Dates",

                            style=dict(
                                fontSize=30,
                                fontFamily='Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                            DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                            Helvetica, Arial, sans-serif',
                                fontWeight=100,
                                width=500
                            ),
                            className="header-med"
                        ),

                        html.Div(
                            [
                                # DCC DATE PICKER MENU
                                dcc.DatePickerRange(
                                    id="date-input",
                                    start_date='2016-01-04',
                                    end_date='2017-12-29',
                                    style=dict(
                                        height="48px",
                                    )
                                ),

                            ],
                            style=dict(
                                textAlign="center"
                            )
                        )
                    ]
                )
            ],

            style=dict(
                display="flex",
                justifyContent="space-evenly"
                # verticalAlign="middle",
                # alignItems="center",
                # alignText="center"
            )
        ),

        html.Hr(
            style=dict(
                backgroundColor="white"
            )
        ),

        html.Div(
            [
                # DCC GRAPH THAT OUTPUTS STATE CHANGES TO EITHER PICKER
                dcc.Graph(
                    id='graph-output',
                    figure=dict(
                        data=[
                            go.Scatter(
                                x=yf.download(symbol, start="2016-01-04", end="2017-12-29")["Close"].index,
                                y=yf.download(symbol, start="2016-01-04", end="2017-12-29")["Close"].values,
                                mode="lines",
                                name=symbol,
                                line=dict(
                                    width=1
                                )
                            ) for symbol in ["TSLA", "AAPL"]
                        ],

                        layout=go.Layout(
                            title=dict(
                                text="Closing Prices for: {}".format(', '.join(["TSLA", "AAPL"]))
                            ),
                            xaxis=dict(
                                title="Date"
                            ),

                            yaxis=dict(
                                title="Closing Price",
                            ),

                            plot_bgcolor="black",
                            paper_bgcolor="black",

                            font=dict(
                                color="white",
                                family="Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                            DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                            Helvetica, Arial, sans-serif",
                                size=16,
                            )
                        )
                    )
                )
            ]
        ),

        html.Hr(
            style=dict(
                marginTop="40px",
                backgroundColor="white"
            )
        ),

        html.Div(
            [
                html.H1(
                    "Selected Company Info:",

                    style=dict(
                        fontFamily='Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                            DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                            Helvetica, Arial, sans-serif'
                    )
                ),

                html.Hr(),

                html.Div(
                    id="card-output"
                )
            ],

            style=dict(
                marginTop="50px"
            )
        ),

        dcc.Store(
            id='store-cached'
        )
    ],
    style=dict(
        padding="40px",
        backgroundColor="black"
    )
)


@app.callback(Output('store-cached', 'data'),
              [Input('state-button', 'n_clicks')],
              [State('stock-input', 'value'),
               State('date-input', 'start_date')])
def store_date(_, value, start):
    return json.dumps({"value": value, "start": start})


@app.callback(Output('graph-output', 'figure'),
              [Input('store-cached', 'data')],
              [State('date-input', 'end_date')])
def update_ticker_graph(cached, end):

    if cached is None:
        raise dash.exceptions.PreventUpdate

    obj = json.loads(cached)
    selected_tickers, start = obj['value'], obj['start']

    data = []

    for symbol in selected_tickers:

        info = yf.download(symbol, start=start, end=end, progress=False)["Close"]

        dateRange = info.index
        closePrice = info.values

        data.append(
            go.Scatter(
                x=dateRange,
                y=closePrice,
                mode="lines",
                name=symbol,
                line=dict(
                    width=1
                )
            )
        )

    return dict(
        data=data,

        layout=go.Layout(
            title="Closing Prices for: {}".format(', '.join(selected_tickers)),
            xaxis=dict(
                title="Date",
            ),

            yaxis=dict(
                title="Closing Price",
            ),

            plot_bgcolor="black",
            paper_bgcolor="black",

            font=dict(
                color="white",
                family="Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                            DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                            Helvetica, Arial, sans-serif",
                size=14
            )
        )
    )

@app.callback(Output('card-output', 'children'),
              [Input('store-cached', 'data')])
def callback_stats(cached):

    if cached is None:
        raise dash.exceptions.PreventUpdate

    obj = json.loads(cached)
    selected_tickers, start = obj['value'], obj['start']

    meta = []

    for symbol in selected_tickers:
        invalid = False

        if len(yf.Ticker(symbol).history(period="1d", start=start)) == 0:
            invalid = True

        card = create_card(comp=symbol, founded=stocks_df.loc[symbol]['metadata']['founded'],
                        employees=stocks_df.loc[symbol]['metadata']['employees'], invalid=invalid)

        meta.append(card)


    return dbc.Row(
        meta,

        style=dict(
            display="flex",
            justifyContent="center"
        )
    )


if __name__ == '__main__':
    app.run_server('0.0.0.0', 5001, debug=True)



