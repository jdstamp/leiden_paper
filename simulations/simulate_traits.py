from subprocess import run

import pandas as pd
import numpy as np

import random


def gcta(file_prefix, traits_file, n_causal, heritability, maf=0.05):
    sim_traits = 1
    causal_snps = f"{traits_file}_causal_snps.txt"

    gcta_sim_cmd = (
        f"gcta-1.94.1 --bfile {file_prefix} --simu-qt --simu-causal-loci {causal_snps} "
        f"--simu-hsq {heritability} --simu-rep {sim_traits} --out {traits_file}"
    )

    snps = pd.read_csv(
        f"{file_prefix}.bim",
        delim_whitespace=True,
        usecols=[0, 1],
        skiprows=1,
        names=["chr", "snp_id"],
    )

    snp_idx = sorted(random.sample(list(snps["snp_id"]), n_causal))
    snp_effect = np.random.normal(0, 1, n_causal)

    causal = pd.DataFrame(list(zip(snp_idx, snp_effect)), columns=["snp", "effect"])
    causal.to_csv(causal_snps, header=None, index=None, sep="\t", mode="w")

    run(gcta_sim_cmd.split(" "))
