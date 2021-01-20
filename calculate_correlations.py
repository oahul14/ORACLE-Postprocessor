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
        df = df[df['Start_UTC'] > 30000]
        df = df[df['rBC_massConc'].notna()]
        
        ft = df[df['GPS_Alt'] >= 1200]
        ft_map = get_background(ft)
        ft_BCpCO = getBCRatio(ft, ft_map['bgCO_ppbv'])

        bl = df.loc[(df['GPS_Alt'] < 1200) & (df['GPS_Alt'] > 100)]
        # bl = filter_lat(bl, [-15, -2])
        bl_map = get_background(bl)
        bl_BCpCO = getBCRatio(bl, bl_map['bgCO_ppbv'])
        # if i == 5:
        #     bl_BCpCO = [np.nan, np.nan]
        row = [date, ft_BCpCO[0], ft_BCpCO[1], bl_BCpCO[0], bl_BCpCO[1]]
        BCpCO.loc[i] = row
    return BCpCO

def getBCRatioBySpace_df():
    csvs = os.listdir(tar_dir)
    fields = ['GPS_Alt', 'Latitude', 'CO_ppbv', 'CO2_ppmv', 'rBC_massConc', 'Start_UTC']
    res = pd.DataFrame(columns=['Area', 'FT_BC/dCO', 'FT_BC/dCO.STD', 'BL_BC/dCO', 'BL_BC/dCO.STD'])
    bc = pd.read_csv(os.path.join(tar_dir, csvs[0]), skipinitialspace=True, usecols=fields)
    for i in range(1, len(csvs)):
        df = pd.read_csv(os.path.join(tar_dir, csvs[i]), skipinitialspace=True, usecols=fields)
        bc = pd.concat([bc, df], ignore_index=True)
    ft, bl = bc[bc['GPS_Alt'] >= 1200], df.loc[(df['GPS_Alt'] < 1200) & (df['GPS_Alt'] > 100)]
    for j, r in enumerate(lat_range):
        rs = lat_rs[j]
        rft = filter_lat(ft, r)
        rft_BCpCO = [np.nan, np.nan]
        if len(rft) != 0:
            rft_map = get_background(rft)
            rft_BCpCO = getBCRatio(rft, rft_map['bgCO_ppbv'])

        rbl_BCpCO = [np.nan, np.nan]
        rbl = filter_lat(bl, r)
        if len(rbl) != 0:
            rbl_map = get_background(rbl)
            rbl_BCpCO = getBCRatio(rbl, rbl_map['bgCO_ppbv'])

        row = [rs, rft_BCpCO[0], rft_BCpCO[1], rbl_BCpCO[0], rbl_BCpCO[1]]
        res.loc[j] = row
    return res

def getOARatioByTime_df():
    OApCO = pd.DataFrame(columns=['Date', 'FT_OA/dCO', 'FT_OA/dCO.STD', 'BL_OA/dCO', 'BL_OA/dCO.STD'])
    csvs = ['Adf_0813.csv','Adf_0815.csv', 'Adf_0824.csv', 'Adf_0826.csv']
    for i, csv in enumerate(csvs):
        date = str(dates_oa[i]) + '/08'
        df = pd.read_csv(os.path.join(tar_dir, csv))
        ft = df[df['GPS_Alt'] >= 1200]
        ft_map = get_background(ft)
        ft_OApCO = getOARatio(ft, ft_map['bgCO_ppbv'])

        bl = df.loc[(df['GPS_Alt'] < 1200) & (df['GPS_Alt'] > 100)]
        bl_map = get_background(bl)
        bl_OApCO = getOARatio(bl, bl_map['bgCO_ppbv'])

        row = [date, ft_OApCO[0], ft_OApCO[1], bl_OApCO[0], bl_OApCO[1]]
        OApCO.loc[i] = row
    return OApCO

def getOARatioBySpace_df():
    csvs = ['Adf_0813.csv','Adf_0815.csv', 'Adf_0824.csv', 'Adf_0826.csv']
    fields = ['GPS_Alt', 'Start_UTC', 'Latitude', 'CO_ppbv', 'CO2_ppmv', 'rBC_massConc', 'ORG']
    res = pd.DataFrame(columns=['Area', 'FT_OA/dCO', 'FT_OA/dCO.STD', 'BL_OA/dCO', 'BL_OA/dCO.STD'])
    bc = pd.read_csv(os.path.join(tar_dir, csvs[0]), skipinitialspace=True, usecols=fields)
    for i in range(1, len(csvs)):
        df = pd.read_csv(os.path.join(tar_dir, csvs[i]), skipinitialspace=True, usecols=fields)
        bc = pd.concat([bc, df], ignore_index=True)
    ft, bl = bc[bc['GPS_Alt'] >= 1200], df.loc[(df['GPS_Alt'] < 1200) & (df['GPS_Alt'] > 100)]
    for j, r in enumerate(lat_range):
        rs = lat_rs[j]
        rft = filter_lat(ft, r)
        rft_OApCO = [np.nan, np.nan]
        if len(rft) != 0:
            rft_map = get_background(rft)
            rft_OApCO = getOARatio(rft, rft_map['bgCO_ppbv'])

        rbl_OApCO = [np.nan, np.nan]
        rbl = filter_lat(bl, r)
        if len(rbl) != 0:
            rbl_map = get_background(rbl)
            rbl_OApCO = getOARatio(rbl, rbl_map['bgCO_ppbv'])

        row = [rs, rft_OApCO[0], rft_OApCO[1], rbl_OApCO[0], rbl_OApCO[1]]
        res.loc[j] = row
    return res

