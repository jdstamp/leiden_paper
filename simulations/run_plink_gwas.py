import os
from pathlib import Path
from subprocess import run


def epistasis(file_prefix, traits_file):
    plink_epistasis_cmd = (
        f"plink --bfile {file_prefix} --pheno {traits_file}.phen --epistasis --epi1 1 --out {traits_file} --allow-no-sex"
    )
    run(plink_epistasis_cmd.split(" "))

def pca(file_prefix):
    plink_ld_prune_cmd = f"plink --bfile {file_prefix} --indep-pairwise 1000 50 0.2 --exclude range high-ld-hg19-regions.txt --allow-no-sex --out {file_prefix}_pruned"
    run(plink_ld_prune_cmd.split(" "))
    plink_pca_cmd = f"plink --bfile {file_prefix} --extract {file_prefix}_pruned.prune.in --pca --allow-no-sex --out {file_prefix}_pruned_pca"
    run(plink_pca_cmd.split(" "))
