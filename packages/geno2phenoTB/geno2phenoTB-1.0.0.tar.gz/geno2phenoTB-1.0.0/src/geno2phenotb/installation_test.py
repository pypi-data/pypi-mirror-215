"""Self test of installation and dependencies."""


import logging
import os
from hashlib import sha256
from tempfile import TemporaryDirectory

import requests
from tqdm.auto import tqdm

from geno2phenotb.predict import predict
from geno2phenotb.utils import check_output, get_static_dir

__author__ = "Jules Kreuer, Bernhard Reuter"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"

_logger = logging.getLogger(__name__)


def check_sha256(file_path: str, expected_hash: str) -> bool:
    """
    Checks the sha256 hash of a file and throws does not match.

    Parameters
    ----------
    file_path : str
        The path to the file.
    expected_hash : str
        Expected sha256 hash of the file.

    Returns
    ----------
    matching : bool
        True, if file matches the hash.
    """
    _logger.debug(f"Checking sha2567 hash of {file_path}.")
    file_hash = sha256()
    with open(file_path, "rb") as f:
        # Read by block
        for block in iter(lambda: f.read(4096), b""):
            file_hash.update(block)
    matching = file_hash.hexdigest() == expected_hash

    return matching


def download_file(url: str, file_name: str, expected_hash: str) -> None:
    """
    Downloads a file and save it, if it does not exists.

    Displays a progress bar and throws an exception if the sha256 hash does not match.

    Parameters
    ----------
    file_name : str
        The name of model file.
    expected_hash : str
        The sha256 hash of model.

    Returns
    -------
    None
        Throws an exception if the sha256 hash of the model is not equal to the hash.
    """
    _logger.info(f"Downloading: {file_name}")

    dirname = get_static_dir()

    file_path = os.path.join(
        dirname,
        "test_files",
        "ERR551304",
        file_name,
    )

    if os.path.isfile(file_path):
        if check_sha256(file_path, expected_hash):
            _logger.debug("File already exist and hashes match up.")
            return
        _logger.debug("File already exist but hashes do not match up.")

    r = requests.get(url, stream=True)
    total_size = int(r.headers.get("content-length", 0))
    with open(file_path, "wb") as file, tqdm(
        total=total_size, unit="B", unit_scale=True, unit_divisor=1024
    ) as pbar:
        for data in r.iter_content(1024):
            pbar.update(len(data))
            file.write(data)

    _logger.debug("Download complete.")

    if not check_sha256(file_path, expected_hash):
        raise AssertionError(
            f"File {file_name} was not downloaded properly."
            "Check your network connection and retry the same command to download the files and "
            "restart the test."
        )

    return


def download_test_files() -> None:
    """Download the forward / reverse reads with accession id ERR551304 from the ENA."""

    url_forward_reads = "https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR551/ERR551304/ERR551304_1.fastq.gz"
    url_reverse_reads = "https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR551/ERR551304/ERR551304_2.fastq.gz"

    fn_forward = "ERR551304_X_R1.fastq.gz"
    fn_reverse = "ERR551304_X_R2.fastq.gz"

    sha256_forward = "cd18f464f8bb35135a601eabe85e64b42d71f7d0916f46ee573119ce6ffa3b2b"
    sha256_reverse = "b3d89ecb14804945495e9244bc2eb2a78d6ec2d5cc188bf2696d3242f4535faf"

    print("Downloading / Checking file 1 / 2")
    download_file(url_forward_reads, fn_forward, sha256_forward)
    print("Downloading / Checking file 2 / 2")
    download_file(url_reverse_reads, fn_reverse, sha256_reverse)

    return


def self_test(sample_id: str, complete: bool) -> None:
    """
    Performs a self test by running everything and comparing it to the precomputed ground truth.

    Parameters
    ----------
    sample_id : str
        The sample ID. One of ERR551304, ERR551304, ERR553187.
    complete : bool
        Run the complete test. Only available for ERR551304.

    Returns
    ----------
    None
        Throws an exception if the output differs from the ground truth.
    """
    with TemporaryDirectory(prefix="geno2phenotb_selftest_") as output_dir:
        _logger.info("Starting installation test.")
        _logger.debug(f"Temp dir: {output_dir}")

        dirname = get_static_dir()

        fastq_dir = os.path.join(
            dirname,
            "test_files",
        )

        ground_truth_dir = os.path.join(
            dirname,
            "ground_truth",
            sample_id,
        )

        if complete:
            fastq_dir = os.path.join(fastq_dir, sample_id)
            download_test_files()

            print(f"Checking complete run for {sample_id}.")
            print("This may take a while ...")
            _, _, _ = predict(
                fastq_dir,
                output_dir,
                sample_id,
                skip_mtbseq=False,
            )

        else:
            fastq_dir = os.path.join(fastq_dir, f"{sample_id}_pre")
            print(f"Checking prediction for {sample_id} ...")
            _, _, _ = predict(
                fastq_dir,
                output_dir,
                sample_id,
                skip_mtbseq=True,
            )

        check_output(output_dir, ground_truth_dir, sample_id, only_preprocess=False)

    return
