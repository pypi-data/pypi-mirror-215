# -*- coding: utf-8 -*-
"""
@author: ftong
"""
import sys
import pandas as pd
import scipy.io
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy import read_events
import numpy as np


def read_mat(matlab_file, mag_label, **kwargs):
    
    mag = []
    time = []
    
    mat = scipy.io.loadmat(matlab_file)

    for i in range(0,len(mat['Catalog'][0])):
        
        # Extract magnitudes
        if mat['Catalog'][0][i][0]==mag_label:
            mag_frame = mat['Catalog'][0][i]
            mag = mag_frame[2].flatten()
            continue
    
        # Extract times
        if mat['Catalog'][0][i][0]=='Time':
            time_frame = mat['Catalog'][0][i]
            t1 = time_frame[2].flatten()
            datenums = np.array(t1)
            t2= pd.to_datetime(datenums-719529, unit='D') #convert from Matlab's datenum format to human readable format
            time = [UTCDateTime(str(t)) for t in t2] # convert to list of obspy UTCDateTime objects
            
    if len(mag)==0:
        print("Magnitude column not found in .mat file")
        sys.exit()

    return time, mag

def read_csv(csv_file,  datenum= True, **kwargs):
    
    # df = pd.read_csv(csv_file, engine="pyarrow", **kwargs) #use pyarrow for faster input
    df = pd.read_csv(csv_file, **kwargs)
    
    df.columns= df.columns.str.lower() # convert header to all lowercase letters
    header = df.columns
    
    # replace with common column names if present
    if 'time' in header:
        t_label = 'time'
    elif 't' in header:
        t_label = 't'

    if 'lon' in header:
        x_label = 'lon'
    elif 'long' in header:
        x_label = 'long'
    elif 'longitude' in header:
        x_label = 'longitude'
    elif 'x' in header:
        x_label = 'x'
        
    if 'lat' in header:
        y_label = 'lat'
    elif 'latitude' in header:
        y_label = 'latitude'
    elif 'y' in header:
        y_label = 'y'

    if 'depth' in header:
        z_label = 'depth'
    elif 'z' in header:
        z_label = 'z'

    if 'mag' in header:
        mag_label = 'mag'    
    elif 'ml' in header:
        mag_label = 'ml'
    elif 'magnitude' in header:
        mag_label = 'magnitude'

    t_raw = df[t_label].to_numpy()
    lat = df[y_label].to_numpy()
    lon = df[x_label].to_numpy()
    depth = df[z_label].to_numpy()
    mag = df[mag_label].to_numpy()
    
    if datenum:    
        timestamps = pd.to_datetime(t_raw-719529, unit='D') #convert from Matlab's datenum format to human readable format
        
    time = timestamps.to_numpy() # get time as numpy datetime64 objects
    time = [UTCDateTime(str(t)) for t in time] # convert to list of obspy UTCDateTime objects
    
    return time, lat, lon, depth, mag


def read_fdsn(service, save_to_file=None, file_format="QUAKEML", **kwargs):
       
    client = Client(service)    
    cat = client.get_events(**kwargs)
    
    if save_to_file != None:
        cat.write(filename=save_to_file, format=file_format, **kwargs)
    
    return extract_from_obspy_cat(cat)


def read_obspy(file, **kwargs):
    
    cat = read_events(file)
    
    return extract_from_obspy_cat(cat)


def extract_from_obspy_cat(cat):
    
    mag = np.array([event.preferred_magnitude().mag for event in cat])
    time = [event.preferred_origin().time for event in cat]
    lat = [event.preferred_origin().latitude for event in cat]
    lon = [event.preferred_origin().longitude for event in cat]
    depth = [event.preferred_origin().depth for event in cat]
    
    return time, lat, lon, depth, mag