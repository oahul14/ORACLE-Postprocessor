import pandas as pd
import numpy as np
from scipy import odr, stats
import matplotlib.pyplot as plt
import os
from consts import field_map, cur_dir, time_slots, dates, params, lat_range

def filter_lat(df, r):
    return df.loc[(df['Latitude'] >= r[0]) & (df['Latitude'] <= r[1])]

def read_txt(date, tp):
    fields = field_map[tp]
    dname = "{}_txt".format(tp)
    fname = "{}_08{}.txt".format(tp, date)
    fname = os.path.join(cur_dir, dname, fname)
    df = pd.read_csv(fname, usecols=fields, low_memory=False, skipinitialspace=True)
    return df

def round_co_table(df):
    df.Start_UTC = df.Start_UTC.round(0)
    df_new = df.groupby(df['Start_UTC']).aggregate({'CO_ppbv': 'mean', 'CO2_ppmv': 'mean', 'Mid_UTC': 'mean'})
    df_new.Mid_UTC = df_new.Mid_UTC.round(0)
    return df_new

def drop_unavails(df, cols):
    for col in cols:
        df = df[df[col] > int(-1000.0)]
    return df

def filter_cloud(df):
    df = df[df.CDP_LWC < 0.1]
    return df

def filter_platform(df, d):
    return df[df["Start_UTC"] > time_slots[d]]

def get_background(df):
    df_clean = df[df['rBC_massConc'] < 100]
    res = {}
    res['bgCO_ppbv'] = df_clean['CO_ppbv'].mean()
    res['bgCO2_ppbv'] = (df_clean['CO2_ppmv']*1000).mean()
    return res

def getOutput(xa, ya):
    def f(B, x):
        return B[0]*x+B[1]
    linear = odr.Model(f)
    mydata = odr.Data(xa, ya)
    myodr = odr.ODR(mydata, linear, beta0=[1., 10.])
    myoutput = myodr.run()
    return myoutput

def getMCE(df, bgCO, bgCO2):
    y = df.CO_ppbv - bgCO
    x = df.CO2_ppmv*1000 - bgCO2
    # MCE = (df['dCO2_ppbv'] / (df['dCO2_ppbv'] + df['dCO_ppbv'])).mean()
    # COmean, COstd = df['dCO_ppbv'].mean(), df['dCO_ppbv'].std()
    # CO2mean, CO2std = df['dCO2_ppbv'].mean(), df['dCO2_ppbv'].std()
    # print("CO: ", COmean, COstd)
    # print("CO2: ", CO2mean, CO2std)
    # dSum = ((df['dCO_ppbv']+df['dCO2_ppbv']).std()) / (COmean + CO2mean)**2
    # pCO2 = (CO2std / CO2mean) ** 2 
    # pCOCO2 = 2 * (CO2std)**2 / (CO2mean * (CO2mean + COmean))
    # dMCE = MCE * (dSum + pCO2 - pCOCO2)**0.5
    # print(MCE, dMCE)
    # print(df['dCO2_ppbv'].isnull().sum(), df['dCO_ppbv'].isnull().sum())
    myoutput = getOutput(x, y)
    B = myoutput.beta
    plt.plot(x, B[0]*x+B[1])
    plt.scatter(x, y)
    myoutput.pprint()
    print("\n")
    plt.show()

def getBCRatio(df, bgCO, COout=False):
    df.loc[:, 'dCO_ppbv'] = df.CO_ppbv - bgCO
    sim = df[['GPS_Alt', 'dCO_ppbv', 'rBC_massConc', 'Start_UTC', 'Latitude']].copy()
    sim = sim.dropna()
    sim = sim.loc[sim['rBC_massConc'] > 100]
    if COout:
        sim = sim.drop(sim[(sim['dCO_ppbv'] < 10) & (sim['rBC_massConc'] > 100)].index)
    # myoutput = getOutput(sim['dCO_ppbv'], sim['rBC_massConc'])
    # myoutput.pprint()
    B = [np.nan]*5
    if len(sim) > 0:
        B = stats.linregress(sim['dCO_ppbv'], sim['rBC_massConc'])
    # B = myoutput.beta
    # plt.plot(sim['dCO_ppbv'], B[0]*sim['dCO_ppbv']+B[1])
    # plt.scatter(sim['dCO_ppbv'],sim['rBC_massConc'], c=sim['Latitude'], cmap=plt.cm.get_cmap('RdYlBu'))
    # plt.colorbar()
    # plt.show()
    return B[0], B[-1]
    # return myoutput.beta[0], myoutput.sd_beta[0]

def getOARatio(df, bgCO):
    df.loc[:, 'dCO_ppmv'] = (df.CO_ppbv - bgCO)/1000
    sim = df[['GPS_Alt', 'dCO_ppmv', 'ORG', 'rBC_massConc', 'Start_UTC', 'Latitude']].copy()
    sim = sim.dropna()
    sim = sim.loc[sim['rBC_massConc'] > 100]
    print(sim[['ORG', 'dCO_ppmv']])
    # myoutput = getOutput(sim['dCO_ppmv'], sim['ORG'])
    # B = myoutput.beta
    B = [np.nan]*5
    if len(sim) > 0:
        B = stats.linregress(sim['dCO_ppmv'], sim['ORG'])
    # plt.plot(sim['dCO_ppmv'], B[0]*sim['dCO_ppmv']+B[1])
    # plt.scatter(sim['dCO_ppmv'],sim['ORG'])
    # plt.show()
    return B[0], B[-1]
    # return myoutput.beta[0], myoutput.sd_beta[0]

def has_empty_row(df, cols):
    for _, row in df.iterrows():
        rowpos = [row[col]==np.nan for col in cols]
        if int(sum(rowpos)) == len(rowpos):
            return True
    return False

