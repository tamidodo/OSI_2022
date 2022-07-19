import plotly.express as px
import plotly.graph_objects as go


def fig_style(fig):
    return (
        fig.update_layout(
            paper_bgcolor="#1c2022", plot_bgcolor="#1c2022", font_color="#A3AAB7"
        )
        .update_xaxes(gridcolor="#3F3F3F")
        .update_yaxes(gridcolor="#3F3F3F")
    )


def orbital_fig(df_Earth, df_Ast, df_Sat1, df_Sat2):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=df_Earth["x"],
            y=df_Earth["y"],
            z=df_Earth["z"],
            mode="markers",
            marker=dict(size=3),
            name="Earth",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_Ast["x"],
            y=df_Ast["y"],
            z=df_Ast["z"],
            mode="markers",
            marker=dict(size=3),
            name="Apophis",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_Sat1["x"],
            y=df_Sat1["y"],
            z=df_Sat1["z"],
            mode="markers",
            marker=dict(size=3),
            name="Satellite 1",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=df_Sat2["x"],
            y=df_Sat2["y"],
            z=df_Sat2["z"],
            mode="markers",
            marker=dict(size=3),
            name="Satellite 2",
        )
    )
    fig.update_layout(legend_title_text="Objects", title="Orbital Path")
    return fig_style(fig)


def dist_fig(df_dist):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_dist["times"],
            y=df_dist["dist1"],
            mode="markers",
            marker=dict(size=3),
            name="Distance to Satellite 1",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_dist["times"],
            y=df_dist["dist2"],
            mode="markers",
            marker=dict(size=3),
            name="Distance to Satellite 2",
        )
    )
    fig.update_layout(title="Distance from Apophis over time", legend_y=1, legend_x=0)
    fig.update_xaxes(title_text="Sim Time (days)", range=[0, 0.17 * 365.25])
    fig.update_yaxes(title_text="Distance (km)")
    return fig_style(fig)


def dist_diff_fig(df_dist):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_dist["times"],
            y=df_dist["diff"],
            mode="markers",
            marker=dict(size=3),
            name="Difference in distance",
        )
    )
    fig.update_layout(title="Difference in distance to Apophis")
    fig.update_xaxes(title_text="Sim Time (days)", range=[0, 0.17 * 365.25])
    fig.update_yaxes(title_text="Difference in distance (km)")
    return fig_style(fig)


def diff_btwn_fig(df_btwn):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_btwn["times"],
            y=df_btwn["dist_btwn"],
            mode="markers",
            marker=dict(size=3),
            name="Distance between satellites",
        )
    )
    fig.update_layout(title="Distance between satellites over time")
    fig.update_xaxes(title_text="Sim Time (days)", range=[0, 0.17 * 365.25])
    fig.update_yaxes(title_text="Difference in distance (km)")
    return fig_style(fig)
