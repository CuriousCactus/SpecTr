##from scipy.optimize import fmin
##from scipy.optimize import fminbound
##from scipy.optimize import minimize
##def rosen(x):  # The Rosenbrock function  
##        return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)  
##
##x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
##
##xopt = fmin(rosen, x0)  
##
## 
##print xopt
##
##f = lambda x: x*x
##x0=3
##x1=-100
##x2=100
##res=minimize(f,x0)
##print res.x
import scipy
from scipy.optimize import minimize, rosen
#scipy.optimize.show_options('minimize', 'Nelder-Mead')
x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
res = minimize(rosen, x0, method='Nelder-Mead',options={'ftol': 1e-8})
print rosen(x0)
print res.fun
