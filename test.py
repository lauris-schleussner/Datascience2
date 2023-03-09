import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
import utm




BINS = 100
BLUR = 0

plt.rcParams['figure.dpi'] = 300

df = pd.read_csv("population_data/1.csv", sep = ",", names = ["lat","lon","weight"], skiprows = 1)

x = df["lat"].tolist()
y = df["lon"].tolist()
weight = df["weight"].tolist()

data = np.histogram2d(x, y, weights = weight, bins=BINS)[0]
data = gaussian_filter(data, sigma=BLUR)

plt.pcolormesh(data.T, cmap='inferno', shading='gouraud')

plt.savefig("population_us")