def load_zfk2_cdfs_data(ID):
    """
    Load ZFK2 data for CDFS fields (which uses ZFOURGE catalogue)
    """
    from astropy.io import ascii
    import numpy as np
    from config import parse_config

    cat_dir = parse_config('directories','cat_dir')
    cat_name = parse_config('CDFS','cat_name') 
    cat = ascii.read(cat_dir+cat_name)

    # IDs aren't sequential for these catalogues so get row number corresponding to ID
    idx = np.where(cat['id']==int(ID))[0][0]
    
    # get the flux names from the filter.res.translate file. Ignore second column as it's EAZY stuff.
    translate_data = np.genfromtxt('zfourge_FILTER.RES.translate',dtype=str,usecols=0)
    # Order is flx,eflx.
    flx_name = list(translate_data[::2])
    err_name = list(translate_data[1::2])
    
    #Don't fit f_Ksall which is total flux Ks band but sometimes different to f_Ks which should be correct to total
    #flx_name = list(np.array(flx_name)[[flx_ != 'f_Ksall' for flx_ in flx_name]])
    #err_name = list(np.array(err_name)[[err_ != 'e_Ksall' for err_ in err_name]])

    fluxes = list(cat[idx][flx_name]); fluxerrs = list(cat[idx][err_name])

    # Turn these into a 2D array.
    photometry = np.c_[fluxes, fluxerrs]

    photometry = bagpipe_recommended_pre_proc(photometry,flx_name)
 
    #Finally convert into microjanskies
    photometry *= 0.3631

    return photometry

def load_zfk2_cdfs_data_nokbr(ID):
    """
    Load ZFK2 data for CDFS fields (which uses ZFOURGE catalogue)
    """
    from astropy.io import ascii
    import numpy as np
    from config import parse_config

    cat_dir = parse_config('directories','cat_dir')
    cat_name = parse_config('CDFS','cat_name') 
    cat = ascii.read(cat_dir+cat_name)

    # IDs aren't sequential for these catalogues so get row number corresponding to ID
    idx = np.where(cat['id']==int(ID))[0][0]
    
    # get the flux names from the filter.res.translate file. Ignore second column as it's EAZY stuff.
    translate_data = np.genfromtxt('zfourge_FILTER.RES.translate',dtype=str,usecols=0)
    translate_data = translate_data[:-4]
    # Order is flx,eflx.
    flx_name = list(translate_data[::2])
    err_name = list(translate_data[1::2])
    
    #Don't fit f_Ksall which is total flux Ks band but sometimes different to f_Ks which should be correct to total
    #flx_name = list(np.array(flx_name)[[flx_ != 'f_Ksall' for flx_ in flx_name]])
    #err_name = list(np.array(err_name)[[err_ != 'e_Ksall' for err_ in err_name]])

    fluxes = list(cat[idx][flx_name]); fluxerrs = list(cat[idx][err_name])

    # Turn these into a 2D array.
    photometry = np.c_[fluxes, fluxerrs]

    photometry = bagpipe_recommended_pre_proc(photometry,flx_name)
 
    #Finally convert into microjanskies
    photometry *= 0.3631

    return photometry


def load_zfk2_cosmos_data(ID):
    """
    Load ZFK2 data for COSMOS fields (which uses UVISTA catalogue)
    """
    from astropy.io import ascii
    import numpy as np
    from config import parse_config

    cat_dir = parse_config('directories','cat_dir')
    cat_name = parse_config('COSMOS_352','cat_name') 
    cat = ascii.read(cat_dir+cat_name)

    # IDs aren't sequential for these catalogues so get row number corresponding to ID
    idx = np.where(cat['id']==int(ID))[0][0]
    
    # get the flux names from the filter.res.translate file. Ignore second column as it's EAZY stuff.
    translate_data = np.genfromtxt('uvista_FILTER.RES.translate',dtype=str,usecols=0)
    # Skip first row as it's total flux. Order is flx,eflx.
    flx_name = list(translate_data[1:][::2])
    err_name = list(translate_data[1:][1::2])

    # UVISTA catalogue has fixed aperture fluxes so need to correct to total
    ap_cor = cat[idx]['Ks_tot']/cat[idx]['Ks']
    for band in flx_name:
        cat[idx][band] *= ap_cor
    for band in err_name:
        cat[idx][band] *= ap_cor

    fluxes = list(cat[idx][flx_name]); fluxerrs = list(cat[idx][err_name])

    # Turn these into a 2D array.
    photometry = np.c_[fluxes, fluxerrs]

    photometry = bagpipe_recommended_pre_proc(photometry,flx_name)
 
    #Finally convert into microjanskies
    photometry *= 0.3631

    return photometry

def load_zfk2_cosmos_data_nokbr(ID):
    """
    Load ZFK2 data for COSMOS fields (which uses UVISTA catalogue)
    """
    from astropy.io import ascii
    import numpy as np
    from config import parse_config

    cat_dir = parse_config('directories','cat_dir')
    cat_name = parse_config('COSMOS_352','cat_name') 
    cat = ascii.read(cat_dir+cat_name)

    # IDs aren't sequential for these catalogues so get row number corresponding to ID
    idx = np.where(cat['id']==int(ID))[0][0]
    
    # get the flux names from the filter.res.translate file. Ignore second column as it's EAZY stuff.
    translate_data = np.genfromtxt('uvista_FILTER.RES.translate',dtype=str,usecols=0)
    translate_data = translate_data[:-4]
    # Skip first row as it's total flux. Order is flx,eflx.
    flx_name = list(translate_data[1:][::2])
    err_name = list(translate_data[1:][1::2])

    # UVISTA catalogue has fixed aperture fluxes so need to correct to total
    ap_cor = cat[idx]['Ks_tot']/cat[idx]['Ks']
    for band in flx_name:
        cat[idx][band] *= ap_cor
    for band in err_name:
        cat[idx][band] *= ap_cor

    fluxes = list(cat[idx][flx_name]); fluxerrs = list(cat[idx][err_name])

    # Turn these into a 2D array.
    photometry = np.c_[fluxes, fluxerrs]

    photometry = bagpipe_recommended_pre_proc(photometry,flx_name)
 
    #Finally convert into microjanskies
    photometry *= 0.3631

    return photometry

def bagpipe_recommended_pre_proc(photometry,flx_name):

    # blow up the errors associated with any missing fluxes.
    for i in range(len(photometry)):
        if (photometry[i, 0] == 0.) or (photometry[i, 1] <= 0):
            photometry[i,:] = [0., 9.9*10**99.]

    # Enforce a maximum SNR of 20, or 10 in the IRAC channels.
    irac_mask = ['ch' in flx_ or 'IRAC' in flx_ for flx_ in flx_name]
    for i in range(len(photometry)):

        if irac_mask[i]:
            max_snr = 10.

        else:
            max_snr = 20.

        if photometry[i, 0]/photometry[i, 1] > max_snr:
            photometry[i, 1] = photometry[i, 0]/max_snr

    return photometry

