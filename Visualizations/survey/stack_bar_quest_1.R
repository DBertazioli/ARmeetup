df <- read.table('https://raw.githubusercontent.com/DBertazioli/ARmeetup/master/Visualizations/survey/Questionario%20psicometrico%20(VIZ_1).txt', header = TRUE, sep = ",")
df_stack <- df[,c(-1,-8)]

str(df_stack)
df_stack = ifelse(df_stack <= 3, 0, 1)

df_stack <- t(df_stack)

df_stack <- as.data.frame(df_stack)


# df_stack$Group <- row.names(df_stack)
# rownames(df_stack) = 1:6

negativo <- rowSums(df_stack[1:6,] == 0)
positivo <- rowSums(df_stack[1:6,] == 1)
df_fin <- as.data.frame(cbind(negativo, positivo))
df_fin$Group <- row.names(df_fin)
rownames(df_fin) = 1:6

library(ggplot2)
library(plyr)
library(reshape2)
library(tibble)

melted <- melt(df_fin, id.vars='Group')
# means <- ddply(melted, c('variable','Group'), summarise,
#                mean=mean(value))

ggplot(data=melted, aes(x=Group, y=value, fill=variable)) + 
  geom_bar(stat="identity",
           width = 0.5) +                           
  xlab(" ") + ylab("number of response") + 
  theme_classic(base_size = 14, base_family = "Helvetica") + 
  theme(axis.text.y=element_text(size=9)) + 
  theme(axis.title.y=element_text(size=12, face="bold", vjust=1)) + 
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1, size=11)) +
  theme(legend.position="right")

# Calc SEM  
means.sem <- ddply(melted, c("variable", "Group"), summarise,
                   mean=mean(value), sem=sd(value)/sqrt(length(value)))
means.sem <- transform(means.sem, lower=mean-sem, upper=mean+sem)
means.sem[means.sem$variable=='Labeled',5:6] <- means.sem[means.sem$variable=='Labeled',3] + means.sem[means.sem$variable=='Unlabeled',5:6]

# Add SEM & change appearance of barplot
plotSEM <- plot + geom_errorbar(data=means.sem, aes(ymax=upper,  ymin=lower), 
                                width=0.15)
  