library(argparse)
library(dplyr)
library(ggplot2)
library(qqplotr)

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
dp <- list(rate=log(10))
di <- "exp"
de <- FALSE # enabling the detrend option

# TODO: change causal snp facet labels
gg <- df %>% ggplot(mapping = aes(
  sample = -log10(P),
  color = adjusted # change colors to SteelBlue and Indianred, Bonferroni line black dashed
)) +
  theme_bw() +
  stat_qq_band(distribution = di,
               dparams = dp,
               detrend = de,
               alpha = 0.5) +
  stat_qq_line(distribution = di, dparams = dp, detrend = de) +
  stat_qq_point(distribution = di, dparams = dp, detrend = de) +
  facet_grid(n_causal ~  adjusted ) +
  theme(legend.position = "none") +
  geom_hline(yintercept=-log10(0.05 / ntest$n[1]), linetype='dashed', col = 'black') +
  labs(x = bquote("Theoretical Quantiles " -log[10](p)),
       y = bquote("Sample Quantiles " -log[10](p))) +
  scale_color_manual(values = c("SteelBlue", "Indianred"))

# TODO: do we need to produce a different file format?
ggsave(paste0(args$file_path, ".png"), plot = gg, width = 6, height = 4, dpi = 300)
