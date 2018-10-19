from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from testing5 import d
d = d()

#f = Figure(figsize=(5,4), dpi=100)
f = plt.figure()
a = f.add_subplot(111)
a.plot(d['xp'],d['didata'], 'r-', d['xp'], d['intdata']/100, 'g-', d['sigsp'], d['heights'], 'bo')
plt.xlim(d['xmax'],0)
plt.ylim(d['ymin'])
plt.xlabel(r'$\delta$'+' / ppm')
plt.show()
