from copy import deepcopy
from utils import load_stops, chunks

import json
from tqdm import tqdm
from geopy.distance import geodesic as GD
import seaborn as sns
import matplotlib.pyplot as plt


# approximation: nur neighbours
def all_distances(coordinate, cur_haltestellen):
    cur_haltestellen.remove(coordinate)
    distances = []
    for other_coordinate in cur_haltestellen:
        #if coordinate == other_coordinate:
        #    continue
        coordinate, other_coordinate = tuple(coordinate), tuple(other_coordinate)
        distances.append(
            #GD(coordinate, other_coordinate).m
            ((coordinate[0]-other_coordinate[0])**2+(coordinate[0]-other_coordinate[0])**2)**(1/2)
        )
    if 0 in distances:
        distances = distances.remove(0)
    if distances is None:
        return 0
    value = sum([1/x for x in distances])
    return value

def haltestellendichte_working():
    with open("lvb_auswertung/coordinates.json", "r") as f:
        data = json.load(f)
        coordinates = [data[elem] for elem in data]
    #coordinates = [[float(c) for c in elem[-2:]] for elem in load_stops()]
    values = []
    for elem in tqdm(coordinates):
        values.append([elem, all_distances(elem, deepcopy(coordinates))])
    with open("lvb_auswertung/dichte.json", "w+") as f:
        json.dump(values, f, indent=4)


def to_coordinates(level_num):
    with open(f"lvb_auswertung/neighbours_{level_num}.json", "r") as f:
        data:dict = json.load(f)
    coords = extract_coordinates()
    data:list = [[coords[k], [coords[elem] for elem in v]] for k, v in data.items()]
    return data

def distances(level_num):
    data = to_coordinates(level_num)
    data_new = []
    for elem in tqdm(data):
        data_new.append([
            elem[0], [(GD(tuple(elem[0]), tuple(other)).m) for other in elem[1]]
        ])
    print(data_new[0])
    return data_new

def extract_coordinates():
    from pyproj import Proj
    data = {}
    with open("gtfsmdvlvb/stops.txt", "r") as f:
        txt = [elem.split(",") for elem in f.read().split("\n")[1:-1]]
    for elem in tqdm(txt):
        #data[elem[0]] = [float(elem[-2]), float(elem[-1])]
        data[elem[0]] = Proj('epsg:31468')(float(elem[-1]), float(elem[-2]))
    with open("lvb_auswertung/coordinates.json", "w+") as f:
        json.dump(data, f, indent=4)
    return data

def plot_data():
    with open("lvb_auswertung/dichte.json", "r") as f:
        data = json.load(f)
    x = [elem[0][0] for elem in data]
    y = [elem[0][1] for elem in data]
    s = [elem[1] for elem in data]
    s_max = max(s)
    s = [elem/s_max for elem in s]
    plt.scatter(x,y)
    plt.show()
    
    

if __name__ == "__main__":
    haltestellendichte_working()
    

# Idee: Wir multiplizieren schließlich noch den 1/x-Wert für jede Station mit der Anzahl an Fahrten an der Station in 24 Stunden, um sie zu gewichten -> Wir erhalten: ich muss eine Strecke von x zurücklegen, um c Anschlüsse zu erhalten, repräsentiert durch den Quotienten c/x