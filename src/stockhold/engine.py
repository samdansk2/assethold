# Standard library imports
import os
import sys

# Third party imports
from assetutilities.common.ApplicationManager import ConfigureApplicationInputs
from assetutilities.common.update_deep import AttributeDict
from assetutilities.common.yml_utilities import ymlInput
from stockhold.custom.stocks import Stocks
stks = Stocks()

library_name = "stockhold"

def engine(inputfile=None):
    inputfile = validate_arguments_run_methods(inputfile)

    cfg = ymlInput(inputfile, updateYml=None)
    cfg = AttributeDict(cfg)
    if cfg is None:
        raise ValueError("cfg is None")

    basename = cfg["basename"]
    application_manager = ConfigureApplicationInputs(basename)
    application_manager.configure(cfg, library_name)
    cfg_base = application_manager.cfg

    if "file_management" in cfg_base and cfg["file_management"]["flag"]:
        cfg_base = ou.file_management(cfg_base)

    #TODO
    if basename in "stock":
        cfg = stks.router(cfg)
        cfg_base = stks.router(cfg_base)   
    else:
       raise (Exception(f"Analysis for basename: {basename} not found. ... FAIL"))

    # Third party imports
    from assetutilities.common.utilities import save_application_cfg
    
    # save_application_cfg(cfg_base=cfg_base)

    # return cfg_base


def validate_arguments_run_methods(inputfile):
    """
    Validate inputs for following run methods:
    - module (i.e. python -m digitalmodel input.yml)
    - from python file (i.e. )
    """

    if len(sys.argv) > 1 and inputfile is not None:
        raise (
            Exception(
                "2 Input files provided via arguments & function. Please provide only 1 file ... FAIL"
            )
        )

    if len(sys.argv) > 1:
        if not os.path.isfile(sys.argv[1]):
            raise (FileNotFoundError(f"Input file {sys.argv[1]} not found ... FAIL"))
        else:
            inputfile = sys.argv[1]

    if len(sys.argv) <= 1:
        if not os.path.isfile(inputfile):
            raise (FileNotFoundError(f"Input file {inputfile} not found ... FAIL"))
        else:
            sys.argv.append(inputfile)

    return inputfile
