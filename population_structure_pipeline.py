import os.path

import simulations.simulate_genotypes as geno
import simulations.vcf_to_plink as vcf
import simulations.simulate_traits as traits
import simulations.run_plink_gwas as plink
import simulations.correct_traits_pca as correct_traits

def main():
    data_path = "data/"
    data_set = "stdpopsim"
    file_prefix = os.path.join(data_path, data_set)

    # genotype simulation parameters
    n_samples = 10
    sequence_length = 1_000_000
    maf = 0.05
    thin_count = 1000

    # trait simulation parameters
    num_traits = 2
    n_causal = 100
    heritability = 1

    geno.msprime_sims(data_path, data_set, n_samples, sequence_length)
    vcf.vcf_to_plink(data_path, data_set, maf=maf, thin_count=thin_count)
    plink.pca(file_prefix)

    for j in range(num_traits):
        traits_file = os.path.join(data_path, f"{data_set}_trait_{j+1:02d}")
        traits.gcta(file_prefix, traits_file, n_causal, heritability)
        plink.epistasis(file_prefix, traits_file)

        adjusted_traits_file = f"{traits_file}.pca_adjusted"
        correct_traits.pc_adjust(f"{traits_file}.phen", f"{file_prefix}.eigenvec", f"{adjusted_traits_file}.phen")
        plink.epistasis(file_prefix, adjusted_traits_file)

if __name__ == "__main__":
    main()