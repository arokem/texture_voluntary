import numpy as np
from matplotlib.mlab import csv2rec
from scipy.optimize import leastsq

def get_data(file_name):
    file_read = file(file_name,'r')
    l = file_read.readline()
    p = {} #This will hold the params
    l = file_read.readline()
    data_rec = []
    
    if l=='':
        return p,l,data_rec

    while l[0]=='#':
        try:
            p[l[1:l.find(':')-1]]=float(l[l.find(':')+1:l.find('\n')]) 
        except:
            p[l[2:l.find(':')-1]]=l[l.find(':')+1:l.find('\n')]
        l = file_read.readline()

    try:
        data_rec = csv2rec(file_name)
    except ValueError:
        p = []
    
    return p,l,data_rec
   
def analyze(odd_ecc,correct):
    def func(pars):
        a,b,c = pars
        return a*(x**2) + b*x + c 

    def errfunc(pars):
        return y-func(pars)
       #Analysis:
    #Bin the eccentricities: 
        a = np.floor(odd_ecc)
        eccs_used = np.unique(a)
    #Initialize counters: 
        b = np.zeros(len(eccs_used))
        c = np.zeros(len(eccs_used))

    #Loop over the trials and add the correct to one counter and the number of
    #trials to the other: 
        for i in xrange(len(correct)):
            idx = np.where(eccs_used==np.floor(odd_ecc[i]))
            b[idx]+=correct[i]
            c[idx]+=1

        p_correct = b/c

        for i,p in enumerate(p_correct):
            plt.plot(eccs_used[i],p,'o',color='b',markersize=c[i])

    x = []
    y = []

    for i,this_ecc in enumerate(eccs_used):
        x = np.hstack([x,c[i]*[this_ecc]])    
        y = np.hstack([y,c[i]*[p_correct[i]]])
