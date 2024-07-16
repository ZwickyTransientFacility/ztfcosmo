
import os
import pandas

def get_ztfcosmodir(directory=None):
    """ simple function to access the directory where the data is """
    if directory is not None:
        return directory
    
    directory = os.getenv("ZTFCOSMODIR", None)
    if directory is None:
        directory = input('Please specify the directory where data are (or where to download them):')
        if os.path.isdir( os.path.dirname( directory ) ):
            raise IOError(f"No such directory: {os.path.dirname( directory )} ")
            
        os.environ['ZTFCOSMODIR'] = directory
    
    return directory

# ============= #
#   Tables      #
# ============= #
def get_data(good_coverage=None, good_lcfit=None, redshift_range=None):
    """ """
    sndata = get_sn_data()
    globalhost = get_globalhost_data()
    localhost = get_localhost_data()

    # merging naming convention
    param_keys = ["mass", "mass_err", "restframe_gz", "restframe_gz_err"]
    globalhost = globalhost.rename({f"{k}":f"global{k}" for k in param_keys}, axis=1)
    localhost = localhost.rename({f"{k}":f"local{k}" for k in param_keys}, axis=1)

    # out dataframe
    joined_df = sndata.join( globalhost.join(localhost) )


    #
    # some additional Selections
    # 
    if good_coverage is not None:
        if good_coverage:
            joined_df = joined_df[joined_df["lccoverage_flag"].astype(bool)]
        else:
            joined_df = joined_df[~joined_df["lccoverage_flag"].astype(bool)]


    if good_lcfit is not None:
        if good_lcfit:
            joined_df = joined_df[joined_df["fitquality_flag"].astype(bool)]
        else: # lcquality_flag
            joined_df = joined_df[~joined_df["fitquality_flag"].astype(bool)]

    if redshift_range is not None:
        joined_df = joined_df[joined_df["redshift"].between(*redshift_range)]

    return joined_df

def get_sn_data():
    """ """
    ztfcosmodir = get_ztfcosmodir()
    fullpath = os.path.join(ztfcosmodir, "snia_data.csv")
    return pandas.read_csv(fullpath, index_col=0)

def get_globalhost_data():
    """ """
    ztfcosmodir = get_ztfcosmodir()
    fullpath = os.path.join(ztfcosmodir, "globalhost_data.csv")
    return pandas.read_csv(fullpath, index_col=0)

def get_localhost_data():
    """ """
    ztfcosmodir = get_ztfcosmodir()
    fullpath = os.path.join(ztfcosmodir, "localhost_data.csv")
    return pandas.read_csv(fullpath, index_col=0)


# ============= #
#   Spectra     #
# ============= #
def get_target_spectra(name):
    """ """
    raise NotImplementedError("get_spectra to be done.")

# ============= #
#  LightCurves  #
# ============= #
def get_target_lightcurve(name, as_data=True):
    """ get the dataframe of a target's lightcurve """
    if as_data:
        ztfcosmodir = get_ztfcosmodir()
        fullpath = os.path.join(ztfcosmodir, "lightcurves", f"{name}_lc.csv")
        return pandas.read_csv(fullpath,  delim_whitespace=True, comment='#')

    from .lightcurve import LightCurve
    return LightCurve.from_name(name)


# ============= #
#   Download    #
# ============= #
def download_release(which="dr2", directory=None):
    """ download the ZTF Cosmo release.

    Parameters
    ----------
    which: str
        release id:
        - dr2
        - dr2.5 [not available yet]
        - dr3 [not available yet]

    directory: path
        which should the data be downloaded.

    Returns
    -------
    None
    """
    if which not in ["dr2"]:#, "dr2.5", "dr3"]:
        raise ValueError(f'Only "dr2" implemented, {which} given')
        
    directory  = get_ztfcosmodir(directory)
    this_directory = os.path.join(directory, which)

    
    
