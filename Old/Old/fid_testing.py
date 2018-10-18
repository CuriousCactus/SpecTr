##print '\xff'.decode('latin-1')
##print ord('\x00')

##def split_len(seq, length):
##    return [seq[i:i+length] for i in range(0, len(seq), length)]
##fid=split_len(open('fid', 'rb').read(200),1)
##print ord(fid[0])

##fid=open('fid', 'rb').read(1000)
##x=0
##print int(fid, 16)
##fidlist=[]
##while x<len(fid):
##    fidlist.append(ord(fid[x]))
##    x=x+1
##print fidlist
##import matplotlib.pyplot as plt
##plt.plot(fidlist)
##plt.ylabel('some numbers')
##plt.show()
#import numpy as np
#f = open("LMO_3BrAP_1/20/fid", "rb")
#np.frombuffer(f.read(),dtype='>i4', count=20)


import nmrglue as ng
import numpy as np
import matplotlib.pyplot as plt
import pylab
td=32768
sw=14.9830424544763
sf01=400.132606921855
bf1=400.13
x = int( np.ceil(td/256.)*256 )/2
#dic,data = ng.pipe.read('test.fid/test.fid')
#print data
#print data.ndim
dic,data = ng.bruker.read('LMO_3BrAP_1/20',shape=(x),cplex=True)
#print data
ftdata=ng.proc_base.ft(data)
#print ftdata
realdata=np.real(data)
#print realdata
realftdata=np.real(ftdata)
#plt.plot(realftdata)
#plt.show()
uc = ng.fileiobase.unit_conversion(size=x, cplx=True, sw=sw, obs=bf1, car=sf01)
z=0
ucdata=[]
while z<len(realftdata):
    ucdata.append(uc.ppm(realftdata[z]))
    print uc.ppm(realftdata[z])
    z=z+1
print ucdata[0:4]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(uc.ppm_scale(),realftdata,'k-')
#plt.show()
#print dic["pprog"]
#print data
#print data.ndim
#dic,data = ng.bruker.read('LMO_3BrAP_1/20')
#dic,data = ng.bruker.read_binary("LMO_3BrAP_1/20/fid")
#pprog=ng.bruker.read_pprog("LMO_3BrAP_1/20/pulseprogram")
#print pprog
