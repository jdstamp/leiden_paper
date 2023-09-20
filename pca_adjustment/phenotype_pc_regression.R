#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
if (length(args)<2) {
  stop("At least two arguments must be supplied: 1.)Simulated phenotype file (quantitative) and 2.)Plink format PCA file", call.=FALSE)
} else if (length(args)==2) {
    phenos = read.table(args[1],stringsAsFactors = FALSE, header = FALSE,colClasses = c("character","character","numeric"))
    pcs = read.table(args[2],stringsAsFactors = FALSE, header = FALSE)

    ###Regress pheno~PCs, take the residuals as the adjusted phenotype:
    phenotype = phenos[,3]
    lm_fit = lm(phenotype ~as.matrix(pcs[,3:22]))
    ###Save the residuals: 
    corrected_phenotype = resid(lm_fit)
    phenos[,3] = corrected_phenotype
    write.table(phenos,paste0(args[1],".adjusted_20pcs"),quote = FALSE, row.names = FALSE, col.names = FALSE)
}