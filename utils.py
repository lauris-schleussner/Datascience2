import json
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


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load_coordinates():
    with open("lvb_auswertung/coordinates.json", "r") as f:
        return json.load(f)

def load_all_neighbours():
    with open("lvb_auswertung/neighbours.json", "r") as f:
        return json.load(f)


