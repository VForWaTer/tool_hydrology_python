# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:05:42 2023
Local version of tool_hydrology_python

@author: Ashish
"""

#%% Import Modules
import pandas as pd
import matplotlib.pyplot as plt
import hydrostats.data as hd

#%% Plotting Simulated vs Reservoir Inverted Inflow Mass Balance
discharge_inp = pd.read_csv(r'u:\02_Software\Github\tool_hydrology_python\in\discharge\burgberg_60min.csv'
                      ,delimiter=',',engine='c')

# Add new column with Time
discharge_inp['Date'] = pd.to_datetime(discharge_inp['tstamp'])

# Set Index as Time
discharge_inp = discharge_inp.set_index('Date')

#Resampling to Daily and Monthly Average streamflows
discharge_monthly = discharge_inp.resample('M').mean()# Since we are dealing with Instantaneous values
discharge_daily = discharge_inp.resample('D').mean()

#Creating Seasonal Daily and Monthly Average streamflows
discharge_daily_seasonal=hd.daily_average(discharge_inp)
discharge_monthly_seasonal=hd.monthly_average(discharge_inp)


# %%
import baseflow
b, KGEs = baseflow.separation(discharge_inp['discharge'], discharge_inp['tstamp'])

# %%
from Hydrograph.hydrograph import sepBaseflow, filterpeaks, maxFlowVolStats
discharge = pd.DataFrame(discharge_inp)
# Add new column with Time
discharge['Date'] = pd.to_datetime(discharge['tstamp'])

# Set Index as Time
discharge = discharge.set_index('Date')

# Rename Column
discharge.rename(columns = {'discharge':'Total runoff [m^3 s^-1]'}, inplace = True)

discharge_df = discharge['discharge':'Total runoff [m^3 s^-1]'].copy()

sepBaseflow(discharge['Total runoff [m^3 s^-1]'],dt=60,A=1000,k=0.000546, dt_max=None, tp_min=None)

# %%
import hydrotoolbox
from hydrotoolbox import hydrotoolbox

ntsd = hydrotoolbox.baseflow_sep.boughton(input_ts=discharge_inp.loc[1:500,'discharge'])