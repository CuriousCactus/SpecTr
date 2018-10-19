from matplotlib import use
use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter import Tk, Frame, Text, Button, Checkbutton, PhotoImage, Label, Entry, DoubleVar, BooleanVar, N, S, W, E, END, WORD, DISABLED, BOTH, filedialog, simpledialog, messagebox

from getdata import getdata

from miscfunctions import average, bracket, s2i

from types import MethodType

from translators import hformatter, cformatter

from nmrglue import bruker

from numpy import arange, ravel, array, where

from solvs import solvsdic

#set up the window
root = Tk()
root.title('SpecTr')
root.state('zoomed')
root.iconbitmap(default = 'Images\icon.ico')

def getppm(event):
    hthres = event.ydata
    print(hthres)
    hthresvar.set(hthres)

def getppminclick():
    print(hthresbuttonvar.get())
    if hthresbuttonvar.get() == True:
        cid = fig.canvas.mpl_connect('button_press_event', getppm)
        return cid
    elif hthresbuttonvar.get() == False:
        fig.canvas.mpl_disconnect(4)
        update()

def onpick(event):
    thisline = event.artist
    xdata2 = thisline.get_xdata()
    ydata2 = thisline.get_ydata()
    ind = event.ind
    print('onpick points:', zip(xdata2[ind], ydata2[ind]))
    print(xdata2[ind])
    global mult
    mult.append(xdata2[ind])

def addmult():
    global mult
    print(mult)
    mults.append(mult)
    mult = []
    print(mults)

#plot the figure
#add the navigation toolbar
def plot(data):

    #set up the figure
    global fig, ax
    fig = Figure(figsize = (7,6), dpi = 80)
    fig.subplots_adjust(bottom = 0.16)
    ax = fig.add_subplot(111)
    ax.plot(xp,spectrum, 'r-')
    ax.plot(peaksxp, peaksy, 'b|', markersize = 12, picker=5)
    if nuc1 == '1H':
        ax.plot(xp, integration / 100, 'g-')

    #set the axis limits and labels
    ax.set_xlim(xmax, 0)
    ax.set_ylim(ymin)
    ax.autoscale()
    ax.set_xlabel(r'$\delta$' + ' / ppm')

    #plot the figure
    canvas = FigureCanvasTkAgg(fig, root)
    canvas._tkcanvas.config(borderwidth=0, highlightthickness=0)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 1, columnspan = 4, sticky = N + S + W + E)

    #add the toolbar
    toolbarframe = Frame(root)
    toolbarframe.grid(row = 0, column = 2, sticky = W)
    toolbar = NavigationToolbar2Tk(canvas, toolbarframe)
    toolbar.grid(row = 0, column = 2, sticky = W) 
    toolbar.update()

def update():
    global hthresvar, data
    hthres = hthresvar.get()
    data['options']['hthres'] = hthres
    data = getdata(folder)
    globals().update(data)
    plot(data)

    text.pack_forget()

#get which folder contains the fid file you want to open
def browse():

    #get the folder
    global folder
    folder = filedialog.askdirectory(initialdir = 'Examples/1/pdata/1')

    try:
        global text
        text.grid_remove()
    except:
        pass

    #plot the data if the folder contains a fid file
    try:
        if len(folder) > 0:
            dic, fiddata = bruker.read(folder) #raises IOError if there is no fid file

            #say the figure is loading
            root.title('SpecTr - ' + folder + ' - Loading...')
            
            #plot the data in the folder
            global data
            data = getdata(folder)
            globals().update(data)
            plot(data)

            settingsframe = Frame(root)
            settingsframe.grid(row = 1, column = 4, sticky = W + E + N + S)
            globals().update(data['options'])

            global textframe
            textframe = Frame(root, height = 36)
            textframe.grid(row = 2, columnspan = 4, sticky = W + E + N + S)

            hthreslabel = Label(settingsframe, text = 'Peak pick threshold')
            hthreslabel.grid(row = 1, column = 1, columnspan = 1, sticky = W + E + N + S)

            #make the text box
            global hthresvar, hthresbuttonvar
            hthresvar = DoubleVar()
            hthresentry = Entry(settingsframe, textvariable = hthresvar)
            hthresvar.set(hthres)
            hthresentry.grid(row = 1, column = 2, columnspan = 1, sticky = W + E + N + S)

            hthresbuttonvar = BooleanVar()
            hthresbutton = Checkbutton(settingsframe, text = 'Set', command = getppminclick, indicatoron = False, variable = hthresbuttonvar)
            hthresbutton.grid(row = 1, column = 3, columnspan = 1, sticky = W + E + N + S)

            updatebutton = Button(settingsframe, text = 'Update', command = update)
            updatebutton.grid(row = 2, column = 1, columnspan = 3, sticky = W + E + S)

            global mult, mults
            mult = []
            mults = []
            pickbutton = Button(settingsframe, text = 'Pick', command = addmult)
            pickbutton.grid(row = 3, column = 1, columnspan = 3, sticky = W + E + S)            

            #activate the process button
            processbutton.configure(state = 'normal')

            fig.canvas.mpl_connect('pick_event', onpick)

            #say the figure has loaded
            root.title('SpecTr - ' + folder)

    #warn if the folder contains no fid file
    except IOError:
        messagebox.showwarning("Open file","No Bruker fid file in this folder\n%s" % folder)

#process the open data
def process():

    #make the initial multiplicities all singlets
    global peaksxp
    connect = arange(1, len(peaksxp) + 1)

    #ask what the connectivity of the peaks is if the spectrum is 1H
    if nuc1 == '1H':
        connect = simpledialog.askstring(title = 'SpecTr', prompt = 'Enter peak connectivity', initialvalue = '1 2 2 3 3 4 4 5 5 5 6 6 7 8 9 10')

        #get the connectivity list
        if connect != None:
            connect = connect.split(' ')
            connect = s2i(connect)

        #do nothing if cancel is clicked
        elif connect == None:
            return
    
    #say the figure is loading
    global folder
    root.title('SpecTr - ' + folder + ' - Loading...')

    #get the text
    global data
    if nuc1 == '1H':
        solvs = solvsdic['DMSO']['H']
        hdata = hformatter(peaksxp, peakints, solvs, connect, groupedsigs = mults)
        data = dict(data.items() + hdata.items())
    elif nuc1 == '13C':
        cdata = cformatter(peaksxp, connect)
        data = dict(data.items() + cdata.items())
    globals().update(data)

    #make the text box
    global text
    text = Text(textframe, height = 2, wrap = WORD)
    text.pack(fill = BOTH)

    #put the text in the textbox
    text.insert(END, textout)

    #clear the peak labels
    del ax.texts[:]

    #label the peaks
    b = 1
    e = 1
    while b <= len(peaksxp):

        #get the points in the multiplet
        c = 0
        multipletx = []
        multiplety = []
        while c<len(solvlessconnect):
            if solvlessconnect[c] == b:
                multipletx.append(sigs[c])
                multiplety.append(peaksy[c])
            c = c + 1

        #label the multiplet
        if len(multipletx) > 0:
            ax.bracket = MethodType(bracket, ax)
            ax.bracket(multipletx, multiplety, e)
            e = e + 1
        b = b + 1

    #update the figure
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas._tkcanvas.config(borderwidth=0, highlightthickness=0)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 1, columnspan = 4, sticky = W + E + N + S)

    #update the toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.grid(row = 0, column = 2, sticky = W) 
    toolbar.update()

    #say the figure has loaded
    root.title('SpecTr - ' + folder)

#make the SpecTr toolbar
spectrtoolbar = Frame(root)
spectrtoolbar.grid(row = 0, column = 0, sticky = W, pady = 2, padx = 2)

#make the open button
openimage = PhotoImage(file = 'Images/open.gif')
openbutton = Button(spectrtoolbar, text = 'Open', image = openimage, command = browse)
openbutton.grid(row = 0, column = 0, sticky = W)

#make the process button
processimage = PhotoImage(file = 'Images/process.gif')
processbutton = Button(spectrtoolbar, text = 'Process', image = processimage, command = process, state = DISABLED)
processbutton.grid(row = 0, column = 1, sticky = W)



#configure the geometry
root.columnconfigure(0, weight = 0)
root.columnconfigure(1, weight = 0)
root.columnconfigure(2, weight = 0)
root.columnconfigure(3, weight = 1)
root.columnconfigure(4, weight = 0)
root.rowconfigure(1, weight = 1)

#initialise the window
root.mainloop()



#1 2 2 3 3 4 4 5 5 5 6 6 7 8 9 10

#label coupling
#tables of data
#resize text box?
#update and process
#draw line for peak pick threshold
#multiplicities with mouse
#don't replot when changing ppmin
#deal with blank connect
#connect doesn't always match annotation
#keep original coords after re-picking peaks
#table of peaks to exclude
#auto multiplets
#bigger point on click
#save formatting

