import matplotlib.pyplot as plt
import numpy as np
import bagpipes as pipes
def plot_fit_gal(fit,ax_,lab='',plt_phot=True,scl=1e19,smth_sig=None,noisy_spec=False,plt_kbr='',sed_color='k',zorder=4):
    
    fit.posterior.get_advanced_quantities() #uses bagpipe functions to make the best fit spectrum
    model = fit.posterior.fitted_model.model_galaxy
    redshift = model.model_comp['redshift']

    spec_wavs = np.copy(model.wavelengths) * ( redshift + 1 )
    spec_wavs *= 1e-4 #convert to mu
    wav_mask = (spec_wavs > 0.2) & (spec_wavs < 10)
    spec_full = np.median(fit.posterior.samples["spectrum_full"], axis=0).T * scl
    #spec_full = np.copy(model.spectrum_full)*scl

    if noisy_spec:
        spec_post = np.percentile(fit.posterior.samples["spectrum_full"],(16, 84), axis=0).T * scl
        spec_post = spec_post.astype(float)
    
        #ax_.plot(spec_wavs, spec_post[:, 0], color="gray", zorder=zorder-1)
        #ax_.plot(spec_wavs, spec_post[:, 1], color="gray", zorder=zorder-1)
    
        ax_.fill_between(spec_wavs, spec_post[:, 0], spec_post[:, 1],
                        zorder=zorder-1, color="lightgray", linewidth=0,alpha=0.5)
    
    phot_wv,phot,ephot = np.copy(fit.galaxy.photometry).T
    phot_mask = phot!=0
    phot *= scl; ephot *=scl
    phot_wv *= 1e-4 #convert to mu

    mask = (fit.galaxy.photometry[:, 1] > 0.)
    upper_lims = fit.galaxy.photometry[:, 1] + fit.galaxy.photometry[:, 2]
    ymax = 1.05*np.max(upper_lims[mask])

    eff_wavs = fit.galaxy.filter_set.eff_wavs * 1e-4
    phot_post = np.percentile(fit.posterior.samples["photometry"],
                              (16, 84), axis=0).T

    for j in range(fit.galaxy.photometry.shape[0]):
        if phot[j] != 0.:
            phot_band = fit.posterior.samples["photometry"][:, j]
            mask = (phot_band > phot_post[j, 0]) & (phot_band < phot_post[j, 1]) 
            phot_1sig = phot_band[mask]*scl
            wav_array = np.zeros(phot_1sig.shape[0]) + eff_wavs[j]

            if phot_1sig.min() < ymax*scl:
                ax_.scatter(wav_array, phot_1sig, color="gray",
                           zorder=zorder, alpha=0.05, s=100, rasterized=True)

    if smth_sig:
        spec_full = convolve(spec_full,Gaussian1DKernel(smth_sig))

    p = ax_.plot(spec_wavs[wav_mask], spec_full[wav_mask], c=sed_color, lw=1, label=lab)

def sed_pofz_plot(fit,fit_comp=None,savefig=None):
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(8,4), gridspec_kw={'width_ratios': [3, 1]})
    plot_mod_gal(fit,ax1,lab=fit.galaxy.ID,noisy_spec=True,plt_kbr=True)
    if fit_comp:
        plot_mod_gal(fit_comp,ax1,lab=fit_comp.galaxy.ID,plot_phot=False,sed_color='darkorange')
    ax1.set_xlabel(r'$\lambda$ ($\mu$m)')
    ax1.set_ylabel(r'Relative Flux ($f_{\lambda}$)')
    ax1.set_xscale('log')
    ax1.set_xlim(1.5,5)
    ax1.set_ylim(0.4,1.8)
    ax1.set_xticks([2, 3, 4, 5])
    ax1.get_xaxis().set_minor_formatter(mpl.ticker.NullFormatter())
    ax1.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

    ax2.hist(fit.posterior.samples['redshift'],bins=25,density=True,alpha=0.5,facecolor='gray')
    if fit_comp:
        ax2.hist(fit_comp.posterior.samples['redshift'],bins=25,density=True,alpha=0.3,facecolor='darkorange')
    ax2.set_xlabel('redshift')
    ax2.set_ylabel('PDF')

    if savefig:
        #'mass_cand_kbr-break.png'
        fig.savefig(savefig,dpi=150)
    else:
        fig.show()

def plot_cdfs_z2_el_photz():
    cat_data = ascii.read('zfk2_CDFS_imv0.90_v1.0_opt_ap_0.7arcsec_z2_cands.cat')

    with fits.open(cat_F2) as hdu:
        data_F2 = hdu[1].data
        dz_1_z_F2 = np.array([(data_F2['redshift_50'] - cat_data['z_spec']) / ( 1 + cat_data['z_spec'] )])

    with fits.open(cat_no_F2) as hdu:
        data_no_F2 = hdu[1].data
        dz_1_z_no_F2 = np.array([(data_no_F2['redshift_50'] - cat_data['z_spec']) / ( 1 + cat_data['z_spec'] )])

    deltz_F2 = np.array((z_F2-cat_data['z_spec'])/(1+cat_data['z_spec']))
    deltz_no_F2 = np.array((z_no_F2-cat_data['z_spec'])/(1+cat_data['z_spec']))

    plt.scatter(cat_data['z_spec'], data_F2['redshift_50'],marker='o',c='royalblue', label='with F2')
    plt.scatter(cat_data['z_spec'], data_no_F2['redshift_50'],marker='o',facecolor='none',edgecolor='k', label='no F2')
    plt.quiver(cat_data['z_spec'], data_no_F2['redshift_50'],np.zeros(len(data_no_F2['redshift_50'])),data_F2['redshift_50']-data_no_F2['redshift_50'],scale_units='xy',scale=1,width=0.003,headwidth=5)
    plt.plot(np.arange(1.5,3.5,0.1),np.arange(1.5,3.5,0.1),ls='--',c='k')
    #plt.legend() 
    plt.xlabel(r'$z_{spec}$')
    plt.ylabel(r'$z_{phot}$')
    plt.xlim(1.75,2.9); plt.ylim(1.75,2.9)
    #plt.title('BAGPIPES emission line galaxies with and without F2')
    plt.text(1.8,2.8,f'$\sigma_z$ = {round(np.median(deltz_no_F2),3)}',color='k')
    plt.text(1.8,2.75,f'$\sigma_z$ = {round(np.median(deltz_F2),3)}',color='royalblue')
    #plt.show()
    plt.savefig('cdfs_z2_el_photz_v_specz.png',dpi=200)

