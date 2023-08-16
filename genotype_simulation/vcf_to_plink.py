from subprocess import run


def main():
    data_set = "stdpopsim"
    plink_convert_cmd = f"plink --vcf {data_set}.vcf --out {data_set} --make-bed"
    run(plink_convert_cmd.split(" "))


if __name__ == "__main__":
    main()
