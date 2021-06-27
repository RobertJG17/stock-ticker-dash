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
app = dash.Dash()


# TICKER / COMPANY INFO
sap_code = pytickersymbols.Statics().Indices().US_SP_500
sap_filter = pytickersymbols.PyTickerSymbols().get_stocks_by_index(index=sap_code)
sap_df = pd.DataFrame.from_records(sap_filter).set_index("symbol")
tickers = sap_df.index


# MAIN APPLICATION LAYOUT
app.layout = html.Div(
    [
        html.H1(
            "Stock Ticker Dashboard"
        ),

        # LEVEL 1 Div holding inner divs for both of our DCC and H3 components
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Select Stock Name"
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
                                width="400px"
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
                            "Select Start and End Dates"
                        ),

                        # DCC DATE PICKER MENU
                        dcc.DatePickerRange(
                            id="date-input",
                            start_date='2016-01-04',
                            end_date='2017-12-29',
                            style=dict(
                                font="Times New Roman"
                            )
                        ),

                        html.Button(
                            id="state-button",
                            children="Submit",
                            style=dict(
                                height="43%"
                            )
                        )
                    ]
                )
            ],

            style=dict(
                display="flex",
                flexDirection="row"
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
                            title="Closing Prices for: {}".format(', '.join(["TSLA", "AAPL"])),
                            xaxis=dict(
                                title="Date",
                            ),

                            yaxis=dict(
                                title="Closing Price",
                            )
                        )
                    )
                )
            ]
        ),

        html.Div(
            [

                dbc.CardGroup(
                    id='card-group',
                )
            ],

            style=dict(
                fontSize=20
            )
        )
    ]
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
            )
        )
    )


@app.callback(Output('div-card', 'children'),
              [Input('state-button', 'n_clicks')],
              [State('stock-input', 'value')])
def callback_stats(_, value):
    meta = [
        # dbc.Card(
        #
        # ),
        f"""
        ```
            Company: {sap_df.loc[data]['name']}
            Founded: {sap_df.loc[data]['metadata']['founded']}
            Employees: {sap_df.loc[data]['metadata']['employees']}
        ```
        """
    for data in value]

    return meta


if __name__ == '__main__':
    app.run_server()
