import tkinter as tk
import webbrowser
import matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import csv
import tkcalendar
import datetime
import ScrumblesData
import ScrumblesObjects

from SDynamics import *
from SLists import *

from styling import styling as style
from tkinter import ttk

class SLineGraph(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

        self.x = [1,2,3,4,5,6,7,8,9,10]
        self.y = [1,4,2,5,1,4,2,5,1,4]
        self.label = None

        self.figure = Figure(figsize=(4, 4), dpi=100)
        self.graph = self.figure.add_subplot(1,1,1)


    def setTitle(self, title):
        self.label = tk.Label(self, text=title)

    def setAxes(self, xAxis, yAxis):
        self.graph.set_xlabel(xAxis)
        self.graph.set_ylabel(yAxis)
        self.figure.subplots_adjust(left=.15)
        self.figure.subplots_adjust(bottom=.15)

    def importDataFromCSV(self, fileName, delimeter):
        with open(fileName, 'r') as file:
            plots = csv.reader(file, delimeter)
            for row in plots:
                self.x.append(int(row[0]))
                self.y.append(int(row[1]))

    def displayGraph(self):
        self.graph.plot(self.x, self.y)
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.draw()
        if self.label is not None:
            self.label.pack(side=tk.TOP, fill=tk.X)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=1, pady=1)

    def changeBackgroundColor(self, color):
        self.graph.set_facecolor(facecolor=color)


class SHistogram(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

    def generateGraph(self, x, y, xAxis, yAxis):
        self.graphInitilazition()
        self.showGraph(x, y, xAxis, yAxis)

    def graphInitilazition(self):
        self.f = Figure(figsize=(5,5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=False)


    def showGraph(self, bins, y, xAxis, yAxis):
        self.p = self.f.gca()
        self.p.hist(y, bins)
        self.p.set_xlabel(xAxis, fontsize=15)
        self.p.set_ylabel(yAxis, fontsize=15)
        self.p.set_xticks(range(0,bins))

        loc = matplotlib.ticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
        self.p.yaxis.set_major_locator(loc) #we don't want to count freq to determine y max


        self.canvas.draw()