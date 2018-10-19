from nmrglue import proc_base, bruker, analysis
from numpy import sort, flipud, array, linspace, ravel
from scipy.optimize import minimize, show_options
from miscfunctions import rdf

def getdata(folder, options={'hthres' : 1000000}):

    #get the options
    globals().update(options)
    
    #get the dictionary of parameters and the fid data
    dic, fiddata = bruker.read(folder)

    #get the nucleus
    nuc1 = dic['acqus']['NUC1']

    #apply window function
    if nuc1 == '1H':
        wdata = proc_base.gmb(fiddata, a = 0, b = 0.000001) #gaussian window function
    elif nuc1 == '13C':
        wdata = proc_base.em(fiddata, lb = 0.00005) #exponential window function

    #zero-fill the data
    zfdata = proc_base.zf(wdata)

    #remove the digital filter
    csdata = rdf(dic, zfdata)

    #fourier transform the data
    ftdata = proc_base.fft(csdata)

    #clip off the curved-down ends of the spectrum
    clip = 200
    cldata = ftdata[clip:len(ftdata) - clip]

    #apply a phase shift to the data
    x0 = [0, 0]
    phsh = lambda x: -proc_base.ps(cldata, p0 = x[0], p1 = x[1]).real.min()
    res = minimize(phsh, x0, method='Nelder-Mead', options={'xtol': 2,'ftol': 2,'maxfev': 200,'maxiter': 200})
    psdata = proc_base.ps(cldata, p0 = res.x[0], p1 = res.x[1])

    #delete the imaginary part of the data
    spectrum = proc_base.di(psdata)

    #pick the peaks
    if nuc1 == '1H':
        ppdata = analysis.peakpick.pick(spectrum, pthres = hthres, algorithm = 'downward', est_params = True)        
    elif nuc1 == '13C':
        ppdata = analysis.peakpick.pick(spectrum, pthres = 8000000, algorithm = 'downward', est_params = True)
    peaks = sort(ppdata, axis = 0)
    peaks = flipud(peaks)

    #get the integral trace
    if nuc1 == '1H':
        integration = proc_base.integ(spectrum)
        integration = max(integration) - integration

    #get all of the x values in ppm
    sw = dic['acqus']['SW']
    bf1 = dic['acqus']['BF1']
    o1 = dic['acqus']['O1']
    size = len(spectrum) + 2 * clip
    clipp=clip * sw / size
    o1p = o1 / bf1
    swp = sw - 2 * clipp
    x0 = o1p + swp / 2
    x1 = o1p - swp / 2
    size = len(spectrum)
    xp = linspace(x1, x0, size)

    #get the x values for each peak segment
    b = 0
    segxs = []
    while b < len(peaks):
        segxs.append(sort(analysis.segmentation.find_downward(spectrum, int(peaks[b][0]), thres = 7000), axis = 0))
        b = b + 1

    #get the y values and integrals for each peak segment
    d = 0
    segys = []
    peakints = []
    while d < len(segxs):
        e = 0
        segy = []
        while e < len(segxs[d]):
            segy.append(spectrum[segxs[d][e]])
            e = e + 1
        segys.append(segy)
        peakints.append(sum(segy))
        d = d + 1

    segys = segys[::-1]

    #get the height of each peak
    #get the x value of each peak in ppm
    #get the x values for each peak segment in ppm
    a = 0
    peaksy = []
    peaksxp = []
    segxsp = []
    while a < len(peaks):
        pointnum = int(peaks[a][0])
        peaksy.append(spectrum[pointnum])
        peaksxp.append(xp[pointnum])
        c = 0
        segxp = []
        while c < len(segxs[a]):
            segxp.append(xp[segxs[a][c]])
            c = c + 1
        segxsp.append(segxp)
        a = a + 1

    xy = array([ravel(peaksxp),ravel(peaksy)])
    xy = xy[:,xy[0].argsort()]

    peaksxp = ravel(xy[0])
    peaksxp = peaksxp[::-1]

    peaksy = ravel(xy[1])
    peaksy = peaksy[::-1]

    segxsp = segxsp[::-1]

    #get the graph limits
    xmax = max(peaksxp) + 1
    ymin = min(spectrum) - max(spectrum) / 10

    #put the necessary data in a dictionary
    datadic = dict()
    datadic['xp'] = xp
    datadic['spectrum'] = spectrum
    datadic['peaksxp'] = peaksxp
    datadic['peaksy'] = peaksy
    datadic['xmax'] = xmax
    datadic['ymin'] = ymin
    datadic['nuc1'] = nuc1
    datadic['peakints'] = ravel(peakints)
    datadic['options'] = options
    if nuc1 == '1H':
        datadic['integration'] = integration

    return datadic


