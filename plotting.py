import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from consts import *

cmap = ['r', 'g', 'b', 'y', 'c', 'k']

def filter_lat(df, r):
    return df.loc[(df['Latitude'] >= r[0]) & (df['Latitude'] <= r[1])]

def cal_mean_avg(df, pos, col_name):
    def custom_round(x, base=20):
        return int(base * round(float(x)/base))
    df["GPS_Alt"] = df["GPS_Alt"].apply(lambda x: custom_round(x, pos)) # round to a certain position
    def pop_std(x):
        return x.std(ddof=0)
    df = df.groupby(['GPS_Alt'], as_index=False).agg({col_name:['mean', pop_std]}) # calculate std and average
    df.columns = ['GPS_Alt',col_name,'STD']
    df.reindex(columns=sorted(df.columns))
    return df

def plot_OA(r, fac):
    pname = os.path.join(cur_dir, "Plots", "{}_{}-{}.png".format("OA", r[0], r[1]))
    for i, n in enumerate(["NOP_Adf_0813.txt", "NOP_Adf_0815.txt", "NOP_Adf_0826.txt", "NOP_Adf_0828.txt"]):
        dname = os.path.join(cur_dir, "FilteredData", "PlatformFiltered", n)
        fields = ["Latitude", "GPS_Alt", "ORG"]
        df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
        df = filter_lat(df, r)
        df = cal_mean_avg(df, len(df)/fac, "ORG")
        label = n.replace("NOP_Adf_", "OA ")
        label = label.replace(".txt", "")
        plt.plot(df["ORG"], df['GPS_Alt'], c=cmap[i], label=label) # plot mean values
        plt.legend()
    plt.savefig(pname)

def plot_others(r, tp, fac):
    pname = os.path.join(cur_dir, "Plots", "MA_{}_{}-{}.png".format(tp, r[0], r[1]))
    f_dir = os.path.join(cur_dir, "FilteredData", "PlatformFiltered")
    for i, n in enumerate(os.listdir(f_dir)):
        dname = os.path.join(f_dir, n)
        fields = ["Latitude", "GPS_Alt", params[tp]]
        df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
        df = filter_lat(df, r)
        df = cal_mean_avg(df, len(df)/fac, params[tp])
        df['MA_alt'] = df['GPS_Alt'].rolling(window=5).mean()
        df['MA_val'] = df[params[tp]].rolling(window=5).mean()
        label = n.replace("NOP_Adf_", tp+" ")
        label = label.replace(".txt", "")
        plt.plot(df['MA_val'], df['MA_alt'], c=cmap[i], label=label) # plot mean values
        plt.legend()
    plt.savefig(pname)

if __name__ == "__main__":
    for i, r in enumerate(lat_range):
        plot_others(r, "CCN", 100)
        plt.clf()
        plot_others(r, "CO", 100)
        plt.clf()
        plot_others(r, "BC", 100)
        plt.clf()
        plot_OA(r, 100)
        plt.clf()