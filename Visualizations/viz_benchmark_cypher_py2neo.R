# packages ----------------------------------------------------------------
options(scipen = 999)
library(ggthemes)
library(ggplot2)
library(ggpubr)


# realize cypher performance dataframe ------------------------------------
cy_perf <- data.frame(Time = c(0.045, 0.072, 0.312, 2.464, 12.897),
                      index_list = c(100, 1000, 10000, 100000, 500000),
                      type = rep("cypher", 5))
cy_perf


# importing py2neo perfomance data ----------------------------------------
py2neo_perf <- read.csv("GIT/Data_Management_Project/Visualizations/py2neo_import_performance.csv")
py2neo_perf
py2neo_perf$type <- rep("py2neo", 5)



# merging data ------------------------------------------------------------
data_final <- rbind(cy_perf, py2neo_perf)
data_final


# full plot ---------------------------------------------------------------
full <- ggplot(data_final, aes(x = as.integer(index_list), y = Time, group = type, color = type)) +
  geom_point(size = 2) + geom_line(size = 1.2) +
  scale_y_continuous(breaks = c(0,1000,2000,3000,4000,5000)) +
  #coord_cartesian(xlim = c(0,100000)) +
  theme_bw() +
  labs(subtitle = "in creating nodes on Neo4j", x = "Number of nodes created",
       y = "Time required in seconds") +
  ggtitle("Difference between cypher and py2neo API") + 
  scale_colour_manual(values = c("#D35400", "#1F618D"),
                      name = "Structure \ntype",
                      breaks = c("cypher", "py2neo"),
                      labels = c("Cypher", "Py2neo"))
full


# zoomed plot -------------------------------------------------------------
zoom <- ggplot(data_final, aes(x = as.integer(index_list), y = Time, group = type, color = type)) +
  geom_point(size = 2) + geom_line(size = 1.2) +
  #scale_y_continuous(breaks = c(0,1000,2000,3000,4000,5000)) +
  coord_cartesian(xlim = c(0,1000), ylim = c(0,25)) +
  theme_bw() +
  labs(subtitle = "in creating nodes on Neo4j", x = "Number of nodes created",
       y = "Time required in seconds") +
  ggtitle("Difference between cypher and py2neo API") + 
  scale_colour_manual(values = c("#D35400", "#1F618D"),
                      name = "Structure \ntype",
                      breaks = c("cypher", "py2neo"),
                      labels = c("Cypher", "Py2neo"))
zoom


# combined plot -----------------------------------------------------------
full <- ggplot(data_final, aes(x = as.integer(index_list), y = Time, group = type, color = type)) +
  geom_point(size = 2) + geom_line(size = 1.2) +
  scale_y_continuous(breaks = c(0,1000,2000,3000,4000,5000)) +
  #coord_cartesian(xlim = c(0,100000)) +
  theme_bw() +
  labs(subtitle = "in creating nodes on Neo4j", x = "",
       y = "") +
  ggtitle("Difference between cypher and py2neo API") + 
  scale_colour_manual(values = c("#D35400", "#1F618D"),
                      name = "Import \nmode",
                      breaks = c("cypher", "py2neo"),
                      labels = c("Cypher", "Py2neo"))


zoom <- ggplot(data_final, aes(x = as.integer(index_list), y = Time, group = type, color = type)) +
  geom_point(size = 2) + geom_line(size = 1.2) +
  #scale_y_continuous(breaks = c(0,1000,2000,3000,4000,5000)) +
  coord_cartesian(xlim = c(0,1000), ylim = c(0,25)) +
  theme_bw() +
  labs(title = "Focus on 0-1000 nodes interval", x = "",
       y = "") +
  scale_colour_manual(values = c("#D35400", "#1F618D"),
                      name = "Import \nmode",
                      breaks = c("cypher", "py2neo"),
                      labels = c("Cypher", "Py2neo")) +
  theme(legend.position = "none")


# combaning ---------------------------------------------------------------
figure <- ggarrange(full, zoom,
                    ncol = 1, nrow = 2,
                    common.legend = TRUE, legend = "right")

annotate_figure(figure,
                left = text_grob("Time required in seconds", color = "black", rot = 90),
                bottom = text_grob("Number of nodes created", color = "black")
)
