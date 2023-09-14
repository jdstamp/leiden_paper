from subprocess import run

##NB: For real data please ensure sufficient QC has been used first (i.e. relatives removed etc.)
def main():
    data_set = "stdpopsim"
    plink_ld_prune_cmd = f"plink --bfile {data_set} --indep-pairwise 1000 50 0.2 --exclude range high-ld-hg19-regions.txt --allow-no-sex --out {data_set}_pruned"
    run(plink_ld_prune_cmd.split(" "))
    plink_pca_cmd = f"plink --bfile {data_set} --extract {data_set}_pruned.prune.in --pca --allow-no-sex --out {data_set}_pruned_pca"
    run(plink_pca_cmd.split(" "))



if __name__ == "__main__":
    main()
