from matplotlib import use
use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from Tkinter import Tk, Frame, Text, Button, PhotoImage, N, S, W, E, END, WORD, DISABLED
import tkFileDialog, tkSimpleDialog, tkMessageBox

from getdata import getdata

from miscfunctions import average, bracket, s2i

from types import MethodType

from translators import hformatter, cformatter

from nmrglue import bruker

from numpy import arange

from solvs import solvsdic

#set up the window
root = Tk()
root.title('SpecTr')
root.state('zoomed')
root.iconbitmap(default = 'Images\icon.ico')

#plot the figure
#add the navigation toolbar
def plot(d):

    #set up the figure
    global fig, ax
    fig = Figure(figsize = (7,6), dpi = 80)
    fig.subplots_adjust(bottom = 0.16)
    ax = fig.add_subplot(111)
    ax.plot(xp,spectrum, 'r-', peaksxp, peaksy, 'b|', markersize = 12)
    if nuc1 == '1H':
        ax.plot(xp, integration / 100, 'g-')

    #set the axis limits and labels
    ax.set_xlim(xmax, 0)
    ax.set_ylim(ymin)
    ax.set_xlabel(r'$\delta$' + ' / ppm')

    #plot the figure
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.show()
    canvas.get_tk_widget().grid(row = 1, columnspan = 4, sticky = N + S + W + E)

    #add the toolbar
    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.grid(row = 0, column = 2, sticky = W) 
    toolbar.update()

    #empty the text box
    text.delete(1.0, END)

#get which folder contains the fid file you want to open
def browse():

    #get the folder
    global folder
    folder = tkFileDialog.askdirectory()

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

            #activate the process button
            processbutton.configure(state = 'normal')

            #say the figure has loaded
            root.title('SpecTr - ' + folder)

    #warn if the folder contains no fid file
    except IOError:
        tkMessageBox.showwarning("Open file","No Bruker fid file in this folder\n%s" % folder)

#process the open data
def process():

    #make the initial multiplicities all singlets
    global peaksxp
    connect = arange(1, len(peaksxp) + 1)

    #ask what the connectivity of the peaks is if the spectrum is 1H
    if nuc1 == '1H':
        connect = tkSimpleDialog.askstring(title = 'SpecTr', prompt = 'Enter peak connectivity', initialvalue = '1 2 2 3 3 4 4 5 5 5 6 6 7 8 9 10')

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
        hdata = hformatter(peaksxp, peakints, solvs, connect)
        data = dict(data.items() + hdata.items())
    elif nuc1 == '13C':
        cdata = cformatter(peaksxp, connect)
        data = dict(data.items() + cdata.items())
    globals().update(data)

    #clear the text
    text.delete(1.0, END)

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
    canvas.show()
    canvas.get_tk_widget().grid(row = 1, columnspan = 4, sticky = W + E + N + S)

    #update the toolbar
    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.grid(row = 0, column = 2, sticky = W) 
    toolbar.update()

    #say the figure has loaded
    root.title('SpecTr - ' + folder)

#make the text box
text = Text(root, height = 1, wrap = WORD)
text.grid(row = 2, columnspan = 4, sticky = W + E + N + S)

#make the SpecTr toolbar
spectrtoolbar = Frame(root)
spectrtoolbar.grid(row = 0, column = 1, sticky = W, pady = 2, padx = 2)

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
root.rowconfigure(1, weight = 1)

#initialise the window
root.mainloop()

#label coupling

#tables of data

#resize text box?

#1 2 2 3 3 4 4 5 5 5 6 6 7 8 9 10

