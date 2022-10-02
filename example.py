"""
ausgewertete Daten:
- stops.txt:
    - Liste an Stops mit ID, Name, Lat, Lon, ...
- stop_times.txt:
    - liste an "stop_times" mit Trip ID, Ankunftszeit, Abfahrtszeit, Stop ID, ... (letzte 3 Datenpunkte aktuell nicht relevant)
    - stop_ids in zwei "stop_time" sind benachbart, wenn die stop_times hintereinander vorkommen und dieselbe trip_id haben

"""


import json
from tqdm import tqdm
import time


# load all stops from stops.txt
def load_stops():
    stops = []
    with open("gtfsmdvlvb/stops.txt") as f:
        txt_data = f.read()
    for elem in txt_data.split("\n")[1:]:
        stops.append(elem.split(","))
    stops.remove([''])
    return stops

# load all stop times from stop_times
def load_stop_times():
    stop_times = []
    with open("gtfsmdvlvb/stop_times.txt") as f:
        txt_data = f.read()
    for elem in txt_data.split("\n")[1:]:
        stop_times.append(elem.split(","))
    stop_times.remove([''])
    return stop_times

# find all occurences of a stop id in stop_times-data
def find_occ_numbers(stop_id, **kwargs):
    if "stop_times" in kwargs:
        stop_times = kwargs["stop_times"]
    else:
        stop_times = load_stop_times()
    occ_ind = []
    for ind, elem in enumerate(stop_times):
        if elem[3] == stop_id:
            occ_ind.append(ind)
    return occ_ind

# find all occurencies for all stop ids in stop_times-data
def all_occ_numbers():
    stop_times = load_stop_times()
    line_numbers = {}
    stop_ids = [i[0] for i in load_stops()]
    c = time.perf_counter()
    for elem in tqdm(stop_ids):
        line_numbers[elem] = find_occ_numbers(elem, stop_times=stop_times)
    with open("lvb_auswertung/occ_numbers.json", "w+") as f:
        json.dump(line_numbers, f, indent=4)
# load the data from the all_occ_numbers function
def load_all_occ_numbers():
    with open("lvb_auswertung/occ_numbers.json") as f:
        data = json.load(f)
    return data
# BEACHTEN: Die Indizes sind die Indizes aus der load_stops()-Funktion, nicht die Zeilennummern (die erste Zeile wird in der Funktion entfernt UND es handelt sich um ein Python Array, das mit dem Index 0 startet)
# -> Wenn die Indizes verwendet werden: entweder in Zeilennummern (-1 für Python Array mit head-Zeile, -2 für tatsächliche Zeilennummbern) umrechnen oder Daten aus load_stops() verwenden


# Findet zu allen Haltestellen (nach ID) alle Nachbarhaltestellen (mit direkter Verbindung ohne Stopp dazwischen) nach ID und die jeweils kürzeste Zeit, die für die Verbindung benötigt wird in Sekunden
# Frage zur Diskussion: Sollten wir in die Zeiten auch die anschließenden Wartezeiten mit reinnehmen? -> meine Meinung: nein, wir müssen sowieso vereinfachen, dass man beliebig umsteigen kann, es geht nur um eine grobe Erfassung
# Frage zur Diskussion: Sollte eine Minimalzeit gleich 0 erlaubt sein? -> kommt ab und zu vor (zum Beispiel zwischen Haltestellen 0000145 und 0013282 in trip 32098, aber in fast allen anderen Trips nicht) -> meine Meinung: nein, daher vor Ausführen der Minimum-Funktion Nullen entfernen und nur 0 zurückgeben, wenn immer 0 Zeit benötigt wird
def all_neighbours():
    def time_sec(time):
        time = time.replace('"', '')
        return 3600*int(time[0:2])+60*int(time[3:5])+int(time[6:8])
    # Findet für einen Stop alle Nachbarhaltestellen anhand der Indizes aus der load_stop_times()-Funktion, in denen der Stopp vorkommt
    def find_neighbours(stop_times, occ_numbers):
        neighbours = []
        neighbour_times = []
        for occ_number in occ_numbers:
            point = stop_times[occ_number]
            point_arr = time_sec(stop_times[occ_number][1])
            point_dep = time_sec(stop_times[occ_number][2])
            if occ_number != 0:
                before = stop_times[occ_number-1]
                diff = point_arr-time_sec(stop_times[occ_number-1][2])
                if before[0] == point[0]:
                    neighbour_times.append((before[3], diff))
                    neighbours.append(before[3])
            
            if occ_number != len(stop_times)-1:
                after = stop_times[occ_number+1]
                diff = time_sec(stop_times[occ_number+1][1])-point_dep
                if after[0] == point[0]:
                    neighbour_times.append((after[3], diff))
                    neighbours.append(after[3])
        neighbours = list(set(neighbours))
        def min_time(neighbour):
            min_list = [elem[1] for elem in neighbour_times if elem[0] == neighbour]
            min_list = [elem for elem in min_list if elem != 0]
            if len(min_list) == 0:
                return 0
            return min(min_list)
        return [(
                    neighbour, min_time(neighbour)
                ) for neighbour in neighbours]
        #return list(set(neighbours))
    print("loading data...")
    stop_ids = [i[0] for i in load_stops()]
    stop_times = load_stop_times()
    occ_numbers = load_all_occ_numbers()
    all_neighbours = {}
    print("finding neighbours...")
    #for elem in stop_ids[:1]:
    for elem in tqdm(stop_ids):
        all_neighbours[elem] = find_neighbours(stop_times, occ_numbers[elem])
    with open("lvb_auswertung/neighbours.json", "w+") as f:
        json.dump(all_neighbours, f, indent=4)

def load_all_neighbours():
    with open("lvb_auswertung/neighbours.json") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    #all_occ_numbers()
    all_neighbours()
