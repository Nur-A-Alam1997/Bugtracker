import pandas as pd
import numpy as np
import datetime
pd.options.mode.chained_assignment = None


import datetime
WORK_DURATION_PER_DAY = 495

class TotalWork:
    """work done in total"""

    def __init__(self,data):
        self.data = data
        # to check if any column in the second interval valid but invalid in first
        self.data['First half start'] =self.data['First half start'].fillna(self.data['Second half start'])

        # to check if any column in the first half end invalid but valid in first start
        self.data['First half end'] =self.data['First half end'].fillna(self.data['First half start'])

        # to check if any column in the second interval end invalid but valid in start
        self.data['Second half end'] =self.data['Second half end'].fillna(self.data['Second half start'])
        
        self.work_time = self.data.dropna()  # drop if all NAN in a row

        # dataframe based on the time
        self.work_time = self.work_time[self.work_time['First half start'].str.contains('^-?([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')]
    

    # def working_days(self):
    #     return self.work_time.shape[0]

    @property
    def totalwork_first_interval(self):
        # work done in first interval
        self.work_time['first_td'] = ((self.work_time['First half end'].apply(pd.to_datetime) - self.work_time['First half start'].apply(pd.to_datetime))/np.timedelta64(1, 'm'))
        return self.work_time['first_td'] 

    @property        
    def totalwork_second_interval(self):
        # work done in second interval
        self.work_time['second_td'] = ((self.work_time['Second half end'].apply(pd.to_datetime) - self.work_time['Second half start'].apply(pd.to_datetime))/np.timedelta64(1, 'm'))
        return self.work_time['second_td'] 

    @property        
    def totalwork(self):
        # total work done
        self.work_time['total_work']=self.totalwork_first_interval+self.totalwork_second_interval
        # work_time['first_td']+work_time['second_td']
        return self.work_time['total_work']

    @property
    def total_work_hour(self):
        self.work_time['total_work']=self.totalwork_first_interval+self.totalwork_second_interval
        df = pd.DataFrame(self.work_time, columns= ['total_work','Date'])
        total_work_hour = df.values.tolist()
        return total_work_hour, self.work_time['total_work'].sum()
        
    @property
    def overtime(self):
        # overtime
        self.work_time['over_time']=self.totalwork-WORK_DURATION_PER_DAY
        self.work_time = self.work_time.drop(self.work_time[self.work_time.over_time < 50].index)
        # df = self.work_time[['over_time','Date']]
        df = pd.DataFrame(self.work_time, columns= ['over_time','Date'])
        overtime = df.values.tolist()
        return overtime

if __name__=="__main__":
    totalwork = TotalWork(data)
    totalwork.total_work_hour