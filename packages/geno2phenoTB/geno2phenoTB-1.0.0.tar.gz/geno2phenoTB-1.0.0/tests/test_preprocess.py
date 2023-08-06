"""Tests of the geno2phenotb preprocess package."""

import os
from tempfile import TemporaryDirectory

import pytest

import geno2phenotb.utils as utils
from geno2phenotb.geno2phenotb import main
from geno2phenotb.preprocess import preprocess

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"


@pytest.mark.parametrize(
    "sample_id, run_main",
    [
        ("ERR067579", True),
        ("ERR067579", False),
        ("ERR551304", True),
        ("ERR551304", False),
        ("ERR553187", True),
        ("ERR553187", False),
    ],
)
def test_preproc(sample_id, run_main):
    """
    Tests the preprocessing steps without MTBSeq.

    Parameters
    ----------
        sample_id: str. Sample-ID of the already preprocessed files.
        run_main: bool. Should the call happen through the main function of geno2pheno.
    Returns
    ----------
        None.
    """
    dirname = utils.get_static_dir()

    # Use precomputed MTBSeq output.
    fastq_dir = os.path.join(
        dirname,
        "test_files",
        f"{sample_id}_pre",
    )

    ground_truth_dir = os.path.join(
        dirname,
        "ground_truth",
        sample_id,
    )

    with TemporaryDirectory(prefix="geno2phenotb_test_") as output_dir:
        if run_main:
            args = [
                "run",
                "-i",
                fastq_dir,
                "-o",
                output_dir,
                "--sample-id",
                sample_id,
                "--preprocess",
                "--skip-mtbseq",
            ]

            main(args)

        else:
            preprocess(
                fastq_dir,
                output_dir,
                sample_id,
                skip_mtbseq=True,
            )
        # Check prediction.
        utils.check_output(output_dir, ground_truth_dir, sample_id, only_preprocess=True)
