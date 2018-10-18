import Tkinter as tk
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MyApp(tk.Toplevel):
    """ a trivial application that just plots noise to a graph """
    def __init__(self, master):
        self.master = master
        
        #setup the plot
        self.fPlot = MyPlotCanvas(master)
        self.fPlot.get_tk_widget().grid(row=0)

        tk.Button(master, text='Update', command=self.updatePlot, background='#00FF00').grid(row=1)
        
    def updatePlot(self):
        #get a bunch of random numbers and plot them
        t = np.arange(100)
        y = np.random.normal(size=100)
        self.fPlot.update(t, y)

class MyPlotCanvas(FigureCanvasTkAgg):
    def __init__(self, master=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvasTkAgg.__init__(self, figure = fig,  master = master)
        
        self.ax = fig.add_subplot('111')
        self.ax.hold(False)
        
        self.update([],[])

    def update(self,  x,  y):
        self.ax.fill(x, y, 'r')
        self.ax.set_xlabel('time')
        self.ax.set_ylabel('volts')
        self.draw()

root = tk.Tk()
app = MyApp(root)
root.mainloop()
