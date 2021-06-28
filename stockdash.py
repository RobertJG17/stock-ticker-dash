import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd

import yfinance as yf
import pytickersymbols


# Initialize Application
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# Ticker / Company Info
sap_code = pytickersymbols.Statics().Indices().US_SP_500
sap_filter = pytickersymbols.PyTickerSymbols().get_stocks_by_index(index=sap_code)
sap_df = pd.DataFrame.from_records(sap_filter).set_index("symbol")
tickers = sap_df.index


# Helper Functions
def create_card(comp, founded, employees):
    return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(comp, className="card-title"),
                        html.P(f"Est: {founded}", className="card-text"),
                    ]
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
                fontFamily='Copperplate, fantasy'
            )
        ),

        html.Hr(),

        # LEVEL 1 Div holding inner divs for both of our DCC and H3 components
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Select Stock Name",

                            style=dict(
                                fontSize=30,
                                fontFamily='Frutiger, Frutiger Linotype, Univers, Calibri, Gill Sans, Gill Sans MT, Myriad Pro, Myriad,\
                 DejaVu Sans Condensed, Liberation Sans, Nimbus Sans L, Tahoma, Geneva, Helvetica Neue, \
                 Helvetica, Arial, sans-serif'
                            )
                        ),

                        # DROPDOWN MENU TO SELECT STOCK INDEX#

                        dcc.Dropdown(
                            id='stock-input',
                            options=[
                                dict(
                                    label=sap_df.loc[symbol]["name"],
                                    value=symbol
                                ) for symbol in tickers
                            ],

                            value=['TSLA', 'AAPL'],
                            multi=True,
                            searchable=True,
                            style=dict(
                                width="400px",
                                fontSize=24,
                                height="48px",
                                display="flex",
                                flexFlow="row",
                                flexWrap="wrap",
                                verticalAlign="middle"
                            )
                        )
                    ],

                    style=dict(
                        marginRight="10px"
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
                 Helvetica, Arial, sans-serif'
                            )
                        ),

                        # DCC DATE PICKER MENU
                        dcc.DatePickerRange(
                            id="date-input",
                            start_date='2016-01-04',
                            end_date='2017-12-29',
                            style=dict(
                                border=0

                            )
                        )
                    ]
                ),

                html.Div(
                    [
                        html.Button(
                            id="state-button",
                            children="Submit",

                        )
                    ],

                    style=dict(
                        marginTop="3%"
                    )
                )
            ],

            style=dict(
                display="flex",
                flexDirection="row",
                verticalAlign="middle",
                alignItems="center"
            )
        ),

        html.Hr(),

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
                            title="Closing Prices for: {}".format(', '.join(["TSLA", "AAPL"])),
                            xaxis=dict(
                                title="Date",
                            ),

                            yaxis=dict(
                                title="Closing Price",
                            ),

                            plot_bgcolor="black"
                        )
                    )
                )
            ]
        ),

        html.Hr(
            style=dict(
                marginTop="40px"
            )
        ),

        html.Div(
            [
                html.H1(
                    "Selected Company Info:",

                    style=dict(
                        fontFamily='Copperplate, fantasy'
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
        padding="40px"
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
                x=yf.download(symbol, start=start_date, end=end_date)["Close"].index,
                y=yf.download(symbol, start=start_date, end=end_date)["Close"].values,
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

            plot_bgcolor="black"
        )
    )


@app.callback(Output('card-output', 'children'),
              [Input('state-button', 'n_clicks')],
              [State('stock-input', 'value')])
def callback_stats(_, value):

    meta = []
    for val in value:
        card = create_card(comp=val, founded=sap_df.loc[val]['metadata']['founded'],
                        employees=sap_df.loc[val]['metadata']['employees'])

        meta.append(card)



    return dbc.Row(
        meta,

        style=dict(
            display="flex",
            justifyContent="center"
        )
    )


if __name__ == '__main__':
    app.run_server()
