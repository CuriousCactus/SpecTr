import nmrglue as ng
import numpy as np
import pylab
import scipy
from translators import hformatter

td=32768
size = int( np.ceil(td/256.)*256 )/2

dic,fiddata = ng.bruker.read('LMO_3BrAP_1/20',shape=(size),cplex=True)

#wdata = ng.proc_base.sp(fiddata,off=0.35,end=0.98,pow=2)
wdata = ng.proc_base.gmb(fiddata, a=0, b=0.000001)
zfdata = ng.proc_base.zf(wdata)
csdata=ng.proc_base.cs(zfdata, pts=-70)
ftdata = ng.proc_base.ft(csdata)

phsh = lambda x: -ng.proc_base.ps(ftdata, p0=x[0], p1=x[1]).real.min()
 
p0=0
p1=0
x0=np.array([p0,p1])
res=scipy.optimize.minimize(phsh,x0, method='Nelder-Mead',options={'ftol': 1e-8})

psdata = ng.proc_base.ps(ftdata,p0=res.x[0],p1=res.x[1])
didata = ng.proc_base.di(psdata)
intdata = ng.proc_base.integ(didata)
ppdata = ng.analysis.peakpick.pick(didata,thres=1000000, direction='positive', algorithm='downward', est_params=True)

sigs=np.sort(ppdata[0], axis=0)
intensities=ppdata[2]

a=0
heights=[]
while a<len(sigs):
    heights.append(didata[sigs[a]])
    a=a+1
b=0
segs=[]
sigints=[]
while b<len(sigs):
    segs.append(np.sort(ng.analysis.segmentation.find_downward(didata,sigs[b],thres=100000),axis=0))
    sigints.append(np.sum(np.sort(ng.analysis.segmentation.find_downward(didata,sigs[b],thres=100000),axis=0)))
    b=b+1



##c=0
##while c<len(sigs):
##    print sigs[c], sigints[c]
##    c=c+1


#print dic

##def ppm_limits(self):
##    """
##    Return tuple of left and right edges in ppm
##    """
##    return self.ppm(-0.9972),self.ppm(size-1)
##
##def ppm_scale(self):
##    """
##    Return array of ppm values
##    """
##    x0,x1 = self.ppm_limits()
##    return np.linspace(x0,x1,size)

sw=14.9830424544763
sf01=400.132606921855
bf1=400.13
o1=2606.92185548805
o1p=6.51518720288
x0=o1p+sw/2
x1=o1p-sw/2
print x0,x1, "=x0,x1"
o1p=o1/bf1
size = len(didata)
sw=sw*sf01
obs=bf1
car=sf01
print size, "=size"
delta = -sw/(size*obs) #Hz/(points*MHz) = ppm
print delta, "=delta"
first = car/obs + delta*size/2. # Hz/MHz - ppm*points/2 =ppm
print first, "=first"
#ppm = (pts*delta)+first
uc = ng.fileiobase.unit_conversion(size=size, cplx=False, sw=sw, obs=obs, car=car)
z=0
ucdata=[]
while z<len(didata):
    ucdata.append(uc.ppm(didata[z]))
    #print uc.ppm(didata[z])
    z=z+1
#print ucdata[0:4]


import matplotlib.pyplot as plt

print o1p, "=o1p"
print uc.ppm_scale()
print uc.ppm(0)
print uc.ppm_limits()


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.linspace(x0,x1,size),didata,'k-')
ax.set_xlim(14.5,-1.5)
pylab.show()

##pylab.plot(ucdata, 'r-')
####pylab.plot(sigs, heights, 'bo')
####pylab.plot(intdata/100, 'g-')
####pylab.plot(segs[0], didata[segs[0]], 'y-')
####pylab.plot(segs[1], didata[segs[1]], 'y-')
##pylab.show()
##
##[0,1,1,2,2,3,3,4,4,4,5,5,6,7,8,9]
##[0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 7, 8]

#print hformatter(sigs, sigints)
