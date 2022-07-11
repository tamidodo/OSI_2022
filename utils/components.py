from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import data_utils


def generate_usercomp(df, user, fitness):
    useridx = df.index[df["user_id"] == int(user)].to_list()[0]
    num_pat = len(df)
    if useridx == 0:
        usercomp = dmc.Text(
            f"Of the {num_pat} patients in the study, Patient {user} had the lowest total {fitness.lower()}"
        )
    elif useridx == num_pat - 1:
        usercomp = dmc.Text(
            f"Of the {num_pat} patients in the study, Patient {user} had the highest total {fitness.lower()}"
        )
    else:
        percentile = round((useridx + 1) / num_pat * 100, 2)
        usercomp = dmc.Text(
            f"Patient  had higher total {fitness.lower()} than {percentile}% of the {num_pat} patients in the study"
        )
    return usercomp


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


def controls():
    zangle = dmc.Select(
        id="zangle",
        label="Select the rotation angle in the x-y plane for the velocity vector at flyby (degrees)",
        data=data_utils.get_options("vi_angle"),
        value=0,
    )
    mass = dmc.Select(
        id="a_mass",
        label="Select the mass of Apophis (kg)",
        data=data_utils.get_options("Apophis_mass"),
        value=min(data_utils.get_options("Apophis_mass")),
    )
    return zangle, mass
