import nmrglue as ng
import numpy as np


td=32768
x = int( np.ceil(td/256.)*256 )/2

def ft(data,auto=False,real=False,inv=False,alt=False,neg=False,
    null=False,bruk=False):
    """
    Complex Fourier Transform

    Choosing multiply conflicting modes produces results different from
    NMRPipe.

    Parameters:

    * dic   Dictionary of NMRPipe parameters.
    * data  array of spectral data.

    Set any of the following to True to choose a mode.
    * auto  Choose mode automatically
    * real  Transform Real-only data
    * inv   Inverse transform
    * alt   Sign Alternate
    * neg   Negate Imaginaties
    * null  Do not apply transform, only adjust headers
    * bruk  Process Redfield sequential data (same as alt=True,real=True)

    """
    size = data.shape[-1]

    # super-flags
    if auto:
        # turn off all flags
        real = False
        inv  = False
        alt  = False
        neg  = False
        null = False
        bruk = False

    if bruk:
        real = True
        alt = True

    if real:    # keep real data
        if np.iscomplexobj(data):
            data.imag = 0.0
    
    if alt: # sign alternate
        if inv == False:    # inv with alt, alternates the inverse
            data[...,1::2] = data[...,1::2]*-1.

    if neg: # negate the imaginary 
        if np.iscomplexobj(data):
            data.imag = data.imag * -1.

    # recast data if needed
    if data.dtype!="complex64":
        data = data.astype("complex64")

    if inv: # inverse transform
        data = ng.proc_base.icomplexft(data)
        if alt:
            data[...,1::2] = data[...,1::2]*-1
    else:
        data = ng.proc_base.complexft(data)

    if real:
        # return a complex array with double size
        data = np.array(data[...,size/2:],dtype="complex64")

    return data

# read in the file
dic,fiddata = ng.bruker.read('LMO_3BrAP_1/20',shape=(x),cplex=True)

# process the direct dimension
#data = ng.proc_base.sp(data,off=0.35,end=0.98,pow=2)
c=0.5
#data[...,0] = data[...,0]*c
#data = ng.proc_base.zf(data)
ftdata = ft(fiddata, auto=True)
data = ng.proc_base.ps(ftdata,p0=-75.79,p1=-3.25)
data = ng.proc_base.di(data)
data = ng.proc_bl.med(data)

import pylab
pylab.plot(fiddata, 'r-')
pylab.show()
