import matplotlib.pyplot as plt
from process import average, bracket
import types

plt.figure(1, figsize=(6,4))
ax = plt.subplot(111)
x=[1,2,2.5]
y=[2,2,3]
ax.plot(x,y,'b|')

##def bracket(self, x, y, text=''):
##    self.bracket = self.annotate(text, xy=(average([x[0],x[-1]]), max(y)), verticalalignment='bottom',
##           horizontalalignment='center', textcoords='offset points', xytext=(0, 35),
##            arrowprops=dict(arrowstyle="-", shrinkB=18))
##    a=1
##    while a<len(x):
##        self.bracket = self.annotate('', xy=(x[0], max(y)),  xycoords='data',xytext=(x[a], max(y)), textcoords='data',
##               arrowprops=dict(arrowstyle="-",connectionstyle="arc,angleA=90,angleB=90,armA=20,armB=20",shrinkA=5, shrinkB=5))
##        a=a+1

ax.bracket = types.MethodType(bracket, ax)

ax.bracket(x, y, 'this')
ax.set_ylim(0, 10000000)

print len(ax.texts)
del ax.texts[0]
##print ax.lines[0]

plt.show()
