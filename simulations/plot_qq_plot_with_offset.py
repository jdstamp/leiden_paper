from subprocess import run


def qqplot(traits_file, num_snps):
    qqplot_command = f"Rscript --vanilla simulations/plot_qq_plot_with_offset.R {traits_file} {num_snps}"
    run(qqplot_command.split(" "))


def qqplot_all(pvalue_file):
    qqplot_command = (
        f"Rscript --vanilla simulations/plot_qq_ggplot.R --file {pvalue_file}"
    )
    run(qqplot_command.split(" "))
