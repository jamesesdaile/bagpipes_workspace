import numpy as np 
import bagpipes as pipes
import matplotlib.pyplot as plt
import matplotlib as mpl
from astropy.io import fits,ascii
from astropy.convolution import convolve, Gaussian1DKernel

from load_data import load_zfk2_cosmos_data, load_zfk2_cosmos_data_nokbr, load_zfk2_cdfs_data, load_zfk2_cdfs_data_nokbr
from plot_pipes import plot_fit_gal, sed_pofz_plot 
from model_param import std_model_param, cust_model_param

def fit_cat_F2_test(IDS,filt_list,fit_instructions,run):

    fit_cat = pipes.fit_catalogue(IDS, fit_instructions, load_zfk2_cdfs_data, spectrum_exists=False, cat_filt_list=filt_list,run=run)

    fit_cat.fit(verbose=False) 

    fit_cat_nokbr = pipes.fit_catalogue(IDS, fit_instructions, load_zfk2_cdfs_data_nokbr, spectrum_exists=False, cat_filt_list=filt_list[:-2],run=run+'_no_kbr')

    fit_cat_nokbr.fit(verbose=False) 

    print('Done!')

    return fit_cat,fit_cat_nokbr

if __name__ == "__main__":

    IDS = np.genfromtxt('CDFS_z2_cands.cat',dtype=str)

    filt_list = np.loadtxt("filters/zfourge_filters.txt", dtype="str")

    fit_instructions = std_model_param(fit_nebular=True)

    fit_cat,fit_cat_nobkr = fit_cat_F2_test(IDS,filt_list,fit_instructions,'z2_el')
