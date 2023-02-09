import warnings
warnings.simplefilter(action='ignore')

from utils import load_stop_times_df
from tqdm import tqdm
import pandas as pd
from utils import load_stops
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import os
from multiprocessing import Pool, cpu_count



def main():
     pass

"""
    # get all city names in the dataset
    all_city_paths = glob.glob("data/*")
    all_city_paths.pop(0)

    all_city_paths = all_city_paths[0:10]


    # every thread peaks at around 4GB Memory, even with GC
    pool = Pool(processes=(5))
    pool.map(plot, all_city_paths)
    pool.close()   

    # for each city look up square coordinates
""" 

def plot(city_name):
        #print(city_name + "\n")

        # load stops
        try:
            df = load_stop_times_df(os.path.basename(city_name))
        except: 
             return

        # check if enough points
        if df.shape[0] <= 100:
             return


        # shift some rows around so comparing a row with the one after it becomes easier
        df["shift_up"] = df["trip_id"].shift(-1)
        df["shifted_up_stop_id"] = df["stop_id"].shift(-1)

        # set the column "neighbour" to NaN incase the line after has a new trip_id eq. is not a neighbour of the 
        df.loc[df["trip_id"] == df["shift_up"], "neighbour"] = df["shifted_up_stop_id"]

        # load coordinates as df (stop_id, lat, lon)
        df_coordinates = load_stops()
        df_coordinates.head()

        # join both together
        joined_df = pd.DataFrame()
        joined_df = df.join(df_coordinates.set_index('stop_id'), on='stop_id')

        # select only relevant cols
        only_coordinates_df = joined_df[["trip_id", "stop_lat", "stop_lon"]]

        # convert datatypes to str, else join() in the lambda wont work
        only_coordinates_df[["stop_lat", "stop_lon"]] = only_coordinates_df[["stop_lat", "stop_lon"]].astype("str")

        # group df by trip_id and list all coordinates after
        grouped_df = only_coordinates_df.groupby("trip_id").agg({'stop_lat': lambda x: ' '.join(x), 'stop_lon': lambda x: ' '.join(x)})

        # convert to 2d list [all_lat, all_lon]
        as_list = grouped_df.values.T.tolist()

        # plotting

        fig = plt.figure(dpi=3000)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_axis_off()

        print(city_name + "\n" + str(len(as_list[0])))     


        for x, y in zip(as_list[0], as_list[1]):
            # x and y are long string with one for each trip_id. They are not yet split
            
            # seperate long x bzw y string into list
            x_list = x.split(" ")
            y_list = y.split(" ")

            x_list = list(map(float, x_list)) # convert to float
            y_list = list(map(float, y_list)) # convert to float

            ax.plot(x_list, y_list, linestyle = "-", c= "#ff9400", linewidth = "0.2")



        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax.view_init(elev=90, azim=45)

        plt.savefig("linegraphs/" + os.path.basename(city_name) + ".png")

        plt.close()
        import gc
        del df, df_coordinates, joined_df, as_list, x_list, y_list
        gc.collect()


        print("done with", city_name + "\n")

        return






if __name__ == "__main__":
    plot("GER_Saxony_Leipzig")