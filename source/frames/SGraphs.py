import tkinter as tk
import webbrowser
import numpy as np
import matplotlib
matplotlib.use("TKAgg")
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import csv
import tkcalendar
import datetime
from data import ScrumblesData
from data import ScrumblesObjects

from frames.SDynamics import *
from frames.SLists import *

from styling import styling as style
from tkinter import ttk

class SLine(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

    def generateGraph(self, x, y, labelsPosition=None, labels=None, xtitle=None, ytitle=None):
        self.graphInitialization()
        self.showGraph(x, y, labelsPosition, labels, xtitle, ytitle)

    def graphInitialization(self):
        self.f = plt.figure(figsize=(4, 4), dpi=100)
        #self.ax = self.figure.add_subplot(1,1,1)

    def showGraph(self, x, y, labelsPosition, labels, xtitle, ytitle):

        self.p = plt.plot(x,y)
        plt.xlabel(xtitle)
        plt.ylabel(ytitle)
        plt.xticks(labelsPosition, labels)

        #self.ax.set_xticklabels(labels)

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

class SBar(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self,controller)

    def generateGraph(self, titles, values, xtitle, ytitle, isOrange=False, tickValue=1, isGantt=False):
        self.graphInitialization()
        if isGantt is False:
            self.showGraph(titles, values, xtitle, ytitle, isOrange, tickValue)
    def graphInitialization(self):
        self.f = Figure(figsize=(4,5), dpi=100)
        self.ax = self.f.add_subplot(111)
    def showGraph(self, titles, values, xtitle, ytitle, isOrange=False, tickValue=1):
        ind = np.arange(len(values))
        width = .5
        bars = self.ax.bar(ind, values, width)
        self.ax.set_ylabel(ytitle)
        self.ax.set_xlabel(xtitle)
        loc = matplotlib.ticker.MultipleLocator(base=tickValue)  # this locator puts ticks at regular intervals
        self.ax.yaxis.set_major_locator(loc) #we don't want to count freq to determine y max
        self.ax.set_xticks(ind)
        self.ax.set_xticklabels(titles)
        #pretty colors
        children = self.ax.get_children()
        barlist = filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), children)
        itera = 0
        for bar in barlist:
            itera += 1
            if isOrange is True:
                bar.set_color(style.scrumbles_orange)
                isOrange = False
            else:
                bar.set_color(style.scrumbles_blue)
                isOrange = True
        barlist = filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), children)
        for i in range(0, itera):
            item = next(barlist)
            if i == itera-1:
                item.set_color('w')
        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class SGantt(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self,controller)

    def generateGraph(self, bottoms, tops, xlabels, yticks, ylabels, xtitle, ytitle):
        self.graphInitialization()
        self.showGraph(bottoms, tops, xlabels, yticks, ylabels, xtitle, ytitle)

    def graphInitialization(self):
        self.f = Figure(figsize=(4,5), dpi=100)
        self.ax = self.f.add_subplot(111)
    def showGraph(self, bottoms, tops, xlabels, yticks, ylabels, xtitle, ytitle, isOrange=False):
        ind = np.arange(len(xlabels))
        width = .50
        bars = self.ax.barh(ind, tops, width, bottoms)
        self.ax.set_xlabel(ytitle)
        self.ax.set_ylabel(xtitle)

        self.ax.set_yticks(ind)
        self.ax.set_yticklabels(xlabels)

        self.ax.set_xticks(yticks)
        self.ax.set_xticklabels(ylabels)

        # pretty colors
        children = self.ax.get_children()
        barlist = filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), children)
        itera = 0
        for bar in barlist:
            itera += 1
            if isOrange is True:
                bar.set_color(style.scrumbles_orange)
                isOrange = False
            else:
                bar.set_color(style.scrumbles_blue)
                isOrange = True
        barlist = filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), children)
        for i in range(0, itera):
            item = next(barlist)
            if i == itera - 1:
                item.set_color('w')
        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class SHistogram(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

    def generateGraph(self, x, y, xAxis, yAxis, xticks=1):
        self.graphInitialization()
        self.showGraph(x, y, xAxis, yAxis, xticks)

    def graphInitialization(self):
        self.f = Figure(figsize=(4,5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def showGraph(self, bins, y, xAxis, yAxis, xticks=1):
        self.p = self.f.gca()
        oldBins = bins
        N, bins, patches = self.p.hist(y, bins=bins)
        fracs = N/N.max()
        norm = colors.Normalize(fracs.min(), fracs.max())
        for thisfrac, thispatch in zip(fracs,patches):
            color = plt.cm.viridis(norm(thisfrac))
            thispatch.set_facecolor(color)


        self.p.set_xlabel(xAxis, fontsize=15)
        self.p.set_ylabel(yAxis, fontsize=15)
        self.p.set_xticks(range(0, oldBins, int(xticks)))

        loc = matplotlib.ticker.MultipleLocator(base=1)  # this locator puts ticks at regular intervals
        self.p.yaxis.set_major_locator(loc) #we don't want to count freq to determine y max


        self.canvas.draw()

class SPie(tk.Frame):
    def __init__(self,controller):
        tk.Frame.__init__(self, controller)

    def generateGraph(self, labels, values, title):
        self.graphInitialization(title)
        self.showGraph(labels, values)

    def graphInitialization(self, title):
        self.f = plt.figure(figsize=(4,5), dpi=100)
        self.f.suptitle(title)


    def showGraph(self, labels, values):
        explode = list()
        for label in labels:
            explode.append(0.1)

        self.p = plt.pie(values, labels=labels, explode=explode, autopct='%1.1f%%')
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()
