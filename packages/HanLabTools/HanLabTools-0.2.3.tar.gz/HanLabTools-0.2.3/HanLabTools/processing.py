"""
Processing Tools for HanLabTools

Collection of processing tools for DNPLab specific to data from the Han Lab.

Thorsten Maly
Bridge12 Technologies, Inc.
"""

import numpy as _np
import dnplab as _dnp


def sc_integrate(data, regions):
    out = data.copy()

    out = _dnp.integrate(out, dim="f2", regions=regions)
    out = _dnp.update_axis(
        out, dim=0, new_dims="idx", start_stop=(0, len(out.values) - 1)
    )

    return out


def sc_calc_coherence_order(data):
    """Calculate Coherence Order

    The coherence order is calculated from the Fourier Transform of the integrals over the echo echo intensity.

    Args:
        data (DNPData):     DNPData object containing integrals

    Returns:
        data (DNPData):     Calculated coherence order
    """

    out = data.copy()

    out = _dnp.fourier_transform(out, dim="idx")

    start_stop = _np.linspace(-1 * len(out) / 2, len(out) / 2, len(out))
    start_stop = start_stop.astype(int)

    out = _dnp.update_axis(out, dim=0, new_dims="CO", start_stop=start_stop)

    return out
