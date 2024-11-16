# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:23:59 2024

@author: agnre
"""
'''Hello, let me introduce myself.

   My name is Alexander Rechter and I am studying Physics at LION at Leiden University and focus myself primarily on research in
   experimental physics. My main interests are not in physics however, they are in the field of meteorology and understanding and
   quantizing the weather using physics. Not only is my goal to help society I also love to contribute to science and generally keep
   myself busy with doing science and having fun in it.
   
   The python code you have opened in front of you now is what I am currently working on. This is only 4% of the entire future system of codes.
   This is called the "Python_peaks_RECON"-module and allows the analyst to determine where the minima and maxima of pressure are located in the dataset.
   It can be used to analyse data from the hurricane hunters as it comes in live and does not require the guessing and estimating by eye as most
   of you are used to. It also eliminates the need for CKZ and other relationships for most part as it takes the data from the center right during
   the heat of the event so to speak.
   
   Throughout the code I have sprinkled some other docstrings for you to read to understand the code better and make proper use of it.
   
   Disclaimer: I am not responsible for any problems you or your computer might experience when running this code. 
               It is your own responsibility to use the code responsibly and not abuse it for pushing your computer to the limit.
               If you do, it is your own risk. So I hereby urge you to be careful and make sure you do not randomly remove parts of the code.
               



    I hope you will have a lot of fun with the code and use it responsibly. I hope it will be useful and for any questions please contact me via:
        s3794180@vuw.leidenuniv.nl or agnrechter@gmail.com for inquiries about the code. My discord tag is @disaster_0125 and username NuclearPastaPhys.
        Feel free to contact me anytime and I will hopefully respond within 1-2 working days.
        

GOOD LUCK!
   '''
#IMPORTS DO NOT TOUCH

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from scipy.signal import find_peaks
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2

#HANDY CALCULATIONS, DO NOT TOUCH

# Calculates the distances between two lat/lon points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in kilometers (SI units supremacy)
    dlat = radians(lat2 - lat1)
    dlon = radians(lat2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Function needed to convert DMS to decimal degrees
def dms_to_decimal(coord):
    direction = coord[-1]
    degrees = int(coord[:-1]) // 100
    minutes = int(coord[:-1]) % 100
    decimal = degrees + minutes / 60.0
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

file_path = r"C:\Users\agnre\OneDrive\Documenten school\Bureaublad\RECON data raw\Milton\RawDataPass2v1.txt"
# Reading and processing the data
data = []

with open(file_path, 'r') as file:
    for line in file:
        columns = line.split()
        
        # Ensure there are enough columns to process
        if len(columns) < 7:
            continue  # Skip lines with insufficient columns
        
        # Unpack columns if the line has enough data
        time_str, lat_str, lon_str, pressure_str, windspeed_str, mmm_str, ppp_str = columns[0], columns[1], columns[2], columns[5], columns[6], columns[-3], columns[-1]
        
        # Skipping lines with "////" in any field
        if "////" in columns[0:6]:
            continue
        
        # Additional validation and processing here (as described before)
        if pressure_str.startswith(''):  # Example for processing 9XXX pressure values
            if len(lat_str) < 5 or len(lon_str) < 5:  # Validate lat/lon format
                continue
            
            if lat_str[-1] in ['N', 'S'] and lon_str[-1] in ['W', 'E']:
                try:
                    latitude = dms_to_decimal(lat_str)  # Convert latitude
                    longitude = dms_to_decimal(lon_str)  # Convert longitude
                    pressure = float(pressure_str) / 10.0  # Convert pressure to hPa
                    windspeed = float(windspeed_str)  # Windspeed in m/s or knots
                    mmm = float(mmm_str) if mmm_str != '///' else None  # Peak windspeed in knots
                    ppp = float(ppp_str) if ppp_str != '///' else None  # Rain rate in mm/hr
                    if pressure >= 800:    
                        data.append([time_str, latitude, longitude, pressure, windspeed, mmm, ppp])
                except ValueError:
                    continue  # Skip invalid rows

# Creating the DataFrame
df = pd.DataFrame(data, columns=['Time', 'Latitude', 'Longitude', 'Pressure', 'Windspeed', 'Peak Windspeed (MMM)', 'Rain Rate (PPP)'])


# We determine the minima using find_peaks on the inverted pressure data
inverted_pressure = -df['Pressure'].values
pressure = df['Pressure'].values


'''Ýou are allowed to only adjust one parameter here. It is the distance parameter.
If you adjust other things or rename things the code is going to not function and I would rather plot with a working code than a not-working one.

Kind regards,
Alexander Rechter (Leiden University; LION)'''


# Adjust this 'distance' parameter to control sensitivity of finding the minima
minima, _ = find_peaks(inverted_pressure, distance=90)  

#Uncomment if it plots one or multiple minima too much if so scale the -1 to -2, -3, etc.
#minima = minima[:-1] 

# Adjust this 'distance' parameter to control sensitivity of finding the maxima
maxima, _ = find_peaks(pressure, distance = 90)

#DO NOT TOUCH

#Here we extract the latitude, longitude, and pressure for the troughs (lows)
trough_data = df.iloc[minima]
ridge_data = df.iloc[maxima]

#Making the labels
coord_labels = [f"{lat:.2f}, {lon:.2f}" for lat, lon in zip(df['Latitude'], df['Longitude'])]
time_labels = [datetime.strptime(time, '%H%M%S').strftime('%H:%M:%S') for time in df['Time']]

#SCALE THIS TO DIFFERENT FORMATS IF YOU WANT
plt.figure(figsize=(16, 9))

# Plotting of all data points
plt.plot(time_labels, df['Pressure'], marker='.', linestyle='-', color='black', label='Pressure Data')

# Highlighting the minima and maxima in red
plt.plot(minima, df['Pressure'].iloc[minima], "rx", label='Pressure minima')
plt.plot(maxima, df['Pressure'].iloc[maxima], "ro", label='Pressure maxima')

# Plot locations and values of minima
for idx in minima:
    lat = df.iloc[idx]['Latitude']
    lon = df.iloc[idx]['Longitude']
    time = df.iloc[idx]['Time']
    Pmin = df.iloc[idx]['Pressure']
    mmm = df.iloc[idx]['Peak Windspeed (MMM)']
    ppp = df.iloc[idx]['Rain Rate (PPP)']
    plt.text(idx, Pmin - 12, f"{lat:.2f}, {lon:.2f}\n{Pmin:.1f} hPa\nMMM: {mmm if mmm else 'N/A'} knots\nPPP: {ppp if ppp else 'N/A'} mm/h", 
             fontsize=10, ha='center', color='blue')

# Plot locations and values of maxima
for idx in maxima:
    lat = df.iloc[idx]['Latitude']
    lon = df.iloc[idx]['Longitude']
    time = df.iloc[idx]['Time']
    Pmax = df.iloc[idx]['Pressure']
    mmm = df.iloc[idx]['Peak Windspeed (MMM)']
    ppp = df.iloc[idx]['Rain Rate (PPP)']
    plt.text(idx, Pmax + 2, f"{lat:.2f}, {lon:.2f}\n{Pmax:.1f} hPa\nMMM: {mmm if mmm else 'N/A'} knots\nPPP: {ppp if ppp else 'N/A'} mm/h", 
             fontsize=10, ha='center', color='red')

#Positioning the labels correctly
x_ticks_positions = list(range(0, len(df), 5))
x_ticks_labels = [time_labels[i] for i in x_ticks_positions] 

plt.title('Pressure vs Time (hPa, UTC)')

#labeling the axes
plt.xlabel('Time (UTC)')
plt.ylabel('Pressure (hPa)')

#pressure range
plt.ylim(882, 1013)
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.locator_params(axis='x', nbins = 5) 
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))

'''Alright I see you like coding in Python. So here we have the part that makes it possible to plot the time labels on the x-axis.
    
    Let's take a tour.
    
    The x_ticks_positions function makes it possible to adjust how many labels we want to be plotted. Keep the number small as otherwise..
    ..it would be unreadable and well that is just not something my heart skips a beat for.
    
    The x_ticks_labels function makes it possible to generate the labels. Please do not touch. Thank you very much.
    
    Instructions of how to use it: See comment.
    '''
#Time labels for x-axis
x_ticks_positions = list(range(0, len(df),5))  #Adjust the number after len(df) for the amount of time labels on the x-axis
x_ticks_labels = [time_labels[i] for i in x_ticks_positions] 
plt.xticks(x_ticks_positions, x_ticks_labels, rotation=45, ha='right')

#Plot labels of the lat-lon for the x-axis
#x_ticks_positions = list(range(0, len(df), 12))  #Adjust this for the amount of time labels on the x-axis
#x_ticks_labels = [coord_labels[i] for i in x_ticks_positions] 
#plt.xticks(x_ticks_positions, x_ticks_labels, rotation=45, ha='right')

#Creates the plot and legend
plt.legend()
plt.show()

'''This part of the code is for the hardcore physical programming nerds.

    Let's take a tour together.
    
    So we start with the function that prints the data from the "troughs" in the data. That are those small valleys you see until it hits the minima.
    I defined it as local/absolute minima as two put together makes one a local the other absolute. For one single pass it is the absolute minimum and then there are..
    two local maxima. 
    
    Hope that that makes it clear.
    
    Next up we have the part of the code that makes it possible to print the additional information we might want to know
    about the storm. Such as the latitudes and longitudes of these observations and how far the plane has travelled to the next pass,
    which can be used to determine how fast the hurricane hunters flew on average.
    
    This average flight speed can then be used in error analysis so any potential pressure measurement mistakes due to the plane's velocity can be..
    filtered out and thus would result in valid data. So keep in mind it is still RAW.
    '''
# Printing of the minima data
print("Pressure Troughs (local / absolute minima):")

#Printing the additional information
prev_lat, prev_lon = None, None
for idx, row in trough_data.iterrows():
    lat, lon, pressure, time = row['Latitude'], row['Longitude'], row['Pressure'], row['Time']
    if prev_lat is not None and prev_lon is not None:
        distance = haversine(lat, lon, prev_lat, prev_lon)
        print(f"Latitude: {lat:.2f} N, Longitude: {lon:.2f} E, Pressure: {pressure:.1f} hPa, Distance from previous: {distance:.2f} km, Time of observation: {time} UTC")
    else:
        print(f"Latitude: {lat:.2f}, Longitude: {lon:.2f}, Pressure: {pressure:.1f} hPa, Time of observation: {time}")
    prev_lat, prev_lon = lat, lon

#Determines the index of minimum and maximum pressure
min_pressure_idx = df['Pressure'].idxmin()
max_pressure_idx = df['Pressure'].idxmax()

# Finds the latitude and longitude corresponding to the minimum and maximum pressure
min_lat, min_lon = df.iloc[min_pressure_idx]['Latitude'], df.iloc[min_pressure_idx]['Longitude']
max_lat, max_lon = df.iloc[max_pressure_idx]['Latitude'], df.iloc[max_pressure_idx]['Longitude']

# Printing the minimum and maximum pressure along with corresponding latitude and longitude
print(f"\nMinimum Pressure: {df['Pressure'].min()} hPa, Phi: {min_lat:.2f} N, Lambda: {min_lon:.2f} E")
print(f"Maximum Pressure: {df['Pressure'].max()} hPa, Phi: {max_lat:.2f} N, Lambda: {max_lon:.2f} E")