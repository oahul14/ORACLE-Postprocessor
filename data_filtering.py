import pandas as pd
import matplotlib.pyplot as plt
import os
from consts import field_map, cur_dir, time_slots, dates, params, lat_range

def filter_lat(df, r):
    return df.loc[(df['Latitude'] >= r[0]) & (df['Latitude'] <= r[1])]

def get_co_plume():
    f_dir = os.path.join(cur_dir, "FilteredData", "CombinedData")
    for r in lat_range:
        print("Lat range: ", r)
        d = dict()
        for n in os.listdir(f_dir):
            dname = os.path.join(f_dir, n)
            fields = ["Latitude", "Longitude", "GPS_Alt", params['CO']]
            df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
            df = filter_lat(df, r)
            if len(df) != 0:
                row = df.loc[df[params['CO']].idxmax()]
                d[n] = {'alt':row["GPS_Alt"], 'lat':row["Latitude"], 'lon':row["Longitude"]}
                print('%s: %s' % (n, d[n]))

def read_txt(date, tp):
    fields = field_map[tp]
    dname = "{}_txt".format(tp)
    fname = "{}_08{}.txt".format(tp, date)
    fname = os.path.join(cur_dir, dname, fname)
    df = pd.read_csv(fname, usecols=fields, low_memory=False, skipinitialspace=True)
    return df

def round_co_table(df):
    df.Start_UTC = df.Start_UTC.round(0)
    df_new = df.groupby(df['Start_UTC']).aggregate({'CO_ppbv': 'mean', 'Mid_UTC': 'mean'})
    df_new.Mid_UTC = df_new.Mid_UTC.round(0)
    return df_new

def drop_unavails(df, cols):
    for col in cols:
        df = df[df[col] > int(-8888.0)]
    return df

def filter_cloud(df):
    df = df[df.CDP_LWC < 0.1]
    return df

def filter_platform(df, d):
    return df[df["Start_UTC"] > time_slots[d]]

if __name__ == "__main__":
    for d in dates:
        adf_name = "Adf_08{}.txt".format(d)

        co = drop_unavails(round_co_table(read_txt(d, "CO")), ["CO_ppbv"])
        aod = drop_unavails(read_txt(d, "AOD"), ["GPS_Alt", "AOD0501"])
        adf = pd.merge(aod, co, on='Start_UTC')
        
        ccn = drop_unavails(read_txt(d, "CCN"), ["Number_Concentration"])
        ccn.rename(columns={'UTC_mid': 'Mid_UTC'}, inplace=True)

        adf = pd.merge(adf, ccn, how="outer")
        
        bc = drop_unavails(read_txt(d, "BC"), ["rBC_massConc"])
        
        adf = pd.merge(adf, bc, how="outer")
        
        oa = None
        try: 
            oa = drop_unavails(read_txt(d, "OA"), ["ORG"])
            oa.Start_UTC = oa.Start_UTC.round(0)
            adf = pd.merge(adf, oa, how="outer")
        except:
            pass

        cdp = drop_unavails(read_txt(d, "CDP"), ["CDP_LWC"])
        adf = pd.merge(adf, cdp, how='outer')
        adf = filter_cloud(adf)
        print(len(adf))
        adf.to_csv(os.path.join(cur_dir, "FilteredData", "CombinedData", adf_name), index=False)

        adf = filter_platform(adf, d)
        print(len(adf))
        adf.to_csv(os.path.join(cur_dir, "FilteredData", "PlatformFiltered", "NOP_"+adf_name), index=False)
