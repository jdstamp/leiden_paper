from subprocess import run

import pandas as pd
import numpy as np



def pc_adjust():
    data_set = "stdpopsim"
    pca = f"{data_set}_pruned_pca.eigenvec"
    num_traits = 100
    

    for j in range(num_traits):

        input_phenotype = f"traits_{data_set}_{j+1:02d}.phen"
        pca_adjust_command = f"Rscript --vanilla phenotype_pc_regression.R {input_phenotype} {pca}"
        run(pca_adjust_command.split(" "))


if __name__ == "__main__":
    pc_adjust()
