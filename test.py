with open("gtfsmdvlvb/stop_times.txt", "r") as f:
    lines = f.read().split("\n")

for ind, line in enumerate(lines):
    if ",0011652," in line:
        if ",0013000," in lines[ind-1] or ",0013000," in lines[ind+1]:
            print(line.split(",")[0])