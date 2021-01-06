import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from consts import *
from data_management import *
from calculate_correlations import *

cmap = ['r', 'green', 'b', 'orange', 'purple', 'k']

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

def plot_OA(l, r, t, directory, fac, window):
    pname = os.path.join(cur_dir, "Plots", "MA_{}_{}_{}-{}.png".format(directory, "OA", r[0], r[1]))
    if window == 1:
        pname = "N" + pname
    for i, n in enumerate(["Adf_0813.txt", "Adf_0815.txt", "Adf_0826.txt", "Adf_0828.txt"]):
        dname = os.path.join(cur_dir, "FilteredData", directory, n)
        fields = ["Latitude", "GPS_Alt", "ORG"]
        df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
        df = filter_lat(df, r)
        df = cal_mean_avg(df, len(df)/fac, "ORG")
        df['MA_alt'] = df['GPS_Alt'].rolling(window=window).mean()
        df['MA_val'] = df["ORG"].rolling(window=window).mean()
        label = n.replace("Adf_", "OA ")
        label = label.replace(".txt", "")
        plt.plot(df["ORG"], df['GPS_Alt'], linewidth=3, c=cmap[i], label=label) # plot mean values
        plt.ylabel("Altitude (m)", fontsize=14)
        plt.xlabel("OA "+units["OA"], fontsize=14)
        plt.ylim([0, 6700])
        plt.title("({})".format(l), loc='left', fontsize=15)
        plt.title("{}".format(t), loc='center', fontsize=15)
        plt.legend(loc="upper right", prop={'size': 13})
    plt.tight_layout() 
    plt.savefig(pname)
    plt.clf()

def plot_others(l, r, t, directory, tp, fac, window):
    pname = os.path.join(cur_dir, "Plots", "MA_{}_{}_{}-{}.png".format(directory, tp, r[0], r[1]))
    if window == 1:
        pname = "N" + pname
    f_dir = os.path.join(cur_dir, "FilteredData", directory)
    for i, n in enumerate(os.listdir(f_dir)):
        dname = os.path.join(f_dir, n)
        fields = ["Latitude", "GPS_Alt", params[tp]]
        df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
        df = filter_lat(df, r)
        df = cal_mean_avg(df, len(df)/fac, params[tp])
        df['MA_alt'] = df['GPS_Alt'].rolling(window=window).mean()
        df['MA_val'] = df[params[tp]].rolling(window=window).mean()
        label = n.replace("Adf_", tp+" ")
        label = label.replace(".txt", "")
        plt.plot(df['MA_val'], df['MA_alt'], linewidth=3, c=cmap[i], label=label) # plot mean values
        plt.ylabel("Altitude (m)", fontsize=14)
        plt.xlabel(tp+" "+units[tp], fontsize=14)
        plt.ylim([0, 6700])
        plt.title("({})".format(l), loc='left', fontsize=15)
        plt.title("{}".format(t), loc='center', fontsize=15)
        plt.legend(loc="upper right", prop={'size': 13})
    plt.tight_layout() 
    plt.savefig(pname)
    plt.clf()

def plot_cor_in_time():
    bc = getBCRatioByTime_df()
    oa = getOARatioByTime_df()
    bc.to_csv(os.path.join(cur_dir, "cor_csvs", "inTime_bc.csv"))
    oa.to_csv(os.path.join(cur_dir, "cor_csvs", "inTime_oa.csv"))
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.errorbar(bc['Date'], bc['FT_BC/dCO'], yerr=bc['FT_BC/dCO.STD'], c='b', capsize=4, fmt='o', mfc='white', label='FT')
    ax1.errorbar(bc['Date'], bc['BL_BC/dCO'], yerr=bc['BL_BC/dCO.STD'], c='r', capsize=4, fmt='o', mfc='white', label='BL')
    ax1.set_ylabel("BC/dCO \n$ng/{m^{3}}  /  ppbv$")
    ax1.legend()
    ax2.errorbar(oa['Date'], oa['FT_OA/dCO'], yerr=oa['FT_OA/dCO.STD'], c='b', capsize=4, fmt='o', mfc='white', label='FT')
    ax2.errorbar(oa['Date'], oa['BL_OA/dCO'], yerr=oa['BL_OA/dCO.STD'], c='r', capsize=4, fmt='o', mfc='white', label='BL')
    ax2.set_ylabel("OA/dCO \n$ng/{m^{3}}  /  ppbv$")
    ax2.set_xlabel("Date")
    ax2.legend()
    plt.show()

def plot_cor_in_space():
    bc = getBCRatioBySpace_df()
    oa = getOARatioBySpace_df()
    bc.to_csv(os.path.join(cur_dir, "cor_csvs", "inSpace_bc.csv"))
    oa.to_csv(os.path.join(cur_dir, "cor_csvs", "inSpace_oa.csv"))
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.errorbar(bc['Area'], bc['FT_BC/dCO'], yerr=bc['FT_BC/dCO.STD'], c='b', capsize=4, fmt='o', mfc='white', label='FT')
    # ax1.errorbar(bc['Area'], bc['BL_BC/dCO'], yerr=bc['BL_BC/dCO.STD'], c='r', capsize=4, fmt='o', mfc='white', label='BL')
    ax1.set_ylabel("BC/dCO \n$ng/{m^{3}}  /  ppbv$")
    ax1.legend()
    ax2.errorbar(oa['Area'], oa['FT_OA/dCO'], yerr=oa['FT_OA/dCO.STD'], c='b', capsize=4, fmt='o', mfc='white', label='FT')
    # ax2.errorbar(oa['Area'], oa['BL_OA/dCO'], yerr=oa['BL_OA/dCO.STD'], c='r', capsize=4, fmt='o', mfc='white', label='BL')
    ax2.set_ylabel("OA/dCO \n$ng/{m^{3}}  /  ppbv$")
    ax2.set_xlabel("Area")
    ax2.legend()
    plt.show()

if __name__ == "__main__":
    plot_cor_in_space()
    plot_cor_in_time()