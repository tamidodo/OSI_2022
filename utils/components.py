from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import data_utils


def header(app, header_color, subheader=None, header_background_color="transparent"):

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
                    html.Div("OSI", style={"color": "#7976F7"}),
                    html.Div(" Satellite Simulations ", style={"padding": "0px 15px"}),
                ],
                className="header-title",
            ),
            html.Div(subheader, className="subheader-title"),
        ],
        style={"color": header_color},
        className="header-text-middle",
    )

    return html.Div(
        [osi_logo, header],
        className="header",
        style={"background-color": header_background_color},
    )
