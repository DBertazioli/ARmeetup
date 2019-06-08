
# packages ----------------------------------------------------------------
library(ggplot2)
library(plyr)
library(reshape2)
library(tibble)
library(dplyr)
library(tidyr)
library(ggthemes) # <-- guardati i temi che ci sono qui che magari ne trovi che ti piacciono



# import data -------------------------------------------------------------
df <- read.table('https://raw.githubusercontent.com/DBertazioli/ARmeetup/master/Visualizations/survey/Questionario%20psicometrico%20(VIZ_1).txt', header = TRUE, sep = ",")
df_stack <- df[,c(-1,-8)]
df_stack
str(df_stack)
head(df_stack)
df_stack = ifelse(df_stack <= 3, 0, 1)
table(df_stack)
class(df_stack)



# reshaping ---------------------------------------------------------------
df_stack <- as.data.frame(df_stack) # converto in dataframe
df_stack
new_data <- cbind(table(df_stack$Utile), #credo tabella di contingenza
      table(df_stack$Intuitiva),
      table(df_stack$Chiara),
      table(df_stack$Informativa),
      table(df_stack$Bella),
      table(df_stack$Valore.complessivo))

new_data
class(new_data)
row.names(new_data) <- c("1-3", "4-6")
colnames(new_data) <- c("Utile", "Intuitiva", "Chiara", "Informativa", "Bella", "Valore.complessivo")
new_data
new_data <- as.data.frame(new_data)
n <- length(df_stack[,1]) 
n
new_data <- new_data/n # frequenze relative
new_data

reshaped <- gather(new_data, "question", "answer") # reshape con pacchetto tidyr
reshaped$mod <- c("1-3","4-6","1-3","4-6","1-3","4-6","1-3","4-6","1-3","4-6","1-3","4-6")
# reshaped$answer + (1.96*sqrt((1-reshaped$answer)/n))

reshaped$up <- reshaped$answer + (1.96*sqrt((1-reshaped$answer)/n)) # definisco conf int
reshaped$low <- reshaped$answer - (1.96*sqrt((1-reshaped$answer)/n))
reshaped_error <- reshaped[c(2,4,6,8,10,12),] # prendo solo valori per p non per 1-p
reshaped_error

ggplot(reshaped,
       aes(fill = mod,
           y = answer,
           x = question)) + 
  geom_bar(stat = "identity",
           position = "fill") +
  geom_errorbar(data = reshaped_error,
                aes(x = question,
                    ymax = up,
                    ymin = low),
                width = .15) +
  geom_hline(yintercept = 0.50, linetype = "dashed", color = "black", size = 1) +
  coord_flip() +
  theme_bw() # versione base, poi puoi arricchirlo come ti piace
  # theme_classic(base_size = 14, base_family = "Helvetica") +
  # theme(axis.text.x=element_text(size=9)) +
  # theme(axis.title.y=element_text(size=12, face="bold", vjust=1)) +
  # theme(axis.text.y=element_text(angle=45,hjust=1,vjust=1, size=11)) +
  # theme(legend.position="right")


# da qui riprende tuo script ----------------------------------------------
df_stack <- t(df_stack)
df_stack

df_stack <- as.data.frame(df_stack)
df_stack

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
melted
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

