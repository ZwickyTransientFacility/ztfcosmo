# ztfcosmo
ZTF Cosmo Data Release repository

Download and visualize ZTF SN Ia DR2 ([Rigault et al. 2025](https://ui.adsabs.harvard.edu/abs/2024arXiv240904346R/abstract)). See  also the dedicated [ZTF SN Ia DR2 frontend](http://ztfcosmo.in2p3.fr/).

***
# Setup

## installation
```bash
pip install ztfcosmo
```

## data
Download [these data](http://ztfcosmo.in2p3.fr/download) and uncompress it.

Create the environmnent variable `$ZTFCOSMODIR` pointing to the `ztfsniadr2` directory you just created (e.g., `'~/data/ztf/ztfsniadr2'`)


***
# Basic usage

## access data tables

```python
import ztfcosmo
data = ztfcosmo.get_data() # see options
```

## Plot a lightcurve
```python
lc = ztfcosmo.get_target_lightcurve("ZTF18aaqfziz", as_data=False) # see options
fig = lc.show()
```
![](docs/figures/ZTF18aaqfziz_lcfit.png)

## Plot a spectrum
Remark that a target may have several spectra, if so spec is a `list`.
```python
spec = ztfcosmo.get_target_spectra("ZTF18aaqfziz", as_data=False) 
fig = spec.show()
```
![](docs/figures/ZTF18aaqfziz_spectrum.png)

***
# Citing

If you have been using ztfcosmo for your research, please cite [Rigault et al. 2025](https://ui.adsabs.harvard.edu/abs/2024arXiv240904346R/abstract).
