from matplotlib.figure import Figure

from SpecTr.testing5 import d

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
a.plot(d()['xp'],d()['didata'])
f.show()
