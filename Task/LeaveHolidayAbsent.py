import pandas as pd
import numpy as np
import datetime
pd.options.mode.chained_assignment = None

class LeaveHolidayAbsent:
    """present leave holiday absent"""
    def __init__(self,data):
        self.data = data
        self.data['First half start'] =self.data['First half start'].fillna(self.data['Second half start'])
    
    @property
    def leave(self):
        leave = self.data[['Date','First half start']]
        leave = leave[leave['First half start'].str.contains('Leave')] # check if any leave word
        return leave.shape[0]
    
    @property
    def holiday(self):
        holiday = self.data[['Date','First half start']]
        holiday = holiday[holiday['First half start'].str.contains('^[a-zA-Z0-9_ ]*$')] #check if string
        holiday = holiday.shape[0]-self.leave
        return holiday

    @property
    def present(self):
        time = self.data[['Date','First half start','Second half start']].dropna(how="any")
        time = time[time['First half start'].str.contains('^-?([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')]#check if date
        return time.shape[0]

    @property
    def absent(self,):
        """total = present + leave + holiday + absent"""
        absent = (self.data.shape[0]-self.present-self.leave-self.holiday)
        return absent
if __name__ == "__main__":
    leave=LeaveHolidayAbsent(data)
    leave.absent
    