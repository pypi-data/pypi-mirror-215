import numpy as np
import scipy.integrate as integrate
from scipy.interpolate import interp1d
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_squared_error

def generate_cc_waveforms(wf_stat, wf_probe, cc_delay):
    '''Generate overlapping waveform for stationary and probe pulse with each cc time delay.'''
    # Define min and max of the time delay
    tmin = cc_delay[0]
    tmax= cc_delay[-1]
    
    # Define time axes for data and simulated waveform
    dt = (wf_stat[0,-1]-wf_stat[0,0])/len(wf_stat[0]) # data time step
    delay_step = (tmax-tmin)/len(cc_delay)            # simulation delay-time step
    
    # add zeros of size half the scan range to each side as a fraction of Tpts  
    stat_wave = np.pad(wf_stat[1],[int(abs(tmin/dt)),int(abs(tmax/dt))]) 
    probe_wf = np.pad(wf_probe[1],[int(abs(tmin/dt)),int(abs(tmax/dt))]) 

    # adjustable wave starts rolled forward by haalf the data time range
    adj_wave = np.roll(probe_wf,int(abs(tmin/dt)))

    # loop through simulation cc time delay and append waveforms for each delay step
    waveforms = []
    for n in range(len(cc_delay)):
        # roll adj wave forward by one delay step each loop iteration
        wave = stat_wave + np.roll(adj_wave,-int(n*delay_step/dt))
        # append the waveforms after removing the padding
        waveforms.append(wave[int(abs(tmin/dt)):-int(abs(tmax/dt))])
        
    return waveforms

def rectify_Qt(wf, iv):
    '''Rectify each waveform on extracted Iv curve.'''
    IV_interp = interp1d(iv[0], iv[1])
    try:
        It = IV_interp(wf[1])
    except:
        It = [np.nan]*len(wf[0])
        #print("Out of interpolation range, set to zero.")
    else: 
        It = IV_interp(wf[1])
    qt = integrate.simps(It,x=(wf[0]))
    return qt

def simulate_Thz_CC(wf, efield, ext_iv, probe_size=0.05, t_min=-5, t_max=5, delay_pts=400): # wf two cols norm., efield in %, ext_iv two cols
    '''Simulate the THz-CC waveform measurement using a waveform at a specific E_THz.'''  
    e_max = 100 # probe size refers to e_max, if e_max = 100% and probe_size = 0.05 => probe peak at 5%
    
    # Stationary (big) waveform
    wf_stat = np.vstack((wf[0], wf[1]*efield))
    # Small probe waveform has opposite sign of stationary wf
    wf_probe = np.vstack((wf[0], wf[1]*e_max*probe_size*(-1)*np.sign(efield)))
    
    # set up delay array
    cc_delay = np.linspace(t_min, t_max, delay_pts)
    
    # generate waveforms for each delay
    cc_wfs = generate_cc_waveforms(wf_stat, wf_probe, cc_delay)
    
    # Rectify and calculate waveform
    thz_cc_wf = np.zeros(delay_pts)
    for i in range(len(cc_wfs)):
        # Rectify each waveform on extracted Iv curve 
        thz_cc_wf[i] = rectify_Qt(np.vstack((wf[0], cc_wfs[i])), ext_iv)
        
    # Remove mean offset and normalize
    thz_cc_wf = np.subtract(thz_cc_wf, np.mean(thz_cc_wf)) 
    thz_cc_sim = np.vstack((cc_delay, thz_cc_wf)) 
    
    return thz_cc_sim