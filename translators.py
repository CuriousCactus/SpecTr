from sys import stdout
from miscfunctions import approxmatch, approxmatchb, removesolvs
full='no'
from numpy import arange, ravel, array, where
    
def hformatter(sigs,ints,solvs,connect,broadlist=None,groupedsigs=[]):

    solvlesssigs, solvlessints, DMSOpeak, removedsigs, solvlessconnect = removesolvs(sigs, ints, solvs, connect)
    solvlesssigs, solvlessints, DMSOpeak, removedsigs, solvlessconnect = sigs, ints, 2.5, {}, connect
    print(sigs)
    array(sigs).tolist()
    print(sigs)
    list(sigs)
    print(sigs)

    #states where the DMSO peak is
    
    if full == 'yes':
        print('\nThe DMSO peak is seen at ', '%.4f' %DMSOpeak,'and should be at 2.50\n', '%.4f' %float(2.5-DMSOpeak), 'has been subtracted from all peaks\n')
        print('Uncalibrated\tCalibrated')
    calsigs=[]
    
    #makes a list of calibrated signals with referance to the DMSO peak

    i=0
    while i<len(solvlesssigs):
        calsigs.append(solvlesssigs[i]-DMSOpeak+2.5)
        if full =='yes':
            print(solvlesssigs[i],'\t\t', '%.4f' %calsigs[i])
        i=i+1

    #creates an list of lists of the peaks within each integral, and the number of peaks per integral
    #displays a table of the data used

    if groupedsigs == []:
        q=0
        sigsperint=[]
        summedints=[]
        while q<len(ints):
            r=0
            sigsinint=[]
            intsum=0
            while r<len(calsigs):
                if connect[r]==q:
                    sigsinint.append(float('%.4f' %calsigs[r]))
                    intsum=intsum+solvlessints[r]
                r=r+1
            groupedsigs.append(sigsinint)
            sigsperint.append(len(sigsinint))
            summedints.append(intsum)
            q=q+1
    else:
        print(groupedsigs)
        q=0
        sigsperint=[]
        summedints=[]
        while q<len(groupedsigs):
            sigsperint.append(len(groupedsigs[q]))
            r = 0
            intsum=0
            while r < len(groupedsigs[q]):
                intsum=intsum+ints[where(sigs == groupedsigs[q][r])]
                r=r+1
            summedints.append(intsum)
            q=q+1            
                                  

    print(sigsperint)
    
    #creates lists of integral values, peaks per integral and signals without including integral ranges with no peaks in them
    #displays a table of the data used, without the integral ranges with no peaks in them

    t=0
    newints=[]
    newsigsperint=[]
    newsigs=[]
    if full == 'yes':
        stdout.write('\nIntegral Value\tSignals per Integral\tSignals\n')
    while t<len(sigsperint):
        if sigsperint[t]>0:
            newints.append(summedints[t])
            newsigsperint.append(sigsperint[t])
            print(t)
            print(groupedsigs[t])
            newsigs.append(groupedsigs[t])
            if full == 'yes':
                stdout.write(str('%.5f' %summedints[t]).rjust(len(str(max(ints))))+ ' \t'+ str(sigsperint[t])+ '\t\t\t'+str(groupedsigs[t]).strip('[]')+'\n')
        t=t+1

    print(newsigs)

    #divides the integral values by the smallest to create a list of calibrated integrals
        
    u=0
    smallest=min(newints)
    calints=[]
    while u<len(newints):
        #calints.append(round(newints[u]/smallest))
        calints.append(newints[u]/smallest)
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
    if full == 'yes':
        stdout.write('\nSignals\t\t\t\tCouplings\n')
    while b<len(newsigs):
        k=0
        while k<len(newsigs[b]):
            if full == 'yes':
                stdout.write(str('%.4f' %newsigs[b][k]))
            if k<len(newsigs[b])-1:
                if full == 'yes':
                    stdout.write(', ')
            k=k+1
        if full == 'yes':
            stdout.write((5-len(newsigs[b]))*'\t')
        j=0
        coupling=[]
        while j<len(newsigs[b])-1:
            coupling.append((newsigs[b][j]-newsigs[b][j+1])*400)
            if full == 'yes':
                stdout.write(str('%.2f' %((newsigs[b][j]-newsigs[b][j+1])*400)))
            if j<len(newsigs[b])-2:
                if full == 'yes':
                    stdout.write(', ')
            j=j+1
        if full == 'yes':
            stdout.write('\n')
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
            avcouplingstext.append(', J = '+str(round(avcouplings[c],1))+' Hz')
        else:
            avcouplingstext.append('')
        c=c+1

    #creates a list of peak multiplicities
    
    h=0
    mults=[]
    while h<len(newsigsperint):
        if newsigsperint[h] == 1:
            mults.append('s')
        elif newsigsperint[h] == 2:
            mults.append('d')
        elif newsigsperint[h] == 3 and avcouplings[h] !=0:
            mults.append('t')
        elif newsigsperint[h] == 4 and avcouplings[h] !=0:
            mults.append('q')
        else:
            mults.append('m')
        h=h+1

##    if broadlist == None:
##        stdout.write('\nSignal No.\tSignal Value\n')
##        x=0
##        while x<len(peakavs):
##            stdout.write(str(x+1)+'\t\t'+'%.2f' %peakavs[x]+'\n')
##            x=x+1

    #writes the data in the correct format

    g=0
    textout = ''
    while g<len(peakavs):
        if broadlist==None:
            textout = textout + str('%.2f' %peakavs[g])+ ' (' + str('%.0f' %calints[g])+ 'H, '+ str(mults[g])+str(avcouplingstext[g])+')'
            if g<len(peakavs)-1:
                textout = textout + ', '
        else:
            textout = textout + str('%.2f' %peakavs[g])+ ' (' + str('%.0f' %calints[g])+ 'H, '+ str(mults[g])+str(avcouplingstext[g])
            if broadlist[g]=='br':
                textout = textout + ', br'
            textout = textout + ')'
            if g<len(peakavs)-1:
                textout = textout + ', '            
        g=g+1

    h={'textout':textout, 'sigs':sigs, 'ints':ints, 'solvs':solvs, 'solvlesssigs':solvlesssigs,
                 'solvlessints':solvlessints, 'removedsigs':removedsigs, 'DMSOpeak':DMSOpeak, 'solvlessconnect' : solvlessconnect}

    return h

def cformatter(peaks, connect, broadlist=None):

##    #creates a list of the DMSO peaks
##    
##    DMSOpeaks=[]
##    y=0
##    while y<len(peaks):
##        if 39<peaks[y]<41:
##            DMSOpeaks.append(peaks[y])
##        y=y+1
##
##    if full == "yes":
##        stdout.write("\nDMSO peaks: "+listrounder(DMSOpeaks, 4)+"\n")
##
##    if len(DMSOpeaks) != 7:
##        stdout.write("!!!Incorrect number of DMSO peaks!!!")
##
##    #calibrates the list of peaks to the middle DMSO peak
##
##    calpeaks=[]
##    f=0
##    while f<len(peaks):
##        if peaks[f] not in DMSOpeaks:
##            calpeaks.append(peaks[f]+39.5-DMSOpeaks[3])
##        f=f+1
##
##    if full == "yes":
##        stdout.write("\nCalibrated peaks: "+listrounder(calpeaks,4)+"\n")
##        
##    peakavs=calpeaks
##
##    #makes a list of the peaks for output
##
##    g=0
##    textout = ""
##    while g<len(peakavs):
##        textout = textout + str("%.2f" %peakavs[g])
##        if g<len(peakavs)-1:
##            textout = textout + ", "
##        g=g+1

    g=0
    textout = ""
    while g<len(peaks):
        textout = textout + str("%.2f" %peaks[g])
        if g<len(peaks)-1:
            textout = textout + ", "
        g=g+1

    solvlessconnect = connect

    processdic = dict()
    processdic['textout'] = textout
    processdic['sigs'] = peaks
    processdic['solvlessconnect'] = solvlessconnect
    
    return processdic

##    return (textout, peakavs, DMSOpeaks[3], len(peakavs))
