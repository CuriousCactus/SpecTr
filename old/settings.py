from Tkinter import Tk, Frame, Label, Entry, Text, Button, PhotoImage, Checkbutton, BooleanVar, StringVar, DoubleVar, N, S, W, E, END, WORD, DISABLED

from getdata import getdata

datadic = getdata('LMO_3BrAP_1/20')
globals().update(datadic['options'])

root = Tk()
root.title('SpecTr')
root.iconbitmap(default = 'Images/icon.ico')

def update():
    hthres = hthresvar.get()
    datadic['options']['hthres'] = hthres
    globals().update(datadic)
    print getdata('LMO_3BrAP_1/20', options=options)['options']
    
settingsframe = Frame(root, background='blue')
settingsframe.grid(row = 1, column = 1)
globals().update(datadic['options'])


hthreslabel = Label(settingsframe, text = 'Peak pick threshold')
hthreslabel.grid(row = 1, column = 1, columnspan = 1, sticky = W + E + N + S)

#make the text box
hthresvar = DoubleVar()
hthresentry = Entry(settingsframe, textvariable = hthresvar)
hthresvar.set(hthres)
hthresentry.grid(row = 1, column = 2, columnspan = 1, sticky = W + E + N + S)

updatebutton = Button(settingsframe, text = 'Update', command = update)
updatebutton.grid(row = 2, column = 1, columnspan = 2, sticky = W + E + N + S)

#initialise the window
root.mainloop()

