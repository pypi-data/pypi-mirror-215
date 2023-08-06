#!/bin/bash

# This script executes several steps of MTBSeq.

# author: Bernhard Reuter, Jules Kreuer
# copyright: = Bernhard Reuter, Jules Kreuer
# license = LGPL-3.0-only


workdir="$1"
accession="$2"
threads="$3"
error=0

# TODO make it work with relative folder names
if [ -d "${workdir}" ]; then

    cd "${workdir}" || { echo "Couldn't cd into ${workdir}"; exit 1; }

    err="${workdir}/exec_mtbseq_${accession}.err"
    out="${workdir}/exec_mtbseq_${accession}.out"

    # TODO change to universal filenames
    if [ ! -s "${accession}_X_R1.fastq.gz" ]; then
        error=102
        echo "${accession}_X_R1.fastq.gz  is missing in ${workdir}. Skipping" >> "$err" 2>&1
    else
        # print out MTBseq version
        MTBseq --version 2> "$err" 1>> "$out"
        echo "==================================================" >> "$out"

        # --------------------------------------------------------------------------
        # execute the relevant parts of the MTBseq pipeline with standard parameters
        MTBseq --step TBbwa --threads "$threads" 2>> "$err" 1>> "$out"
        echo "==================================================" >> "$out"

        MTBseq --step TBrefine --threads "$threads" 2>> "$err" 1>> "$out"
        echo "==================================================" >> "$out"

        MTBseq --step TBpile --threads "$threads" 2>> "$err" 1>> "$out"
        echo "==================================================" >> "$out"

        MTBseq --step TBlist --threads "$threads" 2>> "$err" 1>> "$out"
        echo "==================================================" >> "$out"

        MTBseq --step TBstrains 2>> "$err" 1>> "$out"
        echo "==================================================" >> "$out"
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # low-frequency variant calling:
        # create folder Called, since MTBseq expects that it exist already
        mkdir "Called" 2>> "$err" 1>> "$out"

        # call low-frequency variants with MTBseq
        MTBseq --step TBvariants --lowfreq_vars --mincovf 2 --mincovr 2 --minphred20 4 --minfreq 15 2>> "$err" 1>> "$out"
        echo "==================================================" >> "$out"

        # move standard folder Called created by MTBseq to customized folder
        mv "Called" "Called_low_freq" 2>> "$err" 1>> "$out"
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # super-low-frequency variant calling:
        # again create folder Called, since MTBseq expects that they exist already
        mkdir "Called" 2>> "$err" 1>> "$out"

        # call super-low-frequency variants with MTBseq
        MTBseq --step TBvariants --lowfreq_vars --mincovf 2 --mincovr 2 --minphred20 1 --minfreq 1 2>> "$err" 1>> "$out"
        echo "==================================================" >> "$out"

        # move standard folder Called created by MTBseq to customized folder
        mv "Called" "Called_super_low_freq" 2>> "$err" 1>> "$out"
        # --------------------------------------------------------------------------

        # check, if all relevant files were produced and are nonempty
        if [ ! -s "Mpileup/${accession}_X.gatk.mpileup" ]; then
            error=$((error+1))
            echo "Error: .gatk.mpileup file doesn't exist or has zero size." >> "$err" 2>&1
        fi
        if [ ! -s "Position_Tables/${accession}_X.gatk_position_table.tab" ]; then
            error=$((error+1))
            echo "Error: .gatk_position_table.tab file doesn't exist or has zero size." >> "$err" 2>&1
        fi
        if [ ! -s "Called_low_freq/${accession}_X.gatk_position_variants_cf2_cr2_fr15_ph4_outmode001.tab" ]; then
            error=$((error+1))
            echo "Error: low-frequency .gatk_position_variants file doesn't exist or has zero size." >> "$err" 2>&1
        fi
        if [ ! -s "Called_super_low_freq/${accession}_X.gatk_position_variants_cf2_cr2_fr1_ph1_outmode001.tab" ]; then
            error=$((error+1))
            echo "Error: super-low-frequency .gatk_position_variants file doesn't exist or has zero size." >> "$err" 2>&1
        fi
        if [ ! -s "Classification/Strain_Classification.tab" ]; then
            error=$((error+1))
            echo "Error: Strain_Classification file doesn't exist or has zero size." >> "$err" 2>&1
        fi

    fi

else

    error=100
    err="exec_mtbseq_${accession}.err"
    echo "Accession folder ${workdir} doesn't exist. Skipping." >> "$err" 2>&1

fi

exit ${error}
