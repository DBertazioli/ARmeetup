library(ggplot2)
library(plotmath)
library(extrafont)

data <- read.csv("GIT/Data_Management_Project/csv/exported_queries/Jaccard_similarity_topic.csv")
head(data)

ggplot(data, aes(x = jac_similarity, y = ..density..)) +
  geom_density(fill = "#800080", alpha = .75, color = "black") + 
  theme_classic() +
  labs(x = "Jaccard Similarity", 
       y = "Density",
       title = "Jaccard similarity for topics between members",
       subtitle = "considering 'declared_interest_in' and 'is_interested_in' relations") +
  annotate(geom = "label",
           x = 0.35,
           y = 7.5,
           label = "The greatest part of the member \nreached a value near 0",
           size = 4) +
  geom_vline(xintercept = mean(data$jac_similarity), linetype = "longdash", color = "black") +
  annotate(geom = "text",
           x = 0.09,
           y = 1.5,
           label = 'Mean ~ 0.10',
           size = 4,
           color = "white",
           angle = 90,
           fontface = 2,
           alpha = .8) +
  annotate(geom = "label",
           x = 0.8,
           y = 1,
           size = 4,
           label = "Only few of them \nreached a value equal to 1")
