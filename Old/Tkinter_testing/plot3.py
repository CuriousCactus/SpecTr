import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
from testing5 import d

root = tk.Tk()

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)

a.plot(d()['xp'],d()['didata'])

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().grid(row=1, columnspan=2)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.grid(row=0, sticky=tk.W) 
toolbar.update() 

button = tk.Button(root, text='Quit', command = root.destroy)
button.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)

root.mainloop()
