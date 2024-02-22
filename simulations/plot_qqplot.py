from subprocess import run


def qqplot_all(pvalue_file):
    qqplot_command = (
        f"Rscript --vanilla simulations/plot_qq_ggplot.R --file {pvalue_file}"
    )
    run(qqplot_command.split(" "))
