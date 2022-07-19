import numpy as np
import pandas as pd


def clean_data(fname, datatype):
    """
    Takes the filename of a valid simulation dataset and does preliminary cleaning based on data type
    Returns a cleaned dataframe
    """
    if datatype == "spatial":
        dfspatial = pd.read_csv(fname)
        dfsb = dfspatial[dfspatial["dt"] < 0]
        dfsb = dfsb.reset_index().drop(
            columns=["dt", "vi_angle", "Apophis_mass", "rowtype", "index"]
        )
        dfsf = dfspatial[dfspatial["dt"] > 0]
        dfsf = dfsf.reset_index().drop(columns=["dt", "index"])
        dfs_clean = pd.concat([dfsb, dfsf], axis=1)
        return dfs_clean
    elif datatype == "distance":
        dfdist = pd.read_csv(fname)
        return dfdist
    else:
        print("not a valid dataset/data type")


def get_options(option_type):
    """
    Takes one of 'vi_angle', 'Apophis_mass' as input
    Returns the unique options for the parameter
    """
    df = pd.read_csv("sat_sim_spatial.csv")
    df_options = df[option_type].unique().tolist()
    return df_options


def dist_time(df, zangle, a_mass):
    """
    Takes a rotation angle and mass for Apophis as input
    Returns the dataframe to make the distance/time graph
    """
    times_f = np.linspace(0, 0.17 * 365.25, 100)
    times_b = np.linspace(0, -0.17 * 365.25, 100)
    times = np.concatenate((times_f, times_b))
    subset = (df["vi_angle"] == zangle) & (df["Apophis_mass"] == a_mass)
    df_dist = df[(subset)]
    df_dist = df_dist.drop(columns=["vi_angle", "Apophis_mass"])
    df1 = (
        df_dist[df_dist["rowtype"] == "dist1"]
        .drop(columns=["rowtype", "dt"])
        .reset_index()
        .drop(columns="index")
    )
    df1.columns = ["dist1"]
    df2 = (
        df_dist[df_dist["rowtype"] == "dist2"]
        .drop(columns=["dt", "rowtype"])
        .reset_index()
        .drop(columns="index")
    )
    df2.columns = ["dist2"]
    df_dist = pd.concat([df1, df2], axis=1)
    df_dist["diff"] = df_dist["dist2"] - df_dist["dist1"]
    df_dist["times"] = times
    return df_dist


def orbit_path(df, zangle, a_mass):
    """
    Takes a rotation angle and mass for Apophis as input
    Returns the dataframe to make the 3d orbital path graph
    """
    subset = (df["vi_angle"] == zangle) & (df["Apophis_mass"] == a_mass)
    df_orbit = df[(subset)]
    df_orbit = df_orbit.drop(columns=["vi_angle", "Apophis_mass"])
    df_orbit = df_orbit.set_index("rowtype").T
    df_orbit_Earth = df_orbit.iloc[:, ::4]
    df_orbit_Ast = df_orbit.iloc[:, 1::4]
    df_orbit_Sat1 = df_orbit.iloc[:, 2::4]
    df_orbit_Sat2 = df_orbit.iloc[:, 3::4]
    df_dist_btwn = (
        np.sqrt(
            np.square(df_orbit_Sat2["x"] - df_orbit_Sat1["x"])
            + np.square(df_orbit_Sat2["y"] - df_orbit_Sat1["y"])
            + np.square(df_orbit_Sat2["z"] - df_orbit_Sat1["z"])
        )
        * 1.496e8
    )
    df_dist_btwn = df_dist_btwn.to_frame(name="dist_btwn")
    times_f = np.linspace(0, 0.17 * 365.25, 100)
    times_b = np.linspace(0, -0.17 * 365.25, 100)
    times = np.concatenate((times_f, times_b))
    df_dist_btwn["times"] = times
    return df_orbit_Earth, df_orbit_Ast, df_orbit_Sat1, df_orbit_Sat2, df_dist_btwn
