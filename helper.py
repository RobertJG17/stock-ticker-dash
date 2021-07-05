import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

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
                                    hidden=is_valid,
                                    style=dict(
                                        marginLeft="60px",
                                        fontWeight=100
                                    )
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

def create_graph(data, selected_tickers):
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


