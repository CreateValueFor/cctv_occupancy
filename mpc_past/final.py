from pickle import FALSE
import time
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import mpcUtil as u
import matplotlib.dates as mdates
import pandas as pd
import MPC_ver2 as mpcv2


u.show_trends('sorted.csv')


# [dfTime, dfOccupancy, time, occupancy_list] = u.get_occupancy(
#     './sorted.csv')

path = "./final/"

(u.agfregate_csv(path))


print(type(dfTime))
mpcv2.mpc()
