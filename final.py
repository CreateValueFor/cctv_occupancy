from pickle import FALSE
import time
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import mpcUtil as u
import matplotlib.dates as mdates
import pandas as pd

# [dfTime, dfOccupancy, time, occupancy_list] = u.get_occupancy(
#     './logs/20230420.csv')
path = "./final/"

# (u.agfregate_csv(path))

u.show_trends('sorted.csv')
