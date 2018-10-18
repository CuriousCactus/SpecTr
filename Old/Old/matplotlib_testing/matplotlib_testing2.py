import matplotlib.pyplot as plt

plt.figure(1, figsize=(4,4))
ax = plt.subplot(111)
x=[1,2]
y=[2,2]
ax.plot(x,y,'bo')
##ax.annotate("",
##            xy=(0.2, 0.2), xycoords='data',
##            xytext=(0.8, 0.8), textcoords='data',
##            arrowprops=dict(arrowstyle="->",
##                            connectionstyle="arc3"), 
##            )

ax.annotate('4', xy=(average(x,y), max(x,y)), verticalalignment='bottom',
           horizontalalignment='center', textcoords='offset points', xytext=(0, 10),arrowprops=dict(arrowstyle="-[",connectionstyle="bar",shrinkA=5, shrinkB=5))
plt.show()
