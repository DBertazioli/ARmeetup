#install.packages('corrplot')
library(corrplot)
library(psych)
library(Hmisc)
# load data ---------------------------------------------------------------
#viz 1
df <- read.table('https://raw.githubusercontent.com/DBertazioli/ARmeetup/master/Visualizations/survey/Questionario%20psicometrico%20(VIZ_1).txt',
                 header = TRUE, sep = ",")

#viz 2
df2 <- read.table('https://raw.githubusercontent.com/DBertazioli/ARmeetup/master/Visualizations/survey/Questionario%20psicometrico%20(VIZ_2).txt',
                 header = TRUE, sep = ",")

df_corr <- df[,c(-1,-8)]
df_corr2 <- df2[,c(-1,-8)]



# create corr -------------------------------------------------------------

# mcor <- cor(df_corr, method = 'pearson')
# mcor <- rcorr(as.matrix(df_corr), type = 'pearson')

mcor <- corr.test(df_corr, method = 'spearman', adjust = 'none')
mcor2 <- corr.test(df_corr2, method = 'pearson', adjust = 'none')

# viz 1 -------------------------------------------------------------------

#change resolution
png("corr_plot_viz1.png", width = 10, height = 10, units = 'in', res = 800)
corrplot(mcor$r, method = 'circle',
         type = 'upper', order = 'original', tl.col = 'black',
         tl.srt = 45, tl.cex = 0.7, addCoef.col  = 'black', number.cex = 0.85,
         cl.lim=c(-1,1), col=colorRampPalette(c("lightblue","white","orange"))(200),
         p.mat = mcor$p, sig.level = 0.05, insig = 'blank')
dev.off()


# viz 2 -------------------------------------------------------------------

#change resolution
png("corr_plot_viz2.png", width = 10, height = 10, units = 'in', res = 800)
corrplot(mcor2$r, method = 'circle',
         type = 'upper', order = 'original', tl.col = 'black',
         tl.srt = 45, tl.cex = 0.7, addCoef.col  = 'black', number.cex = 0.85,
         cl.lim=c(-1,1), col=colorRampPalette(c("lightblue","white","orange"))(200),
         p.mat = mcor2$p, sig.level = 0.05, insig = 'blank')
dev.off()

#mcor2$p

