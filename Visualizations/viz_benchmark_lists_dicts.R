
# packages ----------------------------------------------------------------
options(scipen = 999)
library(ggplot2)
library(ggthemes)
library(ggpubr)


# import data -------------------------------------------------------------
data <- read.csv("benchmark_lists_dicts.csv")
data$X <- NULL
data$index <- c(100,1000,10000,100000,500000)
data
# data processing ---------------------------------------------------------
data1 <- data[, c(1,3)]
names(data1) <- c("Times", "index")
data1$type <- c(rep("dict",5))
data1
data2 <- data[, c(2,3)]
data2
names(data2) <- c("Times", "index")
data2$type <- c(rep("list", 5))
data2
data_final <- rbind(data1, data2)
data_final



# plot full data ----------------------------------------------------------
full <- ggplot(data_final, aes(x = index, y = Times, group = type, color = type)) +
  geom_point(size = 1.5) + geom_line(size = .9) +
  #coord_cartesian(ylim = c(0,150)) +
  theme_bw() +
  labs(subtitle = "in extracting single instances from Kafka topic", x = "", y = "") +
  ggtitle("Difference between lists and dicts") + 
  scale_colour_manual(values = c("#D35400", "#1F618D"),
                    name = "Structure \ntype",
                    breaks = c("dict", "list"),
                    labels = c("Dict", "List"))



full
# plot zoomed data --------------------------------------------------------
data_final
data_final2 <- data_final[c(1,2,3,6,7,8),]

zoom <- ggplot(data_final, aes(x = index, y = Times, group = type, color = type)) +
  geom_point(size = 1.5) + geom_line(size = .9) +
  coord_cartesian(xlim = c(0,10000), ylim = c(0, 2.5)) +
  theme_bw() +
  labs(x = "Number of single instances extracted", y = "",
       title = "Detail of 100-10000 interval") +
  scale_colour_manual(values = c("#D35400", "#1F618D"),
                      name = "Structure \ntype",
                      breaks = c("dict", "list"),
                      labels = c("Dict", "List")) +
  theme(legend.position = "none")


zoom
# combining the two plots -------------------------------------------------
figure <- ggarrange(full, zoom,
          ncol = 1, nrow = 2,
          common.legend = TRUE, legend = "right")



# realize a common ylab ---------------------------------------------------
annotate_figure(figure,
                left = text_grob("Time required in seconds", color = "black", rot = 90)
)
