import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
from testing import d
from process import average, bracket
import types

d = d()

root = tk.Tk()
root.title('SpecTr')
root.state("zoomed")

f = Figure(figsize=(7,6), dpi=80)
f.subplots_adjust(bottom=0.16)
a = f.add_subplot(111)
a.plot(d['xp'],d['didata'], 'r-', d['xp'], d['intdata']/100, 'g-', d['sigsp'], d['heights'], 'b|', markersize=12)
a.set_xlim(d['xmax'],0)
a.set_ylim(d['ymin'])
a.set_xlabel(r'$\delta$'+' / ppm')
##a.annotate('1', xy=(d['sigsp'][0],d['heights'][0]), verticalalignment='top')
##a.annotate('2', xy=(d['sigsp'][1],d['heights'][1]), verticalalignment='bottom', horizontalalignment='center', textcoords='offset points', xytext=(0, 10))
##a.annotate('3', xy=(average([d['sigsp'][5],d['sigsp'][6]]), max(d['heights'][5],d['heights'][6])), verticalalignment='bottom',
##           horizontalalignment='center', textcoords='offset points', xytext=(0, 10))
##a.annotate('', xy=(d['sigsp'][5],d['heights'][6]),  xycoords='data',xytext=(d['sigsp'][6],d['heights'][6]), textcoords='data',
##           arrowprops=dict(arrowstyle="-",connectionstyle="bar",shrinkA=5, shrinkB=5))
##a.annotate('4', xy=(average([d['sigsp'][3],d['sigsp'][4]]), max(d['heights'][3],d['heights'][4])), verticalalignment='bottom',
##           horizontalalignment='center', textcoords='offset points', xytext=(0, 10),arrowprops=dict(arrowstyle="-[",connectionstyle="bar",shrinkA=5, shrinkB=5))
a.bracket = types.MethodType(bracket, a)
a.bracket([d['sigsp'][5],d['sigsp'][6]],[d['heights'][5],d['heights'][6]], '4')
a.bracket = types.MethodType(bracket, a)
a.bracket([d['sigsp'][3],d['sigsp'][4]],[d['heights'][3],d['heights'][4]], '3')

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().grid(row=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.grid(row=0, sticky=tk.W) 
toolbar.update() 

button = tk.Button(root, text='Quit', command = root.destroy)
button.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)

text = tk.Text(root, height=1, wrap=tk.WORD)
text.insert(tk.END, d['textout'])
text.grid(row=2, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)

root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()

#label signals as a peak
#label coupling

#tables of data
#peak tops as lines
#resize text box?
