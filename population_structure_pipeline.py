import itertools
import os.path

import pandas as pd

import simulations.simulate_genotypes as geno
import simulations.vcf_to_plink as vcf
import simulations.simulate_traits as traits
import simulations.run_plink_gwas as plink
import simulations.correct_traits_pca as correct_traits
from simulations.plot_qq_plot_with_offset import qqplot_all


def main():
    data_path = "data/"
    data_set = "stdpopsim"
    file_prefix = os.path.join(data_path, data_set)

    # genotype simulation parameters
    n_samples = 2500
    sequence_length = 10_000_000
    maf = 0.05
    thin_count = 10000

    # trait simulation parameters
    num_traits = 100
    n_causal = [100, 1000]
    heritability = [0.0, 0.5]
    parameters = list(itertools.product(n_causal, heritability))

    # variant pruning parameters
    window_size = 1000
    step_size = 50
    r2_threshold = 0.2

    geno.msprime_sims(file_prefix, n_samples, sequence_length)
    vcf.vcf_to_plink(file_prefix, maf=maf, thin_count=thin_count)
    plink.pca(file_prefix, window_size, step_size, r2_threshold)

    pvalue_dfs = []
    pvalue_pca_adjusted_dfs = []

    for n_causal, heritability in parameters:
        # Initialize an empty list to collect the "P" columns from the GWAS results
        p_values = []
        p_values_pca_adjusted = []
        for j in range(num_traits):
            traits_file = os.path.join(
                data_path, f"{data_set}_n{n_causal}_h{heritability}_trait_{j+1:02d}")
            adjusted_traits_file = f"{traits_file}.pca_adjusted"

            traits.gcta(file_prefix, traits_file, n_causal, heritability)
            correct_traits.pc_adjust(
                f"{traits_file}.phen", f"{file_prefix}_pruned_pca.eigenvec", f"{adjusted_traits_file}.phen")

            plink.epistasis(file_prefix, traits_file)
            plink.epistasis(file_prefix, adjusted_traits_file)

            df = pd.read_csv(f"{traits_file}.epi.qt", delim_whitespace=True)
            p_values.append(df.dropna())

            df = pd.read_csv(
                f"{adjusted_traits_file}.epi.qt", delim_whitespace=True)
            p_values_pca_adjusted.append(df.dropna())

        pv_df = pd.concat(p_values)
        pv_adj_df = pd.concat(p_values_pca_adjusted)

        pv_df["heritability"] = heritability
        pv_df["n_causal"] = n_causal
        pv_adj_df["heritability"] = heritability
        pv_adj_df["n_causal"] = n_causal

        columns_to_keep = ["P", "heritability", "n_causal"]
        pvalue_dfs.append(pv_df[columns_to_keep])
        pvalue_pca_adjusted_dfs.append(pv_adj_df[columns_to_keep])

    pvalues_file = f"{file_prefix}_p_values.txt"
    pv = pd.concat(pvalue_dfs)
    pv["adjusted"] = "unadjusted"
    pv_adjusted = pd.concat(pvalue_pca_adjusted_dfs)
    pv_adjusted["adjusted"] = "PCA"
    pvalues_all = pd.concat([pv, pv_adjusted])
    pvalues_all.to_csv(pvalues_file, index=False,  header=True)

    qqplot_all(pvalues_file)


if __name__ == "__main__":
    main()
