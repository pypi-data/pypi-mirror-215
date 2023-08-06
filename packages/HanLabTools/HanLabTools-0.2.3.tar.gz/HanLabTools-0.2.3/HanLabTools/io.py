"""
Import Tools for DNPLab

Collection of import tools for DNPLab specific to data from the Han Lab.

Thorsten Maly
Bridge12 Technologies, Inc.
"""

import numpy as _np
import dnplab as _dnp
from .config.config import HanLab_CONFIG


def import_data(path, experiment_type, start_stop=None, spacing="lin", verbose=False):
    """
    Import Han Lab specific experiments

    Args:
        path (str, list):                   Path to data directory or list of directories
        experimnet=nt_type (str)            Experiment type (see list below)
        start_stop (tuple or vector):       Coords for new dimension
        spacing (str):                      "lin" for linear spaced axis or "log" for logarithmically spaced axis
        verbose (boolean):                  For debugging, get more specific information what the module is doing

    Returns:
        data (DNPData):                     Data object

    Currently implemented experiment types:

        **DNPProfile_F:**                   DNP enhancement versus microwave frequency. Data is recorded in TopSpin. Experiment is controlled through SpecMan
        **DNPEnhancementBuildUp:**          DNP enhancement (NMR) versus contact time t<sub>c</sub>. Data is recorded using TopSpin.
        **ELDOR:**                          EPR pump probe experiment. The data is recorded using SpecMan.
        **DNPPowerBuildUp:**                DNP enhancement at a fixed microwave frequency versus microwave power. Data is recorded in TopSpin. The experiment is controlled through SpecMan.
        **EPRT1e:**                         EPR inversion-recovery experiments. Data is recorded in SpecMan.
        **EPRT2e:**                         EPR two-pulse echo decay. Data is recorded in SpecMan.

    """

    if experiment_type in dict.keys(HanLab_CONFIG):
        if verbose == True:
            print("Key exists")
            print(HanLab_CONFIG[experiment_type])

        # Create sub-dictionary for experiment configuration
        temp_keys = dict.keys(HanLab_CONFIG[experiment_type])

        if verbose == True:
            print("temp_keys:", temp_keys)

        # Load data
        if "data_format" in temp_keys:
            data_format = HanLab_CONFIG[experiment_type].get("data_format")
        else:
            data_format = None

        if verbose == True:
            print("data_format:", data_format)

        data = _dnp.load(path, data_format=data_format)

        if verbose == True:
            print("Done! Data loaded")

        # Assign axis. Could probably be more elegant, but this will do for now
        if "dim0" in temp_keys:
            temp = HanLab_CONFIG[experiment_type].get("dim0")
            data.rename("x0", temp)
            data.coords[temp] = data.coords[temp] * 1e-9

        if "dim1" in temp_keys:
            temp = HanLab_CONFIG[experiment_type].get("dim1")
            data = _dnp.update_axis(
                data, dim=1, new_dims=temp, start_stop=start_stop, spacing=spacing
            )

        # if "dim2" in tempKeys:
        #     # Not yet implemented

        # if "dim3" in tempKeys:
        #     # Not yet implemented

        if HanLab_CONFIG[experiment_type].get("data_format") == "specman":
            if verbose == True:
                print("Data format is SpecMan")

            if HanLab_CONFIG[experiment_type].get("make_complex") == "true":
                if verbose == True:
                    print("Create complex array from dimensions [...,0] and [...,1]")
                data = _dnp.create_complex(
                    data, data.values[..., 0], data.values[..., 1]
                )

    else:
        print("Experiment not defined in configuration file. Can't import data.")
        return

    return data
