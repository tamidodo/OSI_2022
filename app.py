from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc
import datetime as dt

from utils import data_utils, figures
import utils.components as comp

app = Dash(__name__, title="OSI Satellite Simulations", update_title=None)
server = app.server

app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme": "light"},
    children=[
        ## Header and app description
        comp.header(
            app,
            header_background_color="#FFFFFF",
        ),
        ## Content
        dmc.Tabs(
            grow=True,
            variant="outline",
            children=[
                dmc.Tab(
                    label="Two-Satellite Simulation Results",
                    children=[
                        dmc.Grid(
                            justify="center",
                            gutter="xs",
                            children=[
                                dmc.Col(
                                    span=12,
                                    children=[
                                        dmc.Grid(
                                            class_name="card",
                                            children=[
                                                ## Simulation selection
                                                dmc.Col(
                                                    html.Div(
                                                        [
                                                            "Select velocity vector rotation angle in x-y plane at flyby (degrees)",
                                                            dcc.Dropdown(
                                                                id="zangle",
                                                                options=data_utils.get_options(
                                                                    "vi_angle"
                                                                ),
                                                                value=-10,
                                                            ),
                                                        ]
                                                    ),
                                                    span=6,
                                                ),
                                                dmc.Col(
                                                    html.Div(
                                                        [
                                                            "Select Apophis mass (solar masses)",
                                                            dcc.Dropdown(
                                                                id="a_mass",
                                                                options=data_utils.get_options(
                                                                    "Apophis_mass"
                                                                ),
                                                                value=min(
                                                                    data_utils.get_options(
                                                                        "Apophis_mass"
                                                                    )
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                    span=6,
                                                ),
                                                ## Details about 2 sat sim
                                                dmc.Col(
                                                    dmc.LoadingOverlay(
                                                        id="sat-sim-deets",
                                                        overlayOpacity=0.95,
                                                        overlayColor="rgb(246,246,246)",
                                                        loaderProps=dict(
                                                            color="violet",
                                                            variant="dots",
                                                        ),
                                                    ),
                                                    span=12,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                ## 4 FIGURES
                                dmc.Col(
                                    span=4,
                                    children=[
                                        html.Div(
                                            className="card",
                                            children=[
                                                dmc.LoadingOverlay(
                                                    dcc.Graph(
                                                        id="dist-fig",
                                                        className="glow",
                                                    ),
                                                    overlayOpacity=0.95,
                                                    overlayColor="rgb(246,246,246)",
                                                    loaderProps=dict(
                                                        color="violet", variant="bars"
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Col(
                                    span=4,
                                    children=[
                                        html.Div(
                                            className="card",
                                            children=[
                                                dmc.LoadingOverlay(
                                                    dcc.Graph(
                                                        id="dist-diff-fig",
                                                        className="glow",
                                                    ),
                                                    overlayOpacity=0.95,
                                                    overlayColor="rgb(246,246,246)",
                                                    loaderProps=dict(
                                                        color="violet", variant="bars"
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Col(
                                    span=4,
                                    children=[
                                        html.Div(
                                            className="card",
                                            children=[
                                                dmc.LoadingOverlay(
                                                    dcc.Graph(
                                                        id="diff-btwn-fig",
                                                        className="glow",
                                                    ),
                                                    overlayOpacity=0.95,
                                                    overlayColor="rgb(246,246,246)",
                                                    loaderProps=dict(
                                                        color="violet", variant="bars"
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Col(
                                    span=12,
                                    children=[
                                        html.Div(
                                            className="card",
                                            style={"height": "900px"},
                                            children=[
                                                dmc.LoadingOverlay(
                                                    dcc.Graph(
                                                        id="orbit-fig",
                                                        className="glow",
                                                        style={"height": "900px"},
                                                    ),
                                                    style={"height": "900px"},
                                                    overlayOpacity=0.95,
                                                    overlayColor="rgb(246,246,246)",
                                                    loaderProps=dict(
                                                        color="violet", variant="bars"
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Affix(
                            html.A(
                                "See code",
                                href="https://github.com/tamidodo/OSI_2022",
                                target="_blank",
                                className="demo-button",
                            ),
                            position={"bottom": 40, "left": 20},
                        ),
                    ],
                ),
                dmc.Tab(
                    label="Two Spheres from Single Satellite",
                    children=[
                        dmc.Grid(
                            justify="center",
                            gutter="xs",
                            children=[
                                dmc.Col(
                                    span=12,
                                    children=[
                                        dmc.Grid(
                                            class_name="card",
                                            children=[
                                                ## Simulation selection
                                                dmc.Col(
                                                    html.Div(
                                                        [
                                                            "Select velocity vector rotation angle in x-y plane at flyby (degrees)",
                                                            dcc.Dropdown(
                                                                id="ball-zangle",
                                                                options=data_utils.get_options(
                                                                    "vi_angle",
                                                                    ball=True,
                                                                ),
                                                                value=-10,
                                                            ),
                                                        ]
                                                    ),
                                                    span=6,
                                                ),
                                                dmc.Col(
                                                    html.Div(
                                                        [
                                                            "Select Apophis mass (solar masses)",
                                                            dcc.Dropdown(
                                                                id="ball-a_mass",
                                                                options=data_utils.get_options(
                                                                    "Apophis_mass",
                                                                    ball=True,
                                                                ),
                                                                value=min(
                                                                    data_utils.get_options(
                                                                        "Apophis_mass",
                                                                        ball=True,
                                                                    )
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                    span=3,
                                                ),
                                                dmc.Col(
                                                    html.Div(
                                                        [
                                                            "Select sphere relative speed (km/s)",
                                                            dcc.Dropdown(
                                                                id="ball-speed",
                                                                options=data_utils.get_options(
                                                                    "ball_speed",
                                                                    ball=True,
                                                                ),
                                                                value=data_utils.get_options(
                                                                    "ball_speed",
                                                                    ball=True,
                                                                )[
                                                                    3
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                    span=3,
                                                ),
                                                ## Details about ball sim
                                                dmc.Col(
                                                    dmc.LoadingOverlay(
                                                        id="ball-sim-deets",
                                                        overlayOpacity=0.95,
                                                        overlayColor="rgb(246,246,246)",
                                                        loaderProps=dict(
                                                            color="violet",
                                                            variant="dots",
                                                        ),
                                                    ),
                                                    span=12,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Col(
                                    span=12,
                                    children=[
                                        html.Div(
                                            className="card",
                                            style={"height": "900px"},
                                            children=[
                                                dmc.LoadingOverlay(
                                                    dcc.Graph(
                                                        id="ball-traj-fig",
                                                        className="glow",
                                                        style={"height": "900px"},
                                                    ),
                                                    style={"height": "900px"},
                                                    overlayOpacity=0.95,
                                                    overlayColor="rgb(246,246,246)",
                                                    loaderProps=dict(
                                                        color="violet", variant="bars"
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Affix(
                            html.A(
                                "See code",
                                href="https://github.com/tamidodo/OSI_2022",
                                target="_blank",
                                className="demo-button",
                            ),
                            position={"bottom": 40, "left": 20},
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    Output("sat-sim-deets", "children"),
    Output("dist-fig", "figure"),
    Output("orbit-fig", "figure"),
    Output("diff-btwn-fig", "figure"),
    Output("dist-diff-fig", "figure"),
    Input("zangle", "value"),
    Input("a_mass", "value"),
)
def make_two_sat_page(zangle, a_mass):
    info = dmc.Text(
        style={"text-align": "left"},
        children=f"Below are graphs of the distance from each of the satellites to Apophis over time and the 3D orbital path over the course of a few months. These are made using simulations where the mass of Apophis was {a_mass} kg and the angle of the satellite velocity vector was rotated in the x-y plane by {zangle} degrees from Apophis' velocity vector at the time of the closest flyby.",
    )
    dist_df = data_utils.dist_time(zangle, a_mass)
    dist_fig = figures.dist_fig(dist_df)
    dist_diff_fig = figures.dist_diff_fig(dist_df)
    dist_btwn_fig = figures.diff_btwn_fig(dist_df)
    (
        df_orbit_Earth,
        df_orbit_Ast,
        df_orbit_Sat1,
        df_orbit_Sat2,
        df_times,
    ) = data_utils.orbit_path(zangle, a_mass)
    orbit_fig = figures.orbital_fig(
        df_orbit_Earth, df_orbit_Ast, df_orbit_Sat1, df_orbit_Sat2
    )
    return (info, dist_fig, orbit_fig, dist_diff_fig, dist_btwn_fig)


@callback(
    Output("ball-sim-deets", "children"),
    Output("ball-traj-fig", "figure"),
    Input("ball-zangle", "value"),
    Input("ball-a_mass", "value"),
    Input("ball-speed", "value"),
)
def make_ball_sat_page(zangle, a_mass, b_speed):
    info = dmc.Text(
        style={"text-align": "left"},
        children=f"Below is a graph showing the trajectories of the Earth, Apophis, a single satellite and two spheres released from the satellite with {b_speed} km/s relative velocity away and towards Apophis, over the course of a few months. These are made using simulations where the mass of Apophis was {a_mass} kg and the angle of the satellite velocity vector was rotated in the x-y plane by {zangle} degrees from Apophis' velocity vector at the time of the closest flyby.",
    )
    df_traj = data_utils.ball_paths(zangle, a_mass, b_speed)
    traj_fig = figures.ball_traj_fig(df_traj)
    return (info, traj_fig)


if __name__ == "__main__":
    app.run_server(debug=True)
