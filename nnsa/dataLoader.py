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

    def load_data(self, preprocess=False):
        self.load_urls()

        for name, url in zip(self.dict['name'], self.dict['url']):
            self.data[name] = parse_kmz(url)

        if preprocess:
            self.preprocess()

    def preprocess(self):
        # preprocess fukushima dataset #1
        dformat = '%m/%d/%Y %H:%M'
        self.data['fuku-at-sea']['Time'] = self.data['fuku-at-sea'].apply(lambda x: datetime.strptime(x['Time'], dformat), axis=1)
        self.data['fuku-at-sea']['GCNORM'] = self.data['fuku-at-sea']['GCNORM'].astype(float)

        # preprocess fukushima dataset #2
        self.data['fuku-iodine'].iloc[:,0] = self.data['fuku-iodine'].iloc[:,0].astype(float)