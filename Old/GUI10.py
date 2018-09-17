from matplotlib import use
use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from Tkinter import Tk, Frame, Text, Button, PhotoImage, N, S, W, E, END, WORD, DISABLED
import tkFileDialog
import tkSimpleDialog
import tkMessageBox

from testing import getdata

from process import average, bracket

from types import MethodType

from translators import hformatter, cformatter

from nmrglue import bruker

from numpy import arange

root = Tk()
root.title('SpecTr')
root.state("zoomed")
root.iconbitmap(default='icon.ico')

##def removeanns():
##    global a
##    del a.texts[:]

def plot(d):
    global f, a
    f = Figure(figsize=(7,6), dpi=80)
    f.subplots_adjust(bottom=0.16)
    a = f.add_subplot(111)
    a.plot(xp,didata, 'r-', sigsp, heights, 'b|', markersize=12)
    if nuc1 == '1H':
        a.plot(xp, intdata/100, 'g-')
    a.set_xlim(xmax,0)
    a.set_ylim(ymin)
    a.set_xlabel(r'$\delta$'+' / ppm')

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().grid(row=1, columnspan=4, sticky=N+S+W+E)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.grid(row=0, column=2, sticky=W) 
    toolbar.update()
    text.delete(1.0, END)

def browse():
    global folder
    folder = tkFileDialog.askdirectory()
    try:
        if len(folder) > 0:
            dic, data = bruker.read(folder)
            root.title('SpecTr - '+folder+' - Loading...')
            global d
            d = getdata(folder)
            globals().update(d)
            plot(d)
            processbutton.configure(state='normal')
            root.title('SpecTr - '+folder)
    except IOError:
        tkMessageBox.showwarning("Open file","No Bruker fid file in this folder\n%s" % folder)

def s2i(slist):
    z=0
    nlist=[]
    while z<len(slist):
        nlist.append(int(slist[z]))
        z=z+1
    return nlist
    

def process():
    global sigsp
    connect=arange(1,len(sigsp)+1)
    #print connect
    #print len(connect)
    if nuc1 == '1H':
        connect = tkSimpleDialog.askstring(title='SpecTr', prompt='Enter peak connectivity', initialvalue='1 2 2 3 3 4 4 5 5 5 6 6 7 8 9 10').split(' ')
    global folder
    root.title('SpecTr - '+folder+' - Loading...')
    connect = s2i(connect)
    global d
    if nuc1 == '1H':
        h = hformatter(sigsp, sigints, solvs, connect)
    elif nuc1 == '13C':
        h = cformatter(sigsp, connect)
    d = dict(d.items() + h.items())
    globals().update(d)
    text.delete(1.0, END)
    text.insert(END, textout)
    global a
    del a.texts[:]

    b=1
    e=1
    #print len(sigsp)
    while b<=len(sigsp):
        print 'b', b
        c=0
        multipletx=[]
        multiplety=[]
        while c<len(solvlessconnect):
            if solvlessconnect[c] == b:
                #print 'match'
                multipletx.append(sigs[c])
                multiplety.append(heights[c])
            c=c+1
        
        if len(multipletx)>0:
            #print 'e', e
            a.bracket = MethodType(bracket, a)
            a.bracket(multipletx, multiplety, e)
            e=e+1
        b=b+1

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().grid(row=1, columnspan=4, sticky=W+E+N+S)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.grid(row=0, column=2, sticky=W) 
    toolbar.update()
    
    root.title('SpecTr - '+folder)

text = Text(root, height=1, wrap=WORD)
text.grid(row=2, columnspan=4, sticky=W+E+N+S)

spectrtoolbar = Frame(root)
spectrtoolbar.grid(row=0, column=1, sticky=W, pady=2, padx=2)

openimage = PhotoImage(file='open.gif')
openbutton = Button(spectrtoolbar, text='Open', image=openimage, command = browse)
openbutton.grid(row=0, column=0, sticky=W)

processimage = PhotoImage(file='process.gif')
processbutton = Button(spectrtoolbar, text='Process', image=processimage, command = process, state=DISABLED)
processbutton.grid(row=0, column=1, sticky=W)

root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=0)
root.columnconfigure(3, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()

#label signals as a peak
#label coupling

#tables of data

#resize text box?

#from testing import variables?
#1 2 2 3 3 4 4 5 5 5 6 6 7 8 9 10

#tell off for no fid
