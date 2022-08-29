from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import data_utils


def header(app, subheader=None, header_background_color="transparent"):

    logo = html.Img(src=app.get_asset_url("images/osi_logo.png"))
    osi_logo = html.A(
        logo,
        href="http://outerspaceinstitute.ca/",
        target="_blank",
        className="header-logos-left",
    )

    header = html.Div(
        [
            html.Div(
                [
                    html.Div("OSI Satellite Simulations", style={"color": "#2B3956"}),
                ],
                className="header-title",
            ),
            html.Div(subheader, className="subheader-title"),
        ],
        className="header-text-middle",
    )

    return html.Div(
        [osi_logo, header],
        className="header",
        style={"background-color": header_background_color},
    )
