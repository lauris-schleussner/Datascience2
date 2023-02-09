import json
import csv
import pandas as pd
from glob import glob
# load all stops from stops.txt
def load_stops(city = "GER_Saxony_Leipzig"):

    # find the path, even if theres a 
    try:
        path = glob("data/" + city + "/**/stops.txt")[0]
    except:
        path = "data/" + city + "/stops.txt"
    
    
    df = pd.read_csv(path, sep = ",", header = 0)
    
    if not(('stop_id' in df.columns) and ("stop_lat" in df.columns) and ("stop_lon" in df.columns)):
        raise ValueError("GTFS data does not contain required rows")
    
    df = df[["stop_id", "stop_lat", "stop_lon"]]

    return df

# load all stop times from stop_times
def load_stop_times_df(city = "GER_Saxony_Leipzig"):

    path = "data/" + city + "/stop_times.txt"

    df = pd.read_csv(path, sep = ",", header = 0)
    df = df[["trip_id","arrival_time","departure_time","stop_id"]]

    return df


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load_coordinates():
    with open("lvb_auswertung/coordinates.json", "r") as f:
        return json.load(f)

def load_all_neighbours():
    with open("lvb_auswertung/neighbours.json", "r") as f:
        return json.load(f)

def load_stops_as_dict(city):

    df = load_stops(city)

    id = df["stop_id"].tolist()
    lat = df["stop_lat"].tolist()
    lon = df["stop_lon"].tolist()


    d = {}
    for i, la, lo in zip(id, lat, lon):
        d[i] = [la, lo]

    return d


if __name__ == "__main__":
    load_stop_times_df("US_Texas_Amarillo")

