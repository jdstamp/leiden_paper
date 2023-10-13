import os
from pathlib import Path
from subprocess import run


def epistasis(file_prefix, traits_file):
    plink_epistasis_cmd = (
        f"plink --bfile {file_prefix} --pheno {traits_file}.phen --epistasis --epi1 1 --out {traits_file} --allow-no-sex"
    )
    run(plink_epistasis_cmd.split(" "))

def pca(file_prefix):
    plink_pca_cmd = f"plink --bfile {file_prefix} --pca --allow-no-sex --out {file_prefix}"
    run(plink_pca_cmd.split(" "))
