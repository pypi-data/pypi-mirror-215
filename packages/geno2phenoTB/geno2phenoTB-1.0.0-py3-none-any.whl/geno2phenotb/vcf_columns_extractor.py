"""Collects all variants appearing in a vcf into a list 'columns' and return it."""


import logging
import os
import re
import warnings
from typing import List, Optional, Set, Tuple

import pandas as pd

import geno2phenotb.utils as utils

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"

_logger = logging.getLogger(__name__)


def vcf_columns_extractor(in_path: str) -> Tuple[Optional[Set[str]], Optional[str]]:
    """Collect all variants from a MTBseq VCF file into a list and return it.

    This function serves to collect all variants from a variant call file
    into a set `columns` and return it.

    Parameters
    ----------
    in_path : str
        Path to the VCF file to extract variants from.

    Returns
    -------
    columns : set
        Set of all variants extracted from the given VCF.
    identifier : str
        Identifier (single ENA run accession number or combination thereof)
        extracted from the VCF file name.
    """
    _logger.debug(f"Extracting VCF columns: {in_path}")

    split = os.path.basename(in_path).split("_")
    identifier_list: List[str] = []
    for x in split:
        if bool(re.match(r"(^ERR[0-9]+)|(^SRR[0-9]+)", x)):
            identifier_list.append(x)
    identifier = "_".join(identifier_list)
    vcf = pd.read_table(
        in_path,
        sep="\t",
        usecols=["#Pos", "Type", "Subst", "Gene"],
        dtype=str,
    )

    # Get regexstring of amino-acids
    amino_ann = utils.get_amino_ann()

    columns: Set[str] = set()
    for i in range(vcf.shape[0]):

        genome_pos = int(vcf.at[i, "#Pos"].strip())
        if not 0 < genome_pos <= 4411532:
            warnings.warn(f"Position {genome_pos} is not in (0,4411532] for {in_path}.")

        allel_type: str = vcf.at[i, "Type"].strip()
        if not bool(re.fullmatch(r"^Ins|Del|SNP$", allel_type)):
            warnings.warn(
                f"""ref_allele is not in [Ins,Del,SNP],
but {allel_type} at position {genome_pos} for {in_path}."""
            )

        ann: str = vcf.at[i, "Subst"].strip()

        gene: str = vcf.at[i, "Gene"].strip()

        if allel_type == "Ins" and not bool(re.fullmatch(amino_ann, ann)):
            if len(ann) > 0:
                pos = int(ann.split("_")[0])
                if not 0 < pos <= 4411532:
                    warnings.warn(f"Position {pos} is not in (0,4411532] for {in_path}.")
                if len(gene) > 0:
                    variant = f"{gene}:{ann}"
                else:
                    variant = "-:" + ann
                columns.update([variant])

        elif allel_type == "Del" and not bool(re.fullmatch(amino_ann, ann)):
            if len(ann) > 0:
                split = ann.split("_")
                if len(split) == 2:
                    if not 0 < int(split[0]) <= 4411532:
                        warnings.warn(f"Position {split[0]} is not in (0,4411532] for {in_path}.")
                elif len(split) == 3:
                    if not 0 < int(split[0]) < int(split[1]) <= 4411532:
                        warnings.warn(
                            f"Unexpected positions in Del annotation {ann} for {in_path}."
                        )
                else:
                    warnings.warn(f"Irregular Del annotation {ann} for {in_path}.")
                if len(gene) > 0:
                    variant = f"{gene}:{ann}"
                else:
                    variant = f"-:{ann}"
                columns.update([variant])

        elif allel_type == "SNP" and not bool(re.fullmatch(amino_ann, ann)):
            if len(ann) > 0:
                if len(gene) > 0:
                    variant = f"{gene}:{ann}"
                else:
                    variant = f"-:{ann}"
                columns.update([variant])
            else:
                warnings.warn(f"Unexpected SNP annotation {ann} for {in_path}.")

        elif allel_type == "SNP" and bool(re.fullmatch(amino_ann, ann)):
            if len(gene) > 0:
                variant = f"{gene}:{ann}"
            else:
                variant = f"-:{ann}"
            columns.update([variant])
        else:
            warnings.warn(
                f"Annotation of type {allel_type} at position {genome_pos} is {ann} for {in_path}."
            )

    if len(columns) > 0:
        return columns, identifier
    else:
        warnings.warn(
            f"""There were no variants found in {in_path}.
{identifier} is excluded from the collection."""
        )
        return None, None
