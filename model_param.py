def std_model_param(fit_eta=False,fit_nebular=True):
    """
    Basic set-up model parameters for BAGPIPES.  Returns dictionary fit
     instructions used when fitting BAGPIPES.
    """
    exp = {}                                  # Tau-model star-formation history component
    exp["age"] = (0.1, 15.)                   # Vary age between 100 Myr and 15 Gyr. In practice 
                                              # the code automatically limits this to the age of
                                              # the Universe at the observed redshift.
    
    exp["tau"] = (0.3, 10.)                   # Vary tau between 300 Myr and 10 Gyr
    exp["massformed"] = (1., 15.)             # vary log_10(M*/M_solar) between 1 and 15
    exp["metallicity"] = (0., 2.5)            # vary Z between 0 and 2.5 Z_oldsolar
    
    nebular = {}                              # Nebular emission component
    nebular["logU"] = -3.                     # log_10(ionization parameter) - can have as free parameter: (-4,-2)
    
    delayed = {}                              # Delayed Tau model t*e^-(t/tau)
    delayed["age"] = (0.1, 15.)               # Time since SF began: Gyr
    delayed["tau"] = (0.3, 10.)               # Timescale of decrease: Gyr
    delayed["massformed"] = (1., 15.)         # vary log_10(M*/M_solar) between 1 and 15
    delayed["metallicity"] = (0., 2.5)        # vary Z between 0 and 2.5 Z_oldsolar
    
    dust = {}                                 # Dust component
    dust["type"] = "Calzetti"                 # Define the shape of the attenuation curve
    dust["Av"] = (0., 3.)                     # Vary Av between 0 and 3 magnitudes
    if fit_eta:
        dust["eta"] = 3.                          # Extra dust for young stars: multiplies Av
    
    fit_instructions = {}                     # The fit instructions dictionary
    fit_instructions["redshift"] = (0., 10.)  # Vary observed redshift from 0 to 10
    fit_instructions["exponential"] = exp
    fit_instructions["dust"] = dust
    if fit_nebular:
        fit_instructions["nebular"] = nebular

    return fit_instructions 


def cust_model_param(age=(0.1, 15.),tau=(0.3, 10.),massform=(1., 15.),nebular_U=(-4,-2),Av=(0.,3.),redshift=(0,10.),Z=(0,2.5),fit_eta=False,fit_nebular=True,sfh='burst'):
    """
    Basic set-up model parameters for BAGPIPES.  Returns dictionary fit
     instructions used when fitting BAGPIPES.
    """
    exp = {}                                  # Tau-model star-formation history component
    exp["age"] = age                          # Vary age between 100 Myr and 15 Gyr. In practice 
                                              # the code automatically limits this to the age of
                                              # the Universe at the observed redshift.
    
    exp["tau"] = tau                          # Vary tau between 300 Myr and 10 Gyr
    exp["massformed"] = massform              # vary log_10(M*/M_solar) between 1 and 15
    exp["metallicity"] = Z                    # vary Z between 0 and 2.5 Z_oldsolar
    
    nebular = {}                              # Nebular emission component
    nebular["logU"] = nebular_U               # log_10(ionization parameter) - can have as free parameter: (-4,-2)
    
    dust = {}                                 # Dust component
    dust["type"] = "Calzetti"                 # Define the shape of the attenuation curve
    dust["Av"] = Av                           # Vary Av between 0 and 3 magnitudes
    if fit_eta:
        dust["eta"] = 3.                          # Extra dust for young stars: multiplies Av
    
    fit_instructions = {}                     # The fit instructions dictionary
    fit_instructions["redshift"] = redshift   # Vary observed redshift from 0 to 10
    fit_instructions[sfh] = exp
    fit_instructions["dust"] = dust
    if fit_nebular:
        fit_instructions["nebular"] = nebular

    return fit_instructions 

