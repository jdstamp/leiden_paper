import os
from pathlib import Path
from subprocess import run


def epistasis(file_prefix, traits_file):
    plink_epistasis_cmd = f"plink --bfile {file_prefix} --pheno {traits_file}.phen --epistasis --epi1 1 --out {traits_file} --allow-no-sex"
    run(plink_epistasis_cmd.split(" "))


def pca(file_prefix, window_size, step_size, r2_threshold):
    plink_ld_prune_cmd = f"plink --bfile {file_prefix} --indep-pairwise {window_size} {step_size} {r2_threshold} --allow-no-sex --out {file_prefix}_pruned"
    run(plink_ld_prune_cmd.split(" "))
    plink_pca_cmd = f"plink --bfile {file_prefix} --extract {file_prefix}_pruned.prune.in --pca --allow-no-sex --out {file_prefix}_pruned_pca"
    run(plink_pca_cmd.split(" "))


def thin_number_of_snps(file_prefix, thin_count):
    plink_thin_cmd = f"plink --bfile {file_prefix} --thin-count {thin_count} --out {file_prefix} --make-bed"
    run(plink_thin_cmd.split(" "))
