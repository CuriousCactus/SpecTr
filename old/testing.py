import nmrglue as ng
import numpy as np
import scipy as sp
import pylab
from translators import hformatter, printer
import process

def getdata(folder):

    solvs={'DMSO':'2.5', 'Water':'3.3', 'Acetone':'2.1'}

    dic,fiddata = ng.bruker.read(folder)
    #print fiddata
    nuc1 = dic['acqus']['NUC1']
    #wdata = ng.proc_base.sp(fiddata,off=0.3,end=0.98,pow=2)
    if nuc1 == '1H':
        wdata = ng.proc_base.gmb(fiddata, a=0, b=0.000001)
    elif nuc1 == '13C':
        wdata = ng.proc_base.em(fiddata, lb=0.00005)
    #wdata = ng.proc_base.gmb(fiddata, a=1, b=1)
    #print wdata
    zfdata = ng.proc_base.zf(wdata)
    #zfdata = ng.proc_base.zf(fiddata)
    #csdata = ng.bruker.remove_digital_filter(dic,zfdata)
    csdata = process.rdf(dic, zfdata)
    ftdata = ng.proc_base.fft(csdata)
##    print ftdata
##    pylab.plot(ftdata, 'y-')
##    pylab.show()
    
    clip=200

    cldata=ftdata[clip:len(ftdata)-clip]
    phsh = lambda x: -ng.proc_base.ps(cldata, p0=x[0], p1=x[1]).real.min()

    p0=0
    p1=0
    x0=np.array([p0,p1])
    res=sp.optimize.minimize(phsh,x0, method='Nelder-Mead',options={'xtol': 1e-12,'ftol': 1e-12,'maxfev': 200,'maxiter': 200})
    #sp.optimize.show_options('minimize','Nelder-Mead')

    psdata = ng.proc_base.ps(cldata,p0=res.x[0],p1=res.x[1])
    didata = ng.proc_base.di(psdata)
    if nuc1 == '1H':
        ppdata = ng.analysis.peakpick.pick(didata,thres=1000000, direction='positive', algorithm='downward', est_params=True)        
    elif nuc1 == '13C':
        ppdata = ng.analysis.peakpick.pick(didata,thres=8000000, direction='positive', algorithm='downward', est_params=True)
    if nuc1 == '1H':
        intdata = ng.proc_base.integ(didata)
        intdata = max(intdata)-intdata

    sigs=np.sort(ppdata[0], axis=0)
    sigs=np.flipud(sigs)

    sw = dic['acqus']["SW"]
    bf1 = dic['acqus']["BF1"]
    o1 = dic['acqus']["O1"]
    size = len(didata)+2*clip
    clipp=clip*sw/size
    o1p = o1/bf1
    swp = sw-2*clipp
    x0 = o1p+swp/2
    x1 = o1p-swp/2
    size = len(didata)

    xp=np.linspace(x1,x0,size)

    b=0
    segxs=[]
    sigints=[]
    while b<len(sigs):
        segxs.append(np.sort(ng.analysis.segmentation.find_downward(didata,sigs[b],thres=7000),axis=0))
        b=b+1

    d=0
    segys=[]
    while d<len(segxs):
        e=0
        segy=[]
        while e<len(segxs[d]):
            segy.append(didata[segxs[d][e]])
            e=e+1
        segys.append(segy)
        sigints.append(sum(segy))
        d=d+1

    a=0
    heights=[]
    sigsp=[]
    segxsp=[]
    while a<len(sigs):
        heights.append(didata[sigs[a]])
        sigsp.append(xp[sigs[a]])
        c=0
        segxp=[]
        while c<len(segxs[a]):
            segxp.append(xp[segxs[a][c]])
            c=c+1
        segxsp.append(segxp)
        a=a+1

    xy=np.array([np.ravel(sigsp),np.ravel(heights)])
    xy=xy[:,xy[0].argsort()]


    sigsp=np.ravel(xy[0])
    sigsp=sigsp[::-1]
    heights=np.ravel(xy[1])
    heights=heights[::-1]

    segxsp=segxsp[::-1]
    segys=segys[::-1]

    xmax = max(sigsp) + 1
    ymin = min(didata) - max(didata)/10

    datadic = dict()
    datadic['didata'] = didata
    datadic['xp'] = xp
    datadic['sigsp'] = sigsp
    datadic['heights'] = heights
    datadic['xmax'] = xmax
    datadic['ymin'] = ymin
    datadic['heights'] = heights
    datadic['sigints'] = np.ravel(sigints)
    datadic['solvs'] = solvs 
    datadic['nuc1'] = nuc1
    if nuc1 == '1H':
        datadic['intdata'] = intdata
##
##    pylab.plot(xp,didata,'r-')
##    pylab.plot(sigsp, heights, 'bo')
##    #pylab.plot(segxsp[10], segys[10], 'y-')
##    pylab.xlim(250,-50)
##    pylab.show()
##
    return datadic



##def unpack(dic):
##    #mydict = {'raw': 'data', 'code': 500}
##    globals().update(dic)
##    print solvs
####    vars()['bread'] = 123
####    print bread
####    print dic.keys()[0], dic.values()[0]
####
####    #print vars()[dic.keys()[0]]
####    global solvs
####    vars()['solvs'] = 123
####    #vars()['solvs'] = dic.values()[0]
####    #vars()[dic.keys()[0]] = dic.values()[0]
####    #exec dic.keys()[0]
####    #dic.keys()[0] = dic.values()[0]
####    print solvs
##    
##
##unpack(getdata('LMO_3BrAP_1/20'))

#print getdata('LMO_3BrAP_1/20').keys()

#print getdata('LMO_3BrAP_1/20')

#h=hformatter(sigsp, sigints, solvs, thing)
#printer(datadic['sigs'], datadic['ints'], datadic['solvs'], datadic['solvlesssigs'], datadic['solvlessints'], datadic['removedsigs'])

#data=getdata('LMO_3BrAP_1\\21')

