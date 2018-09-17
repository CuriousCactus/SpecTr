import nmrglue as ng
import numpy as np
import scipy as sp
import pylab
from translators import hformatter, printer
import process

def getdata(folder):

    solvs={'DMSO':'2.5', 'Water':'3.3', 'Acetone':'2.1'}

    dic,fiddata = ng.bruker.read(folder)

    #wdata = ng.proc_base.sp(fiddata,off=0.35,end=0.98,pow=2)
    wdata = ng.proc_base.gmb(fiddata, a=0, b=0.000001)
    zfdata = ng.proc_base.zf(wdata)
    #csdata = ng.bruker.remove_digital_filter(dic,zfdata)
    csdata = process.rdf(dic, zfdata)
    ftdata = ng.proc_base.fft(csdata)

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
    intdata = ng.proc_base.integ(didata)
    intdata = max(intdata)-intdata
    ppdata = ng.analysis.peakpick.pick(didata,thres=1000000, direction='positive', algorithm='downward', est_params=True)

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

    #h=hformatter(sigsp, sigints, solvs, thing)
    #printer(h['sigs'], h['ints'], h['solvs'], h['solvlesssigs'], h['solvlessints'], h['removedsigs'])

    ##pylab.plot(xp,didata,'r-')
    ##pylab.plot(xp,intdata/100, 'g-')
    ##pylab.plot(sigsp, heights, 'bo')
    ##pylab.plot(segxsp[10], segys[10], 'y-')
    ##pylab.xlim(14.5,-1.5)
    #pylab.show()

    xmax = max(sigsp) + 1
    ymin = min(didata) - max(didata)/10

    h = dict()
    h['didata'] = didata
    h['xp'] = xp
    h['intdata'] = intdata
    h['sigsp'] = sigsp
    h['heights'] = heights
    h['xmax'] = xmax
    h['ymin'] = ymin
    h['heights'] = heights
    h['sigints'] = np.ravel(sigints)
    h['solvs'] = solvs

    ##def d():
    ##    data = {'didata': didata, 'xp': xp, 'intdata': intdata, 'sigsp': sigsp, 'heights': heights, 'xmax': xmax, 'ymin': ymin,
    ##            'textout': h['textout'], 'sigsp': sigsp, 'heights': heights, 'solvlessthing' : h['solvlessthing']}
    ##    return data
    return h

#print getdata('LMO_3BrAP_1/20')
