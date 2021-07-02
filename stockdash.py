import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
import pandas as pd
import json

from pytickersymbols import PyTickerSymbols, Statics
import yfinance as yf

from flask_caching import Cache


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
def create_card(comp, founded, employees, is_valid):

    employees = "N/A" if employees == '' else employees
    founded = "N/A" if founded == '' else founded

    className = "valid-card" if is_valid else "invalid-card"
    error_text = f"""
        Error coagulating stock data for desired time interval.
    """

    card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4(comp, className="card-title"),

                                        html.P(f"Est: {founded}", className="card-text")
                                    ],

                                    className="title-date"
                                ),

                                html.P(
                                    error_text,
                                    className="error-text",
                                    hidden=is_valid
                                )

                            ],

                            className="upper-card-container"
                        )
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
                                textAlign="center"
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
                ),

                html.Div(
                    [
                        dcc.Loading(
                            [
                                dbc.Button(
                                    id="state-button",
                                    children="Visualize",
                                    style=dict(
                                        marginLeft="10px",
                                        height="48px"
                                    ),
                                    className="dbc-button"
                                )
                            ],

                            id="loading-button"
                        )
                    ],

                    style=dict(
                        alignItems="center"
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
                                width=500,
                                textAlign="center"
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

                html.Div(
                    id="graph-div",
                    children=[
                        dcc.Graph(
                            id='graph-output',
                            figure=dict(
                                data=[
                                    go.Scatter(
                                        x=yf.download(symbol, start="2016-01-04", end="2017-12-29", progress=False)["Close"].index,
                                        y=yf.download(symbol, start="2016-01-04", end="2017-12-29", progress=False)["Close"].values,
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
                )
            ]
        ),

        html.Hr(
            style=dict(
                marginTop="50px",
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
                            Helvetica, Arial, sans-serif',
                        fontWeight=100
                    )
                ),

                html.Hr(),

                html.Div(
                    [
                        dbc.Row(
                            [
                                create_card(comp=symbol, founded=stocks_df.loc[symbol]['metadata']['founded'],
                                employees=stocks_df.loc[symbol]['metadata']['employees'], is_valid=True)

                                for symbol in ['TSLA', 'AAPL']
                            ],

                            style=dict(
                                display="flex",
                                justifyContent="center"
                            )
                        )
                        # create_card(comp=symbol, founded=stocks_df.loc[symbol]['metadata']['founded'],
                        # employees=stocks_df.loc[symbol]['metadata']['employees'], is_valid=True)
                        #
                        # for symbol in ['TSLA', 'AAPL']
                    ],


                    id="card-output"
                )
            ],

            style=dict(
                marginTop="50px"
            )
        ),

        html.Div(
            [
                dcc.Store(
                    id='data-store',
                    storage_type="local"
                )
            ],

            id='data-div'
        )

    ],
    style=dict(
        padding="40px",
        backgroundColor="black"
    )
)


@app.callback([Output('data-store', 'data'),
               Output('loading-button', 'loading_state')],
              [Input('state-button', 'n_clicks')],
              [State('stock-input', 'value'),
               State('date-input', 'start_date'),
               State('date-input', 'end_date')])
def data_store(_, value, start, end):

    state_data = {}

    data = []
    invalid = []

    for symbol in value:
        info = yf.Ticker(symbol).history(start=start, end=end)["Close"]
        info_date = info.index.astype(str)

        if len(info) == 0:
            invalid.append(symbol)

        temp = [{date: str(info[date])} for date in info_date]
        data.append({symbol: temp})

    state_data["data"] = data
    state_data["invalid"] = invalid

    return json.dumps(state_data), {"is_loading": False}


@app.callback(Output('graph-div', 'children'),
              [Input('data-store', 'data')])
def update_ticker_graph(state_data):

    if state_data is None:
        raise dash.exceptions.PreventUpdate

    obj = json.loads(state_data)

    selected_tickers = [list(item.keys())[0] for item in obj['data']]

    data = []

    for info in obj["data"]:
        date_closed = list(info.values())[0]

        symbol = list(info.keys())[0]
        dateRange =[list(d.keys())[0] for d in date_closed]
        closePrice = [list(d.values())[0] for d in date_closed]

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

    return dcc.Graph(
        figure=dict(
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
    )

@app.callback(Output('card-output', 'children'),
              [Input('data-store', 'data')])
def callback_stats(state_data):

    if state_data is None:
        raise dash.exceptions.PreventUpdate

    obj = json.loads(state_data)
    selected_tickers = [list(item.keys())[0] for item in obj['data']]

    meta = []

    for symbol in selected_tickers:
        is_valid = True

        if symbol in obj["invalid"]:
            is_valid = False

        card = create_card(comp=symbol, founded=stocks_df.loc[symbol]['metadata']['founded'],
                        employees=stocks_df.loc[symbol]['metadata']['employees'], is_valid=is_valid)

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



