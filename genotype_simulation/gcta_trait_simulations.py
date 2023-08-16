from subprocess import run
import logging

import pandas as pd
import numpy as np

import random


def gcta():
    data_set = "stdpopsim"
    num_traits = 100
    n_causal = 100
    heritability = 1
    sim_traits = 1
    for j in range(num_traits):
        output = f"traits_{data_set}_{j+1:02d}"
        causal_snps = f"causal_snps_{data_set}_{j+1:02d}.txt"

        gcta_sim_cmd = (
            f"gcta-1.94.1 --bfile {data_set} --simu-qt --simu-causal-loci {causal_snps} "
            f"--simu-hsq {heritability} --simu-rep {sim_traits} --out {output}"
        )
        plink_freq_cmd = (
            f"plink --bfile {data_set} --freq --allow-no-sex --out {data_set}"
        )
        run(plink_freq_cmd.split(" "))

        frq = pd.read_csv(
            f"{data_set}.frq",
            delim_whitespace=True,
            usecols=[1, 4],
            skiprows=1,
            names=["snp_id", "maf"],
        )
        common = frq[frq["maf"] >= 0.05]

        logging.info(f"Simulating trait {j+1}/{num_traits}.")
        snp_idx = sorted(random.sample(list(common["snp_id"]), n_causal))
        snp_effect = np.random.normal(0, 1, n_causal)

        causal = pd.DataFrame(list(zip(snp_idx, snp_effect)), columns=["snp", "effect"])
        causal.to_csv(causal_snps, header=None, index=None, sep="\t", mode="w")

        run(gcta_sim_cmd.split(" "))


if __name__ == "__main__":
    gcta()
