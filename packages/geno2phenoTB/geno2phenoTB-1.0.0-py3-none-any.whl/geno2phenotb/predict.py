"""Functions to predict the resistance of an isolate."""

import json
import logging
import os
import warnings
from typing import Dict, List, Optional, Set, Tuple, Union

import joblib
import numpy as np
import pandas as pd

from geno2phenotb.preprocess import preprocess
from geno2phenotb.utils import get_drugs, get_rules

__author__ = "Bernhard Reuter, Jules Kreuer"
__copyright__ = "Bernhard Reuter, Jules Kreuer"
__license__ = "LGPL-3.0-only"

_logger = logging.getLogger(__name__)


def adjusted_classes(
    proba: float,
    t: float,
) -> float:
    """
    This function adjusts class predictions based on the prediction threshold (t).

    Will only work for binary classification problems.

    Parameters
    ----------
    proba : float
        Probability.
    t : float
        Decision threshold.

    Returns
    -------
    class : float
        Predicted class based on the decision threshold `t`:
        will be 1.0, if `proba >= t`, or 0.0 otherwise.
    """
    if proba >= t:
        return 1.0
    else:
        return 0.0


def single_prediction(
    drug: str,
    output_dir: str,
    sample_id: str,
    features: pd.Series,
) -> Tuple[
    Optional[float], float, float, Optional[List[str]], Optional[pd.Series], Optional[List[str]]
]:
    """
    Predicts drug resistance for a single drug based on preprocessed data.

    Parameters
    ----------
    drug : str
        Drug to predict resistance.
        The drug must be one of 'AMK', 'CAP', 'DCS', 'EMB', 'ETH',
        'FQ', 'INH', 'KAN', 'PAS', 'PZA', 'RIF', 'STR'.
    output_dir : str
        Path to output directory.
        A resistance report file '<drug>_resistance_report.txt' is written to this directory.
    sample_id : str
        Sample ID.
    features : pd.Series
        The features (incl. called variants, lineage classification, and genotypes)
        extracted from the supplied FASTQ file(s).

    Returns
    -------
    probability : float, default=None
        Probability (for resistance) against the requested drug.
        If the underlying Machine Learning Model is a Rule-Based Classifier (RBC),
        `probability=None`, since RBcs don't allow to estimate a probability.
    prediction : float
        Machine-Learning-based Prediction (1.0 for resistance, 0.0 for susceptibility)
        for the requested drug.
    catalog_prediction : float
        Resistance catalog based prediction (1.0 for resistance, 0.0 for susceptibility)
        for the requested drug.
    found_catalog_variants : List[str], default=None
        Resistance-causing variants found among the features.
    importances : pd.Series, default=None
        A Series with values quantifying the importance of each feature,
        if the underlying Machine Learning Model provides feature importances.
        None, otherwise.
    rule : List[str], default=None
        A list with features constituting a rule if the underlying
        Machine Learning Model is a Rule-Based Classifier.
        The rule can be constructed by connecting the given features
        with boolean 'or' operators (disjunctions).
        None, otherwise.
    """
    _logger.info(f"Single prediction of {drug}")
    rbc_drugs = [
        "AMK",
        "FQ",
        "RIF",
    ]

    nonrbc_drugs = [
        "CAP",
        "DCS",
        "EMB",
        "ETH",
        "INH",
        "KAN",
        "PAS",
        "PZA",
        "STR",
    ]

    # Load the features known to the drug-specific model from file:
    fn = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "static",
        drug,
        (
            "vcf_collection_low_freq_extended_targets_plus_ge100bp-upstream_"
            f"lin_pheno_geno_{drug}_coocc_columns_1_repeated.txt"
        ),
    )
    if not os.path.isfile(fn):
        raise FileNotFoundError(f"{fn} isn't a regular file or doesn't exist.")
    model_features_index: pd.Series = (
        pd.read_table(
            fn,
            header=None,
            dtype=str,
        )
        .squeeze()
        .iloc[:-1]
    )
    del fn
    model_features_index_list = model_features_index.to_list()

    # Keep only sample features relevant to the model:
    kept_features = features.loc[features.index.isin(model_features_index_list)]

    # Initialize a model feature vector filled with zeros:
    model_features = pd.Series(
        np.zeros(len(model_features_index_list)), index=model_features_index_list
    )
    # Assign the actual values of the relevant sample features to the model feature vector:
    model_features.loc[kept_features.index] = kept_features.to_numpy()

    importances: Optional[pd.Series] = None
    rule: Optional[List[str]] = None
    probability: Optional[float] = None
    geno_only: bool = False

    if drug in rbc_drugs:
        _logger.debug(f"Prediction of {drug} using a Rule-Based Classifier.")
        # Extract RBC rule:
        rule_idx, geno_only = get_rules(drug)
        rule = model_features_index.iloc[pd.Index(rule_idx, dtype=int)].to_list()

        if geno_only:
            warnings.warn(
                f"The Machine-Learning (ML) prediction for the drug {drug} is simply redundant to "
                "the catalog-based prediction, since the underlying ML model is a Rule-Based "
                "Classifier that learned only a simple rule: If the catalog-based prediction (aka "
                "genotype feature) is 'resistant', i.e., '{drug}_geno'=1.0, predict resistance. "
                "Otherwise, predict susceptibility."
            )

        loc_model_features = model_features.iloc[rule_idx]

        if loc_model_features.to_numpy().sum() > 0.0:
            prediction = 1.0
        else:
            prediction = 0.0

    elif drug in nonrbc_drugs:
        _logger.debug(f"Prediction of {drug} using a non RBC method.")

        # Reshape features accordingly as demanded by sklearn:
        x = model_features.to_numpy().reshape((1, model_features.shape[0]))

        # Load the NestedCV results from file:
        fn = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "static",
            drug,
            f"{drug}_repeated_nested_cv_results.json",
        )
        if not os.path.isfile(fn):
            raise FileNotFoundError(f"{fn} isn't a regular file or doesn't exist.")

        with open(fn) as json_file:
            nested_cv_results = json.load(json_file)
        del fn

        # Extract the optimal decision threshold for the model from the NestedCV results:
        threshold = nested_cv_results["average_precision"]["mean_best_threshold"]

        # Load the drug-specific model from file:
        fn = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "static",
            drug,
            f"{drug}_RNCV_average_precision_best_estimator.joblib",
        )

        if not os.path.isfile(fn):
            raise FileNotFoundError(f"{fn} isn't a regular file or doesn't exist.")
        model = joblib.load(fn)
        del fn

        # Get the probability for the sample from the model:
        dummy = model.predict_proba(x)
        if dummy.shape == (1, 2):
            probability = dummy[0, 1]
        else:
            raise ValueError(
                f"Probability returned by sklearn has a shape of {dummy.shape}, "
                "but a shape of (1,2) was expected."
            )

        # Determine the model prediction considering the threshold:
        if probability is not None:
            prediction = adjusted_classes(probability, threshold)
        else:
            raise ValueError(f"Cannot predict for {drug} since probability is None.")

        # Load feature importances:
        fn = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "static",
            drug,
            f"{drug}_RNCV_average_precision_best_estimator_feature_importances.npy",
        )
        if not os.path.isfile(fn):
            raise FileNotFoundError(f"{fn} isn't a regular file or doesn't exist.")
        importances = pd.Series(
            data=np.load(fn),
            index=model_features_index_list,
        )
        del fn

    else:
        raise ValueError(f"Unknown drug '{drug}'.")

    # Load the FZB resistance catalog from file:
    fn = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "static",
        "FZB_catalogue_2020-05-10_BRg_new_abbrevs_resistance_variants_only.tsv",
    )
    if not os.path.isfile(fn):
        raise FileNotFoundError(f"{fn} isn't a regular file or doesn't exist.")
    catalog_variants = pd.read_table(fn, sep="\t", dtype=str).fillna("")
    del fn

    # Extract the drug-specific resistance variants from the catalog:
    single_drug_catalog_variants: Set[str] = set(
        catalog_variants[drug].to_numpy().tolist()
    ).difference({""})

    # Extract drug-specific catalog variants from the sample variants:
    temp = features.loc[features.index.isin(single_drug_catalog_variants)]
    found_catalog_variants: Optional[List[str]]
    if temp.empty:
        found_catalog_variants = None
    elif not temp.isin([1.0]).all():
        raise ValueError("There are variants among the features that weren't called.")
    else:
        found_catalog_variants = temp.index.to_list()
    del temp

    # Determine the catalog-based prediction accordingly:
    if found_catalog_variants is not None:
        catalog_prediction = 1.0
        catalog_prediction_str = "resistant"
    else:
        catalog_prediction = 0.0
        catalog_prediction_str = "susceptible"

    # Define strings to characterize the ML prediction:
    if prediction == 1.0:
        prediction_str = "resistant"
    elif prediction == 0.0:
        prediction_str = "susceptible"
    else:
        raise ValueError(f"Unexpected prediction: prediction={prediction}")

    # Create human-readable prediction results compilation and write it to file:
    fn = os.path.join(output_dir, f"{drug}_resistance_report.txt")
    with open(fn, "w") as f:
        f.write(f"Resistance report for sample {sample_id}\n\n")
        f.write(f"Considered drug: {drug}\n\n")
        f.write(
            "Resistance prediction based on FZB resistance catalog: "
            f"{catalog_prediction} ({catalog_prediction_str})\n\n"
        )
        f.write(
            "Resistance prediction based on Machine Learning: "
            f"{prediction} ({prediction_str})\n\n"
        )

        if geno_only:
            f.write(
                "The Machine-Learning (ML) prediction is simply redundant to the catalog-based "
                "prediction, since the underlying ML model is a Rule-Based Classifier that learned "
                "only a simple rule: If the catalog-based prediction (aka genotype feature) is "
                f"'resistant', i.e., '{drug}_geno'=1.0, predict resistance. "
                "Otherwise, predict susceptibility.\n\n"
            )

        if probability is not None:
            f.write(
                f"Probability for resistance (estimated by Machine Learning): {probability:.3E}\n\n"
            )

        if found_catalog_variants is not None:
            f.write("Resistance variants from the FZB catalog found among the called variants:\n")
            for i in range(len(found_catalog_variants)):
                f.write(f"{found_catalog_variants[i]}\n")
            f.write("\n\n")

        if rule is not None:
            f.write("Rule learned by the Rule-Based Classifier:\n")
            f.write("||".join(rule))
            f.write("\n\n")

    _logger.debug("Prediction successful")

    return (
        probability,
        prediction,
        catalog_prediction,
        found_catalog_variants,
        importances,
        rule,
    )


def predict(
    fastq_dir: str,
    output_dir: str,
    sample_id: str,
    skip_mtbseq: bool = False,
    drugs: Optional[List[str]] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Optional[List[str]]]]:
    """
    Predicts the drug resistance. This will start all preprocessing steps.

    Parameters
    ----------
    fastq_dir : str
        Path to directory containing the fastq files.
    output_dir : str
        Path to output directory.
        A file named '<sample_id>_feature_importance_evaluation.tsv' is written to this directory.
        This file contains a table with feature importance values and catalog info per drug.
        Further, for each drug a resistance report file '<drug>_resistance_report.txt' is output.
    sample_id : str
        Sample ID.
    skip_mtbseq : bool, default=False
        Do not run MTBSeq but use preprocessed data.
    drugs : Union[str, list], default=None
        If None, drug resistance predictions for all drugs known to geno2phenoTB are determined.
        If a list of drugs is supplied, predictions will be only determined for these.
        The drug must be one of 'AMK', 'CAP', 'DCS', 'EMB', 'ETH', 'FQ',
        'INH', 'KAN', 'PAS', 'PZA', 'RIF', 'STR'.

    Returns
    -------
    result : pd.DataFrame
        A DataFrame with the probabilities (for resistance) and predictions
        (1.0 for resistance, 0.0 for susceptibility) for the requested drugs.
    feature_evaluation : pd.DataFrame
        A DataFrame listing the features (called variants, lineage classification,
        genotypes) plus an assessment of the relevance of each feature for the
        Machine-Learning-based and catalog-based resistance prediction per drug.
        For each drug, two columns are given: '<drug> feature importance' and
        '<drug> catalog resistance variant'. The first contains the feature
        importance value derived from the Machine Learning model, the second
        informs if the variant is a known catalog resistance variant
        for the considered drug.
    rules : Dict[str, Optional[list[str]]]
        Dict of lists with features constituting a rule.
        If the used Machine Learning Model is a Rule-Based Classifier,
        `rules[drug]` is a list of features constituting a rule
        (the rule can be constructed by connecting the given features
        with boolean 'or' operators (disjunctions)).
        Otherwise, `rules[drug]=None`.
    """
    known_drugs = get_drugs()

    # Check if requested drugs are known:
    if drugs is None:
        used_drugs = known_drugs
    elif isinstance(drugs, list):
        if len(set(drugs) - set(known_drugs)) == 0:
            used_drugs = drugs
        else:
            raise ValueError(
                "Illegal input: Prediction(s) for unknown drug(s) "
                f"{set(drugs) - set(known_drugs)} requested."
            )
    else:
        raise ValueError(
            "Illegal input: 'drugs' keyword must be either None or a list of known drugs."
        )

    # Preprocess FASTQ and return extracted features:
    features = preprocess(
        fastq_dir,
        output_dir,
        sample_id,
        skip_mtbseq=skip_mtbseq,
    )

    # Raise if no features were extracted:
    if features is None:
        raise ValueError("No features were extracted. Thus, prediction can't be executed.")

    # Prepare a DataFrame to collect predictions and probabilities:
    result = pd.DataFrame(
        data=np.full((3, len(used_drugs)), np.nan),
        index=["probability", "prediction", "catalog prediction"],
        columns=used_drugs,
    )

    # Initialize containers to collect further return values from predict:
    rules: Dict[str, Optional[List[str]]] = dict()
    data: Dict[str, Union[List[float], List[str]]] = dict()
    for drug in used_drugs:
        data[f"{drug} feature importance"] = [0.0 for x in range(features.size)]
        data[f"{drug} catalog resistance variant"] = ["no" for x in range(features.size)]
    feature_evaluation = pd.DataFrame(data, index=features.index)
    del data

    # Perform prediction for every single drug:
    for drug in used_drugs:
        (
            probability,
            result.at["prediction", drug],
            result.at["catalog prediction", drug],
            found_catalog_variants,
            importances,
            rules[drug],
        ) = single_prediction(
            drug,
            output_dir,
            sample_id,
            features,
        )
        if probability is not None:
            result.at["probability", drug] = probability
        if importances is not None:
            idx = feature_evaluation.index[feature_evaluation.index.isin(importances.index)]
            feature_evaluation.loc[idx, f"{drug} feature importance"] = importances.loc[
                idx
            ].to_numpy()
        if found_catalog_variants is not None:
            idx = feature_evaluation.index[feature_evaluation.index.isin(found_catalog_variants)]
            feature_evaluation.loc[idx, f"{drug} catalog resistance variant"] = "yes"

    # Write called variants and other features to file,
    # including feature importance values and catalog info per drug:
    fn = os.path.join(output_dir, f"{sample_id}_feature_importance_evaluation.tsv")
    feature_evaluation.to_csv(fn, sep="\t", header=True, index=True, index_label="feature")

    return result, feature_evaluation, rules
