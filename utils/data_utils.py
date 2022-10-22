import numpy as np
import pandas as pd

df = pd.read_csv("osi_sat_sim_results_closer.csv")
dfball = pd.read_csv("osi_ball_sim_results.csv")


def get_options(option_type, ball=False):
    """
    Takes one of 'vi_angle', 'Apophis_mass' as input
    Returns the unique options for the parameter
    """
    if ball:
        df_options = dfball[option_type].unique().tolist()
    else:
        df_options = df[option_type].unique().tolist()
    return df_options


def ball_paths(zangle, a_mass, ball_speed):
    """
    Takes a rotation angle, mass for Apophis and relative speed of the balls as input
    Returns the dataframe to make the ball trajectory graphs
    """
    subset = (
        (dfball["vi_angle"] == zangle)
        & (dfball["Apophis_mass"] == a_mass)
        & (dfball["ball_speed"] == ball_speed)
    )
    df_traj = dfball[(subset)]
    df_traj = df_traj.drop(columns=["vi_angle", "Apophis_mass", "ball_speed"])
    df_traj = df_traj.set_index("rowtype").T
    return df_traj


def ball_dists(df_traj):
    distLBall = np.sqrt(
        np.square(df_traj["xLBall"] - df_traj["xSat"])
        + np.square(df_traj["yLBall"] - df_traj["ySat"])
        + np.square(df_traj["zLBall"] - df_traj["zSat"])
    )
    distRBall = np.sqrt(
        np.square(df_traj["xRBall"] - df_traj["xSat"])
        + np.square(df_traj["yRBall"] - df_traj["ySat"])
        + np.square(df_traj["zRBall"] - df_traj["zSat"])
    )
    print("left", distLBall)
    print("right", distRBall)
    return


def dist_time(zangle, a_mass):
    """
    Takes a rotation angle and mass for Apophis as input
    Returns the dataframe to make all distance/time type graphs
    """
    times = np.linspace(0, 0.17 * 365.25, 200)
    subset = (
        (df["vi_angle"] == zangle)
        & (df["Apophis_mass"] == a_mass)
        & (df["rowtype"].str.contains("dist"))
    )
    df_dist = df[(subset)]
    df_dist = df_dist.drop(columns=["vi_angle", "Apophis_mass"])
    df_dist = df_dist.set_index("rowtype").T
    df_dist["times"] = times
    return df_dist


def orbit_path(zangle, a_mass):
    """
    Takes a rotation angle and mass for Apophis as input
    Returns the dataframe to make the 3d orbital path graph
    """
    subset = (
        (df["vi_angle"] == zangle)
        & (df["Apophis_mass"] == a_mass)
        & (~df["rowtype"].str.contains("dist"))
    )
    df_orbit = df[(subset)]
    df_orbit = df_orbit.drop(columns=["vi_angle", "Apophis_mass"])
    df_orbit = df_orbit.set_index("rowtype").T
    df_orbit_Earth = df_orbit.iloc[:, ::4]
    df_orbit_Ast = df_orbit.iloc[:, 1::4]
    df_orbit_Sat1 = df_orbit.iloc[:, 2::4]
    df_orbit_Sat2 = df_orbit.iloc[:, 3::4]
    times = np.linspace(0, 0.17 * 365.25, 200)
    dftimes = pd.DataFrame(times, columns=["times"])
    return df_orbit_Earth, df_orbit_Ast, df_orbit_Sat1, df_orbit_Sat2, dftimes
