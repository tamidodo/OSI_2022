import plotly.graph_objects as go
from plotly.validators import DataValidator


def fig_style(fig):
    return (
        fig.update_layout(
            paper_bgcolor="#d1d1d1",
            plot_bgcolor="#d1d1d1",
            font_color="#2B3956",
            legend_bgcolor="#ffffff",
        )
        .update_xaxes(gridcolor="#ffffff")
        .update_yaxes(gridcolor="#ffffff")
    )


def ball_traj_fig(df_traj):
    """Returns figure of trajectories for Earth, Apophis, Satellite, Spheres"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=df_traj["xEarth"],
            y=df_traj["yEarth"],
            z=df_traj["zEarth"],
            mode="markers",
            marker=dict(size=3, color="#0948BA"),
            name="Earth",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_traj["xApophis"],
            y=df_traj["yApophis"],
            z=df_traj["zApophis"],
            mode="markers",
            marker=dict(size=3, color="#E6391A"),
            name="Apophis",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_traj["xSat"],
            y=df_traj["ySat"],
            z=df_traj["zSat"],
            mode="markers",
            marker=dict(size=3, color="#ad9176"),
            name="Satellite",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_traj["xLBall"],
            y=df_traj["yLBall"],
            z=df_traj["zLBall"],
            mode="markers",
            marker=dict(size=3, color="#635170"),
            name="Sphere Towards",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_traj["xRBall"],
            y=df_traj["yRBall"],
            z=df_traj["zRBall"],
            mode="markers",
            marker=dict(size=3, color="#E6D1FF"),
            name="Sphere Away",
        )
    )
    fig.update_layout(
        legend_title_text="Objects",
        title="Trajectory",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, orientation="h"),
    )
    return fig_style(fig)


def ball_diff_fig(df_traj):
    return


def orbital_fig(df_Earth, df_Ast, df_Sat1, df_Sat2):
    """Returns figure of orbital paths for Earth, Apophis, Sat1 and Sat2"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=df_Earth["x"],
            y=df_Earth["y"],
            z=df_Earth["z"],
            mode="markers",
            marker=dict(size=3, color="#0948BA"),
            name="Earth",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_Ast["x"],
            y=df_Ast["y"],
            z=df_Ast["z"],
            mode="markers",
            marker=dict(size=3, color="#E6391A"),
            name="Apophis",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_Sat1["x"],
            y=df_Sat1["y"],
            z=df_Sat1["z"],
            mode="markers",
            marker=dict(size=3, color="#ad9176"),
            name="Satellite 1",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_Sat2["x"],
            y=df_Sat2["y"],
            z=df_Sat2["z"],
            mode="markers",
            marker=dict(size=3, color="#635170"),
            name="Satellite 2",
        )
    )
    fig.update_layout(
        legend_title_text="Objects",
        title="Orbital Path",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, orientation="h"),
    )
    return fig_style(fig)


def dist_fig(df_dist):
    """Returns figure showing the distances of the Satellites from Apophis over time"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_dist["times"],
            y=df_dist["dist1"],
            mode="markers",
            marker=dict(size=3, color="#ad9176"),
            name="Distance to Satellite 1",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_dist["times"],
            y=df_dist["dist2"],
            mode="markers",
            marker=dict(size=3, color="#635170"),
            name="Distance to Satellite 2",
        )
    )
    fig.update_layout(title="Distance from Apophis over time", legend_y=1, legend_x=0)
    fig.update_xaxes(title_text="Sim Time (days)", range=[0, 0.17 * 365.25])
    fig.update_yaxes(title_text="Distance (km)")
    return fig_style(fig)


def dist_diff_fig(df_dist):
    """Returns the figure showing the difference in distance to Apophis between the two Satellites"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_dist["times"],
            y=df_dist["distdiff"],
            mode="markers",
            marker=dict(size=3, color="#635170"),
            name="Difference in distance",
        )
    )
    fig.update_layout(title="Difference in distance to Apophis")
    fig.update_xaxes(title_text="Sim Time (days)", range=[0, 0.17 * 365.25])
    fig.update_yaxes(title_text="Difference in distance (km)")
    return fig_style(fig)


def diff_btwn_fig(df_dist):
    """Returns the figure showing the distance between the satellites over time"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_dist["times"],
            y=df_dist["distbtwnsats"],
            mode="markers",
            marker=dict(size=3, color="#635170"),
            name="Distance between satellites",
        )
    )
    fig.update_layout(title="Distance between satellites over time")
    fig.update_xaxes(title_text="Sim Time (days)", range=[0, 0.17 * 365.25])
    fig.update_yaxes(title_text="Difference in distance (km)")
    return fig_style(fig)
