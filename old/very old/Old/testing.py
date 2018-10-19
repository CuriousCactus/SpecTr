import nmrglue as ng
import numpy as np
import scipy
td=32768
x = int( np.ceil(td/256.)*256 )/2
pi=np.pi

def em(data,lb=0.0,inv=False):
    """
    Exponential Apodization

    Functional form:
        em(x_i) = exp(-pi*i*lb)

    Parameters:

    * data  Array of spectral data.
    * lp    Exponential line broadening.
    * inv   Set True for inverse apodization.

    """
    apod = np.exp(-pi*np.arange(data.shape[-1])*lb)
    if inv:
        apod = 1/apod   # invert apodization

    return apod*data

def ps(data,p0=0.0,p1=0.0,inv=False,x=x):
    """ 
    Linear Phase Correction

    Parameters:

    * data  Array of spectral data.
    * p0    Zero order phase in degrees.
    * p1    First order phase in degrees.
    * inv   Set True for inverse phase correction

    """
    p0 = p0*pi/180. # convert to radians
    p1 = p1*pi/180. 
    size = x
    apod = np.exp(1.0j*(p0+(p1*np.arange(size)/size) ))

    if inv:
        apod = 1/apod
    return apod*data

dic,data = ng.bruker.read('LMO_3BrAP_1/20',shape=(x),cplex=True)
#gdata=ng.proc_bl.sol_gaussian(data)
#gdata=ng.proc_base.ft(gdata)
gdata=ng.proc_base.ft(data)
ftdata=ng.proc_base.ft(data)
gdata=ng.proc_bl.sol_gaussian(gdata, w=200)
#gdata=em(gdata)
#gdata=data
p0=0
p1=0

phsh = lambda x: -ps(gdata).min()
x0=np.array([p0,p1])
res=scipy.optimize.minimize(phsh,x0)
print res

psdata=ps(gdata, p0=-100,  p1=-10)

data39= ps(gdata, p0=39,  p1=0)
data95= ps(gdata, p0=95,  p1=0)
datam108= ps(gdata, p0=-108,  p1=0)
datam106= ps(gdata, p0=-75,  p1=0)

p0min=-200
p0max=200

p0=p0min
ps0mins=[]
while p0<p0max:
    ps0mins.append(ps(gdata, p0=p0,  p1=0).real.min())
    p0=p0+1

p1min=-20
p1max=20

p1=p1min
ps1mins=[]
while p1<p1max:
    ps1mins.append(ps(datam106, p0=0,  p1=p1).real.min())
    p1=p1+1
    
datam106= ps(gdata, p0=-75.79,  p1=-3.25)
import pylab
#pylab.plot(np.arange(p0min,p0max),ps0mins)
#pylab.plot(np.arange(p1min,p1max),ps1mins)
#pylab.plot(data, 'r-', gdata, 'g-', psdata, 'b-')
#pylab.plot(data95, 'r-', data39, 'g-', datam108, 'b-', datam106, 'y-')
pylab.plot(ftdata, 'r-')
pylab.show()

res=scipy.optimize.minimize(phsh,x0)
