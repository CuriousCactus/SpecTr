from nmrglue import proc_base

bruker_dsp_table = {
    10: { 
        2    : 44.75,
        3    : 33.5,
        4    : 66.625,
        6    : 59.083333333333333,
        8    : 68.5625,
        12   : 60.375,
        16   : 69.53125,
        24   : 61.020833333333333,
        32   : 70.015625,
        48   : 61.34375,
        64   : 70.2578125,
        96   : 61.505208333333333,
        128  : 70.37890625,
        192  : 61.5859375,
        256  : 70.439453125,
        384  : 61.626302083333333,
        512  : 70.4697265625,
        768  : 61.646484375,
        1024 : 70.48486328125,
        1536 : 61.656575520833333,
        2048 : 70.492431640625,
        },
    11: {
        2    : 46.,
        3    : 36.5,
        4    : 48.,
        6    : 50.166666666666667,
        8    : 53.25,
        12   : 69.5,
        16   : 72.25,
        24   : 70.166666666666667,
        32   : 72.75,
        48   : 70.5,
        64   : 73.,
        96   : 70.666666666666667,
        128  : 72.5,
        192  : 71.333333333333333,
        256  : 72.25,
        384  : 71.666666666666667,
        512  : 72.125,
        768  : 71.833333333333333,
        1024 : 72.0625,
        1536 : 71.916666666666667,
        2048 : 72.03125
        },
    12: {
        2    : 46. ,
        3    : 36.5,
        4    : 48.,
        6    : 50.166666666666667,
        8    : 53.25,
        12   : 69.5,
        16   : 71.625,
        24   : 70.166666666666667,
        32   : 72.125,
        48   : 70.5,
        64   : 72.375,
        96   : 70.666666666666667,
        128  : 72.5,
        192  : 71.333333333333333,
        256  : 72.25,
        384  : 71.666666666666667,
        512  : 72.125,
        768  : 71.833333333333333,
        1024 : 72.0625,
        1536 : 71.916666666666667,
        2048 : 72.03125
        },
    13: {
        2    : 2.75, 
        3    : 2.8333333333333333,
        4    : 2.875,
        6    : 2.9166666666666667,
        8    : 2.9375,
        12   : 2.9583333333333333,
        16   : 2.96875,
        24   : 2.9791666666666667,
        32   : 2.984375,
        48   : 2.9895833333333333,
        64   : 2.9921875,
        96   : 2.9947916666666667
        } 
    }

def rdf(dic, data):

    if 'acqus' not in dic:
        raise ValueError("dictionary does not contain acqus parameters") 
    
    if 'DECIM' not in dic['acqus']:
        raise ValueError("dictionary does not contain DECIM parameter")
    decim = dic['acqus']['DECIM']
    
    if 'DSPFVS' not in dic['acqus']:
        raise ValueError("dictionary does not contain DSPFVS parameter")
    dspfvs = dic['acqus']['DSPFVS']
    
    phase = bruker_dsp_table[dspfvs][decim]
    
    csdata = proc_base.cs(data, pts=-round(phase))

    return csdata

def average(avlist):
    x=0
    total=0
    while x<len(avlist):
        total = total + avlist[x]
        x=x+1
    av = total/len(avlist)
    return av

def bracket(self, x, y, text=''):
    if len(x)>0:
        self.bracket = self.annotate(text, xy=(average([x[0],x[-1]]), max(y)), verticalalignment='bottom',
               horizontalalignment='center', textcoords='offset points', xytext=(0, 35),
                arrowprops=dict(arrowstyle="-", shrinkB=18))
        a=1
        while a<len(x):
            self.bracket = self.annotate('', xy=(x[0], max(y)),  xycoords='data',xytext=(x[a], max(y)), textcoords='data',
                   arrowprops=dict(arrowstyle="-",connectionstyle="arc,angleA=90,angleB=90,armA=20,armB=20",shrinkA=5, shrinkB=5))
            a=a+1
    else:
        pass

def printlist(listin):
    x=0
    textout=''
    while x<len(listin):
        if type(listin) == list:
            textout = textout + str(listin[x]) + '\n'
        elif type(listin) == dict:
            key=listin.keys()[x]
            textout = textout + str(key) + ':\t'
            textout = textout + str(listin[key]) + '\n'
        else:
            textout = str(listin)
        x=x+1
    return textout

def printer(sigs=[], ints=[], solvs={}, solvlessigs=[], solvlessints=[], removedsigs={}):
    
    if len(solvlessigs) != 0:
        sys.stdout.write('The following solvent peaks have been removed:\n\n')
    if len(solvlessigs) == len(sigs) != 0:
        sys.stdout.write('None\n')
    elif len(solvlessigs) != 0:
        sys.stdout.write(printlist(removedsigs))

def isapprox(num, compareto, tolerance):
    
    #compares two values to see if they are approxmately equal with a given tolerance
    
    if -tolerance<float(num)-float(compareto)<tolerance:
        return True

def approxmatch(num, comparelist, tolerance):
    
    #finds the last number in a list which is approximately equal to a number with a given tolerance    
    
    x=0
    while x<len(comparelist):
        if isapprox(num, comparelist[x], tolerance):
            out=comparelist[x]
        x=x+1
    return out

def approxmatchb(num, comparelist, tolerance):
    
    #finds if there is a number in a list which is approximately equal to a number with a given tolerance    

    x=0
    out=False
    while x<len(comparelist):
        if isapprox(num, comparelist[x], tolerance):
            out=True
        x=x+1
    return out

def removesolvs(sigs, ints, solvs, connect):
    
    y=0
    solvlesssigs=[]
    solvlessints=[]
    DMSOpeaks=[]
    removedsigs=dict()
    solvlessconnect=[]
    impvals=list(solvs.values())
    impnames=list(solvs.keys())
    
    while y<len(sigs):
        if approxmatchb(sigs[y], impvals, 0.1):
            removedsigs[(impnames[impvals.index(approxmatch(sigs[y], impvals, 0.1))])]=sigs[y]
            solvlessconnect.append(0)
            if isapprox(sigs[y], solvs['DMSO'], 0.1):
                DMSOpeaks.append(sigs[y])
        else:
            solvlesssigs.append(sigs[y])
            solvlessints.append(ints[y])
            solvlessconnect.append(connect[y])
        y=y+1

    DMSOpeak = sum(DMSOpeaks)/len(DMSOpeaks)

    return solvlesssigs, solvlessints, DMSOpeak, removedsigs, solvlessconnect

def s2i(slist):
    z = 0
    nlist = []
    while z<len(slist):
        nlist.append(int(slist[z]))
        z = z + 1
    return nlist
