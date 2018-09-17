import pylab
import matplotlib.pyplot as plt
##import nmrglue as ng
##dic,data = ng.pipe.read("test.fid")
##
##print data
##print data[0]
##pylab.plot(data[0])
##pylab.show()

import nmrglue as ng
dic,data = ng.pipe.read("test.fid")
print dic

dim=-1

if dim == -1:
    dim = data.ndim - 1 # last dimention 

fn = "FDF" + str(int(dic["FDDIMORDER"][data.ndim-1-dim]))
size = float(data.shape[dim])

# check for quadrature in indirect dimentions
if (dic[fn+"QUADFLAG"] != 1) and (dim !=data.ndim-1):
    size = size/2.
    cplx = True
else:
    cplx = False

sw = dic[fn+"SW"]
if sw == 0.0:   
    sw = 1.0
obs = dic[fn+"OBS"]
if obs == 0.0:
    obs = 1.0

car = dic[fn+"CAR"]*obs

print sw
print obs
print car

##data=ng.proc_base.ft(data)
##data=ng.proc_base.mir_left(data)
##data=ng.proc_base.neg_left(data)
##data=ng.proc_bl.sol_sine(data)
##uc=ng.pipe.make_uc(dic,data)
##sdata=uc.ppm_scale()
##
###pylab.plot(data[0])
##fig=plt.figure()
##ax=fig.add_subplot(111)
##ax.plot(uc.ppm_scale(),data,'k-')
##
##pylab.show()
