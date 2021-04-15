#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BE523 Biosystems Analysis & Design
HW24 - Question 5. Modify code for maximum daily soil temperature
Prof. Waller solution.

Created on Wed Apr 14 14:55:12 2021
@author: eduardo
"""
#======================Block 0: Adding Libraries=============================
from datetime import date
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import scipy

from scipy import interpolate

def import_wsdata_online(location, year, hourly_data, AZ_location_list):        
    AZ_location_num = []
    for i in range(len(AZ_location_list)):
        AZ_location_num.append(str(i+1).zfill(2))
    Loc_num = AZ_location_list.index(location)
    if hourly_data == True:
        url = 'https://cals.arizona.edu/azmet/data/'+AZ_location_num[Loc_num] + \
            str(year)[-2:] + 'rh.txt'
            
        names = ['Year','DOY','Hour of day','Air Temp','RH','VPD',
                  'SR','rainfall','4" Soil Temp','20" Soil Temp',
                  'wind_speed','Wind Vector Magnitude','Wind Vector Direction','Wind Direction Standard Deviation',
                  'Max Wind Speed','ET0','Actual Vapor Pressure','Dew point']
    else:
        url = 'https://cals.arizona.edu/azmet/data/'+AZ_location_num[Loc_num] + \
            str(year)[-2:] + 'rd.txt'
        # str(year)[-2:] will take the last two digits of the year and make it a string so it can be added to the url string
        # str(2019)[-2:] = 19 , str(1999)[-2:] = 99
        # "names" is a list that contains the headers of the data
        names = ['Year','DOY','Station Number','tmax','tmin','Air Temp - Mean','RH - Max','rh','RH - Mean','VPD - Mean',
                  'SR-Total','rainfall','4" Soil Temp Max','4" Soil Temp Min','4" Soil Temp Mean','20" Soil Temp Max','20" Soil Temp Min','20" Soil Temp Mean',
                  'wind_speed','Wind Vector Magnitude','Wind Vector Direction','Wind Direction Standard Deviation',
                  'Max Wind Speed', 'Heat units','ET0', 'et', 'Actual Vapor Pressure','Dew point']
    wsdata = pd.read_csv(url,sep = ',', header = None, names = names)
    wsdata['1/24'] = 1
        
    for col in wsdata.columns:
        if (wsdata[col] == 999).any():
            wsdata[col].replace(999, np.nan, inplace = True)
            wsdata[col].interpolate(inplace = True)
    wsdata['Date'] = dt.datetime(2017,1,1)
    if hourly_data == True:
        wsdata = wsdata[['Date','SR','wind_speed', 'RH']]
        for j in range(1, len(wsdata) + 1):
            wsdata['Date'].loc[j - 1] = dt.datetime(year, 1, 1) + dt.timedelta(hours = j - 1)
    else:
        wsdata = wsdata[['Date','rh', 'wind_speed', 'et', 'rainfall', 'tmax', 'tmin', '1/24', '4" Soil Temp Max']]
        for j in range(1, len(wsdata) + 1):
            wsdata['Date'].loc[j - 1] = dt.datetime(year, 1, 1) + dt.timedelta(days = j - 1)
    return wsdata

hourly_data = False
DOY = 1
RH_hr = np.zeros(24)
Hr = np.zeros(24)
time = np.arange(0,365)
AZ_location_list = ['Tucson', 
                'Yuma Valley',
                'Yuma Mesa',
                'Safford',
                'Coolidge',
                'Maricopa',
                'Aguila',
                'Parker',
                'Bonita',
                'Waddell',
                'Phoenix Greenway',
                'Marana',
                'Yuma North Gila',
                'Phoenix Encanto',
                'Paloma',
                'Mohave',
                'Mohave #2',
                'Queen Creek',
                'Harquahala',
                'Roll',
                'Buckeye',
                'Desert Ridge',
                'Mesa',
                'Flagstaff',
                'Prescott',
                'Payson',
                'Bowie',
                'Kansas Settlement']
location = 'Maricopa'
if location in AZ_location_list:
    NewWeather2018 = import_wsdata_online(location, 2019, hourly_data, AZ_location_list)
    soil_temp = NewWeather2018['4" Soil Temp Max']
    soil_temp_CS = scipy.interpolate.CubicSpline(time, soil_temp)
    
    plt.figure(1)
    plt.plot(time, soil_temp_CS(time),label='Cubic Spline')
    plt.plot(time, soil_temp, label = 'linear interpolation')
    plt.plot(time, soil_temp, 'x', label = 'observed')
    
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
    plt.ylabel('Max Soil Temp (°C)')
    plt.xlabel('DOY, 2017')

    plt.savefig('q5_soil_temp_interp.png', dpi=300, bbox_inches='tight')
    plt.show()
        
else:
    print('Weather at '+location + ' not available.')



