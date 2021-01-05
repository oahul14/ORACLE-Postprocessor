from data_management import *
import pandas as pd
import os
from consts import *

tar_dir = os.path.join(cur_dir, "FilteredData", "CombinedData")

def getBCRatioByTime_df():
    BCpCO = pd.DataFrame(columns=['Date', 'FT_BC/dCO', 'FT_BC/dCO.STD', 'BL_BC/dCO', 'BL_BC/dCO.STD'])
    for i, csv in enumerate(os.listdir(tar_dir)):
        date = str(dates[i]) + '/08'
        df = pd.read_csv(os.path.join(tar_dir, csv))
        ft = df[df['GPS_Alt'] >= 1200]
        ft_map = get_background(ft)
        ft_BCpCO = getBCRatio(ft, ft_map['bgCO_ppbv'])

        bl = df.loc[(df['GPS_Alt'] < 1200) & (df['GPS_Alt'] > 100)]
        bl_map = get_background(bl)
        bl_BCpCO = getBCRatio(bl, bl_map['bgCO_ppbv'])

        row = [date, ft_BCpCO[0], ft_BCpCO[1], bl_BCpCO[0], bl_BCpCO[1]]
        BCpCO.loc[i] = row
    return BCpCO

def getBCRatioBySpace_df():
    csvs = os.listdir(tar_dir)
    fields = ['GPS_Alt', 'Latitude', 'CO_ppbv', 'CO2_ppmv', 'rBC_massConc']
    res = pd.DataFrame(columns=['Area', 'FT_BC/dCO', 'FT_BC/dCO.STD', 'BL_BC/dCO', 'BL_BC/dCO.STD'])
    bc = pd.read_csv(os.path.join(tar_dir, csvs[0]), skipinitialspace=True, usecols=fields)
    for i in range(1, len(csvs)):
        df = pd.read_csv(os.path.join(tar_dir, csvs[i]), skipinitialspace=True, usecols=fields)
        bc = pd.concat([bc, df], ignore_index=True)
    ft, bl = bc[bc['GPS_Alt'] >= 1200], df.loc[(df['GPS_Alt'] < 1200) & (df['GPS_Alt'] > 100)]
    for j, r in enumerate(lat_range):
        rs = str(r[0]) + ', ' + str(r[1])
        rft = filter_lat(ft, r)
        rft_BCpCO = [np.nan, np.nan]
        if len(rft) != 0:
            rft_map = get_background(rft)
            rft_BCpCO = getBCRatio(rft, rft_map['bgCO_ppbv'])

        rbl = filter_lat(bl, r)
        rbl_BCpCO = [np.nan, np.nan]
        if len(rbl) != 0:
            rbl_map = get_background(rbl)
            rbl_BCpCO = getBCRatio(rbl, rbl_map['bgCO_ppbv'])

        row = [rs, rft_BCpCO[0], rft_BCpCO[1], rbl_BCpCO[0], rbl_BCpCO[1]]
        res.loc[j] = row
    return res

def getOARatioByTime_df():
    OApCO = pd.DataFrame(columns=['Date', 'FT_OA/dCO', 'FT_OA/dCO.STD', 'BL_OA/dCO', 'BL_OA/dCO.STD'])
    csvs = ['Adf_0813.csv','Adf_0815.csv', 'Adf_0826.csv']
    for i, csv in enumerate(csvs):
        date = str(dates_oa[i]) + '/08'
        df = pd.read_csv(os.path.join(tar_dir, csv))
        ft = df[df['GPS_Alt'] >= 1200]
        ft_map = get_background(ft)
        ft_OApCO = getOARatio(ft, ft_map['bgCO_ppbv'])

        bl = df.loc[(df['GPS_Alt'] < 1200) & (df['GPS_Alt'] > 100)]
        bl_map = get_background(bl)
        bl_OApCO = getOARatio(bl, bl_map['bgCO_ppbv'])

        row = [date, ft_OApCO[0]*1000, ft_OApCO[1]*1000, bl_OApCO[0]*1000, bl_OApCO[1]*1000]
        OApCO.loc[i] = row
    return OApCO

def getOARatioBySpace_df():
    csvs = ['Adf_0813.csv','Adf_0815.csv', 'Adf_0826.csv']
    fields = ['GPS_Alt', 'Latitude', 'CO_ppbv', 'CO2_ppmv', 'rBC_massConc', 'ORG']
    res = pd.DataFrame(columns=['Area', 'FT_OA/dCO', 'FT_OA/dCO.STD', 'BL_OA/dCO', 'BL_OA/dCO.STD'])
    bc = pd.read_csv(os.path.join(tar_dir, csvs[0]), skipinitialspace=True, usecols=fields)
    for i in range(1, len(csvs)):
        df = pd.read_csv(os.path.join(tar_dir, csvs[i]), skipinitialspace=True, usecols=fields)
        bc = pd.concat([bc, df], ignore_index=True)
    ft, bl = bc[bc['GPS_Alt'] >= 1200], df.loc[(df['GPS_Alt'] < 1200) & (df['GPS_Alt'] > 100)]
    for j, r in enumerate(lat_range):
        rs = str(r[0]) + ', ' + str(r[1])
        rft = filter_lat(ft, r)
        rft_OApCO = [np.nan, np.nan]
        if len(rft) != 0:
            rft_map = get_background(rft)
            rft_OApCO = getOARatio(rft, rft_map['bgCO_ppbv'])

        rbl = filter_lat(bl, r)
        rbl_OApCO = [np.nan, np.nan]
        if len(rbl) != 0:
            rbl_map = get_background(rbl)
            rbl_OApCO = getOARatio(rbl, rbl_map['bgCO_ppbv'])

        row = [rs, rft_OApCO[0]*1000, rft_OApCO[1]*1000, rbl_OApCO[0]*1000, rbl_OApCO[1]*1000]
        res.loc[j] = row
    return res

if __name__ == "__main__":
    print(getOARatioBySpace_df())
