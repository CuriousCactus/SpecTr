import os, os.path, sys, codecs

#compares two values to see if they are approxmately equal with a given tolerance

def approx(num, compareto, tolerance):
    if -tolerance<num-compareto<tolerance:
        return "True"

#finds the lowest number in a list which is approximately equal to a number with a given tolerance

def approxmatch(num, comparelist, tolerance):
    x=0
    #out=0
    while x<len(comparelist):
        if approx(num, comparelist[x], tolerance):
            out=comparelist[x]
        x=x+1
    return out

#sorts compounds into correct, incorrect and needing manual formatting and to be formatted again after checking

def sorter():
    w=0
    correctlistfile=open("correctlist.txt","a")
    manuallistfile=open("manuallist.txt","a")
    skiplistfile=open("skiplist.txt","a")
    while w<1:
        check=str(raw_input("\nInterpretation is correct (y)\nWill be interpreted manually (n)\nData file needs checking (s)\n\n"))
        if check == "y" or check == "Y":
            return 1
            w=1
        elif check == "n" or check == "N":
            return 4
            w=1
        elif check == "s":
            return 0
            w=1
        else:
            w=0
        correctlistfile.close()
        manuallistfile.close()
        skiplistfile.close()

#returns a list saying which peaks are broad

def broadness(length):

    broadpeaks=raw_input("\nList the broad signals, separated by spaces\n\n").split(" ")
    sys.stdout.write("\n")
    broadlist=[]
    x=0
    while x<length:
        if str(x+1) in broadpeaks:
            broadlist.append("br")
        else:
            broadlist.append("")
        x=x+1
    return broadlist

#returns a string which looks like a list, with the numbers rounded to a specified number of decimal places

def listrounder(inputlist, sigfig):

    z=0
    outputlist=[]
    while z<len(inputlist):
        outputlist.append('{:.{sigfig}f}'.format(inputlist[z], sigfig=sigfig))
        #outputlist.append(str(inputlist[z]))
        z=z+1
    outputlist=str(outputlist).replace("'","").replace("[","").replace("]","")
    return outputlist

def hformatter(specpath, specfolder, full="no", broadlist=None):

    #specifies the input peak and integral tables are

    inputsigs = open(specpath+"peaks.txt", "r").read().split()
    inputints= open(specpath+"ints.txt", "r").read().split()

    #creates a list of all the picked peaks with intensity greater than 0.01

    d=inputsigs.index("0001")+2
    sigs=[]
    while d<len(inputsigs):
        if float(inputsigs[d+1])>0.01:
            sigs.append(float(inputsigs[d]))
        d=d+5

    #creates a list of lists conatining an integral vaule, integral starting shift and integral end shift for each integral
            
    e=inputints.index("001")+3
    ints3=[]
    while e<len(inputints):
        inte=[]
        inte.append(float(inputints[e]))
        inte.append(float(inputints[e-2]))
        inte.append(float(inputints[e-1]))
        ints3.append(inte)
        e=e+5

    #sorts the integral triplets into three lists based on the value of the end of the integral range

    ints3 = sorted(ints3, key=lambda x: x[2], reverse=True)
    f=0
    ints=[]
    intstarts=[]
    intends=[]
    while f<len(ints3):
        ints.append(ints3[f][0])
        intstarts.append(ints3[f][1])
        intends.append(ints3[f][2])
        f=f+1

    #creates a list of peaks without the solvent peaks and lists which solvent peaks have been removed
    #finds the average shift of the DMSO peak 

    y=0
    z=0
    solvs=[["2.1","2.5","3.3"],["Acetone","DMSO","Water"]]
    solvlesssigs=[]
    DMSOpeaks=[]
    if full == "yes":
        sys.stdout.write("The following solvent peaks have been removed:\n\n")
    while y<len(sigs):
        if "%.1f" %sigs[y] in solvs[0]:
            if full == "yes":
                sys.stdout.write(str(solvs[1][solvs[0].index(str("%.1f" %sigs[y]))])+" "+str(sigs[y])+"\n")
            z=z+1
            if "%.1f" %sigs[y] == "2.5":
                DMSOpeaks.append(sigs[y])
        else:
            solvlesssigs.append(sigs[y])
        y=y+1
    if z == 0:
        if full == "yes":
            sys.stdout.write("None\n")

    DMSOpeak = sum(DMSOpeaks)/len(DMSOpeaks)

    #states where the DMSO peak is
    
    if full == "yes":
        print "\nThe DMSO peak is seen at ", "%.4f" %DMSOpeak,"and should be at 2.50\n", "%.4f" %float(2.5-DMSOpeak), "has been subtracted from all peaks\n"
        print "Uncalibrated\tCalibrated"
    calsigs=[]
    
    #makes a list of calibrated signals with referance to the DMSO peak

    i=0
    while i<len(solvlesssigs):
        calsigs.append(solvlesssigs[i]-DMSOpeak+2.5)
        if full =="yes":
            print solvlesssigs[i],"\t\t", "%.4f" %calsigs[i]
        i=i+1

    #calibrates the integral ranges
        
    calintstarts=[]
    calintends=[]    
    i=0
    while i<len(intstarts):
        calintstarts.append(intstarts[i]-DMSOpeak+2.5)
        calintends.append(intends[i]-DMSOpeak+2.5)
        i=i+1

    intstarts=calintstarts
    intends=calintends
    
    #creates thing, which helps make groupedsigs
        
    l=0
    thing=[]
    while l<len(intstarts):
        k=0
        while k<len(calsigs):
            if intstarts[l] > calsigs[k] > intends[l]:
                thing.append(l)
            k=k+1
        l=l+1
    print thing

    #creates an list of lists of the peaks within each integral, and the number of peaks per integral
    #displays a table of the data used

    q=0
    groupedsigs=[]
    sigsperint=[]
    if full =="yes":
        sys.stdout.write("\nIntegral Range\tIntegral Value\tSignals per Integral\tSignals\n")
    while q<len(intstarts):
        r=0
        sigsinint=[]
        while r<len(calsigs):
            if intstarts[q] > calsigs[r] >intends[q]:
                sigsinint.append(float("%.4f" %calsigs[r]))
            r=r+1
        groupedsigs.append(sigsinint)
        sigsperint.append(len(groupedsigs[q]))
        if full == "yes":
            sys.stdout.write(str("%.3f" %intstarts[q])+" to "+ str("%.3f" %intends[q])+"\t"+ str("%.5f" %ints[q]).rjust(len(str(max(ints))))+" \t"+str(sigsperint[q])+"\t\t\t"+str(groupedsigs[q]).strip("[]")+"\n")
        q=q+1


    #creates lists of integral values, peaks per integral and signals without including integral ranges with no peaks in them
    #displays a table of the data used, without the integral ranges with no peaks in them

    t=0
    newints=[]
    newsigsperint=[]
    newsigs=[]
    if full == "yes":
        sys.stdout.write("\nIntegral Value\tSignals per Integral\tSignals\n")
    while t<len(sigsperint):
        if sigsperint[t]>0:
            newints.append(ints[t])
            newsigsperint.append(sigsperint[t])
            newsigs.append(groupedsigs[t])
            if full == "yes":
                sys.stdout.write(str("%.5f" %ints[t]).rjust(len(str(max(ints))))+ " \t"+ str(sigsperint[t])+ "\t\t\t"+str(groupedsigs[t]).strip("[]")+"\n")
        t=t+1


    #divides the integral values by the smallest to create a list of calibrated integrals
        
    u=0
    smallest=min(newints)
    calints=[]
    while u<len(newints):
        calints.append(round(newints[u]/smallest))
        u=u+1


    #creates a list of peak centres

    i=0
    peaksums=[]
    peakavs=[]
    while i<len(newsigs):
        peaksum=0
        for num in newsigs[i]:
            peaksum = peaksum + num
        peaksums.append(peaksum)
        peakavs.append(peaksums[i]/newsigsperint[i])
        i=i+1
        
        
    #creates a list of coupling constants
    
    b=0
    couplings=[]
    couplingsums=[]
    couplingavs=[]
    if full == "yes":
        sys.stdout.write("\nSignals\t\t\t\tCouplings\n")
    while b<len(newsigs):
        k=0
        while k<len(newsigs[b]):
            if full == "yes":
                sys.stdout.write(str("%.4f" %newsigs[b][k]))
            if k<len(newsigs[b])-1:
                if full == "yes":
                    sys.stdout.write(", ")
            k=k+1
        if full == "yes":
            sys.stdout.write((5-len(newsigs[b]))*"\t")
        j=0
        coupling=[]
        while j<len(newsigs[b])-1:
            coupling.append((newsigs[b][j]-newsigs[b][j+1])*400)
            if full == "yes":
                sys.stdout.write(str("%.2f" %((newsigs[b][j]-newsigs[b][j+1])*400)))
            if j<len(newsigs[b])-2:
                if full == "yes":
                    sys.stdout.write(", ")
            j=j+1
        if full == "yes":
            sys.stdout.write("\n")
        if j>0:
            diffs=[]
            x=0
            while x<len(coupling):
                y=0
                while y<len(coupling):
                    diffs.append(coupling[x]-coupling[y])
                    y=y+1
                x=x+1
            couplingsum=0
            if max(diffs)<0.1 and min(diffs)>-0.1:
                for num in coupling:
                    couplingsum = couplingsum + num
                couplingsums.append(couplingsum)
                couplingavs.append(couplingsum/(newsigsperint[b]-1))
            else:
                couplingsums.append(0)
                couplingavs.append(0)
        else:
            couplingavs.append(500.0)
        b=b+1
    
    #averages the couplings of pairs and creates a list of them, and a list of them with formatting and spaces
    
    avcouplings=[]
    avcouplingstext=[]
    c=0
    while c<len(couplingavs):
        a=0
        couplingdiffs=[]
        while a<len(couplingavs):
            couplingdiffs.append(abs(couplingavs[c]-couplingavs[a]))
            a=a+1
        couplingdiffs[c]=500
        if min(couplingdiffs)<0.2:
            matchindex=couplingdiffs.index(min(couplingdiffs))
            avcouplings.append((couplingavs[c]+couplingavs[matchindex])/2)
        else:
            avcouplings.append(couplingavs[c])
        if 0<couplingavs[c]<500:
            avcouplingstext.append(", J = "+str(round(avcouplings[c],1))+" Hz")
        else:
            avcouplingstext.append("")
        c=c+1

    #creates a list of peak multiplicities
    
    h=0
    mults=[]
    while h<len(newsigsperint):
        if newsigsperint[h] == 1:
            mults.append("s")
        elif newsigsperint[h] == 2:
            mults.append("d")
        elif newsigsperint[h] == 3 and avcouplings[h] !=0:
            mults.append("t")
        elif newsigsperint[h] == 4 and avcouplings[h] !=0:
            mults.append("q")
        else:
            mults.append("m")
        h=h+1

    if broadlist == None:
        sys.stdout.write("\nSignal No.\tSignal Value\n")
        x=0
        while x<len(peakavs):
            sys.stdout.write(str(x+1)+"\t\t"+"%.2f" %peakavs[x]+"\n")
            x=x+1

    #writes the data in the correct format

    g=0
    textout = ""
    while g<len(peakavs):
        if broadlist==None:
            textout = textout + str("%.2f" %peakavs[g])+ " (" + str("%.0f" %calints[g])+ "H, "+ str(mults[g])+str(avcouplingstext[g])+")"
            if g<len(peakavs)-1:
                textout = textout + ", "
        else:
            textout = textout + str("%.2f" %peakavs[g])+ " (" + str("%.0f" %calints[g])+ "H, "+ str(mults[g])+str(avcouplingstext[g])
            if broadlist[g]=="br":
                textout = textout + ", br"
            textout = textout + ")"
            if g<len(peakavs)-1:
                textout = textout + ", "            
        g=g+1

    return (textout, len(peakavs))

def cformatter(specpath, specfolder, full="no", broadlist=None):

    inputpeaks = open(specpath+"peaks.txt", "r").read().split()

    #creates a list of all the picked peaks

    d=inputpeaks.index("0001")+2
    peaks=[]
    intensities=[]
    while d<len(inputpeaks):
        peaks.append(float(inputpeaks[d]))
        d=d+5

    #creates a list of the DMSO peaks
    
    DMSOpeaks=[]
    y=0
    while y<len(peaks):
        if 39<peaks[y]<41:
            DMSOpeaks.append(peaks[y])
        y=y+1

    if full == "yes":
        sys.stdout.write("\nDMSO peaks: "+listrounder(DMSOpeaks, 4)+"\n")

    if len(DMSOpeaks) != 7:
        sys.stdout.write("!!!Incorrect number of DMSO peaks!!!")

    #calibrates the list of peaks to the middle DMSO peak

    calpeaks=[]
    f=0
    while f<len(peaks):
        if peaks[f] not in DMSOpeaks:
            calpeaks.append(peaks[f]+39.5-DMSOpeaks[3])
        f=f+1

    if full == "yes":
        sys.stdout.write("\nCalibrated peaks: "+listrounder(calpeaks,4)+"\n")
        
    peakavs=calpeaks

    #makes a list of the peaks for output

    g=0
    textout = ""
    while g<len(peakavs):
        textout = textout + str("%.2f" %peakavs[g])
        if g<len(peakavs)-1:
            textout = textout + ", "
        g=g+1

    return (textout, peakavs, DMSOpeaks[3], len(peakavs))

def dformatter(specpath, specfolder, full="no", broadlist=None):

    inputpeaks = open(specpath+"peaks.txt", "r").read().split()

    #creates a list of all the picked peaks

    d=inputpeaks.index("0001")+2
    peaks=[]
    while d<len(inputpeaks):
        peaks.append(float(inputpeaks[d]))
        d=d+5
    
    peakavs=peaks

    #makes a list of the peaks for output

    g=0
    textout = ""
    while g<len(peakavs):
        textout = textout + str("%.2f" %peakavs[g])
        if g<len(peakavs)-1:
            textout = textout + ", "
        g=g+1

    return (textout, peaks, len(peakavs))

sys.stdout.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
sys.stdout.write("#############################################################################\n")
sys.stdout.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
print("NMR Spectrum Interpreter")
print("Author: Lois Overvoorde")

#clears log files if told to

clear=str(raw_input("\nPress c to clear log files "))

if clear == "c":
    correctlistfile=open("correctlist.txt","w")
    manuallistfile=open("manuallist.txt","w")

    correctlistfile.write("")
    manuallistfile.write("")

    correctlistfile.close()
    manuallistfile.close()

#creates a list of the names of folders starting with LMO

x=0
specfolders=[]
cwdcontents = os.listdir(os.getcwd())
while x<len(cwdcontents):
    if cwdcontents[x][0:3]=="LMO":
        specfolders.append(cwdcontents[x])
    x=x+1

#creates the log files if they don't already exist

correctlistfile=open("correctlist.txt","a")
manuallistfile=open("manuallist.txt","a")
printoutfile=open("printout.txt","a")

correctlistfile.close()
manuallistfile.close()
printoutfile.close()

#reads the log files and turns them into lists

correctlistfile=open("correctlist.txt","r")
manuallistfile=open("manuallist.txt","r")

correctlist=correctlistfile.read().split()
manuallist=manuallistfile.read().split()

correctlistfile.close()
manuallistfile.close()

#clears the skiplist log file

skiplistfile=open("skiplist.txt","w")
skiplistfile.write("")
skiplistfile.close()

#formats files if they are present and not already formatted or rejected and returns interpretation for H, C and DEPT

d=0
while d<len(specfolders):
    e=10
    cpeaks=[None, None, None]
    if specfolders[d] not in correctlist and specfolders[d] not in manuallist:
        sys.stdout.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        sys.stdout.write("#############################################################################\n")
        sys.stdout.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    yescount=0

    #formats files if they are present and not already formatted or rejected and returns interpretation for H, C and DEPT
    
    while e<99:
        specpath=specfolders[d]+"/"+str(e)+"/"
        if os.path.exists(specpath):
            if specfolders[d] not in correctlist and specfolders[d] not in manuallist:
                sys.stdout.write("\n" + specpath+" has not yet been formatted\n")
                paramfile=open(specpath+"pdata/1/parm.txt", "r")
                paramlist = paramfile.read().split()
                paramfile.close()
                if paramlist[paramlist.index("PULPROG")+1]=="zg30":
                    sys.stdout.write("It is a 1H spectrum")
                    if os.path.exists(specpath+"peaks.txt") and os.path.exists(specpath+"ints.txt"):
                        sys.stdout.write("\npeaks.txt and ints.txt exist\n")
                        houts=hformatter(specpath, specfolders[d], full="no")
                        sys.stdout.write("\nThe following data have been found for "+specfolders[d]+" (1H):\n\n" + houts[0] + "\n")
                        broadlist=broadness(houts[1])
                        houts=hformatter(specpath, specfolders[d], full="no", broadlist=broadlist)
                        yescount=yescount+1
                        sys.stdout.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    else:
                        sys.stdout.write("\npeaks.txt and ints.txt do not exist\n")
                        sys.stdout.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n") 
                elif paramlist[paramlist.index("PULPROG")+1]=="zgpg30":
                    sys.stdout.write("It is a 13C spectrum")                    
                    if os.path.exists(specpath+"peaks.txt"):
                        sys.stdout.write("\npeaks.txt exists\n")
                        couts=cformatter(specpath, specfolders[d], full="no")
                        sys.stdout.write("\nThe following data have been found for "+specfolders[d]+" (13C):\n\n" + couts[0] + "\n")
                        cpeaks[0]=(couts[1])
                        cpeaks[2]=(couts[2])
                        yescount=yescount+1
                        sys.stdout.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    else:
                        sys.stdout.write("\npeaks.txt does not exist\n")
                        sys.stdout.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")       
                elif paramlist[paramlist.index("PULPROG")+1]=="dept135":
                    sys.stdout.write("It is a DEPT135 spectrum")
                    if os.path.exists(specpath+"peaks.txt"):
                        douts=dformatter(specpath, specfolders[d], full="no")
                        sys.stdout.write("\nThe following data have been found for "+specfolders[d]+" (13C):\n\n" + douts[0] + "\n")
                        cpeaks[1]=(douts[1])
                        yescount=yescount+1
                        sys.stdout.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    else:
                        sys.stdout.write("\npeaks.txt does not exist\n")
                        sys.stdout.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        e=e+1

    if yescount == 3:
        
        #calibrates the dept peaks
    
        j=0
        while j<len(cpeaks[1]):
            cpeaks[1][j]=cpeaks[1][j]+39.5-cpeaks[2]
            j=j+1

        #makes a list indicating which peaks show in the DEPT spectrum
          
        h=0
        tertpeaks=[]
        while h<len(cpeaks[0]):
            tertpeaks.append(0)
            i=0
            while i<len(cpeaks[1]):
                if approx(cpeaks[1][i], cpeaks[0][h], 0.6):
                    tertpeaks[h]=1
                i=i+1
            h=h+1

        #lists which peaks show in the DEPT spectrum in a table

        k=0
        print "\n13C\tDEPT135"
        while k<len(tertpeaks):
            if tertpeaks[k]==1 and cpeaks[0][k]>80:
                sys.stdout.write("%.1f" %cpeaks[0][k]+"\t"+"%.1f" %approxmatch(cpeaks[0][k], cpeaks[1], 0.6)+"\n")
            elif tertpeaks[k]==0 and cpeaks[0][k]>80:
                sys.stdout.write("%.1f" %cpeaks[0][k]+"\n")                
            elif tertpeaks[k]==1 and cpeaks[0][k]<80:
                sys.stdout.write("%.1f" %cpeaks[0][k]+"\t"+"%.1f" %approxmatch(cpeaks[0][k], cpeaks[1], 0.6)+"\n")
            elif tertpeaks[k]==0 and cpeaks[0][k]<80:
                sys.stdout.write("%.1f" %cpeaks[0][k]+"\n")
            k=k+1

        #asks which peaks are broad

        sys.stdout.write("\nSignal No.\tSignal Value\n")
        x=0
        while x<len(couts[1]):
            sys.stdout.write(str(x+1)+"\t\t"+"%.1f" %couts[1][x]+"\n")
            x=x+1
        broadlist=broadness(couts[3])

        #compiles the text for the C and DEPT spectra
        
        k=0
        ctext=u". ¹³C NMR (100 MHz, DMSO): δ/ppm "
        while k<len(tertpeaks):
            ctext = ctext + "%.1f" %cpeaks[0][k]
            if tertpeaks[k]==1 and cpeaks[0][k]>80:
                ctext=ctext + " (CH"
            elif tertpeaks[k]==0 and cpeaks[0][k]>80:
                ctext=ctext + " (C"
            elif cpeaks[0][k]<80:
                ctext=ctext + u" (CH₃"
            if broadlist[k]=="br":
                ctext=ctext+", br)"
            else:
                ctext=ctext+")"                
            if k<len(tertpeaks)-1:
                ctext=ctext+", "
            k=k+1

        #puts all the text together
    
        alltext=(u"¹H NMR (400 MHz, DMSO): δ/ppm "+houts[0]+ctext+".")
        sys.stdout.write("Full text for "+specfolders[d]+":\n\n"+alltext+"\n\n")
        yescount=yescount+sorter()

    #writes the molecule name to the appropriate list depending on whether its spectra were correctly formatted
    
    if yescount == 4:
        correctlistfile=open("correctlist.txt","a")
        correctlistfile.write(specfolders[d]+"\n")
        correctlistfile.close()
    elif yescount<4:
        skiplistfile=open("skiplist.txt","r")
        manuallistfile=open("manuallist.txt","r")
        correctlistfile=open("correctlist.txt","r")
        if specfolders[d] not in skiplistfile.read() and specfolders[d] not in manuallistfile.read() and specfolders[d] not in correctlistfile.read():
            skiplistfile=open("skiplist.txt","a")
            skiplistfile.write(specfolders[d]+"\n")
            skiplistfile.close()
        manuallistfile.close()
        skiplistfile.close()
        correctlistfile.close()
    elif yescount>4:
        manuallistfile=open("manuallist.txt","a")
        manuallistfile.write(specfolders[d]+"\n")
        manuallistfile.close()

    #adds the text for the molecule to the printout

    if yescount == 4:
        printoutfile=codecs.open("printout.txt", mode="r", encoding="utf-8")
        if specfolders[d] in printoutfile.read():
            print "\nMolecule has already been processed, entry modified."
            printoutfile.seek(0)
            printout=printoutfile.read().split("\r\n")
            printout[printout.index(specfolders[d])+1]=alltext
        elif specfolders[d] not in printoutfile.read():
            print "\nMolecule is new to the list, new entry created."
            printoutfile.seek(0)
            printout=printoutfile.read().split("\r\n")
            printout.append(specfolders[d])
            printout.append(alltext)
        alltext="\r\n".join(printout)
        printoutfile.close()
        printoutfile=codecs.open("printout.txt", mode="w", encoding="utf-8")
        printoutfile.write(alltext)
        printoutfile.close()
    
    d=d+1

sys.stdout.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
sys.stdout.write("#############################################################################\n")
sys.stdout.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

#lists what has happened to the files

correctlistfile=open("correctlist.txt","r")
manuallistfile=open("manuallist.txt","r")
skiplistfile=open("skiplist.txt","r")

sys.stdout.write("\nCorrectly formatted files:\n"+correctlistfile.read())
sys.stdout.write("Files to be formatted manually:\n"+manuallistfile.read())
sys.stdout.write("Skipped files:\n"+skiplistfile.read())

correctlistfile.close()
manuallistfile.close()
skiplistfile.close()

sys.stdout.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
sys.stdout.write("#############################################################################\n")
sys.stdout.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
