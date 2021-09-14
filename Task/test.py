import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.mode.chained_assignment = None

class ReadData:
    def __init__(self,filename):
        self.filename=f'./{filename}'
    @property
    def read_data(self):
        data=pd.read_csv(self.filename)
        # display(data)
        return data.dropna(how='all')

import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

class Present:
    """total present date"""

    def __init__(self,data):
        self.data = data

    @property
    def present(self):
        self.data['First half start'] =self.data['First half start'].fillna(self.data['Second half start'])
        time = self.data[['Date','First half start','Second half start']].dropna()
        time = time[time['First half start'].str.contains('^-?([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')]
        return time.shape[0]

# data = ReadData("ole")
# data.read_data
# present = Present(read_data)
# present.present