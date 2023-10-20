#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE)
require(data.table)
data = fread(paste0(args[1],".epi.qt" ),stringsAsFactors = FALSE, header = TRUE)
png(paste0(args[1],".png") )
data=data[!is.na(data$P),]
start = -log10(max(data$P))
expected = ppoints(data$P)
num_tests = (((as.numeric(args[2])*as.numeric(args[2]))/2) - as.numeric(args[2]))
threshold_bonf = 0.05/num_tests
qqplot(-log10(expected) + start ,-log10(data$P), pch=16, main = paste0("QQpplot: ", args[1]),xlab =expression(Expected ~ ~-log[10](italic(p))), 
       ylab = expression(Observed ~ ~-log[10](italic(p))) )
abline(0,1,col = "red")
abline(h=-log10(threshold_bonf),lty = 2,col = "blue")
dev.off()
