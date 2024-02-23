library(argparse)
library(dplyr)
library(ggplot2)

# Define the command-line arguments
parser <- ArgumentParser()
parser$add_argument("--file", dest="file_path", help="Path to the file to read")
# Parse the command-line arguments
args <- parser$parse_args()

# Read the file into a tibble
data <- read.csv(args$file_path)
df <- as_tibble(data)
ntest <- df %>%
  group_by(adjusted, n_causal, heritability) %>%
  summarize(n = n())

#Split into 4 groups to add expected dists and order:
datasub1 <- data[data$n_causal=="high"&data$adjusted=="unadjusted",]
datasub2 <- data[data$n_causal=="low"&data$adjusted=="unadjusted",]
datasub3 <- data[data$n_causal=="high"&data$adjusted=="PCA adjusted",]
datasub4 <- data[data$n_causal=="low"&data$adjusted=="PCA adjusted",]

##########################################
###Generate conf int for a line at x=y based on number of SNPs:
##########################################
ci <- 0.95
n_snps <- ntest$n[1]

clower = -log10(qbeta(
  p = (1 - ci) / 2,
  shape1 = seq(n_snps),
  shape2 = rev(seq(n_snps))
))
cupper = -log10(qbeta(
  p = (1 + ci) / 2,
  shape1 = seq(n_snps),
  shape2 = rev(seq(n_snps))
))

#Add conf ints to each parameter set and order by -log(p):
df1 <- data.frame(observed=-log10(sort(datasub1$P)),
                 expected= -log10(ppoints(n_snps)),
                 clower = clower,
                 cupper = cupper,
                 n_causal = datasub1$n_causal,
                 heritability = datasub1$heritability,
                 adjusted = datasub1$adjusted)
df2 <- data.frame(observed=-log10(sort(datasub2$P)),
                   expected= -log10(ppoints(n_snps)),
                   clower = clower,
                   cupper = cupper,
                   n_causal = datasub2$n_causal,
                   heritability = datasub2$heritability,
                   adjusted = datasub2$adjusted)
df3 <- data.frame(observed=-log10(sort(datasub3$P)),
                  expected= -log10(ppoints(n_snps)),
                  clower = clower,
                  cupper = cupper,
                  n_causal = datasub3$n_causal,
                  heritability = datasub3$heritability,
                  adjusted = datasub3$adjusted)
df4 <- data.frame(observed=-log10(sort(datasub4$P)),
                  expected= -log10(ppoints(n_snps)),
                  clower = clower,
                  cupper = cupper,
                  n_causal = datasub4$n_causal,
                  heritability = datasub4$heritability,
                  adjusted = datasub4$adjusted)


#Combine dataframes for plotting:
df=rbind(df1,df2,df3,df4)

#Plot qq with GWAS style x=y line + conf int:
gg <- df %>%
  ggplot(mapping= aes(x = expected, y = observed,color = adjusted)) +
  theme_bw() +
  facet_grid(n_causal ~  adjusted ) +
  geom_ribbon(aes(ymax = cupper, ymin = clower),
              fill = "#999999", alpha = 0.5,linewidth =0.25
  ) +
  geom_point() +
  geom_segment(
    data = . %>% filter(expected == max(expected)),
    aes(x = 0, xend = expected, y = 0, yend = expected),
    linewidth = 1, alpha = 1, lineend = "round"
  ) +
  geom_hline(yintercept=-log10(0.05 / ntest$n[1]), linetype='dashed', col = 'black') +
  labs(x = bquote("Theoretical Quantiles " -log[10](p)),
       y = bquote("Sample Quantiles " -log[10](p))) +
  theme(legend.position = "none") +
  scale_color_manual(values = c("SteelBlue", "Indianred"))

ggsave(paste0(args$file_path, ".png"), plot = gg, width = 6, height = 4, dpi = 300)
