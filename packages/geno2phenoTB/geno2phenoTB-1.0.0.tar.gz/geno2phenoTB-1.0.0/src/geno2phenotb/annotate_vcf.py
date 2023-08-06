"""Annotates VCF."""

import logging
import re
import warnings
from typing import List, Optional

import pandas as pd

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"

_logger = logging.getLogger(__name__)


def annotate_vcf(in_path: str) -> None:
    """Complete missing annotations in the 'Subst' column of a MTBseq variant call file (VCF).

    Parameters
    ----------
    in_path : str
        Path to the VCF file to annotate/complete.
    Returns
    -------
    None
        Writes output to new file in the same directory.
    """
    _logger.debug(f"Annotating VCF: {in_path}")

    vcf = pd.read_table(in_path, sep="\t", dtype=str)
    vcf_g = vcf.copy(deep=True)
    i = 0
    while i < vcf.shape[0]:
        genome_pos = int(vcf.at[i, "#Pos"].strip())
        if not 0 < genome_pos <= 4411532:
            warnings.warn(f"Position {genome_pos} is not in (0,4411532] for {in_path}.")
        ann: str = vcf.at[i, "Subst"].strip().split(" ")[0]
        amino_ann = (
            r"(^Ala|^Arg|^Asn|^Asp|^Cys|^Gln|^Glu|^Gly|^His|^Ile|^Leu|^Lys|^Met|^Phe|^Pro|^Ser|"
            r"^Thr|^Trp|^Tyr|^Val|^_)[0-9]+(Ala$|Arg$|Asn$|Asp$|Cys$|Gln$|Glu$|Gly$|His$|Ile$|"
            r"Leu$|Lys$|Met$|Phe$|Pro$|Ser$|Thr$|Trp$|Tyr$|Val$|_$)"
        )
        if len(ann) > 0:
            if not bool(re.fullmatch(amino_ann, ann)):
                warnings.warn(
                    f"Annotation is not regular, but {ann} at position {genome_pos} for {in_path}."
                )
        allel_type: str = vcf.at[i, "Type"].strip()
        if not bool(re.fullmatch(r"^Ins|Del|SNP$", allel_type)):
            warnings.warn(
                "ref_allele is not in [Ins,Del,SNP], "
                f"but {allel_type} at position {genome_pos} for {in_path}."
            )
        ref_allele: str = vcf.at[i, "Ref"].strip()
        if not bool(re.fullmatch(r"^[ACGT]$", ref_allele)):
            warnings.warn(
                f"ref_allele is not in [A,C,G,T], but {ref_allele} "
                f"at position {genome_pos} for {in_path}."
            )
        mut_allele: str = vcf.at[i, "Allel"]
        if not bool(re.fullmatch(r"^[ACGT]|GAP$", mut_allele)):
            warnings.warn(
                f"mut_allele is not in [A,C,G,T,GAP], but {mut_allele} "
                f"at position {genome_pos} for {in_path}."
            )

        if allel_type == "Ins" and not bool(re.fullmatch(amino_ann, ann)):
            ins_pos_list: List[int] = []
            mut_allele_list: List[str] = []
            i_list: List[int] = []
            while (
                i < vcf.shape[0]
                and vcf.at[i, "Type"].strip() == "Ins"
                and int(vcf.at[i, "#Pos"].strip()) == genome_pos
            ):
                i_list.append(i)
                ins_pos_list.append(int(vcf.at[i, "Insindex"].strip()))
                mut_allele = vcf.at[i, "Allel"].strip()
                if not bool(re.fullmatch(r"^[ACGT]$", mut_allele)):
                    warnings.warn(
                        "mut_allele is not in [A,C,G,T], but %s at position %s for %s."
                        % (mut_allele, vcf.at[i, "#Pos"].strip(), in_path)
                    )
                mut_allele_list.append(mut_allele)
                if bool(re.fullmatch(amino_ann, vcf.at[i, "Subst"].strip().split(" ")[0])):
                    warnings.warn(
                        "Subst is %s for Ins at position %s for %s."
                        % (str(ann), vcf.at[i, "#Pos"].strip(), in_path)
                    )
                i += 1
            combi = zip(ins_pos_list, mut_allele_list, i_list)
            zipped_sorted = sorted(combi, key=lambda x: x[0])
            ins_pos_list, mut_allele_list, i_list = [list(x) for x in zip(*zipped_sorted)]

            vcf_g.at[i_list[0], "Subst"] = f"{genome_pos}_ins_{''.join(mut_allele_list)}"

        elif allel_type == "Del" and not bool(re.fullmatch(amino_ann, ann)):
            del_len = 0
            init_i = i
            ppp: Optional[int] = None
            while i < vcf.shape[0] and vcf.at[i, "Type"].strip() == "Del":
                del_len += 1
                if not vcf.at[i, "Allel"] == "GAP":
                    warnings.warn(
                        "Mutated allele isn't GAP for Del at position %s for %s."
                        % (vcf.at[i, "#Pos"].strip(), in_path)
                    )
                if del_len > 1:
                    if ppp is None:
                        raise ValueError("prior genome position is undefined.")
                    elif not int(vcf.at[i, "#Pos"].strip()) - 1 == ppp:
                        del_len -= 1
                        break
                ppp = int(vcf.at[i, "#Pos"].strip())
                i += 1
            if del_len > 1:
                vcf_g.at[init_i, "Subst"] = f"{genome_pos}_{ppp}_del"
            else:
                vcf_g.at[init_i, "Subst"] = f"{genome_pos}_del"

        elif allel_type == "SNP" and not bool(re.fullmatch(amino_ann, ann)):
            vcf_g.at[i, "Subst"] = f"{genome_pos}{ref_allele}>{mut_allele}"
            i += 1
        elif allel_type == "SNP" and bool(re.fullmatch(amino_ann, ann)):
            vcf_g.at[i, "Subst"] = ann
            i += 1
        else:
            warnings.warn(
                f"Annotation of type {allel_type} at position {genome_pos} is {ann} for {in_path}."
            )
            i += 1

    if in_path.endswith(".tab"):
        out_path = in_path.rstrip(".tab") + "_mod.tsv"
        vcf_g.to_csv(out_path, sep="\t", index=False)
    else:
        warnings.warn(f"Filename issue for vcf file {in_path}.")
