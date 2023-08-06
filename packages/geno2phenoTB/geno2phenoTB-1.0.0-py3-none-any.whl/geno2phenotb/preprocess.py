"""
Wrapper for all preprocessing steps.

These functions include the assembly and variant calling using MTBseq as well as the
genotype and lineage collection.
"""

import logging
import os
import shutil
import warnings
from subprocess import check_call
from tempfile import TemporaryDirectory
from typing import Optional, Set, Tuple

import numpy as np
import pandas as pd

import geno2phenotb.utils as utils
from geno2phenotb.annotate_vcf import annotate_vcf
from geno2phenotb.vcf_columns_extractor import vcf_columns_extractor
from geno2phenotb.vcf_columns_extractor_geno import vcf_columns_extractor_geno

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"

_logger = logging.getLogger(__name__)


def run_mtbseq(fastq_dir: str, sample_id: str) -> None:
    """
    Execute MTBseq for a single isolate.

    Parameters
    ----------
    fastq_dir : str
        Path to the directory were the FASTQ file(s)
        belonging to a single isolate are located.
    sample_id : str
        SampleID, i.e. run accession (ERR/SRR).

    Returns
    -------
    None
    """
    _logger.info("Running MTBSeq.")

    exec_mtbseq_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "exec_mtbseq.sh")
    _logger.debug(f"MTBSeq Exec Path: {exec_mtbseq_path}")
    _logger.debug(f"MTBSeq Args:\n\t\tFastQ Dir:\t{fastq_dir}\n\t\tSample " f"ID:\t{sample_id}")

    check_call([f"{exec_mtbseq_path} {fastq_dir} {sample_id} 1"], shell=True)
    _logger.debug("MTBSeq Done.")


def determine_genotype(
    catalog_variants: pd.DataFrame, resistance_variants: Set[str]
) -> Tuple[pd.Series, pd.Series]:
    r"""
    Determine the genotype of an isolate.

    Use resistance variants from the FZB catalog plus all InDels and early stop condons
    (e.g. :spelling:ignore:`A123_`) in the following genes (not mentioned in the catalog, i.e.,
    additionally to the known resistance variants from the Masterlist) to assign a resistant
    genotype: ethA=Rv3854c (ETH), pncA=Rv2043c (PZA), gidB/gid=Rv3919c (STR), rpoB=Rv0667 (RIF),
    Rv0678 (BDQ/CFZ), ald=Rv2780 (DCS), katG=Rv1908c (INH), ddn=Rv3547 (DLM), tlyA=Rv1694 (CAP).

    Parameters
    ----------
    catalog_variants : pd.DataFrame
        DataFrame of resistance-related variants from the FZB catalog.
        There is one column per drug. The column contains the variants from
        the FZB catalog that are related with resistance against the drug.
    resistance_variants : Set[str]
        Resistance-related variants that were found for an isolate.

    Returns
    -------
    genotypes : pd.Series[float]
        Series of per-drug genotypes.
    geno_variants : pd.Series[str]
        Series of resistance-related variants per drug.
    """
    _logger.info("Determining genotype.")

    key_genes = utils.get_key_genes()

    drugs = catalog_variants.columns
    variants_series: pd.Series = pd.Series(list(resistance_variants), dtype=str)

    genotypes: pd.Series = pd.Series(
        np.zeros(len(drugs)),
        index=[f"{x}_geno" for x in drugs],
        dtype=float,
    )

    geno_variants: pd.Series = pd.Series(index=[f"{x}_geno" for x in drugs], dtype=str)
    if not geno_variants.isna().all():
        raise ValueError("found_resistance_variants initialization error.")
    for drug in drugs:
        drug_geno = f"{drug}_geno"
        set_ = resistance_variants & set(catalog_variants.loc[:, drug]).difference({""})

        if set_:
            genotypes.at[drug_geno] = 1.0
            geno_variants.at[drug_geno] = ",".join(list(set_))
        if drug in key_genes.keys():
            mask = variants_series.str.match("|".join(key_genes[drug]), na=False)
            if np.any(mask):
                genotypes.at[drug_geno] = 1.0
                list_ = variants_series.loc[mask].to_list()
                if isinstance(geno_variants.at[drug_geno], str):
                    list_.append(geno_variants.at[drug_geno])
                    geno_variants.at[drug_geno] = ",".join(list_)
                else:
                    geno_variants.at[drug_geno] = ",".join(list_)
    return genotypes, geno_variants


def collect_lineages(classification_file: str) -> pd.Series:
    """
    Collect lineage classification.

    Parameters
    ----------
    classification_file : str
        Full path to the Strain_Classification.tab file.

    Returns
    -------
    lineage_classification : pd.Series
        Series of floats from {0.0, 1.0} denoting,
        if the isolate is classified to belong to a lineage,
        i.e. `classification["lineage X"]=1.0`, or not,
        i.e. `classification["lineage X"]=0.0`.
    """
    _logger.info("Collecting lineages.")
    _logger.debug(f"Classification file: {classification_file}")
    # Get list of lineages
    lineages = utils.get_lineages()

    # Reads table ans strips values
    temp = pd.read_table(
        classification_file, dtype="object", keep_default_na=False, na_values=["", "'-"]
    ).applymap(lambda x: utils.stripper(x))

    if not temp.shape[0] == 1:
        raise ValueError("classification table has more than 1 row.")

    classification: pd.Series = temp.squeeze()

    del temp

    lineage_classification: pd.Series = pd.Series(
        np.zeros(len(lineages)), index=lineages, dtype=float
    )
    if not classification.empty:
        lineage: float = classification.at["Coll lineage (easy)"]
        if f"Lineage {lineage}" in lineage_classification.index:
            lineage_classification.at[f"Lineage {lineage}"] = 1.0
        else:
            warnings.warn(f"Lineage {lineage} extracted from {classification_file} is unknown.")
    else:
        raise ValueError(f"{classification_file} is empty.")
    return lineage_classification


def preprocess(
    fastq_dir: str,
    output_dir: str,
    sample_id: str,
    skip_mtbseq: bool = False,
) -> Optional[pd.Series]:
    """
    Runs all preprocessing steps.

    Parameters
    ----------
    fastq_dir : str
        Path to directory containing the FASTQ files.
    output_dir : str
        Path to output directory.
        Two files are written to this directory.
        A file named '<sample_id>_resistant_genotype_variants.tsv' with resistance-related variants
        per drug and a file named '<sample_id>_extracted_features.tsv' with per-drug genotypes.
    sample_id : str
        Sample ID.
    skip_mtbseq : bool, default=False
        Do not run MTBSeq  but use preprocessed data.

    Returns
    -------
    features : pd.Series, default=None
        The features (incl. called variants, lineage classification, and genotypes)
        extracted from the supplied FASTQ file(s).
    """
    # Align/Analyze FASTQ (this results in variant call files (VCFs)):
    # Use temp directory
    with TemporaryDirectory(prefix="geno2phenotb_pre_") as mtbseq_output_dir:
        fastq_files = []

        if skip_mtbseq:
            # Use folder with preprocessed MTBSeq results instead of computing them.
            mtbseq_output_dir = fastq_dir
        else:
            # Use temporary directory and run MTBSeq

            # Check for correct naming and existence of fastq files.
            fastq_files = utils.check_fastq_filenames(fastq_dir, sample_id)

            # Copy fastq files to temp dir.
            _logger.debug(f"Copying fastq files to tempdir: {mtbseq_output_dir}")
            for file_name in fastq_files:
                _logger.debug(f"Copying: {file_name}")
                file_path = os.path.join(fastq_dir, file_name)
                shutil.copy(file_path, mtbseq_output_dir)

            # Execute MTBSeq.
            run_mtbseq(mtbseq_output_dir, sample_id)

        # Resistance Variants
        resi_vars_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "static",
            "FZB_catalogue_2020-05-10_BRg_new_abbrevs_resistance_variants_only.tsv",
        )
        if not os.path.isfile(resi_vars_file):
            raise FileNotFoundError(f"{resi_vars_file} isn't a regular file or doesn't exist.")

        low_freq_vcf_dir = os.path.join(mtbseq_output_dir, "Called_low_freq")
        _logger.debug(f"Low-Frequency VCF Dir: {low_freq_vcf_dir}")
        # Low-Frequency VCF

        low_freq_vcf_path = os.path.join(
            low_freq_vcf_dir,
            f"{sample_id}_X.gatk_position_variants_cf2_cr2_fr15_ph4_outmode001.tab",
        )
        if not os.path.isfile(low_freq_vcf_path):
            raise FileNotFoundError(f"{low_freq_vcf_path} isn't a regular file or doesn't exist.")

        # Annotate low-frequency VCF:
        annotate_vcf(low_freq_vcf_path)

        # Collect all variants from the annotated low-frequency VCF:
        annotated_vcf_path = os.path.join(
            low_freq_vcf_dir,
            f"{sample_id}_X.gatk_position_variants_cf2_cr2_fr15_ph4_outmode001_mod.tsv",
        )

        if not os.path.isfile(annotated_vcf_path):
            raise FileNotFoundError(f"{annotated_vcf_path} isn't a regular file or doesn't exist.")

        variants_lf, _ = vcf_columns_extractor(annotated_vcf_path)
        features: Optional[pd.Series]
        if variants_lf:
            features = pd.Series(np.ones(len(variants_lf)), index=sorted(variants_lf), dtype=float)
        else:
            features = None
            warnings.warn(f"No variants were extracted from {annotated_vcf_path}")

        # Collect lineage classification info:
        classific_path = os.path.join(
            mtbseq_output_dir, "Classification", "Strain_Classification.tab"
        )
        if not os.path.isfile(classific_path):
            raise ValueError(f"{classific_path} isn't a regular file or doesn't exist.")

        lineage_classification = collect_lineages(classific_path)

        if features is not None:
            features = features.append(
                lineage_classification, ignore_index=False, verify_integrity=True
            )
        else:
            features = lineage_classification

        # Annotate super-low-frequency VCF:

        super_freq_vcf_dir = os.path.join(mtbseq_output_dir, "Called_super_low_freq")
        super_freq_vcf_path = os.path.join(
            super_freq_vcf_dir,
            f"{sample_id}_X.gatk_position_variants_cf2_cr2_fr1_ph1_outmode001.tab",
        )

        if not os.path.isfile(super_freq_vcf_path):
            raise FileNotFoundError(f"{super_freq_vcf_path} isn't a regular file or doesn't exist.")

        annotate_vcf(super_freq_vcf_path)

        # Load the resistance associated variants from the catalog:
        catalog_variants = pd.read_table(resi_vars_file, sep="\t", dtype=str).fillna("")

        catalog_variants_set = set()
        for col in catalog_variants.columns:
            catalog_variants_set.update(catalog_variants.loc[:, col].to_list())
        catalog_variants_set = catalog_variants_set.difference({""})

        # Collect only resistance-related variants from the annotated super-low-frequency VCF:
        super_annotated_vcf_path = os.path.join(
            super_freq_vcf_dir,
            f"{sample_id}_X.gatk_position_variants_cf2_cr2_fr1_ph1_outmode001_mod.tsv",
        )

        if not os.path.isfile(super_annotated_vcf_path):
            raise FileNotFoundError(
                f"{super_annotated_vcf_path} isn't a regular file or doesn't exist."
            )

        resistance_variants_slf, _ = vcf_columns_extractor_geno(
            super_annotated_vcf_path, catalog_variants_set
        )
        if resistance_variants_slf is None:
            resistance_variants_slf = set()

        # Create output folder
        os.makedirs(output_dir, exist_ok=True)

        # Determine the genotype from the super-low-frequency variants:
        genotypes, geno_variants = determine_genotype(catalog_variants, resistance_variants_slf)

        super_res_geno_var = os.path.join(
            output_dir, f"{sample_id}_resistant_genotype_variants.tsv"
        )
        geno_variants.to_csv(super_res_geno_var, sep="\t", header=False)

        if features is not None:
            features = features.append(genotypes, ignore_index=False, verify_integrity=True)
            fn = os.path.join(output_dir, f"{sample_id}_extracted_features.tsv")
            features.to_csv(fn, sep="\t", header=False)
        else:
            raise ValueError(f"No features for {sample_id}")

        return features
