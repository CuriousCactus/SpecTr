import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
from testing import getdata
from process import average, bracket
import types
import numpy as np
import tkFileDialog
import tkSimpleDialog
from translators import hformatter

root = tk.Tk()
root.title('SpecTr')
root.state("zoomed")

quitbutton = tk.Button(root, text='Quit', command = root.destroy)
quitbutton.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)

### defining options for opening a directory
##dir_opt = options = {}
##options['initialdir'] = 'C:\\'
##options['mustexist'] = False
##options['parent'] = root
##options['title'] = 'This is a title'

##e1 = tk.Text(root)
##e1.grid(row=0, column=3, sticky=tk.E+tk.N+tk.S)
##
def plot(d):

    f = Figure(figsize=(7,6), dpi=80)
    f.subplots_adjust(bottom=0.16)
    a = f.add_subplot(111)
    a.plot(d['xp'],d['didata'], 'r-', d['xp'], d['intdata']/100, 'g-', d['sigsp'], d['heights'], 'b|', markersize=12)
    a.set_xlim(d['xmax'],0)
    a.set_ylim(d['ymin'])
    a.set_xlabel(r'$\delta$'+' / ppm')

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().grid(row=1, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.grid(row=0, sticky=tk.W) 
    toolbar.update()



def browser():
    folder = tkFileDialog.askdirectory()
    if len(folder) > 0:
        #e1.insert(tk.END, folder)
        root.title('SpecTr - '+folder)
        global d
        d = getdata(folder)
        #print d
        plot(d)

def process():
    connect = tkSimpleDialog.askstring('SpecTr', 'Enter peak connectivity').split(', ')
    print d
    hformatter(d['sigsp'], d['sigints'], d['solvs'], list(connect))
    text = tk.Text(root, height=1, wrap=tk.WORD)
    text.insert(tk.END, d['textout'])
    text.grid(row=2, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)

    b=0
    e=0
    while b<len(d['sigsp']):
        c=0
        multipletx=[]
        multiplety=[]
        while c<len(d['solvlessthing']):
            if d['solvlessthing'][c] == b:
                multipletx.append(d['sigs'][c])
                multiplety.append(d['heights'][c])
            c=c+1
        if e>0:
            a.bracket = types.MethodType(bracket, a)
            a.bracket(multipletx, multiplety, e)
        
        if len(multipletx)>0:
            e=e+1
        b=b+1

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().grid(row=1, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.grid(row=0, sticky=tk.W) 
    toolbar.update()

openbutton = tk.Button(root, text='Open', command = browser)
openbutton.grid(row=0, column=2, sticky=tk.E+tk.N+tk.S)

processbutton = tk.Button(root, text='Process', command = process)
processbutton.grid(row=0, column=3, sticky=tk.E+tk.N+tk.S)

root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()

#label signals as a peak
#label coupling

#tables of data

#resize text box?

#from testing import variables?
