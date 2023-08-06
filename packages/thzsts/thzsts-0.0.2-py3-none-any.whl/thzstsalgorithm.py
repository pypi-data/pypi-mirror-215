import numpy as np
import scipy.integrate as integrate
from scipy.interpolate import interp1d
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_squared_error

def inversion_algorithm_splits(wf, qe, p_order, splits, train_test_ratio, rand_seed=2237, mse_metrics=False):
    """Main function to perform extraction algorithm using shuffle splits."""

    # Calculate Coefficient (ref. Algorithm paper)
    Bn = calculate_Bn(wf, p_order)   # calculate waveform integral up to order p
    Cn, test_loss_avg, test_loss_std, train_loss_avg, train_loss_std, fit_qe, mse_qe_fit = shuffle_splits_fit(
        qe, p_order, splits, train_test_ratio, rand_seed)
    
    ext_didv = 0
    ext_iv = 0
    # loop to calculate An (polynomial prefactors for the IV and dIdV curves)
    for i in range(len(Cn)):
        # calculate An
        An = Cn[i] / Bn[i]
        # add contributions to recovered didv
        ext_didv += (i+2)*An*qe[0]**(i-1+2)
        ext_iv += An*qe[0]**(i+2)

    # make I(E) and dIdE two column matrices 
    ext_didv = np.vstack((qe[0], ext_didv))
    ext_iv = np.vstack((qe[0], ext_iv))

    # calculate current pulses i(t) and and simulate the qe measurement 
    sim_qe, sim_it = rectify_QE(wf, ext_iv)
    
    # if interpolation range out of range set error to nan
    try:
        mse_qe_sim = mean_squared_error(qe[1], sim_qe[1])
    except:
        mse_qe_sim = np.nan
    
    if mse_metrics is True:
        return (ext_iv, ext_didv, fit_qe, sim_qe, sim_it, test_loss_avg, test_loss_std, 
               train_loss_avg, train_loss_std, mse_qe_fit, mse_qe_sim)
    else:
        return ext_iv, ext_didv, fit_qe, sim_qe, sim_it

def calculate_Bn(wf, p_order):
    """Calculate the B factor that only depend on the waveform."""
    Bn = np.zeros(p_order-1) # leave of constant and linear term
    for i in range(p_order-1):
        Bn[i] = np.real(integrate.simps(y=wf[1]**(i+2),x=wf[0]))        
    return Bn

def shuffle_splits_fit(qe, p_order, splits, train_test_ratio, rand_seed):
    """Perform inversion with shuffle split fit."""
    
    # Make a design matrix with polynomial features
    # start with quadratic term (constant term not included)
    poly = PolynomialFeatures((2, p_order), include_bias=False)   
    DM = poly.fit_transform(np.reshape(qe[0], (qe[0].size, 1)))  # qe needs specific shape
    
    # set up fit model for fit
    lin_mod = linear_model.LinearRegression

    # set up shuffle split sampling with given parameters, if random_state None different every time
    shuffle = ShuffleSplit(splits, test_size=train_test_ratio, random_state=rand_seed)

    # array to hold errors between train and test data sets
    test_losses = np.zeros(splits)
    train_losses = np.zeros(splits)
    # array to hold coefficients for polynomial terms
    coeffs = np.zeros((splits, p_order-1))
    
    idx = 0
    q = qe[1]
    # loop through split sets
    for train, test in shuffle.split(qe.T):
        
        # fit the polynomial model to the training data without an intercept (zero crossing at zero)
        reg = lin_mod(fit_intercept=False).fit(DM[train], q[train])
        # predict the QE curve for the test data with the fit model from the train data
        pred_q_test = reg.predict(DM[test])
        pred_q_train = reg.predict(DM[train])
        
        # calculate the mean squared error loss between the predicte Q from the train data and the actual Q
        test_losses[idx] = mean_squared_error(pred_q_test, q[test])
        train_losses[idx] = mean_squared_error(pred_q_train, q[train])
        # get fit coefficients from linear regression model  
        coeffs[idx, :] = reg.coef_
        idx += 1
        
    # calculate loss outputs
    test_loss_avg = np.mean(test_losses)
    test_loss_std = np.std(test_losses)
    train_loss_avg = np.mean(train_losses)
    train_loss_std = np.std(train_losses)
    
    # calculate the mean value for all coefficients over all splits
    Cn = np.mean(coeffs, axis=0)
    
    # calculate the fitted QE curve
    fit_qe = np.dot(DM, Cn)
    fit_qe = np.vstack((qe[0], fit_qe))
    
    # calculate more error statistics
    mse_qe_fit = mean_squared_error(qe[1], fit_qe[1])
    
    return Cn, test_loss_avg, test_loss_std, train_loss_avg, train_loss_std, fit_qe, mse_qe_fit

def rectify_QE(wf, iv, bias=0):
    """Rectify the waveform on the recovered IV curve to get simulated QE curve."""
    
    # interpolate the extracted IV curve to be able to rectify on arbitrary points
    interp_IV = interp1d(x=iv[0], y=iv[1])

    # set up Vpk array, 1:-1 to avoid interpolation range error 
    Vpks = iv[0] #, 1:-1]
    
    # set up array for rectified QE 
    sim_qe = np.zeros((2, len(Vpks)))
    sim_qe[0] = Vpks
    
    #  set up array for current pulses
    sim_it = np.zeros((len(Vpks), len(wf[0])))

    # loop to rectify waveform for each Vpk
    for i, Vpk in enumerate(Vpks):
        VTHz = Vpk * wf[1] + bias
        
        try:
            ITHz = interp_IV(x=VTHz)
        except:
            ITHz = [np.nan]*len(wf[0])
            
        sim_it[i, :] = ITHz
        sim_qe[1, i] = integrate.simps(y=ITHz, x=wf[0])
        
    return sim_qe, sim_it
