import pandas as pd
import holoviews as hv

import hvplot.pandas
import datetime as dt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import hvplot
from amortization.amount import calculate_amortization_amount
from amortization.period import calculate_amortization_period
from amortization.period import calculate_amortization_period
from amortization.schedule import amortization_schedule
from tabulate import tabulate
import csv
import sys
import fire
import matplotlib.pyplot as plt
import numpy as np

amount = calculate_amortization_amount(100000, 0.07, 300)

period = calculate_amortization_period(100000, 0.07, 706.78)


#df = pd.DataFrame(amortization_schedule())
#df = 'test'

