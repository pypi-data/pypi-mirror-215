import sys
from .fermion_symmetry import U11, U1, Z4, Z2, Z22

this = sys.modules[__name__]
this.SVD_SCREENING = 1e-28
this.DEFAULT_SYMMETRY = U11
this.DEFAULT_FLAT = True
this.DEFAULT_AD = False
this.DEFAULT_FERMION = True
this.DEFAULT_LARGE = False
this.DEFAULT_CUPY = False

symmetry_map = {"U11": U11,
                "U1": U1,
                "Z2": Z2,
                "Z4": Z4,
                "Z22": Z22}

def set_symmetry(symmetry):
    if isinstance(symmetry, str):
        symmetry = symmetry.upper()
        if symmetry not in symmetry_map:
            raise KeyError("input symmetry %s not supported" % symmetry)
        this.DEFAULT_SYMMETRY = symmetry_map[symmetry]
    else:
        this.DEFAULT_SYMMETRY = symmetry

def set_flat(flat):
    this.DEFAULT_FLAT = flat

def set_fermion(fermion):
    this.DEFAULT_FERMION = fermion

def set_large(large):
    this.DEFAULT_LARGE = large

def set_ad(ad):
    this.DEFAULT_AD = ad

def set_cupy(cupy):
    this.DEFAULT_CUPY = cupy

def set_options(**kwargs):
    symmetry = kwargs.pop("symmetry", None)
    fermion = kwargs.pop("fermion", None)
    flat = kwargs.pop("flat", None)
    ad = kwargs.pop("ad", None)
    large = kwargs.pop("large", None)
    cupy = kwargs.pop("cupy", None)
    assert len(kwargs) == 0
    if symmetry is not None:
        set_symmetry(symmetry)
    if fermion is not None:
        set_fermion(fermion)
    if flat is not None:
        set_flat(flat)
    if ad is not None:
        set_ad(ad)
    if large is not None:
        set_large(large)
    if cupy is not None:
        set_cupy(cupy)

def dispatch_settings(**kwargs):
    keys = list(kwargs.keys())
    for ikey in keys:
        if kwargs.get(ikey) is None:
            kwargs[ikey] = getattr(this, "DEFAULT_" + ikey.upper())
    _settings = [kwargs.pop(ikey) for ikey in keys]
    if len(_settings) == 1:
        _settings = _settings[0]
    return _settings
