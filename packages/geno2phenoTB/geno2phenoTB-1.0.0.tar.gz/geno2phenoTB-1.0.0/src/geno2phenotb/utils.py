"""Small utility functions."""


import logging
import os
from typing import Dict, List, Tuple, Union

from numpy import isnan

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"

_logger = logging.getLogger(__name__)


def check_fastq_filenames(fastq_dir: str, sample_id: str) -> List[str]:
    """
    Checks if the fastq files in a folder are following the MTBSeq naming scheme.::

        [SampleID]_[LibID]_[*]_[Direction].f(ast)q.gz
                            ^- Optional values.
        Direction must be one of R1, R2.

    Parameters
    ----------
    fastq_dir : str
        Path to the directory containing the fastq files.

    Returns
    -------
    None
        Throws an error if the names do not follow the assumed scheme.
    """
    _logger.info("Checking naming scheme of fastq files")

    # Checks if at least one fastq file is present.
    fastq_files = []

    for file_name in os.listdir(fastq_dir):
        if file_name.startswith(sample_id) and (
            file_name.endswith(".fq.gz") or file_name.endswith(".fastq.gz")
        ):
            _logger.debug(f"Checking: {file_name}")

            segment_check = 2 <= file_name.count("_")

            direction = file_name.split("_")[-1].split(".")[0]
            direction_check = direction in ["R1", "R2"]

            if segment_check and direction_check:
                # All checks passed.
                fastq_files.append(file_name)
                continue

            raise RuntimeError(
                f"FASTQ file {file_name} does not follow naming scheme:\n"
                "[SampleID]_[LibID]_[*]_[Direction].f(ast)q.gz"
            )

    # No fastq file in folder.
    if len(fastq_files) == 0:
        raise FileNotFoundError(f"No FASTQ file/s in folder {fastq_dir} starting with {sample_id}.")

    _logger.debug("All fastq files passed the saming scheme test")

    return fastq_files


def stripper(x) -> Union[str, float]:
    """Strips string / float input. Throws error if type does not match."""
    if isinstance(x, str):
        return x.strip().lstrip("'")
    elif isinstance(x, float):
        if isnan(x):
            return x
        else:
            raise ValueError(f"{x} passed to stripper is float but not np.nan.")
    else:
        raise ValueError(f"{x} passed to stripper is neither str nor float.")


def get_drugs() -> List[str]:
    """Returns a list of two / three letter drug codes."""
    return [
        "AMK",
        "CAP",
        "DCS",
        "EMB",
        "ETH",
        "FQ",
        "INH",
        "KAN",
        "PAS",
        "PZA",
        "RIF",
        "STR",
    ]


def get_aminos() -> str:
    """Returns regex of amino-acids."""
    return "(Ala|Arg|Asn|Asp|Cys|Gln|Glu|Gly|His|Ile|Leu|Lys|Met|Phe|Pro|Ser|Thr|Trp|Tyr|Val|_)"


def get_amino_ann() -> str:
    """Returns regex of amino-acid annotations."""
    return "(^Ala|^Arg|^Asn|^Asp|^Cys|^Gln|^Glu|^Gly|^His|^Ile|^Leu|^Lys|^Met|^Phe|^Pro|^Ser|^Thr|^Trp|^Tyr|^Val|^_)[0-9]+(Ala$|Arg$|Asn$|Asp$|Cys$|Gln$|Glu$|Gly$|His$|Ile$|Leu$|Lys$|Met$|Phe$|Pro$|Ser$|Thr$|Trp$|Tyr$|Val$|_$)"  # noqa: E501


def get_key_genes() -> Dict[str, List[str]]:
    """Returns a dict of genes used to determine the genotype of an isolate."""
    aminos = get_aminos()
    return {
        "BDQ": [
            r"^Rv0678:[0-9]+_ins_[ACGT]+$",
            r"^Rv0678:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv0678:" + aminos + "[0-9]+_$",
        ],
        "CAP": [
            r"^Rv1694:[0-9]+_ins_[ACGT]+$",
            r"^Rv1694:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv1694:" + aminos + "[0-9]+_$",
        ],
        "CFZ": [
            r"^Rv0678:[0-9]+_ins_[ACGT]+$",
            r"^Rv0678:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv0678:" + aminos + "[0-9]+_$",
        ],
        "DCS": [
            r"^Rv2780:[0-9]+_ins_[ACGT]+$",
            r"^Rv2780:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv2780:" + aminos + "[0-9]+_$",
        ],
        "DEL": [
            r"^Rv3547:[0-9]+_ins_[ACGT]+$",
            r"^Rv3547:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv3547:" + aminos + "[0-9]+_$",
        ],
        "ETH": [
            r"^Rv3854c:[0-9]+_ins_[ACGT]+$",
            r"^Rv3854c:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv3854c:" + aminos + "[0-9]+_$",
        ],
        "INH": [
            r"^Rv1908c:[0-9]+_ins_[ACGT]+$",
            r"^Rv1908c:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv1908c:" + aminos + "[0-9]+_$",
        ],
        "PZA": [
            r"^Rv2043c:[0-9]+_ins_[ACGT]+$",
            r"^Rv2043c:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv2043c:" + aminos + "[0-9]+_$",
        ],
        "RIF": [
            r"^Rv0667:[0-9]+_ins_[ACGT]+$",
            r"^Rv0667:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv0667:" + aminos + "[0-9]+_$",
        ],
        "STR": [
            r"^Rv3919c:[0-9]+_ins_[ACGT]+$",
            r"^Rv3919c:([0-9]+_){0,1}[0-9]+_del$",
            r"^Rv3919c:" + aminos + "[0-9]+_$",
        ],
    }


def get_lineages() -> List[str]:
    """Returns a list of lineages."""
    return [
        "Lineage 1",
        "Lineage 1.1",
        "Lineage 1.1.1",
        "Lineage 1.1.1.1",
        "Lineage 1.1.2",
        "Lineage 1.1.3",
        "Lineage 1.2.1",
        "Lineage 1.2.2",
        "Lineage 2.1",
        "Lineage 2.2.1",
        "Lineage 2.2.1.1",
        "Lineage 2.2.1.2",
        "Lineage 2.2.2",
        "Lineage 3",
        "Lineage 3.1.1",
        "Lineage 3.1.2",
        "Lineage 3.1.2.1",
        "Lineage 3.1.2.2",
        "Lineage 4",
        "Lineage 4.1",
        "Lineage 4.1.1",
        "Lineage 4.1.1.1",
        "Lineage 4.1.1.2",
        "Lineage 4.1.1.3",
        "Lineage 4.1.2",
        "Lineage 4.1.2.1",
        "Lineage 4.2",
        "Lineage 4.2.1",
        "Lineage 4.2.2",
        "Lineage 4.2.2.1",
        "Lineage 4.3",
        "Lineage 4.3.1",
        "Lineage 4.3.2",
        "Lineage 4.3.2.1",
        "Lineage 4.3.3",
        "Lineage 4.3.4",
        "Lineage 4.3.4.1",
        "Lineage 4.3.4.2",
        "Lineage 4.3.4.2.1",
        "Lineage 4.4",
        "Lineage 4.4.1",
        "Lineage 4.4.1.1",
        "Lineage 4.4.1.2",
        "Lineage 4.4.2",
        "Lineage 4.5",
        "Lineage 4.6",
        "Lineage 4.6.1",
        "Lineage 4.6.1.1",
        "Lineage 4.6.1.2",
        "Lineage 4.6.2",
        "Lineage 4.6.2.1",
        "Lineage 4.6.2.2",
        "Lineage 4.7",
        "Lineage 4.8",
        "Lineage 4.9",
        "Lineage 5",
        "Lineage 6",
        "Lineage 7",
        "Lineage BOV",
    ]


def get_rules(drug: str) -> Tuple[List[int], bool]:
    """
    Returns the rules learned by the Rule-Based Classifier.

    Parameters
    ----------
    drug : str
        Drug for which the rule, obtained from a Rule-Based Classifier, shall be returned.

    Returns
    -------
    rule : list[int]
        List of integer indices to index the features that are resistance-causing.
    geno_only : bool
        If True, the returned rule contains only the index of the FZB genotype feature.
    """
    if drug == "AMK":
        return [807], False
    elif drug == "FQ":
        return [1552], True
    elif drug == "RIF":
        return [
            150,
            1212,
            1326,
            1327,
            1328,
            1330,
            1332,
            1371,
            1372,
            1373,
            1385,
            1386,
            1387,
            1417,
            1419,
            1420,
            1421,
            1422,
            1423,
            1439,
            1455,
            1472,
            1476,
            1505,
            1508,
            1511,
            1512,
            1515,
            1516,
            1539,
            1540,
            1643,
            1663,
            1756,
            2518,
            2651,
            3003,
            3145,
            3150,
            3165,
            3683,
            3702,
            3922,
            4379,
            5055,
            5518,
            5550,
            5955,
            6236,
        ], False
    else:
        raise ValueError(f"Illegal input: {drug} is not modeled by a Rule-Based Classifier.")


def check_output(
    output_dir: str, ground_truth_dir: str, sample_id: str, only_preprocess: bool
) -> bool:
    """
    Checks the resistance prediction, extracted features and feature importance evaluation
    against the ground truth.

    Throws an assertion error if the files do not match up.

    Parameters
    ----------
    output_dir : str
        Output directory of prediction.
    ground_truth_dir : str
        Directory of ground truth files.
    sample_id : str
        ID of sample.
    preprocess : bool
        If True, check only the preprocess output.

    Returns
    -------
    bool, default=True
        Throws an exception if the files do not match.
    """

    # Check the extracted features.
    _logger.debug("Checking: Extracted features")
    true_feat_path = os.path.join(ground_truth_dir, f"{sample_id}_ground_truth_features.tsv")
    out_feat_path = os.path.join(output_dir, f"{sample_id}_extracted_features.tsv")

    with open(true_feat_path) as true_file, open(out_feat_path) as out_file:
        true_features = set(true_file.readlines())
        out_features = set(out_file.readlines())
        assert true_features == out_features

    _logger.debug("Check passed: Extracted features")

    if only_preprocess:
        return True

    # Check feature importance evaluation
    _logger.debug("Checking: Feature evaluation")

    true_eval_path = os.path.join(
        ground_truth_dir, f"{sample_id}_feature_importance_evaluation.tsv"
    )
    out_eval_path = os.path.join(output_dir, f"{sample_id}_feature_importance_evaluation.tsv")

    with open(true_eval_path) as true_file, open(out_eval_path) as out_file:
        true_features = set(true_file.readlines())
        out_features = set(out_file.readlines())
        assert true_features == out_features

    _logger.debug("Check passed: Feature evaluation")

    # Check resistance report predictions drug
    for drug in get_drugs():
        _logger.debug(f"Checking: Resistance report {drug}")
        true_report_path = os.path.join(ground_truth_dir, f"{drug}_resistance_report.txt")
        out_report_path = os.path.join(output_dir, f"{drug}_resistance_report.txt")

        with open(true_report_path) as true_file, open(out_report_path) as out_file:
            true_report = true_file.readlines()
            out_report = out_file.readlines()

            assert true_report == out_report
        _logger.debug(f"Check passed: {drug}")

    return True


def get_static_dir() -> str:
    """Returns the absolute path of the static folder."""
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
