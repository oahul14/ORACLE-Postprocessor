from data_management import filter_lat
import pandas as pd
import os
from consts import lat_range, cur_dir, params

def get_co_plume():
    f_dir = os.path.join(cur_dir, "FilteredData", "CombinedData")
    for r in lat_range:
        print("Lat range: ", r)
        d = dict()
        for n in os.listdir(f_dir):
            dname = os.path.join(f_dir, n)
            fields = ["Start_UTC", "Latitude", "Longitude", "GPS_Alt", params['CO']]
            df = pd.read_csv(dname, usecols=fields, low_memory=False, skipinitialspace=True)
            df = filter_lat(df, r)
            if len(df) != 0:
                row = df.loc[df[params['CO']].idxmax()]
                d[n] = {'UTC': row['Start_UTC']//3600, 'alt':row["GPS_Alt"], 'lat':row["Latitude"], 'lon':row["Longitude"]}
                print('%s: %s' % (n, d[n]))

if __name__ == "__main__":
    get_co_plume()
