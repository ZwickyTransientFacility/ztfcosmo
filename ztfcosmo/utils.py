import numpy as np

def nmad(*args, **kwargs):
    """ stats.median_abs_deviation forcing scale='normal' """
    from scipy import stats
    return stats.median_abs_deviation(*args, scale="normal", **kwargs)


def mag_to_flux(mag, magerr=None, units="zp", zp=25.0, wavelength=None):
    """converts magnitude into flux
    Parameters
    ----------
    mag: [float or array]
        AB magnitude(s)
    magerr: [float or array] -optional-
        magnitude error if any
    units: [string] -optional-
        Unit system in which to return the flux:
        - 'zp':   units base on zero point as required for sncosmo fits
        - 'phys': physical units [erg/s/cm^2/A)
    zp: [float or array] -optional-
        zero point of for flux; required if units == 'zp'
    wavelength: [float or array] -optional-
        central wavelength of the photometric filter.
        In Angstrom; required if units == 'phys'
    Returns
    -------
    - float or array (if magerr is None)
    - float or array, float or array (if magerr provided)
    """
    if units not in ["zp", "phys"]:
        raise ValueError("units must be 'zp' or 'phys'")
    elif units == "zp":
        if zp is None:
            raise ValueError("zp must be float or array if units == 'zp'")
        flux = 10 ** (-(mag - zp) / 2.5)
    else:
        if wavelength is None:
            raise ValueError("wavelength must be float or array if units == 'phys'")
        flux = 10 ** (-(mag + 2.406) / 2.5) / wavelength ** 2

    if magerr is None:
        return flux

    dflux = np.abs(flux * (-magerr / 2.5 * np.log(10)))  # df/f = dcount/count
    return flux, dflux


def flux_to_mag(flux, dflux, wavelength=None, zp=None, inhz=False):
    """ Converts fluxes (erg/s/cm2/A) into AB or zp magnitudes


    Parameters
    ----------
    flux, fluxerr: [float or array]
        flux and its error 

    wavelength: [float or array] -optional-
        = Ignored if inhz=True =
        central wavelength [in AA] of the photometric filter.


    zp: [float or array] -optional-
        = Ignored if inhz=True =
        = Ignored if wavelength is provided =
        zero point of for flux;

    inhz:
        set to true if the flux (and flux) are given in erg/s/cm2/Hz
        (False means in erg/s/cm2/AA)
        
    Returns
    -------
    - float or array (if magerr is None)
    - float or array, float or array (if magerr provided)
    
    """
    if inhz:
        zp = -48.598 # instaad of -48.60 such that hz to aa is correct
        wavelength = 1
    else:
        if zp is None and wavelength is None:
            raise ValueError("zp or wavelength must be provided")
        if zp is None:
            zp = -2.406 
        else:
            wavelength=1
            
    mag_ab = -2.5*np.log10(flux*wavelength**2) + zp
    if dflux is None:
        return mag_ab, None
    
    dmag_ab = +2.5/np.log(10) * dflux / flux
    return mag_ab, dmag_ab
