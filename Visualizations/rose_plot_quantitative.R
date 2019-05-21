library(ggplot2)
library(ggthemes)

data <- read.csv("GIT/ArangoDB_Meetup/csv/exported_queries/Gruppi_per_paese.csv")
data1 <- read.csv("GIT/ArangoDB_Meetup/csv/exported_queries/Eventi_per_paese.csv")
head(data)
head(data1)

names(data1) <- c("Numero_eventi", "Country")
head(data1)
names(data) <- c("Country", "Numero_gruppi")
head(data)

data_final <- merge(data, data1, intersect("Country", "Country"))
head(data_final)
data_final_ordered <- data_final[order(data_final$Numero_gruppi, decreasing = TRUE), c(1:3)]
data_final_ordered <- data_final_ordered[2:10,]
data_final_ordered
data_final_italy <- data_final[data_final$Country =="it",]
data_final_italy
data_plot <- rbind(data_final_ordered, data_final_italy)
data_plot
#population <- c(32720000, 64170000, 36503000, 25197700,
                81800000, 47198000, 67795000, 1335250000,
                126440000, 60483973)
data_plot$Country <- toupper(data_plot$Country)
#data_plot$Eventi_norm <- data_plot$Numero_eventi/data_plot$Numero_gruppi
#data_plot$Gruppi_norm <- data_plot$Numero_gruppi/population
#data_plot <- data_plot[-1,]
#data_plot <- data_plot[-c(7,8),]
#data_plot <- data_plot[order(data_plot$Gruppi_norm, decreasing = TRUE), c(1:5)]
#data_plot$Eventi_norm <- 1/data_plot$Eventi_norm
ggplot(data_plot, aes(x = Country, y = Numero_gruppi, fill = Numero_eventi)) +
  geom_bar(stat = "identity", width = 1, color = "black") +
  coord_polar() +
  theme_bw() +
  scale_fill_distiller(type = "seq", palette = "BuPu", direction = 1, name = "Number of events") +
  labs(x = "",
       y = "Number of groups", 
       title = "Rose plot of quantity of groups and events for country",
       subtitle = "USA are not shown because completely out of scale") +
  theme(legend.key.size = unit(1.5, "cm"),
        legend.key.width = unit(.75, "cm"),
        legend.direction = "vertical") +
  guides(fill = guide_colorbar(title.position = "right"))
data_plot
