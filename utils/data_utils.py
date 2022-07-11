import numpy as np
import pandas as pd

df = pd.read_csv("osi_sat_sim_results.csv")
df["Apophis_mass"] = df["Apophis_mass"] * 1.98847e30
times = np.linspace(0, 0.17, 100)
dfb = df[df["dt"] < 0]
dfb.drop(columns=["dt", "vi_angle", "Apophis_mass", "rowtype"])
dff = df[df["dt"] > 0]
dff.drop(columns=["dt"])
df_clean = pd.concat([dfb, dff], axis=1)


def get_options(option_type):
    """
    Takes one of 'vi_angle', 'Apophis_mass' as input
    Returns the unique options for the parameter
    """
    df_options = dfb[option_type].unique().tolist()
    return df_options


def dist_time(zangle, a_mass):
    """
    Takes a rotation angle and mass for Apophis as input
    Returns the dataframe to make the distance/time graph
    """
    times_f = np.linspace(0, 0.17, 100)
    times_b = np.linspace(-0.17, 0, 100)
    times = np.concatenate((times_b, times_f))
    subset = (df_clean["rowtype"] == "dist1") | (df_clean["rowtype"] == "dist2") & (
        df_clean["vi_angle"] == zangle
    ) & (df_clean["Apophis_mass"] == a_mass)
    df_dist = df_clean[subset]
    df_dist.drop(columns=["vi_angle", "Apophis_mass"])
    df_dist = df_dist.set_index("rowtype").T
    df_dist["times"] = times
    df_dist["diff"] = df_dist["dist2"] - df_dist["dist1"]
    return df_dist


def orbit_path(zangle, a_mass):
    """
    Takes a rotation angle and mass for Apophis as input
    Returns the dataframe to make the 3d orbital path graph
    """
    subset = (
        (df_clean["rowtype"] == "x")
        | (df_clean["rowtype"] == "y")
        | (df_clean["rowtype"] == "z")
        & (df_clean["vi_angle"] == zangle)
        & (df_clean["Apophis_mass"] == a_mass)
    )
    df_orbit = df_clean[subset]
    df_orbit.drop(columns=["vi_angle", "Apophis_mass"])
    df_orbit = df_orbit.set_index("rowtype").T
    df_orbit_Earth = df_orbit.iloc[:, ::4]
    df_orbit_Ast = df_orbit.iloc[:, 1::4]
    df_orbit_Sat1 = df_orbit.iloc[:, 2::4]
    df_orbit_Sat2 = df_orbit.iloc[:, 3::4]
    return df_orbit_Earth, df_orbit_Ast, df_orbit_Sat1, df_orbit_Sat2
