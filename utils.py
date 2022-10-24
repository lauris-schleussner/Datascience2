import json
import csv
# load all stops from stops.txt
def load_stops():
    with open('data/GER_Saxony_Leipzig/stops.txt', newline='', encoding = "utf-8") as f:
        reader = csv.reader(f)
        stops_file = list(reader)
        stops_file.pop(0)
        
    return stops_file

# load all stop times from stop_times
def load_stop_times():
    stop_times = []
    with open("gtfsmdvlvb/stop_times.txt") as f:
        txt_data = f.read()
    for elem in txt_data.split("\n")[1:]:
        stop_times.append(elem.split(","))
    stop_times.remove([''])
    return stop_times


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load_coordinates():
    with open("lvb_auswertung/coordinates.json", "r") as f:
        return json.load(f)

def load_all_neighbours():
    with open("lvb_auswertung/neighbours.json", "r") as f:
        return json.load(f)


