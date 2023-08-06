"""Collects variants relevant to the resistance genotype appearing in a vcf."""


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


def vcf_columns_extractor_geno(
    in_path: str, resistance_variants_set: Set[str]
) -> Tuple[Optional[Set[str]], str]:
    r"""
    Collect known resistance variants from a VCF file into a list and return it.

    This function serves to collect known resistance variants,
    which are relevant to determine the resistance genotype,
    from a variant call file into a list `columns` and return it.
    The variants are collected from the VCF based on a set `resistance_variants_set`
    of known resistance variants. Additionally all InDels and early stop condons
    (e.g. :spelling:ignore:`A123_`) in the following genes (not mentioned in the catalog)
    are extracted as well, since they result in a resistant genotype:
    ethA=Rv3854c (ETH), pncA=Rv2043c (PZA), gidB/gid=Rv3919c (STR), rpoB=Rv0667 (RIF),
    Rv0678 (BDQ/CFZ), ald=Rv2780 (DCS), katG=Rv1908c (INH), ddn=Rv3547 (DLM), tlyA=Rv1694 (CAP).

    Parameters
    ----------
    in_path : str
        Path to the  VCF file to extract variants from.
    resistance_variants_set : set
        Set of all known resistance variants.

    Returns
    -------
    columns : set or None
        Set of all variants extracted from the given VCF.
        If no resistance variants were found `columns` will be `None`.
    identifier : str
        Identifier (single ENA run accession number or combination thereof)
        extracted from the VCF file name.
    """
    _logger.debug(f"Extracting VCF geno columns: {in_path}")

    # Get regexstring of amino acids
    aminos = utils.get_aminos()

    # All InDels and early stop condons (e.g. Ala123) in the following genes (not mentioned in the
    # catalog) result in a genotype=R (additionally to the known resistance variants from the
    # Masterlist) and are thus extracted as well:
    # ethA=Rv3854c (ETH), pncA=Rv2043c (PZA), gidB/gid=Rv3919c (STR), rpoB=Rv0667 (RIF),
    # Rv0678 (BDQ/CFZ), ald=Rv2780 (DCS), katG=Rv1908c (INH), ddn=Rv3547 (DLM), tlyA=Rv1694 (CAP)
    key_genes = re.compile(
        r"(^Rv3854c:[0-9]+_ins_[ACGT]+$)|(^Rv3854c:([0-9]+_){0,1}[0-9]+_del$)|(^Rv3854c:"
        + aminos
        + "[0-9]+_$)"
        + "|(^Rv2043c:[0-9]+_ins_[ACGT]+$)|(^Rv2043c:([0-9]+_){0,1}[0-9]+_del$)|(^Rv2043c:"
        + aminos
        + "[0-9]+_$)"
        + "|(^Rv3919c:[0-9]+_ins_[ACGT]+$)|(^Rv3919c:([0-9]+_){0,1}[0-9]+_del$)|(^Rv3919c:"
        + aminos
        + "[0-9]+_$)"
        + "|(^Rv0667:[0-9]+_ins_[ACGT]+$)|(^Rv0667:([0-9]+_){0,1}[0-9]+_del$)|(^Rv0667:"
        + aminos
        + "[0-9]+_$)"
        + "|(^Rv0678:[0-9]+_ins_[ACGT]+$)|(^Rv0678:([0-9]+_){0,1}[0-9]+_del$)|(^Rv0678:"
        + aminos
        + "[0-9]+_$)"
        + "|(^Rv2780:[0-9]+_ins_[ACGT]+$)|(^Rv2780:([0-9]+_){0,1}[0-9]+_del$)|(^Rv2780:"
        + aminos
        + "[0-9]+_$)"
        + "|(^Rv1908c:[0-9]+_ins_[ACGT]+$)|(^Rv1908c:([0-9]+_){0,1}[0-9]+_del$)|(^Rv1908c:"
        + aminos
        + "[0-9]+_$)"
        + "|(^Rv3547:[0-9]+_ins_[ACGT]+$)|(^Rv3547:([0-9]+_){0,1}[0-9]+_del$)|(^Rv3547:"
        + aminos
        + "[0-9]+_$)"
        + "|(^Rv1694:[0-9]+_ins_[ACGT]+$)|(^Rv1694:([0-9]+_){0,1}[0-9]+_del$)|(^Rv1694:"
        + aminos
        + "[0-9]+_$)"
    )
    # extract deletions from resi_variants_set
    deletions: List[str] = []
    for var in resistance_variants_set:
        if bool(re.match(r".*_del$", var)):
            deletions.append(var)

    split = os.path.basename(in_path).split("_")
    identifier_list = []
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
    amino_ann = re.compile(utils.get_amino_ann())
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
                    variant = f"-:{ann}"
                if bool(re.fullmatch(key_genes, variant)) or {variant} & resistance_variants_set:
                    columns.update([variant])

        elif allel_type == "Del" and not bool(re.fullmatch(amino_ann, ann)):
            if len(ann) > 0:
                split = ann.split("_")
                if len(gene) > 0:
                    variant = f"{gene}:{ann}"
                else:
                    variant = "-:" + ann
                if len(split) == 2:
                    if not 0 < int(split[0]) <= 4411532:
                        warnings.warn(f"Position {split[0]} is not in (0,4411532] for {in_path}.")
                    if bool(re.fullmatch(key_genes, variant)):
                        columns.update([variant])
                    else:
                        pos = int(split[0])
                        for ref in deletions:
                            split1 = ref.split(":")
                            ref_gene = split1[0]
                            ref_ann = split1[1]
                            split1 = ref_ann.split("_")
                            ref_pos = int(split1[0])
                            if pos == ref_pos and gene == ref_gene:
                                columns.update([variant])
                elif len(split) == 3:
                    if not 0 < int(split[0]) < int(split[1]) <= 4411532:
                        warnings.warn(
                            f"Unexpected positions in Del annotation {ann} for {in_path}."
                        )
                    if bool(re.fullmatch(key_genes, variant)):
                        columns.update([variant])
                    else:
                        pos1 = int(split[0])
                        pos2 = int(split[1])
                        for ref in deletions:
                            split1 = ref.split(":")
                            ref_gene = split1[0]
                            ref_ann = split1[1]
                            split1 = ref_ann.split("_")
                            ref_pos = int(split1[0])
                            if pos1 <= ref_pos <= pos2 and gene == ref_gene:
                                columns.update([variant])
                else:
                    warnings.warn(f"Irregular Del annotation {ann} for {in_path}.")

        elif allel_type == "SNP" and not bool(re.fullmatch(amino_ann, ann)):
            if len(ann) > 0:
                if len(gene) > 0:
                    variant = f"{gene}:{ann}"
                else:
                    variant = f"-:{ann}"
                if {variant} & resistance_variants_set:
                    columns.update([variant])
            else:
                warnings.warn(f"Unexpected SNP annotation {ann} for {in_path}.")

        elif allel_type == "SNP" and bool(re.fullmatch(amino_ann, ann)):
            if len(gene) > 0:
                variant = f"{gene}:{ann}"
            else:
                variant = f"-:{ann}"
            if bool(re.fullmatch(key_genes, variant)) or {variant} & resistance_variants_set:
                columns.update([variant])
        else:
            warnings.warn(
                f"Annotation of type {allel_type} at position {genome_pos} is {ann} for {in_path}."
            )

    if len(columns) > 0:
        return columns, identifier
    else:
        return None, identifier
