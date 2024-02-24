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

###Sort Ps in each group and calculate expected values for plotting:
df = df %>%
  group_by(adjusted, n_causal, heritability) %>%
  arrange(P, .by_group = TRUE) %>%
  mutate(
    cupper = cupper,
    clower = clower,
    expected= -log10(ppoints(n_snps)),
    observed = -log10(P)
  )

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
