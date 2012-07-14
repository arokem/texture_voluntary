import sys
import os
from matplotlib.mlab import csv2rec
import matplotlib.pyplot as plt
import numpy as np
from psychopy.gui import fileOpenDlg
import analysis_utils as utils
from scipy.optimize import leastsq


def main(file_name=None):
    """ Run the analysis on data in a file"""

    # Define these two within the scope of main:
    def func(pars):
        a,b,c = pars
        return a*(x**2) + b*x + c 

    def errfunc(pars):
        return y-func(pars)

    if file_name is None: 
        #path_to_files = '/Volumes/Plata1/Shared/Ariel/texture_data/'
        file_name =  fileOpenDlg()[0]
    
    p,l,data_rec = utils.get_data(file_name)

    # For backwards compatibility, check if this variable exists: 
    if 'eye_moved' in l: 
        data_rec = data_rec[np.where(data_rec['eye_moved']==0)]

    neutral = data_rec[np.where(data_rec['neutral'])]
    peripheral = data_rec[np.where(data_rec['neutral']==0)]
    cond_str = ['Neutral', 'Cued']
    colors = ['b','r']
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    print("SOA used was: %s msec"%(1000*p[' texture_dur']))
    print("% correct: ")

    for cond_idx,cond_rec in enumerate([neutral,peripheral]):
        correct = cond_rec['correct']
        ecc = cond_rec['target_ecc']

        #Bin the eccentricities: 
        a = np.floor(ecc)
        eccs_used = np.unique(a)

        #Initialize counters: 
        b = np.zeros(len(eccs_used))
        c = np.zeros(len(eccs_used))

        #Loop over the trials and add the correct to one counter and the number of
        #trials to the other: 
        for i in xrange(len(correct)):
                idx = np.where(eccs_used==np.floor(ecc[i]))
                b[idx]+=correct[i]
                c[idx]+=1.0

        p_correct = b/c
        print("%s: %s "%(cond_str[cond_idx], np.mean(p_correct)*100))
        
        for i,p in enumerate(p_correct):
                ax.plot(eccs_used[i],p,'o',color=colors[cond_idx],markersize=c[i])

        x = []
        y = []

        for i,this_ecc in enumerate(eccs_used):
            x = np.hstack([x,c[i]*[this_ecc]])    
            y = np.hstack([y,c[i]*[p_correct[i]]])

        guess = 1,1,1
        fit, mesg = leastsq(errfunc,guess)
        x = np.arange(0,np.max(x),0.01)        
        ax.plot(x,func(fit),'--',color=colors[cond_idx],
                label=cond_str[cond_idx])
        
    ax.legend()
    ax.set_xlim([-1,13])
    ax.set_ylim([0,1.1])
    ax.set_xlabel('Eccentricity (degrees)')
    ax.set_ylabel('Proportion correct responses')

    fig_name = 'figures/' + file_name.split('.')[0].split('/')[-1] + '.png'
    fig.savefig(fig_name)
    os.system('open %s'%fig_name)
    
if __name__=="__main__":
    main()

