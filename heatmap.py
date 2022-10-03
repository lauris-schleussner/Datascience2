from copy import deepcopy
from utils import load_stops, chunks

import json
from tqdm import tqdm
from geopy.distance import geodesic as GD

import multiprocessing


def all_distances(coordinate, cur_haltestellen):
    cur_haltestellen.remove(coordinate)
    distances = []
    for other_coordinate in cur_haltestellen:
        if coordinate == other_coordinate:
            continue
        coordinate, other_coordinate = tuple(coordinate), tuple(other_coordinate)
        distances.append(
            GD(coordinate, other_coordinate).m
        )
    value = sum([1/x for x in distances if x != 0])
    return value

def haltestellendichte_working():
    coordinates = [[float(c) for c in elem[-2:]] for elem in load_stops()]
    values = []
    for elem in tqdm(coordinates):
        values.append([elem, all_distances(elem, coordinates)])
    with open("lvb_auswertung/dichte.json", "w+") as f:
        json.dump(values, f, indent=4)



    

if __name__ == "__main__":
    haltestellendichte_working()