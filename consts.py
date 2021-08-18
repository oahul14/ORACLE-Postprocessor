import os

dates = ["12", "13", "15", "24", "26", "28"]
dates_oa = ["13", "15", "24", "26"]

cur_dir    = os.path.dirname(os.path.realpath(__file__))
aod_fields = ["Start_UTC", "Latitude", "Longitude", "GPS_Alt", "AOD0501"]
co_fields  = ["Start_UTC", "Mid_UTC", "CO_ppbv", "CO2_ppmv"]
bc_fields  = ["Start_UTC", "rBC_massConc"]
oa_fields  = ["Start_UTC", "ORG"]
ccn_fields = ["UTC_mid", "Number_Concentration"]
cdp_fields = ["Start_UTC", "CDP_LWC"]
field_map  = {"CO": co_fields, "AOD": aod_fields, "CDP": cdp_fields, "BC": bc_fields, "OA": oa_fields, "CCN": ccn_fields}

time_slots = {"12": 40000, "13": 35500, "15": 40000, "24": 40000, "26": 37000, "28": 37500}

lat_range = [[-15, -7], [-7, -2], [-2, 1]]
lat_rs = ['15S - 7S', '7S - 2S', '2S - 1N']

params = {"CO": "CO_ppbv", "AOD": "AOD0501", "OA": "ORG", "BC": "rBC_massConc", "CCN": "Number_Concentration"}
units = {"CO": "(ppmv)", "BC": "($\mu g$/${m^3}$)", "OA": "($\mu g$/${m^3})$", "CCN": "$({m^{-3}}$)"}