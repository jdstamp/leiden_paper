import os
from subprocess import run


def vcf_to_plink(file_prefix, maf, thin_count):
    plink_convert_cmd = (
        f"plink --vcf {file_prefix}.vcf --maf {maf} --out {file_prefix} --make-bed"
    )
    run(plink_convert_cmd.split(" "))
    plink_thin_cmd = (
        f"plink --bfile {file_prefix} --thin-count {thin_count} --out {file_prefix} --make-bed"
    )
    run(plink_thin_cmd.split(" "))
