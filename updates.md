## Updates: 
- simulate_genotypes.py: Parameters changed for simulation to produce fewer individuals (n_samples=1000, computational speed considerations) but more genotypes (sequence_length=100,000,000 as there were to few common vars generated by original settings)  
- vcf_to_plink.py: Added a hard minor allele frequency threshold of >1% when making plink files. Also added a thinning function to subset to 100k SNPs to speed up downstream epistasis analysis.

# TODO:
- [x] Change color of QQplot to SteelBlue and Indianred
- [x] Change Bonferroni line to dashed and black
- [x] Figure out a good facet label for polygenicity
- [x] delete unused code
- [x] clean up dependencies and documentation
- [x] link to poetry documentation