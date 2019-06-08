#df <- read.csv('Questionario psicometrico (VIZ_1).csv')
df <- read.table('https://raw.githubusercontent.com/DBertazioli/ARmeetup/master/Visualizations/survey/Questionario%20psicometrico%20(VIZ_1).txt', header = TRUE, sep = ",")
df_corr <- df[,-1]
df_corr <- df_corr[, -7]

mcor <- cor(df_corr, method = 'kendall')

install.packages('corrplot')

#change resolution
png("corr_plot_viz1.png", width = 10, height = 10, units = 'in', res = 800)

library(corrplot)
corrplot(mcor, method = 'circle',
         type = 'upper', order = 'hclust', tl.col = 'black',
         tl.srt = 45, tl.cex = 0.7, addCoef.col  = 'black', number.cex = 0.85)

dev.off()

