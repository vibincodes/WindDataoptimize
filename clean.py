#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 12:23:26 2023

@author: vibinsmac
"""

import pandas as pd
import numpy as np
import re
import time
import glob



# 1 - Range Test
# 2 - Relational Test
# 4 - Trend Test
# 8 - Icing
# 16 - Constant 
# 32 - Spike

class clean:

    def __init__(self,path,config):
        self.wind =pd.read_csv(path,parse_dates=['Date/Time'], index_col=('Date/Time'))
        self.config = config
        self.wind_speed = []
        self.windspeed_std = []
        self.windspeed_max = []
        self.wind_direction = []
        self.winddirection_std = []
        self.wind_temperature = []
        self.wind_pressure = []
        self. wind_humidity = []
        self.solar_radiation = []
        self.flag_columns = []
        
        def custom_key(value):
            match = re.search(r'\d+', value)
            if match:
                int_value = int(match.group())
                if int_value >= 100:
                    return (1, int_value)
                else:
                    return (0, -int_value)
            else:
                return (0, 0)

        for col in self.wind:
            if ('m/s' in col.lower() or 'speed' in col.lower()) and 'std' not in col.lower():
                col_renamed='wind_speed_'+re.findall('\d+', col)[0]+'m'
                if col_renamed in self.wind_speed:
                    col_renamed = 'wind_speed_'+re.findall('\d+', col)[0]+'m'+'_B'
                self.wind = self.wind.rename(columns={col: col_renamed})
                self.wind_speed.append(col_renamed)
                
            if ('m/s' in col.lower() or 'speed' in col.lower()) and 'std' in col.lower():
                col_renamed = 'windspeed_std'+re.findall('\d+', col)[0]+'m'
                if col_renamed in self.windspeed_std:
                    col_renamed= 'windspeed_std'+re.findall('\d+', col)[0]+'m''_B'
                self.wind = self.wind.rename(columns={col: col_renamed})
                self.windspeed_std.append(col_renamed)
                
            if ('m/s' in col.lower() or 'speed' in col.lower()) and 'max' in col.lower():
                col_renamed ='windspeed_max'+re.findall('\d+', col)[0]+'m'
                if col_renamed in self.windspeed_max:
                    col_renamed = 'windspeed_max'+re.findall('\d+', col)[0]+'m'+'_B'
                self.wind = self.wind.rename(columns={col:col_renamed })
                self.windspeed_max.append(col_renamed)
                
            if (('°' in col.lower() and 'temp' not in col.lower() and 'std' not in col.lower()) or ('dir' in col.lower() and 'std' not in col.lower())):
                col_renamed = 'wind_direction_'+re.findall('\d+', col)[0]+'m'
                self.wind = self.wind.rename(columns={col: col_renamed})
                self.wind_direction.append(col_renamed)    
                
            if (('°' in col.lower() and 'std' in col.lower() and 'temp' not in col.lower()) or ('dir' in col.lower() and 'std' in col.lower())):
                col_renamed = 'wind_direction_std_'+re.findall('\d+', col)[0]+'m'
                self.wind = self.wind.rename(columns={col: col_renamed})
                self.winddirection_std.append(col_renamed)
                
                
            if ('°c' in col.lower() or 'temp' in col.lower()):
                match_list = re.findall('\d+', col)
                if len(match_list)>0 :
                    col_renamed = 'temperature_'+re.findall('\d+', col)[0]+'m'
                else:
                    col_renamed = 'temperature_'
                self.wind = self.wind.rename(columns={col: col_renamed})
                self.wind_temperature.append(col_renamed)
                
            if 'mbar' in col.lower()or 'press' in col.lower():
                match_list = re.findall('\d+', col)
                if len(match_list)>0 :
                    col_renamed = 'pressure_'+re.findall('\d+', col)[0]+'m'
                else:
                    col_renamed = 'pressure_'
                self.wind = self.wind.rename(columns={col: col_renamed})
                self.wind_pressure.append(col_renamed)
                
            if 'hum' in col.lower():
                match_list = re.findall('\d+', col)
                if len(match_list)>0 :
                    col_renamed = 'humidity_'+re.findall('\d+', col)[0]+'m'
                else:
                    col_renamed = 'humidity_'
                self.wind = self.wind.rename(columns={col:col_renamed })
                self.wind_humidity.append(col_renamed)
                
        for col in self.wind:
            self.wind[col+'Flag'] = 0b0
            #Getting Flag columns
        for col in self.wind:
            if 'Flag' in col:
                self.flag_columns.append(col)
         
        #Checking for chronological order
    def chrono_check(self):
        sorted_wind = self.wind.sort_index()
        if not sorted_wind.equals(self.wind):
            self.wind = sorted_wind
        print('Chrono check DONE')
    #Removing repeated time stamps
    def repeated_timestamps(self):
        self.wind_duplicated = self.wind[self.wind.index.duplicated()]
        self. wind = self.wind[~self.wind.index.duplicated()]  
        print('Duplicates check DONE')
    
    
    #missing Time Stamps
    def missing_time(self):
        all_timestamps = pd.date_range(start=self.wind.index.min(), end=self.wind.index.max(), freq='10min')
        self.missing_timestamps = [ts for ts in all_timestamps if ts not in self.wind.index]
        print('Missing timestamp check DONE')
    
              

    #Range Test
    def range_test(self):
        for col in self.wind_speed:
            
            self.wind.loc[(self.wind[col]<0 )|(self.wind[col]> self.config.speed_range_max[0]),[col+'Flag']]|=0b1
        for col in self.windspeed_std:
           
            self.wind.loc[(self.wind[col]<0)|(self.wind[col]>self.config.speed_range_std)[0],[col+'Flag']]|=0b1
        for col in self.wind_direction:
            
            self.wind.loc[(self.wind[col]<0)|(self.wind[col]>360),[col+'Flag']]|=0b1
        for col in self.winddirection_std:
            
            self.wind.loc[(self.wind[col]<self.config.direction_std_min[0])|(self.wind[col]>self.config.direction_std_max[0]),[col+'Flag']]|=0b1    
        for col in self.wind_temperature:
            
            self.wind.loc[(self.wind[col]<self.config.temp_range_min[0])|(self.wind[col]>self.config.temp_range_max[0]),[col+'Flag']]|=0b1
        for col in self.wind_pressure:
            
            self.wind.loc[(self.wind[col]<self.config.pressure_range_min[0])|(self.wind[col]>self.config.pressure_range_max[0]),[col+'Flag']]|=0b1
        for col in self.wind_humidity:
            
            self.wind.loc[(self.wind[col]<0)|(self.wind[col]>100),[col+'Flag']]|= 0b1  
        print('Range test DONE')
        
        
        
        
    #Relational Test
    def relational_test(self):
        for i in range(len(self.wind_speed)):
            if i<len(self.wind_speed)-1:
                self.wind.loc[abs((self.wind[self.wind_speed[i]]) - (self.wind[(self.wind_speed[i+1])])) >= self.config.wind_speed_relation[0] ,[self.wind_speed[i]+'Flag',self.wind_speed[i+1]+'Flag']] |= 0b10
        for i in range(len(self.wind_direction)-1):
            diff_direction = self.wind[self.wind_direction[i]]-self.wind[self.wind_direction[i+1]]
            diff_direction[diff_direction < -180] += 360
            diff_direction[diff_direction > 180] -= 360
            abs_diff_direction = abs(diff_direction)
            self.wind.loc[abs_diff_direction > self.config.wind_direction_relation[0], [self.wind_direction[i]+'Flag',self.wind_direction[i+1]+'Flag' ]] |= 0b10
        print('Relational test DONE')
    
    #Trend Test
    def trend_test(self):
        for col in self.wind_speed:
            self.wind.loc[abs(self.wind[col] - self.wind[col].rolling(6).mean()) > self.config.windpseed_trend[0], col+'Flag'] |= 0b100
        for col in self.wind_temperature:
            self.wind.loc[abs(self.wind[col] - self.wind[col].rolling(6).mean()) > self.config.temperature_trend[0], col+'Flag'] |= 0b100
        for col in self.wind_pressure:
            self.wind.loc[abs(self.wind[col] - self.wind[col].rolling(6).mean()) > self.config.pressure_trend[0], col+'Flag'] |= 0b100
        print('Trend test DONE')
    
    #Icing
    def icing(self):
        for col ,col1,col2,col3 in zip(self.wind_speed,self.wind_temperature,self.wind_humidity,self.winddirection_std): 
            self.wind.loc[(self.wind[col3] <= 0.5) & (self.wind[col1]) < 2 & (self.wind[col2]>80) ,col+'Flag']|= 0b1000
        print('Icing test DONE')
    
    #Constant Value 
    def constant_check(self):
        for col in self.wind_speed:
            self.wind.loc[(self.wind[col].groupby([self.wind[col].diff().ne(0).cumsum()]).transform('size').ge(5).astype('bool')) & (self.wind[col]>2),col+'Flag'] |= 0b10000
        for col,col1 in zip(self.wind_direction,self.wind_speed):
            self.wind.loc[(self.wind[col].groupby([self.wind[col].diff().ne(0).cumsum()]).transform('size').ge(5).astype('bool'))& (self.wind[col1]>2),col+'Flag'] |= 0b10000
        for col in self.wind_pressure:
            self.wind.loc[self.wind[col].groupby([self.wind[col].diff().ne(0).cumsum()]).transform('size').ge(5).astype('bool'),col+'Flag'] |= 0b10000
        for col in self.wind_temperature:
            self.wind.loc[self.wind[col].groupby([self.wind[col].diff().ne(0).cumsum()]).transform('size').ge(5).astype('bool'),col+'Flag'] |= 0b10000                
        print('Constant test DONE') 
        
    #spike Test 
    def spike_test(self):
        for col,col1 in zip(self.wind_speed,self.windspeed_std):
            if re.findall('\d+', col)[0] == re.findall('\d+', col1)[0]:
                self.wind.loc[self.wind[col] > (self.wind[col].rolling(24).mean() + self.wind[col1].rolling(24).mean()), col+'Flag'] |= 0b100000
            else:
                self.wind.loc[self.wind[col] > (self.wind[col].rolling(24).mean()), col+'Flag'] |= 0b100000
        print('Spike test DONE')
    
   
        
                        
   
    def imp_csv(self):
        self.wind.to_csv('/Users/vibinsmac/Library/Mobile Documents/com~apple~CloudDocs/Wind/Data/file_name.csv')
