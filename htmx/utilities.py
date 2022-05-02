import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components
from bokeh.plotting import figure
import math






class GiniIndex:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.data = []
        self.countries = []
        self.vals = []


        self.symbols = [
            {'symbol': 'SIPOVGINIFRA', 'title': 'FRANCE'},
            {'symbol': 'SIPOVGINIITA', 'title': 'ITALY'},
            {'symbol': 'SIPOVGININOR', 'title': 'NORWAY'},
            {'symbol': 'SIPOVGINIPOL', 'title': 'POLAND'},
            {'symbol': 'SIPOVGINISWE', 'title': 'SWEDEN'},
            {'symbol': 'SIPOVGINIGBR', 'title': 'UK'}
        ]    


    def get_data(self):
        result = None
        for symbol in self.symbols:
            try:
                df = pdr.DataReader(symbol['symbol'], 'fred', start=self.start, end=self.end)
                df = df.rename(columns={df.columns[0]: symbol['title']})
                if result is None:
                    result = df.copy()
                else:
                    result = pd.merge_asof(left=result.copy(), right=df, on='DATE')
                    result = result.set_index('DATE')
            except RemoteDataError:
                result = {'Error': ['RemoteDataError']}
        return result

    def get_inputs(self):
        fred_data = self.get_data()
        data = {}
        for item in fred_data:
            data[item] = fred_data[item][0]
        sorted_data = sorted(data.items(), key=lambda x: x[1])
        for obj in sorted_data:
            self.countries.append(obj[0])
            self.vals.append(obj[1])

    def get_context(self, year):
        self.get_inputs()
        cds = ColumnDataSource(data=dict(countries=self.countries, vals=self.vals))
        fig = figure(x_range=self.countries, sizing_mode='stretch_both', title=f"GINI Index for ({year})")
        fig.title.align = 'center'
        fig.title.text_font_size = '1.5em'
        fig.xaxis.major_label_orientation = math.pi / 4
        fig.vbar(source=cds, x='countries', top='vals', width=0.8 )
        tooltips = [
            ('Country', '@countries'),
            ('GINI', '@vals')
        ]
        fig.add_tools(HoverTool(tooltips=tooltips))
        script, div = components(fig)
        context = {
            'script': script,
            'div': div,
            'years': range(2010,2019)
        }
        return context

import requests
from bs4 import BeautifulSoup as bs

api_key = 'b519a08f380ad1b925acec1d68eb6c4f'
endpoint = 'https://fred.stlouisfed.org/data/SIPOVGINIFRA.txt'

params = {
'api_key': api_key,
'file_type': 'json'
            }

response = requests.get(endpoint,params=params)
soup = bs(response.text,"lxml")

# soup.text is to get the returned text
# split function, splits the entire text into different lines (using '\n') and stores in a list. You can define your own splitter.
# each line is stored as an element in the allLines list.
allLines = soup.text.split('\n') 

for line in allLines:
    if '2004' in line:
        print(line[11:-1])


    



