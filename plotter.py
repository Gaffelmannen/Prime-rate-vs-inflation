import bokeh
import json
import csv
from datetime import date
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from scipy.interpolate import make_interp_spline

class Plotter():
    def __init__(self):
        self.INFLATION_FILENAME = "./files/inflation_swe.csv"

    def _datetime_to_float(self, d):
        epoch = datetime.fromtimestamp(0)
        total_seconds =  (d - epoch).total_seconds()
        return total_seconds

    def trendline(self, json_str):
        json_data = json.loads(json_str)
        datapoints = [point for point in json_data]
        data = pd.DataFrame(datapoints, columns=["date", "value"])
        
        min_date = mpl.dates.date2num(data.index.min())
        max_date = mpl.dates.date2num(data.index.max())
        x_new = np.linspace(min_date, max_date, 1000)

        print(data.values)

        a_BSpline = make_interp_spline(data.index.map(mpl.dates.date2num), data.values)
        y_new = a_BSpline(x_new)

        return x_new, y_new

    def plot_inflation(self):
        x = [] 
        y = [] 

        with open(self.INFLATION_FILENAME, 'r') as csvfile: 
            plots = csv.reader(csvfile, delimiter = ';') 
            for row in plots:
                x.append(row[0]) 
                y.append((row[1])) 
        plt.bar(x, y, color = 'g', width = 0.72, label = "Inflation percentage") 
        #ax = plt.axes()
        plt.xlabel('Year') 
        plt.ylabel('Rate of inflation') 
        plt.title('Age of empires II') 
        plt.legend() 
        plt.show() 

    def plot_prime_interest_rate(self, data):
        df = pd.read_json(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(df)

        plt.title("Sweden’s central bank - prime rate statistics")
        plt.xlabel("Date")
        plt.ylabel("Percentage")
        plt.legend(["Prime rate"])
        plt.show()

    def plot_both(self, json_str):
        # Interest rate data
        json_data = json.loads(json_str)
        datapoints = [point for point in json_data]
        data = pd.DataFrame(datapoints, columns=["date", "value"])

        # Inflation data
        original_values = {}
        inflation_data = []
        with open(self.INFLATION_FILENAME, 'r') as csvfile: 
            plots = csv.reader(csvfile, delimiter = ';') 
            for row in plots:
                if int(row[0]) >= 1994:
                    original_values[row[0]] = row[1]
        
        for val in data["date"]:
            datetime_object = datetime.strptime(val, '%Y-%m-%d')
            inflation_data.append(original_values[str(datetime_object.year)])

        fig, ax1 = plt.subplots(figsize=(8,5))

        x = np.asarray(data["date"], dtype='datetime64[s]')

        color = 'tab:blue'
        ax1.set_xlabel('Year')
        ax1.set_ylabel("Prime rate [%]", color=color)
        ax1.plot(x, data["value"], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx() 
        color = 'tab:red'
        ax2.set_ylabel('Inflation [%]', color=color)
        ax2.plot(x, np.asarray(inflation_data, float), color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
        fig.legend(["Prime rate", "Inflation"], loc='upper center', bbox_to_anchor=(0.5, 0.9))
        
        plt.title("Prime rate vs Inflation in Sweden")

        filename = "./output/rate_vs_inflation-{}.png".format(datetime.now().strftime("%Y-%m-%d"))
        plt.savefig(filename, bbox_inches="tight")
        print("File: {} created.".format(filename))
