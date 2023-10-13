import os
from subprocess import run


def vcf_to_plink(data_path, data_set, maf, thin_count):
    file_prefix = os.path.join(data_path, data_set)
    plink_convert_cmd = (
        f"plink --vcf {file_prefix}.vcf --maf {maf} --out {file_prefix} --make-bed"
    )
    run(plink_convert_cmd.split(" "))
    plink_thin_cmd = (
        f"plink --bfile {file_prefix} --thin-count {thin_count} --out {file_prefix} --make-bed"
    )
    run(plink_thin_cmd.split(" "))
