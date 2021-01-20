from data_management import *

if __name__ == "__main__":
    for d in dates:
        adf_name = "Adf_08{}.csv".format(d)

        co = read_txt(d, "CO")
        co = round_co_table(co)
        co = drop_unavails(co, ["CO_ppbv", "CO2_ppmv"])

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

        # adf = filter_platform(adf, d)
        # print(len(adf))
        # adf.to_csv(os.path.join(cur_dir, "FilteredData", "PlatformFiltered", "NOP_"+adf_name), index=False)
