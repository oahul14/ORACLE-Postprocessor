import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from consts import *
from data_management import *
from calculate_correlations import *

cmap = ['r', 'green', 'b', 'orange', 'purple', 'grey']
cmap2 = ['green', 'b', 'purple', 'grey']

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
    for i, n in enumerate(["Adf_0813.csv", "Adf_0815.csv", "Adf_0824.csv", "Adf_0826.csv"]):
        dname = os.path.join(cur_dir, "FilteredData", directory, n)
        fields = ["Latitude", "GPS_Alt", "ORG"]
        df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
        df = filter_lat(df, r)
        df = cal_mean_avg(df, len(df)/fac, "ORG")
        df['MA_alt'] = df['GPS_Alt'].rolling(window=window).mean()
        df['MA_val'] = df["ORG"].rolling(window=window).mean()
        label = n.replace("Adf_", "OA ")
        label = label.replace(".csv", "")
        plt.plot(df["ORG"], df['GPS_Alt'], linewidth=3, c=cmap2[i], label=label) # plot mean values
        plt.ylabel("Altitude (m)", fontsize=14)
        plt.xlabel("OA "+units["OA"], fontsize=14)
        plt.ylim([0, 6700])
        plt.xlim([-5, 70])
        plt.title("({})".format(l), loc='left', fontsize=15)
        plt.title("{}".format(t), loc='center', fontsize=15)
        plt.legend(loc="upper right", prop={'size': 13})
    plt.tight_layout() 
    plt.savefig(pname)
    plt.clf()

def plot_BC(l, r, t, directory, fac, window):
    pname = os.path.join(cur_dir, "Plots", "MA_{}_{}_{}-{}.png".format(directory, 'BC', r[0], r[1]))
    if window == 1:
        pname = "N" + pname
    f_dir = os.path.join(cur_dir, "FilteredData", directory)
    for i, n in enumerate(os.listdir(f_dir)):
        dname = os.path.join(f_dir, n)
        fields = ["Latitude", "GPS_Alt", params["BC"]]
        df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
        df = filter_lat(df, r)
        df = cal_mean_avg(df, len(df)/fac, params["BC"])
        df['MA_alt'] = df['GPS_Alt'].rolling(window=window).mean()
        df['MA_val'] = df[params["BC"]].rolling(window=window).mean()
        label = n.replace("Adf_", "BC"+" ")
        label = label.replace(".csv", "")
        plt.plot(df['MA_val']/1000, df['MA_alt'], linewidth=3, c=cmap[i], label=label) # plot mean values
        plt.ylabel("Altitude (m)", fontsize=14)
        plt.xlabel("BC"+" "+units["BC"], fontsize=14)
        plt.ylim([0, 6700])
        plt.xlim([-0.3, 7])
        plt.title("({})".format(l), loc='left', fontsize=15)
        plt.title("{}".format(t), loc='center', fontsize=15)
        plt.legend(loc="upper right", prop={'size': 13})
    plt.tight_layout() 
    plt.savefig(pname)
    plt.clf()

def plot_CO(l, r, t, directory, fac, window):
    pname = os.path.join(cur_dir, "Plots", "MA_{}_{}_{}-{}.png".format(directory, "CO", r[0], r[1]))
    if window == 1:
        pname = "N" + pname
    f_dir = os.path.join(cur_dir, "FilteredData", directory)
    for i, n in enumerate(os.listdir(f_dir)):
        dname = os.path.join(f_dir, n)
        fields = ["Latitude", "GPS_Alt", params["CO"]]
        df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
        df = filter_lat(df, r)
        df = cal_mean_avg(df, len(df)/fac, params["CO"])
        df['MA_alt'] = df['GPS_Alt'].rolling(window=window).mean()
        df['MA_val'] = df[params["CO"]].rolling(window=window).mean()
        label = n.replace("Adf_", "CO"+" ")
        label = label.replace(".csv", "")
        plt.plot(df['MA_val']/1000, df['MA_alt'], linewidth=3, c=cmap[i], label=label) # plot mean values
        plt.ylabel("Altitude (m)", fontsize=14)
        plt.xlabel("CO"+" "+units["CO"], fontsize=14)
        plt.ylim([0, 6700])
        plt.xlim([0, 0.52])
        plt.title("({})".format(l), loc='left', fontsize=15)
        plt.title("{}".format(t), loc='center', fontsize=15)
        plt.legend(loc="upper right", prop={'size': 13})
    plt.tight_layout() 
    plt.savefig(pname)
    plt.clf()

def antByXY(ax, c, xs, ys, j):
    for x,y in zip(xs, ys):
        l = "{:.2f}".format(y)
        plt.text(x, y+j, l, {'color': c},horizontalalignment='center')

def plot_cor_in_time():
    bc = getBCRatioByTime_df()
    oa = getOARatioByTime_df()
    bc.to_csv(os.path.join(cur_dir, "cor_csvs", "inTime_bc.csv"))
    oa.to_csv(os.path.join(cur_dir, "cor_csvs", "inTime_oa.csv"))

    plt.style.use('ggplot')
    fig = plt.figure()
    ##############
    ax1 = fig.add_subplot(2, 1, 1)

    ax1.errorbar(bc['Date'], bc['FT_BC/dCO'], yerr=bc['FT_BC/dCO.STD'], c='b', capsize=4, fmt='o', mfc='white', label='FT')
    antByXY(ax1, 'b', bc['Date'], bc['FT_BC/dCO'], 3)

    ax1.errorbar(bc['Date'], bc['BL_BC/dCO'], yerr=bc['BL_BC/dCO.STD'], c='r', capsize=4, fmt='o', mfc='white', label='BL')
    antByXY(ax1, 'r', bc['Date'], bc['BL_BC/dCO'], -4)

    ax1.set_ylabel("BC/dCO \n$ug/{m^{3}}  /  ppmv$")
    ax1.set_ylim([0, 27])
    ax1.legend()

    ##############
    ax2 = fig.add_subplot(2, 1, 2)

    ax2.errorbar(oa['Date'], oa['FT_OA/dCO'], yerr=oa['FT_OA/dCO.STD'], c='b', capsize=4, fmt='o', mfc='white', label='FT')
    antByXY(ax2, 'b', oa['Date'], oa['FT_OA/dCO'], 11)

    ax2.errorbar(oa['Date'], oa['BL_OA/dCO'], yerr=oa['BL_OA/dCO.STD'], c='r', capsize=4, fmt='o', mfc='white', label='BL')
    antByXY(ax2, 'r', oa['Date'], oa['BL_OA/dCO'], -36)

    ax2.set_ylabel("OA/dCO \n$ug/{m^{3}}  /  ppmv$")
    ax2.set_ylim([-50, 230])
    ax2.set_xlabel("Date")
    ax2.legend()

    ##############
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(cur_dir, "Plots", "cor_in_time.png"))

def plot_cor_in_space():
    bc = getBCRatioBySpace_df()
    oa = getOARatioBySpace_df()
    bc.to_csv(os.path.join(cur_dir, "cor_csvs", "inSpace_bc.csv"))
    oa.to_csv(os.path.join(cur_dir, "cor_csvs", "inSpace_oa.csv"))

    plt.style.use('ggplot')
    fig = plt.figure()

    ##############
    ax1 = fig.add_subplot(2, 1, 1)

    ax1.errorbar(bc['Area'], bc['FT_BC/dCO'], yerr=bc['FT_BC/dCO.STD'], c='b', capsize=4, fmt='o', mfc='white', label='FT')
    antByXY(ax1, 'b', bc['Area'], bc['FT_BC/dCO'], 0.5)

    # ax1.errorbar(bc['Area'], bc['BL_BC/dCO'], yerr=bc['BL_BC/dCO.STD'], c='r', capsize=4, fmt='o', mfc='white', label='BL')
    ax1.set_ylabel("BC/dCO \n$ug/{m^{3}}  /  ppmv$")
    ax1.set_ylim([12, 20])
    ax1.legend()

    ##################
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.errorbar(oa['Area'], oa['FT_OA/dCO'], yerr=oa['FT_OA/dCO.STD'], c='b', capsize=4, fmt='o', mfc='white', label='FT')
    antByXY(ax2, 'b', oa['Area'], oa['FT_OA/dCO'], 6)
    # ax2.errorbar(oa['Area'], oa['BL_OA/dCO'], yerr=oa['BL_OA/dCO.STD'], c='r', capsize=4, fmt='o', mfc='white', label='BL')
    ax2.set_ylabel("OA/dCO \n$ug/{m^{3}}  /  ppmv$")
    ax2.set_xlabel("Area")
    ax2.set_ylim([70, 160])
    ax2.legend()
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(cur_dir, "Plots", "cor_in_space.png"))

if __name__ == "__main__":
    df_dir = os.path.join(cur_dir, "FilteredData", "CombinedData")
    dfs_all = []
    dfs_oa = []
    for i, f_dir in enumerate(os.listdir(df_dir)):
        dname = os.path.join(df_dir, f_dir)
        fields = ["GPS_Alt", "rBC_massConc", "CO_ppbv"]
        if i in [1,2,3,4]:
            fields = ["GPS_Alt", "ORG", "rBC_massConc", "CO_ppbv"]
        df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
        dfs_all.append(df)
    for df in dfs_all:
        try:
            oa = df["ORG"]
            dfs_oa.append(df) 
        except:
            continue

    figs, axs = plt.subplots(3, 2, figsize=(10,11))
    tar_cols = [["ORG", "rBC_massConc", "GPS_Alt"], ["rBC_massConc", "CO_ppbv", "GPS_Alt"], ["ORG", "CO_ppbv", "GPS_Alt"]]
    
    for i, df in enumerate(dfs_oa):
        oa_bc = df.dropna(subset=tar_cols[0])
        oa_bc_ft = oa_bc[oa_bc['GPS_Alt'] > 1200]
        oa_bc_bl = oa_bc[oa_bc['GPS_Alt'] <= 1200]
        axs[0][0].scatter(oa_bc[tar_cols[0][1]]/1000, oa_bc[tar_cols[0][0]], c=cmap2[i], label='Flight 08'+str(dates_oa[i]), alpha=0.4, s=12)
        axs[0][1].scatter(oa_bc_ft[tar_cols[0][1]]/1000, oa_bc_ft[tar_cols[0][0]], c='red', label='FT' if i == 0 else "", alpha=0.4, s=12)
        axs[0][1].scatter(oa_bc_bl[tar_cols[0][1]]/1000, oa_bc_bl[tar_cols[0][0]], c='blue', label='BL' if i == 0 else "", alpha=0.4, s=12)
        axs[0][0].set_title("a)", loc='left')
        axs[0][0].set_ylabel("OA (ug/${m^3})$")
        axs[0][0].set_xlabel("BC (ug/${m^3}$)")
        axs[0][1].set_title("b)", loc='left')
        axs[0][1].set_ylabel("OA (ug/${m^3})$")
        axs[0][1].set_xlabel("BC (ug/${m^3}$)")
        axs[0][0].legend()

        oa_co = df.dropna(subset=tar_cols[2])
        oa_co_ft = oa_co[oa_co['GPS_Alt'] > 1200]
        oa_co_bl = oa_co[oa_co['GPS_Alt'] <= 1200]
        axs[2][0].scatter(oa_co[tar_cols[2][1]]/1000, oa_co[tar_cols[2][0]], c=cmap2[i], label='Flight 08'+str(dates_oa[i]), alpha=0.4, s=12)
        axs[2][1].scatter(oa_co_ft[tar_cols[2][1]]/1000, oa_co_ft[tar_cols[2][0]], c='r', label='FT' if i == 0 else "", alpha=0.4, s=12)
        axs[2][1].scatter(oa_co_bl[tar_cols[2][1]]/1000, oa_co_bl[tar_cols[2][0]], c='b', label='BL' if i == 0 else "", alpha=0.4, s=12)
        axs[2][0].set_title("e)", loc='left')
        axs[2][0].set_ylabel("OA (ug/${m^3})$")
        axs[2][0].set_xlabel("CO (ppmv)")
        axs[2][1].set_title("f)", loc='left')
        axs[2][1].set_ylabel("OA (ug/${m^3})$")
        axs[2][1].set_xlabel("CO (ppmv)")
        axs[2][0].legend()
    axs[0][1].legend()
    axs[2][1].legend()

    for i, df in enumerate(dfs_all):
        bc_co = df.dropna(subset=tar_cols[1])
        bc_co_ft = bc_co[bc_co['GPS_Alt'] > 1200]
        bc_co_bl = bc_co[bc_co['GPS_Alt'] <= 1200]
        axs[1][0].scatter(bc_co[tar_cols[1][1]]/1000, bc_co[tar_cols[1][0]]/1000, c=cmap[i], label='Flight 08'+str(dates[i]), alpha=0.4, s=12)
        axs[1][1].scatter(bc_co_ft[tar_cols[1][1]]/1000, bc_co_ft[tar_cols[1][0]]/1000, c='r', label='FT' if i == 0 else "", alpha=0.4, s=12)
        axs[1][1].scatter(bc_co_bl[tar_cols[1][1]]/1000, bc_co_bl[tar_cols[1][0]]/1000, c='b', label='BL' if i == 0 else "", alpha=0.4, s=12)
        axs[1][0].set_title("c)", loc='left')
        axs[1][0].set_ylabel("BC (ug/${m^3}$)")
        axs[1][1].set_ylabel("BC (ug/${m^3}$)")
        axs[1][1].set_title("d)", loc='left')
        axs[1][0].set_xlabel("CO (ppmv)")
        axs[1][1].set_xlabel("CO (ppmv)")
        axs[1][0].legend()
    axs[1][1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(cur_dir, "Plots", "comp_vert"))
        

    