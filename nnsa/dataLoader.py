from datetime import datetime
import yaml
import pandas as pd
from nnsa.util import kml_parser, parse_kmz

class dataLoader:

    def __init__(self):
        self.dict = {}
        self.data = {}

    def load_urls(self):
        with open('environment.yml', 'r') as stream:
            f = yaml.safe_load(stream)
        
        for name, url in f['files'].items():
            self.dict[name] = url

    def load_data(self, preprocess=False, only_load=None):
        self.load_urls()

        if isinstance(only_load, int):
            only_load = list(only_load)

        for i, (name, url) in enumerate(zip(self.dict['name'], self.dict['url'])):
            if only_load is not None and i not in only_load:
                pass
            else:
                self.data[name] = parse_kmz(url)

        if preprocess:
            self.preprocess()

    def preprocess(self):

        try:
            # preprocess fukushima dataset #1
            dformat = '%m/%d/%Y %H:%M'
            self.data['fuku-at-sea']['Time'] = self.data['fuku-at-sea'].apply(lambda x: datetime.strptime(x['Time'], dformat), axis=1)
            self.data['fuku-at-sea'].iloc[:,1:] = self.data['fuku-at-sea'].iloc[:,1:].astype(float)
            self.data['fuku-at-sea']['NumDet'] = self.data['fuku-at-sea']['NumDet'].astype(int)
            self.data['fuku-at-sea'].drop(['NumDet'], axis=1, inplace=True)
        except (IndexError, ValueError, KeyError):
            print(f'Preprocessing skipped for [fuku-at-sea]')

        try:
            # preprocess fukushima dataset #2
            self.data['fuku-iodine'].iloc[:,0] = self.data['fuku-iodine'].iloc[:,0].astype(float)
        except (IndexError, ValueError, KeyError):
            print(f'Preprocessing skipped for [fuku-iodine]')

        try:
            # preprocess fukushima dataset #3
            self.data['fuku-nnsa-response'].rename(columns={'lat':'Latitude', 'long':'Longitude'}, inplace=True)
            self.data['fuku-nnsa-response']['Exposure'] = self.data['fuku-nnsa-response']['Exposure'].astype(float)
        except (IndexError, ValueError, KeyError):
            print(f'Preprocessing skipped for [fuku-nnsa-response]')