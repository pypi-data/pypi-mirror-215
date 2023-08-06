"""Tests of the geno2phenotb utils package."""

import os
from typing import List

import pytest

import geno2phenotb.utils as utils
from geno2phenotb.installation_test import download_file

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"


@pytest.mark.parametrize(
    "sample_id",
    [
        "invalid1",
        "invalid2",
        "invalid3",
        "invalid4",
        "invalid5",
        "invalid6",
    ],
)
@pytest.mark.xfail(strict=True, raises=RuntimeError)
def test_check_fq_filenames_xfail(sample_id):
    """
    Tests the Runtime Exception thrown by the check_fastq_filenames function.

    Parameters
    ----------
        sample_id: str. Sample ID
    Returns
    ----------
        None.
    """
    dirname = utils.get_static_dir()
    fastq_dir = os.path.join(
        dirname,
        "test_files",
        "naming_scheme",
        "invalid_fastq",
    )

    utils.check_fastq_filenames(fastq_dir, sample_id)


@pytest.mark.parametrize(
    "sample_id",
    [
        "not_a_fq",
        "",
    ],
)
@pytest.mark.xfail(strict=True, raises=FileNotFoundError)
def test_check_fq_empty_xfail(sample_id: str):
    """
    Tests the FileNotFound Exception thrown by the check_fastq_filenames function.

    Parameters
    ----------
        sample_id: str. Sample ID
    Returns
    ----------
        None.
    """
    dirname = utils.get_static_dir()
    fastq_dir = os.path.join(
        dirname,
        "test_files",
        "naming_scheme",
        "empty_dir",
    )

    utils.check_fastq_filenames(fastq_dir, sample_id)


@pytest.mark.parametrize(
    "sample_id, returns",
    [
        ("valid1", ["valid1_X_R1.fastq.gz", "valid1_X_R2.fastq.gz"]),
        ("valid2", ["valid2_LibID_Additional_R1.fastq.gz", "valid2_LibID_Additional_R2.fastq.gz"]),
        ("valid3", ["valid3_X_R1.fq.gz"]),
        ("valid4", ["valid4_X_R2.fq.gz"]),
    ],
)
def test_check_fq_filenames(sample_id: str, returns: List[str]):
    """
    Tests the check_fastq_filenames function.

    Parameters
    ----------
        sample_id: str. Sample ID
        returns: List[str], filesnames to expect as return
    Returns
    ----------
        None.
    """
    dirname = utils.get_static_dir()
    fastq_dir = os.path.join(
        dirname,
        "test_files",
        "naming_scheme",
        "valid_fastq",
    )
    assert returns == sorted(utils.check_fastq_filenames(fastq_dir, sample_id))


@pytest.mark.parametrize(
    "i",
    [
        int(1),
        float(1),
        True,
    ],
)
@pytest.mark.xfail(strict=True, raises=ValueError)
def test_stripper_xfail(i):
    """Tests the exception thrown by the stripper function."""
    utils.stripper(i)


@pytest.mark.parametrize(
    "i, o",
    [
        ("", ""),
        (" ", ""),
        (" test ", "test"),
        ("'test ", "test"),
    ],
)
def test_stripper(i, o):
    """Tests the exception thrown by the stripper function."""
    assert o == utils.stripper(i)


@pytest.mark.xfail(strict=True, raises=AssertionError)
def test_download_xfail():
    """Tests the exception thrown by the download_model function if the hashs do not match up."""
    download_file("https://example.com/index.html", "index.html", "wrong-hash")


def test_download():
    """Tests the exception thrown by the download_model function if the hashs do not match up."""
    download_file(
        "https://example.com/index.html",
        "index.html",
        "ea8fac7c65fb589b0d53560f5251f74f9e9b243478dcb6b3ea79b5e36449c8d9",
    )
