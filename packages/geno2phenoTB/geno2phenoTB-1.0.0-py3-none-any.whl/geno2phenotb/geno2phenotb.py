"""This is the entry point of the geno2phenoTB console script."""

import logging
import sys
import warnings
from os import path

from geno2phenotb import __version__
from geno2phenotb.installation_test import self_test
from geno2phenotb.parse_args import parse_args
from geno2phenotb.predict import predict
from geno2phenotb.preprocess import preprocess

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"

_logger = logging.getLogger(__name__)


def setup_logging(loglevel):
    """Setup basic logging.

    Parameters
    ----------
    loglevel : int
        Minimum loglevel for emitting messages.
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper that allows :func:`process` to be called with string arguments in a CLI fashion.

    Instead of returning the value from :func:`process`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Parameters
    ----------
    args : List[str]
        Command line parameters as list of strings.
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    _logger.debug(f"Starting geno2phenotb {__version__}")
    _logger.info(f"Arguments:\n{args}")

    if args.mode == "test":
        test_samples = ["ERR067579", "ERR553187"]
        warnings.simplefilter("ignore")
        try:
            for sample_id in test_samples:
                # Fast test without MTBseq.
                self_test(sample_id, False)

            # Optional complete test with MTBseq step.
            self_test("ERR551304", args.complete)
        except AssertionError:
            print("---------------------------")
            print(" Installation test failed! ")
            print("---------------------------")
            return

        print("----------------------------------------")
        print(" Installation test passed successfully! ")
        print("----------------------------------------")

        _logger.info("geno2phenotb installation test finished successfully.")
        return

    # Clean up arguments
    fastq_dir = path.abspath(args.fastq_dir)
    output_dir = path.abspath(args.output_dir)

    # Run only preprocess steps
    if args.preprocess:
        _ = preprocess(
            fastq_dir,
            output_dir,
            args.sample_id,
            skip_mtbseq=args.skip_mtbseq,
        )
        _logger.info("geno2phenotb preprocess only finished successfully.")
        return
    else:
        _, _, _ = predict(
            fastq_dir,
            output_dir,
            args.sample_id,
            skip_mtbseq=args.skip_mtbseq,
            drugs=args.drug,
        )
        _logger.info("geno2phenotb finished successfully.")
        return


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`.

    This function is used as entry point to create a console script with setuptools.
    """
    main(sys.argv[1:])
    _logger.info("geno2phenotb finished successfully.")


if __name__ == "__main__":
    run()
