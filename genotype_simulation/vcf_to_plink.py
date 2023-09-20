from subprocess import run


def main():
    data_set = "stdpopsim"
    plink_convert_cmd = f"plink --vcf {data_set}.vcf --maf 0.01 --out {data_set} --make-bed"
    run(plink_convert_cmd.split(" "))
    plink_thin_cmd = f"plink --bfile {data_set} --thin-count 100000 --out {data_set} --make-bed"
    run(plink_thin_cmd.split(" "))

if __name__ == "__main__":
    main()
