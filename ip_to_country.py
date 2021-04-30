#pip install maxminddb-geolite2
from geolite2 import geolite2
import pandas as pd

def get_country(ip):
    try:
        x = geo.get(ip)
    except ValueError:
        return pd.np.nan
    try:
        return x['country']['iso_code'] if x else pd.np.nan
    except KeyError:
        return pd.np.nan
    
    
geo = geolite2.reader()



unique_ips = users['ip'].unique()
unique_ips = pd.Series(unique_ips, index = unique_ips)
users['country'] = users['ip'].map(unique_ips.apply(get_country))

geolite2.close()
