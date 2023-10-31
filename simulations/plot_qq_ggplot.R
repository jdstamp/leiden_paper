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

di <- "exp"
de <- FALSE # enabling the detrend option

gg <- df %>% ggplot(mapping = aes(
  sample = -log10(P),
  color = adjusted
)) +
  theme_bw() +
  stat_qq_band(distribution = di,
               detrend = de,
               alpha = 0.5) +
  stat_qq_line(distribution = di, detrend = de) +
  stat_qq_point(distribution = di, detrend = de) +
  facet_grid(n_causal ~  adjusted + heritability) +
  theme(legend.position = "none") +
  labs(x = bquote("Theoretical Quantiles " -log[10](p)),
       y = bquote("Sample Quantiles " -log[10](p)))

ggsave(paste0(args$file_path, ".png"), plot = gg, width = 6, height = 4, dpi = 300)