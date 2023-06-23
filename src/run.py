import os
import sys 
from datetime import datetime as dt
from pprint import pprint
from time import time
import pandas as pd
import hydrostats.data as hd
import json

from json2args import get_parameter

# parse parameters
kwargs = get_parameter()

# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'foobar').lower()

# switch the tool
if toolname == 'foobar':
    # RUN the tool here and create the output in /out
    print('This toolbox does not include any tool. Did you run the template?\n')
    
    # write parameters to STDOUT.log
    pprint(kwargs)

# Tool to return daily and monthly statistics
elif toolname == 'daily_monthly':
    # get the parameters
    try:
        discharge_inp = kwargs['discharge_csv']
    except Exception as e:
        print(str(e))
        sys.exit(1)
    
    # Add new column with Time
    discharge_inp['Time'] = pd.to_datetime(discharge_inp['tstamp'])

    # Set Index as Time
    discharge_inp = discharge_inp.set_index('Time')

    #Resampling to Daily and Monthly Average streamflows
    discharge_monthly = discharge_inp.resample('M').mean()# Since we are dealing with Instantaneous values
    discharge_daily = discharge_inp.resample('D').mean()

    #Creating Seasonal Daily and Monthly Average streamflows
    discharge_daily_seasonal=hd.daily_average(discharge_inp)
    discharge_monthly_seasonal=hd.monthly_average(discharge_inp)

    # Save as csv files
    discharge_monthly.to_csv('/out/discharge_monthly.csv')
    discharge_daily.to_csv('/out/discharge_daily.csv')
    discharge_daily_seasonal.to_csv('/out/discharge_daily_seasonal.csv')
    discharge_monthly_seasonal.to_csv('/out/discharge_monthly_seasonal.csv')

# In any other case, it was not clear which tool to run
else:
    raise AttributeError(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
