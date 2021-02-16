# Author: Sam Champer

# This python utility file configures (via the command line) and
# runs a slim file, then parses, and prints the result.

from argparse import ArgumentParser
from slimutil import run_slim, configure_slim_command_line
import numpy as np


def parse_slim(slim_string):
    """
    Arguments: 
        1. slim output to parse [string]
    Returns:
        1. Whether the drive suppressed (0 or 1)
        2. Generation suppressed (10,000 or gen_suppressed) - drop is generation 0
    """
    line_split = slim_string.split('\n')

    suppressed = 0
    gen_suppressed = 10000

    for line in line_split:
        if line.startswith("SUPPRESSED::"):
            spaced_line = line.split()
            suppressed = 1
            gen_suppressed = int(spaced_line[1])

    return (suppressed, gen_suppressed)
    

def config_args(drive, args):
    """
    These are the paramters for the drives in this study.
    """
    if not drive:
        return
    if drive in ["zpg", "zpgX", "zpg_alt", "zpgX_alt"]:
        args["HOMING_PHASE_CUT_RATE_F"] = 0.99
        args["HOMING_PHASE_CUT_RATE_M"] = 0.96
        args["GERMLINE_RESISTANCE_CUT_RATE_F"] = 0.01
        args["GERMLINE_RESISTANCE_CUT_RATE_M"] = 0.02
        args["DD_FITNESS_VALUE"] = 1.0
        args["EMBRYO_RESISTANCE_CUT_RATE_F"] = 0.04454
        args["ZPG"] = True
    if drive in ["zpg", "zpgX"]:
        args["EMBRYO_RESISTANCE_CUT_RATE_M"] = 0.69
        args["SOMATIC_FITNESS_MUTLIPLIER_F"] = 0.7
    if drive in ["zpg_alt", "zpgX_alt"]:
        args["EMBRYO_RESISTANCE_CUT_RATE_M"] = 0.0
        args["SOMATIC_FITNESS_MUTLIPLIER_F"] = 0.5
    if drive in ["zpgX", "zpgX_alt"]:
        args["X_SHRED_RATE"] = 0.93
    if drive in ["nanos", "nanos_f_cost", "nanos_fm_cost"]:
        args["HOMING_PHASE_CUT_RATE_F"] = 0.99
        args["HOMING_PHASE_CUT_RATE_M"] = 0.98
        args["GERMLINE_RESISTANCE_CUT_RATE_F"] = 0.01
        args["GERMLINE_RESISTANCE_CUT_RATE_M"] = 0.01
        args["DD_FITNESS_VALUE"] = 1.0
        args["EMBRYO_RESISTANCE_CUT_RATE_F"] = 0.07911
    if drive in ["nanos_f_cost", "nanos_fm_cost"]:
        args["SOMATIC_FITNESS_MUTLIPLIER_F"] = 0.55
    if drive in ["nanos_fm_cost"]:
        args["SOMATIC_FITNESS_MUTLIPLIER_M"] = 0.55

def main():
    """
    1. Configure using argparse.
    2. Generate cl string and run SLiM.
    3. Parse the output of SLiM.
    4. Print the results.
    """
    # Get args from arg parser:
    parser = ArgumentParser()
    parser.add_argument('-src', '--source', default="merged_same_site_spatial.slim", type=str,
                        help="SLiM file to be run.")
    parser.add_argument('-header', '--print_header', action='store_true', default=False,
                        help='If this is set, python prints a header for a csv file.')
    parser.add_argument('-nreps', '--num_repeats', type=int, default=10,
                        help='Results will be averaged from this many simulations. Default 20.')

    # The following argument names exactly match the names of the variable parameters in SLiM.
    parser.add_argument('--GERMLINE_RESISTANCE_CUT_RATE_F', default=0.0, type=float)
    parser.add_argument('--GERMLINE_RESISTANCE_CUT_RATE_M', default=0.0, type=float)
    parser.add_argument('--EMBRYO_RESISTANCE_CUT_RATE_F', default=0.0, type=float)
    parser.add_argument('--EMBRYO_RESISTANCE_CUT_RATE_M', default=0.0, type=float)
    parser.add_argument('--DD_FITNESS_VALUE', default=1.0, type=float)
    parser.add_argument('--SOMATIC_FITNESS_MUTLIPLIER_M', default=1.0, type=float)
    parser.add_argument('--SOMATIC_FITNESS_MUTLIPLIER_F', default=1.0, type=float)
    parser.add_argument('--HOMING_PHASE_CUT_RATE_F', default=1.0, type=float)
    parser.add_argument('--HOMING_PHASE_CUT_RATE_M', default=1.0, type=float)
    parser.add_argument('--X_SHRED_RATE', default=0.0, type=float)
    parser.add_argument('--ZPG', action='store_true', default=False)

    parser.add_argument('-d', '--drive_macro', default="", type=str,
                        help="Choice of [zpg, zpgX, zpg_alt, zpgX_alt, nanos, nanos_f_cost, nanos_fm_cost]")

    args_dict = vars(parser.parse_args())
    sim_reps = args_dict.pop("num_repeats")
    drive_macro = args_dict.pop("drive_macro")
    config_args(drive_macro, args_dict)
    if args_dict.pop("print_header", None):
        # Print the variable names. First bools, then the rest.
        if not drive_macro:
            print(','.join(f"{arg}" for arg in args_dict if type(args_dict[arg]) == bool), end=",")
            print(','.join(f"{arg}" for arg in args_dict if type(args_dict[arg]) != bool and arg != "source"), end=",")
        # Print headers for the data being collected:
        print(f"drive,suppressed,gens_till_suppression")

    # Assemble the command line arguments to use for SLiM:
    clargs = configure_slim_command_line(args_dict)

    # Run the file with the desired arguments.
    for i in range(sim_reps):
        slim_result = run_slim(clargs)
        suppressed, gen_suppressed = parse_slim(slim_result)
        csv_line = "{},{},{}".format(drive_macro,suppressed,gen_suppressed)
        print(csv_line)


if __name__ == "__main__":
    main()
