# leiden_paper
Collaboration on code for the "A multidisciplinary approach to epistasis detection" conference review paper.

## Requirements (Should provide specific versions for users):
plink1.9  
gcta 1.94.1  
msprime 
data.table (R package)

See `pyproject.toml` for python dependencies.

## To add:
1.) Script for generating PCA and PC adjusted phenotypes  
2.) Scripts for running epistasis software  
3.) Script for testing output (QQ-plots, Type 1 error rate etc.)  

## Updates: 
- simulate_genotypes.py: Parameters changed for simulation to produce fewer individuals (n_samples=1000, computational speed considerations) but more genotypes (sequence_length=100,000,000 as there were to few common vars generated by original settings)  
- vcf_to_plink.py: Added a hard minor allele frequency threshold of >1% when making plink files. Also added a thinning function to subset to 100k SNPs to speed up downstream epistasis analysis.  
