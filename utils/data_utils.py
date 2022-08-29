import numpy as np
import pandas as pd

df = pd.read_csv("osi_sat_sim_results_closer.csv")


def get_options(option_type):
    """
    Takes one of 'vi_angle', 'Apophis_mass' as input
    Returns the unique options for the parameter
    """
    df_options = df[option_type].unique().tolist()
    return df_options


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
