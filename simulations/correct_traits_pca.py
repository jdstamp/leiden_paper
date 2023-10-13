from subprocess import run


def pc_adjust(input_phenotype, pca_file, output_phenotype):
    pca_adjust_command = (
        f"Rscript --vanilla simulations/correct_traits_pca.R {input_phenotype} {pca_file} {output_phenotype}"
    )
    run(pca_adjust_command.split(" "))
