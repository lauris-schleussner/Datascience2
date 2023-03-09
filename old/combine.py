
import glob
from geopy.geocoders import Nominatim
import requests as r
import os
from tqdm import tqdm
import multiprocessing as mp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


# get location
locator = Nominatim(user_agent="Helloworld")
location = locator.geocode("US_Alaska_Klawock")
lat, lon = location.latitude, location.longitude

# easier
global LATMAX, LONMAX, LATMIN, LONMIN

# get all city names in the dataset
all_city_paths = glob.glob("data/*")[1:2]

# get populationdata at location
def scan_popdata(filenumber):

    df = pd.read_csv("population_data/" + str(filenumber) + ".csv", sep = ",", names = ["y","x","weight"], dtype = np.float64, skiprows = 1)
    df = df[(df.x >= LATMIN) & (df.x <= LATMAX)]
    df = df[(df.y >= LONMIN) & (df.y <= LONMAX)]

    print(len(df))

    return df

# for each city look up square coordinates
for city_name in tqdm(all_city_paths):

    print(city_name)

    # get coordinates in square around city center
    resp = r.get("https://api.maptiler.com/geocoding/legacy/q/" + os.path.basename(city_name) +".js?key=XsDCgwk8uMC75zY8VXtN")
    LATMIN, LONMIN, LATMAX, LONMAX = resp.json()["results"][0]["boundingbox"]

    df = pd.DataFrame()
    for i in range(1,7):
        df = pd.concat([df, scan_popdata(i)])

    print("converting to numpy...")
    # convert to numpy
    x = df["x"].tolist()
    y = df["y"].tolist()
    weight = df["weight"].tolist()

    BINS = 200
    BLUR = 0