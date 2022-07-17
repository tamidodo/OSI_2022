from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc
import datetime as dt

from utils import data_utils, figures
import utils.components as comp

app = Dash(__name__, title="OSI Satellite Simulations", update_title=None)
server = app.server

app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme": "dark"},
    children=[
        ## Header and app description
        comp.header(
            app,
            "#FFFFFF",
            header_background_color="#111014",
        ),
        ## Content
        html.Div(
            [
                dmc.Grid(
                    justify="center",
                    gutter="xl",
                    children=[
                        dmc.Col(
                            span=10,
                            children=[
                                dmc.Grid(
                                    class_name="card",
                                    children=[
                                        ## Simulation selection
                                        html.Div(
                                            [
                                                "Select the rotation angle in the x-y plane for the velocity vector at flyby (degrees)",
                                                dcc.Dropdown(
                                                    id="zangle",
                                                    options=data_utils.get_options(
                                                        "vi_angle"
                                                    ),
                                                    value=0,
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                "Select the mass of Apophis (solar masses)",
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
                                        ## USER TEXT INFO 1
                                        dmc.Col(
                                            dmc.LoadingOverlay(
                                                id="sat-sim-deets",
                                                overlayOpacity=0.95,
                                                overlayColor="#1D2022",
                                                loaderProps=dict(
                                                    color="orange", variant="dots"
                                                ),
                                                class_name="user-demo-border",
                                            ),
                                            span=10,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ## 3 FIGURES
                        dmc.Col(
                            span=6,
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
                                            overlayColor="#1D2022",
                                            loaderProps=dict(
                                                color="orange", variant="bars"
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Col(
                            span=6,
                            children=[
                                html.Div(
                                    className="card",
                                    children=[
                                        dmc.LoadingOverlay(
                                            dcc.Graph(
                                                id="orbit-fig",
                                                className="glow",
                                            ),
                                            overlayOpacity=0.95,
                                            overlayColor="#1D2022",
                                            loaderProps=dict(
                                                color="orange", variant="bars"
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dmc.Col(
                            span=10,
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
                                            overlayColor="#1D2022",
                                            loaderProps=dict(
                                                color="orange", variant="bars"
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
)


@callback(
    Output("sat-sim-deets", "children"),
    Output("dist-fig", "figure"),
    Output("orbit-fig", "figure"),
    Output("dist-diff-fig", "figure"),
    Input("zangle", "value"),
    Input("a_mass", "value"),
)
def make_page(zangle, a_mass):
    dfdist = data_utils.clean_data("sat_sim_dist.csv", "distance")
    dfspatial = data_utils.clean_data("sat_sim_spatial.csv", "spatial")
    info = dmc.Text(
        f"Below are graphs of the distance from each of the satellites to Apophis over time and the 3D orbital path over the course of a few months. These are made using simulations where the mass of Apophis was {a_mass} kg and the angle of the satellite velocity vector was rotated in the x-y plane by {zangle} degrees from Apophis' velocity vector at the time of the closest flyby."
    )
    dist_df = data_utils.dist_time(dfdist, zangle, a_mass)
    dist_fig = figures.dist_fig(dist_df)
    dist_diff_fig = figures.dist_diff_fig(dist_df)
    df_orbit_Earth, df_orbit_Ast, df_orbit_Sat1, df_orbit_Sat2 = data_utils.orbit_path(
        dfspatial, zangle, a_mass
    )
    orbit_fig = figures.orbital_fig(
        df_orbit_Earth, df_orbit_Ast, df_orbit_Sat1, df_orbit_Sat2
    )
    return (info, dist_fig, orbit_fig, dist_diff_fig)


if __name__ == "__main__":
    app.run_server(debug=True)
