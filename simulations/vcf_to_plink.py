import os
from subprocess import run


def vcf_to_plink(file_prefix, maf):
    plink_convert_cmd = f"plink --vcf {file_prefix}.vcf --maf {maf} --out {file_prefix}.initial --make-bed"
    run(plink_convert_cmd.split(" "))
