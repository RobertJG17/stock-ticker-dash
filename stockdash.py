import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pytickersymbols
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd

import yfinance as yf
from pytickersymbols import PyTickerSymbols, Statics


# Initialize Application

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


# Ticker / Company Info
pytick = PyTickerSymbols()
index = Statics.Indices.US_NASDAQ
stocks_df = pd.DataFrame.from_records(pytick.get_stocks_by_index(index=index)).set_index("symbol")

tickers = stocks_df.index

print(stocks_df["metadata"])


# Helper Functions
def create_card(comp, founded, employees):

    employees = "N/A" if employees == '' else employees

    return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(comp, className="card-title"),
                        html.P(f"Est: {founded}", className="card-text"),
                    ],

                    style=dict(
                        fontFamily="Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                            DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                            Helvetica, Arial, sans-serif"
                    )
                ),
                dbc.CardFooter(f"Employees: {employees}"),
            ],

            style=dict(
                width="18rem",
                margin="5px"
            )
    )


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
                fontWeight=200,
            )
        ),

        html.Hr(
            style=dict(
                backgroundColor="white"
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
                                fontWeight=100
                            )
                        ),

                        # DROPDOWN MENU TO SELECT STOCK INDEX#

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
                                width="400px",
                                fontSize=24,
                                height="48px",
                                display="inline-block",
                                backgroundColor="black"
                            )

                        )
                    ],

                    style=dict(
                        # marginRight="10px",
                        # marginTop="5px",
                        # flexDirection="row"
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
                                fontWeight=100
                            )
                        ),

                        html.Div(
                            [
                                # DCC DATE PICKER MENU
                                dcc.DatePickerRange(
                                    id="date-input",
                                    start_date='2016-01-04',
                                    end_date='2017-12-29',
                                    style=dict(
                                        height="48px"
                                    )
                                ),

                                dbc.Button(
                                    id="state-button",
                                    children="Submit",
                                    style=dict(
                                        marginLeft="10px",
                                        height="48px"
                                    )
                                )
                            ]
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
        )
    ],
    style=dict(
        padding="40px",
        backgroundColor="black"
    )
)


@app.callback(Output('graph-output', 'figure'),
              [Input('state-button', 'n_clicks')],
              [State('stock-input', 'value'),
               State('date-input', 'start_date'),
               State('date-input', 'end_date')])
def update_ticker_graph(_, symbols, start_date, end_date):

    return dict(
        data=[
            go.Scatter(
                x=yf.download(symbol, start=start_date, end=end_date, progress = False)["Close"].index,
                y=yf.download(symbol, start=start_date, end=end_date, progress= False)["Close"].values,
                mode="lines",
                name=symbol,
                line=dict(
                    width=1
                )
            ) for symbol in symbols
        ],
        layout=go.Layout(
            title="Closing Prices for: {}".format(', '.join(symbols)),
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
              [Input('state-button', 'n_clicks')],
              [State('stock-input', 'value')])
def callback_stats(_, value):

    meta = []
    for val in value:
        card = create_card(comp=val, founded=stocks_df.loc[val]['metadata']['founded'],
                        employees=stocks_df.loc[val]['metadata']['employees'])

        meta.append(card)



    return dbc.Row(
        meta,

        style=dict(
            display="flex",
            justifyContent="center"
        )
    )


if __name__ == '__main__':
    app.run_server('0.0.0.0', 5001)



# .DayPicker_focusRegion.DayPicker_focusRegion_1 {
#     background-color:grey;
# }
#
# .CalendarMonth.CalendarMonth_1 {
#     background-color:grey;
#     font-color:white;
# }
#
# .CalendarMonthGrid.CalendarMonthGrid_1.CalendarMonthGrid__horizontal.CalendarMonthGrid__horizontal_2 {
#     background-color:grey;
# }

