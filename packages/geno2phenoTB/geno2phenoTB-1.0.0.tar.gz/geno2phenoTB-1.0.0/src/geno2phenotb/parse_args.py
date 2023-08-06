"""Creates the argument parser."""

import argparse
import logging

from geno2phenotb import __version__
from geno2phenotb.utils import get_drugs

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"


def parse_args(args):
    """Parse command line parameters.

    Parameters
    ----------
    args : List[str]
        Command line parameters as list of strings (for example  ``["--help"]``).

    Returns
    -------
    :obj:`argparse.Namespace`
        Command line parameters namespace.
    """
    main_parser = argparse.ArgumentParser(
        description="geno2phenoTB is a tool to predict resistance of Mycobacterium tuberculosis against antibiotics using WGS data."  # noqa: E501
    )

    main_parser.add_argument(
        "--version",
        action="version",
        version="geno2phenoTB {ver}".format(ver=__version__),
    )
    main_parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    main_parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    test_run_parser = main_parser.add_subparsers(
        help="Test or run the installation.", dest="mode", required=True
    )

    test_parser = test_run_parser.add_parser(
        "test", help="Test the installation and dependencies. "
    )
    fast_complete = test_parser.add_mutually_exclusive_group(required=True)
    fast_complete.add_argument(
        "-f",
        "--fast",
        dest="fast",
        help="Fast test of installation. This will not test the preprocessing / MTBSeq steps.",
        action="store_true",
    )
    fast_complete.add_argument(
        "-c",
        "--complete",
        dest="complete",
        help="Complete test of installation. "
        "This will download ~ 170mb from the ENA and start a complete run. "
        "Depending on your bandwith / hardware this may take a few (5-30) minutes.",
        action="store_true",
    )

    run_parser = test_run_parser.add_parser("run")

    # Skip MTBseq step
    run_parser.add_argument(
        "--skip-mtbseq",
        dest="skip_mtbseq",
        help="Skip the MTBseq step. Precomputed output must be present in fastq-dir.",
        action="store_true",
    )

    # Regular arguments
    run_parser.add_argument(
        "-p",
        "--preprocess",
        dest="preprocess",
        help="Run only the preprocessing steps.",
        action="store_true",
    )
    run_parser.add_argument(
        "-i",
        "--fastq-dir",
        dest="fastq_dir",
        metavar="DIR",
        required=True,
        help="Path to the directory were the FASTQ files are located.",
    )
    run_parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        metavar="DIR",
        required=True,
        help=("Path to the directory were the final output files shall be stored."),
    )
    run_parser.add_argument(
        "--sample-id",
        dest="sample_id",
        metavar="SampleID",
        required=True,
        help="SampleID (i.e. ERR/SRR run accession).",
    )
    run_parser.add_argument(
        "-d",
        "--drug",
        dest="drug",
        help=(
            "The drug for which resistance should be predicted. "
            "If you want predictions for several drugs, use the argument several times,"
            "i.e., -d AMK -d DCS -d STR. "
            "If the flag is not set, predictions for all drugs will be performed."
        ),
        choices=get_drugs(),
        action="append",
        default=None,
        type=str,
    )

    return main_parser.parse_args(args)
