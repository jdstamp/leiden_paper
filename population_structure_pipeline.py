from joblib import Parallel, delayed
import multiprocessing
import itertools
import os.path

import pandas as pd

import simulations.correct_traits_pca as correct_traits
import simulations.run_plink_gwas as plink
import simulations.simulate_genotypes as geno
import simulations.simulate_traits as traits
import simulations.vcf_to_plink as vcf
from simulations.plot_qqplot import qqplot_all

import logging

logging.basicConfig(level=logging.INFO)


num_cores = multiprocessing.cpu_count()


# Configuration
data_path = "data/"
data_set = "stdpopsim"
file_prefix = os.path.join(data_path, data_set)
pvalues_file = f"{file_prefix}_p_values_subsampled.txt"

traits_file_pattern = os.path.join(
    data_path, "{data_set}_n{n_causal}_h{heritability}_trait_{j:02d}"
)
adjusted_traits_file_pattern = "{traits_file}.pca_adjusted"

# genotype simulation parameters
n_samples = 1250  # per population, we have 5000 samples in total
sequence_length = 100_000_000  # 50_000_000 results in ~3400 SNPs after pruning
maf = 0.05
thin_count = 5000

# trait simulation parameters
num_traits = 10
n_causal = [100, 1000]
heritability = [0.5]
parameters = list(itertools.product(n_causal, heritability))

# variant pruning parameters
window_size = 1000
step_size = 50
r2_threshold = 0.2

# p-value subsampling for plotting
subsample_frac = 0.05


def plink_pipeline():
    geno.msprime_sims(file_prefix, n_samples, sequence_length)
    vcf.vcf_to_plink(file_prefix, maf=maf)
    plink.pca(file_prefix, window_size, step_size, r2_threshold)
    plink.thin_number_of_snps(file_prefix, maf, thin_count)

    for n_causal, heritability in parameters:
        logging.info(
            f"Starting run with n_causal={n_causal}, heritability={heritability}"
        )
        Parallel(n_jobs=num_cores)(
            delayed(run_single_trait)(j, heritability, n_causal)
            for j in range(num_traits)
        )


def run_single_trait(j, heritability, n_causal):
    traits_file = traits_file_pattern.format(
        data_set=data_set, n_causal=n_causal, heritability=heritability, j=j + 1
    )
    adjusted_traits_file = adjusted_traits_file_pattern.format(traits_file=traits_file)
    traits.gcta(file_prefix, traits_file, n_causal, heritability)
    correct_traits.pc_adjust(
        f"{traits_file}.phen",
        f"{file_prefix}_pruned_pca.eigenvec",
        f"{adjusted_traits_file}.phen",
    )
    plink.epistasis(file_prefix, traits_file)
    plink.epistasis(file_prefix, adjusted_traits_file)


def qqplot_pvalues():
    pvalue_dfs = []
    pvalue_pca_adjusted_dfs = []

    for n_causal, heritability in parameters:
        logging.info(
            f"Starting run with n_causal={n_causal}, heritability={heritability}"
        )
        # Initialize an empty list to collect the "P" columns from the GWAS results
        p_values = []
        p_values_pca_adjusted = []
        for j in range(num_traits):
            traits_file = traits_file_pattern.format(
                data_set=data_set, n_causal=n_causal, heritability=heritability, j=j + 1
            )
            adjusted_traits_file = adjusted_traits_file_pattern.format(
                traits_file=traits_file
            )

            df = pd.read_csv(f"{traits_file}.epi.qt", delim_whitespace=True)
            p_values.append(df.dropna().sample(frac=subsample_frac))

            df = pd.read_csv(f"{adjusted_traits_file}.epi.qt", delim_whitespace=True)
            p_values_pca_adjusted.append(df.dropna().sample(frac=subsample_frac))

        pv_df = pd.concat(p_values)
        pv_adj_df = pd.concat(p_values_pca_adjusted)

        poligenicity = "low" if n_causal < 1000 else "high"
        pv_df["heritability"] = heritability
        pv_df["n_causal"] = poligenicity
        pv_adj_df["heritability"] = heritability
        pv_adj_df["n_causal"] = poligenicity

        columns_to_keep = ["P", "heritability", "n_causal"]
        pvalue_dfs.append(pv_df[columns_to_keep])
        pvalue_pca_adjusted_dfs.append(pv_adj_df[columns_to_keep])

    pvalues_file = f"{file_prefix}_p_values.txt"
    pv = pd.concat(pvalue_dfs)
    pv["adjusted"] = "unadjusted"
    pv_adjusted = pd.concat(pvalue_pca_adjusted_dfs)
    pv_adjusted["adjusted"] = "PCA adjusted"
    pvalues_all = pd.concat([pv, pv_adjusted])
    pvalues_all.to_csv(pvalues_file, index=False, header=True)

    qqplot_all(pvalues_file)


if __name__ == "__main__":
    plink_pipeline()
    qqplot_pvalues()
