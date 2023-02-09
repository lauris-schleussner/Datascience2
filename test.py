import pandas as pd


data = [[1,"a", "x"],[1,"b", "y"],[1,"c", "z"],[2,"a", "z"],[2,"b", "z"],[3,"a", "z"]]
df = pd.DataFrame(data, columns=["trip", "neighbour", "testneighbour"])

df = df.groupby("trip").agg({"neighbour": lambda x: ' '.join(x), 'testneighbour': lambda x: ' '.join(x)})

#grouped_df = df.groupby("trip_id").agg({'stop_lat': lambda x: ' '.join(x), 'stop_lon': lambda x: ' '.join(x)})

print(df.head())