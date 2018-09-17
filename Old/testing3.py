import nmrglue as ng
import numpy as np
import pylab
import scipy
def phsh(x):
    td=32768
    size = int( np.ceil(td/256.)*256 )/2

    dic,fiddata = ng.bruker.read('LMO_3BrAP_1/20',shape=(size),cplex=True)

    spdata = ng.proc_base.sp(fiddata,off=0.35,end=0.98,pow=2)
    zfdata = ng.proc_base.zf(spdata)
    csdata=ng.proc_base.cs(zfdata, pts=-70)
    ftdata = ng.proc_base.ft(csdata)



    #phsh = lambda x: -ng.proc_base.ps(ftdata, p0=p0, p1=p1).real.min()

    return -ng.proc_base.ps(ftdata, p0=x[0], p1=x[1]).real.min()
p0=0
p1=0
x0=np.array([p0,p1])
print phsh(x0)
p0=243
x0=np.array([p0,p1])
print phsh(x0)
res=scipy.optimize.minimize(phsh,x0, method='Nelder-Mead',options={'ftol': 1e-8})
print res.x


td=32768
size = int( np.ceil(td/256.)*256 )/2
dic,fiddata = ng.bruker.read('LMO_3BrAP_1/20',shape=(size),cplex=True)
spdata = ng.proc_base.sp(fiddata,off=0.35,end=0.98,pow=2)
zfdata = ng.proc_base.zf(spdata)
csdata=ng.proc_base.cs(zfdata, pts=-70)
ftdata = ng.proc_base.ft(csdata)
psdata = ng.proc_base.ps(ftdata,p0=res.x[0],p1=res.x[1])
didata = ng.proc_base.di(psdata)

##p0min=0
##p0max=720
##
##p0=p0min
##ps0mins=[]
##while p0<p0max:
##    ps0mins.append(ng.proc_base.ps(ftdata, p0=p0,  p1=0).real.min())
##    p0=p0+1
##
##p1min=-5
##p1max=5
##
##p1=p1min
##ps1mins=[]
##while p1<p1max:
##    ps1mins.append(ng.proc_base.ps(ftdata, p0=243,  p1=p1).real.min())
##    p1=p1+1

pylab.plot(didata, 'r-')
##pylab.plot(np.arange(p0min,p0max),ps0mins)
##pylab.plot(np.arange(p1min,p1max),ps1mins)
pylab.show()
