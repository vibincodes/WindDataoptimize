#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:17:25 2023

@author: vibinsmac
"""


import pandas as pd
import plotly.graph_objs as go
from clean import clean as cl
import streamlit as st
import numpy as np
data= {"Name":['Default'],
          "speed_range_max":[25],
          "speed_range_std":[3],
          "direction_std_min":[3],
          "direction_std_max":[75], 
          "temp_range_min":[-35],
          "temp_range_max":[35],
          "pressure_range_min":[940],
          "pressure_range_max":[1060],
          "humidity_range_max":[100],
          "wind_speed_relation":[3],
          "wind_direction_relation":[20],
          "windpseed_trend":[5],
          "temperature_trend":[5],
          "pressure_trend":[10]
          }
value= pd.DataFrame(data)

main_menu = ['Default']
current_menu = st.sidebar.selectbox("--Select Config--", main_menu)
config = value.loc[value['Name']==current_menu]
import streamlit as st

try:
    data = st.file_uploader('Upload the file')
    if uploaded_file is not None:
        # process the uploaded file here
        pass
except:
    st.warning("Upload your file.")

check = cl(data,config)
@st.cache
def tests(check):
    check.missing_time()
    check.repeated_timestamps()
    check.chrono_check()
    check.range_test()
    check.relational_test()
    check.trend_test()
    check.icing()
    check.constant_check()
    check.spike_test()
    return check.wind['2018-12-01 00:00:00':'2018-12-31 23:50:00'], check.wind_duplicated , check.missing_timestamps ,check.wind_speed, check.wind_direction,check.wind_pressure,check.wind_humidity,check.wind_temperature   


a = pd.DataFrame()    
if st.sidebar.checkbox('Run all Tests'):
    wi,repeated,missing,wind_speed,wind_direction,wind_pressure,wind_humidity,wind_temperature = tests(check)
    wind = wi.copy()
    flag_col =[]
    for col in wind: 
        if 'Flag' in col:
            flag_col.append(col)
    def show_flag(flag):
        wind,repeated,missing,wind_speed,wind_direction,wind_pressure,wind_humidity,temperature = tests(check)
        mask = 0
        for col in wind: 
            if 'Flag' in col:
                mask |= ((wind[col] & flag)==flag)
        return wind.loc[mask]
    test_list = ['Show Missing Timestamps', 'Show Repeated Timestamps', 'Show Range Test Flagged Entries', 'Show Relational Test Flagged Entries','Show Trend Test Flagged Entries','Show Icing Test Flagged Entries','Show Constant Test Flagged Entries','Show Spike Test Flagged Entries']
    test_type = st.selectbox("Menu", test_list)
    if test_type =='Show Spike Test Flagged Entries':
        df = wi.copy()
        d = show_flag(0b100000)
        count = (d[flag_col]&0b100000)==0b100000
        count_df = count.sum()
        st.write('spike Flagged Entries : ',len(d))
        fig = go.Figure()
        for col in wind_speed:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100000)==0b100000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Speed Time Series', xaxis_title='Timestamp', yaxis_title='Wind Speed (m/s)')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_direction:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100000)==0b100000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Direction Time Series', xaxis_title='Timestamp', yaxis_title='Wind Direction in deg')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_pressure:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100000)==0b100000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Pressure Time Series', xaxis_title='Timestamp', yaxis_title='Pressure in mbar')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_humidity:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100000)==0b100000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Humidity Time Series', xaxis_title='Timestamp', yaxis_title='Humidity in %')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_temperature:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100000)==0b100000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Temperature Time Series', xaxis_title='Timestamp', yaxis_title='Temperature in C')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        st.dataframe(count_df,use_container_width=True)
        st.dataframe(d)
        
    if test_type =='Show Constant Test Flagged Entries':
        df = wi.copy()
        d = show_flag(0b10000)
        count = (d[flag_col]&0b10000)==0b10000
        count_df = count.sum()
        st.write('Constant Flagged Entries : ',len(d))
        fig = go.Figure()
        for col in wind_speed:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10000)==0b10000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Speed Time Series', xaxis_title='Timestamp', yaxis_title='Wind Speed (m/s)')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_direction:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10000)==0b10000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Direction Time Series', xaxis_title='Timestamp', yaxis_title='Wind Direction in deg')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_pressure:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10000)==0b10000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Pressure Time Series', xaxis_title='Timestamp', yaxis_title='Pressure in mbar')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_humidity:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10000)==0b10000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Humidity Time Series', xaxis_title='Timestamp', yaxis_title='Humidity in %')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_temperature:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10000)==0b10000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Temperature Time Series', xaxis_title='Timestamp', yaxis_title='Temperature in C')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        st.dataframe(count_df,use_container_width=True)
        st.dataframe(d)
        
    if test_type =='Show Icing Test Flagged Entries':
        df = wi.copy()
        d = show_flag(0b1000)
        count = (d[flag_col]&0b1000)==0b1000
        count_df = count.sum()
        st.write('Icing Flagged Entries : ',len(d))
        fig = go.Figure()
        for col in wind_speed:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1000)==0b1000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Speed Time Series', xaxis_title='Timestamp', yaxis_title='Wind Speed (m/s)')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_direction:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1000)==0b1000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Direction Time Series', xaxis_title='Timestamp', yaxis_title='Wind Direction in deg')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_pressure:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1000)==0b1000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Pressure Time Series', xaxis_title='Timestamp', yaxis_title='Pressure in mbar')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_humidity:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1000)==0b1000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Humidity Time Series', xaxis_title='Timestamp', yaxis_title='Humidity in %')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_temperature:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1000)==0b1000), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Temperature Time Series', xaxis_title='Timestamp', yaxis_title='Temperature in C')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        st.dataframe(count_df,use_container_width=True)
        st.dataframe(d)
        
    if test_type =='Show Trend Test Flagged Entries':
        df = wi.copy()
        d = show_flag(0b100)
        count = (d[flag_col]&0b100)==0b100
        count_df = count.sum()
        st.write('Trend Flagged Entries : ',len(d))
        fig = go.Figure()
        for col in wind_speed:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100)==0b100), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Speed Time Series', xaxis_title='Timestamp', yaxis_title='Wind Speed (m/s)')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_direction:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100)==0b100), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Direction Time Series', xaxis_title='Timestamp', yaxis_title='Wind Direction in deg')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_pressure:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100)==0b100), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Pressure Time Series', xaxis_title='Timestamp', yaxis_title='Pressure in mbar')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_humidity:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100)==0b100), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Humidity Time Series', xaxis_title='Timestamp', yaxis_title='Humidity in %')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_temperature:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b100)==0b100), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Temperature Time Series', xaxis_title='Timestamp', yaxis_title='Temperature in C')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        st.dataframe(count_df,use_container_width=True)
        st.dataframe(d)
        
    if test_type =='Show Relational Test Flagged Entries':
        df = wi.copy()
        d = show_flag(0b10)
        count = (d[flag_col]&0b10)==0b10
        count_df = count.sum()
        st.write('Relational Flagged Entries : ',len(d))
        fig = go.Figure()
        for col in wind_speed:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10)==0b10), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Speed Time Series', xaxis_title='Timestamp', yaxis_title='Wind Speed (m/s)')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_direction:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10)==0b10), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Direction Time Series', xaxis_title='Timestamp', yaxis_title='Wind Direction in deg')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_pressure:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10)==0b10), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Pressure Time Series', xaxis_title='Timestamp', yaxis_title='Pressure in mbar')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_humidity:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10)==0b10), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Humidity Time Series', xaxis_title='Timestamp', yaxis_title='Humidity in %')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_temperature:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b10)==0b10), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Temperature Time Series', xaxis_title='Timestamp', yaxis_title='Temperature in C')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        st.dataframe(count_df,use_container_width=True)
        st.dataframe(d)
        
    if test_type =='Show Range Test Flagged Entries':
        df = wi.copy()
        d = show_flag(0b1)
        count = (d[flag_col]&0b1)==0b1
        count_df = count.sum()
        st.write('Range Flagged Entries : ',len(d))
        fig = go.Figure()
        for col in wind_speed:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1)==0b1), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Speed Time Series', xaxis_title='Timestamp', yaxis_title='Wind Speed (m/s)')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_direction:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1)==0b1), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Wind Direction Time Series', xaxis_title='Timestamp', yaxis_title='Wind Direction in deg')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_pressure:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1)==0b1), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Pressure Time Series', xaxis_title='Timestamp', yaxis_title='Pressure in mbar')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_humidity:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1)==0b1), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Humidity Time Series', xaxis_title='Timestamp', yaxis_title='Humidity in %')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        
        fig = go.Figure()
        for col in wind_temperature:
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='lines',name = col))
            df.loc[~((df[col+'Flag'] &0b1)==0b1), col] = np.nan
            fig.add_trace(go.Scatter(x=df.index, y=df[col],mode='markers' , name = col+'Flag'))
        fig.update_layout(title='Temperature Time Series', xaxis_title='Timestamp', yaxis_title='Temperature in C')
        fig.update_yaxes(fixedrange=True)
        st.plotly_chart(fig,config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        st.dataframe(count_df,use_container_width=True)
        st.dataframe(d)
        
    if test_type =='Show Repeated Timestamps':
        a = repeated
        st.write('Repeated Time stampEntries : ',len(a))
        st.write(a)
        
    if test_type =='Show Missing Timestamps':
        a = missing
        st.write('Repeated Time stampEntries : ',len(a))
        st.write(a)    
    
     
#st.dataframe(a)   

        
