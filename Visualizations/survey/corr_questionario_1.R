df <- read.csv('Questionario psicometrico (VIZ_1).csv')
df_corr <- df[,-1]

mcor <- cor(df_corr, method = 'kendall')

install.packages('corrplot')
png("test.png", width = 8, height = 8, units = 'in', res = 1000)
library(corrplot)
corrplot(mcor, method = 'circle',
         type = 'upper', order = 'hclust', tl.col = 'black',
         tl.srt = 45, tl.cex = 0.6, addCoef.col  = 'black', number.cex = 0.55,
         p.mat = res1$p, insig = 'p-value')
dev.off()

