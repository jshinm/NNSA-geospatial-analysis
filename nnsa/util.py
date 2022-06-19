import pandas as pd
import re
import io
import requests
from zipfile import ZipFile
import geopandas as gpd
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

def kml_parser(txt):
    lst = re.split(r'<', txt)
    lst = [i[3:].strip() for i in lst if 'td>' in i and '/td>' not in i]
    dic = {}

    for i, item in enumerate(lst):
        if i%2 == 0:
            prev = item
            dic[item] = ''
        else:
            dic[prev] = item

    return pd.DataFrame(dic.items(), index=dic.keys()).T.drop(0)


def parse_kmz(url):
    r = requests.get(url)
    c = io.BytesIO(r.content)
    zf = ZipFile(c).extractall('dat/')

    gpdf = gpd.read_file('dat/doc.kml', driver='KML')

    # print(zf.namelist())
    # return {n: zf.read(n) for n in zf.namelist()}

    df = pd.DataFrame()

    for row in gpdf.Description:
        df = pd.concat([df, kml_parser(row)])

    df = df.reset_index(drop=True)

    return df