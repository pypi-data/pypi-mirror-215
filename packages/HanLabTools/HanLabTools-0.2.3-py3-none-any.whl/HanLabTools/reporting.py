"""
Reporting Tools for HanLabTools

Collection of reporting tools for DNPLab specific to data from the Han Lab.

Thorsten Maly
Bridge12 Technologies, Inc.
"""

import numpy as _np
import dnplab as _dnp
from .config.config import HanLab_CONFIG


def sc_plot_integrals(data, verbose=False):
    _dnp.plot(data, "o-")

    _dnp.plt.grid(True)
    _dnp.plt.xlabel("")
    _dnp.plt.ylabel("Integrated NMR Intensity (a.u.)")
    _dnp.plt.title("Integrals")


def sc_plot_summary(fid, data, integrals, coherence_order, regions=None):
    """Plot Spin Counting Summary

    Streamlined function to plot the results of the spin counting exeperiment

    Args:
        fid (DNPData):              DNPData object containing the FID
        data (DNPData):             DNPData object containing the NMR spectra
        integrals (DNPData):        DNPData object containing the calculated integrals
        coherence_order (DNPData):  DNPData object containing the calculated coherence order
        regions (tuple,list):       Integration region. This input argument is optional

    """
    xaxis_scaling_factor = HanLab_CONFIG["SC_Plot_Parameters"].get(
        "xaxis_scaling_factor"
    )
    bar_width = float(HanLab_CONFIG["SC_Plot_Parameters"].get("bar_width"))

    _dnp.plt.figure()

    # Plot FID
    _dnp.plt.subplot(2, 2, 1)
    _dnp.plot(fid)

    _dnp.plt.grid(True)
    _dnp.plt.title("FID")
    _dnp.plt.xlabel("time (s)")
    _dnp.plt.ylabel("Signal Intensity (a.u.)")

    # Plot NMR Spectra
    _dnp.plt.subplot(2, 2, 2)
    _dnp.plot(data)

    if regions != None:
        integral_regions_array = _np.array(regions)
        integral_regions_max = integral_regions_array[:, 1]
        integral_regions_min = integral_regions_array[:, 0]

        _dnp.plt.vlines(
            x=integral_regions_max,
            ymin=_np.min(data.values),
            ymax=_np.max(data.values),
            linestyles="dashdot",
            colors=_dnp.DNPLAB_CONFIG["COLORS"]["light_grey"],
        )
        _dnp.plt.vlines(
            x=integral_regions_min,
            ymin=_np.min(data.values),
            ymax=_np.max(data.values),
            linestyles="dashdot",
            colors=_dnp.DNPLAB_CONFIG["COLORS"]["light_grey"],
        )

        _dnp.plt.xlim(
            (
                xaxis_scaling_factor * _np.max(regions),
                xaxis_scaling_factor * _np.min(regions),
            )
        )

    _dnp.plt.grid(True)
    _dnp.plt.title("NMR Spectra")
    _dnp.plt.xlabel("Chemical Shift $\delta$ (ppm)")
    _dnp.plt.ylabel("Signal Intensity (a.u.)")

    # Plot Integrals
    _dnp.plt.subplot(2, 2, 3)
    _dnp.plot(integrals, ".-")
    _dnp.plt.grid(True)
    _dnp.plt.title("Integrals")
    _dnp.plt.xlabel("Slice")
    _dnp.plt.ylabel("Intensity (a.u.)")

    # Plot Coherence order

    _dnp.plt.subplot(2, 2, 4)

    x_axis = coherence_order.coords[0][:]
    bar_values = _np.squeeze(_np.real(coherence_order.values))

    if len(coherence_order.coords["integrals"]) == 1:
        bar_width = 1
        _dnp.plt.bar(x=x_axis, height=_np.squeeze(bar_values), width=bar_width)

    else:
        for index in coherence_order.coords["integrals"]:
            bar_height = _np.squeeze(bar_values[:, index])
            _dnp.plt.bar(
                x=x_axis + index * bar_width, height=bar_height, width=bar_width
            )

    _dnp.plt.xlim((0, len(coherence_order) / 2))
    _dnp.plt.grid(True)
    _dnp.plt.title("Coherence Order")
    _dnp.plt.xlabel("Coherence Order")
    _dnp.plt.ylabel("Intensity (a.u.)")

    _dnp.plt.tight_layout()
    _dnp.plt.show()
