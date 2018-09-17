from Tkinter import Tk, Frame, Label, Entry, Text, Button, PhotoImage, Checkbutton, BooleanVar, StringVar, DoubleVar, N, S, W, E, END, WORD, DISABLED

from getdata import getdata

datadic = getdata('LMO_3BrAP_1/20')
globals().update(datadic['options'])

root = Tk()
root.title('SpecTr')
root.iconbitmap(default = 'Images/icon.ico')

##def update():
##    hthres = hthresvar.get()
##    datadic['options']['hthres'] = hthres
##    globals().update(datadic)
##    print getdata('LMO_3BrAP_1/20', options=options)['options']
##    
def click():
    if var.get() == True:
        print 'hi'

var = BooleanVar()
check = Checkbutton(root, variable = var, command = click, text = 'Peak pick threshold')
check.grid(row = 1, column = 1, columnspan = 1, sticky = W + E + N + S)

##hthreslabel = Label(root, text = 'Peak pick threshold')
##hthreslabel.grid(row = 1, column = 1, columnspan = 1, sticky = W + E + N + S)
##
###make the text box
##hthresvar = DoubleVar()
##hthresentry = Entry(root, textvariable = hthresvar)
##hthresvar.set(hthres)
##hthresentry.grid(row = 1, column = 2, columnspan = 1, sticky = W + E + N + S)
##
##updatebutton = Button(root, text = 'Update', command = update)
##updatebutton.grid(row = 2, column = 1, columnspan = 2, sticky = W + E + N + S)

#initialise the window
root.mainloop()

