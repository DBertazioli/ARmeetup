
# packages ----------------------------------------------------------------
library(ggplot2)
library(ggthemes)


# load data ---------------------------------------------------------------

df <- read.table('https://raw.githubusercontent.com/DBertazioli/ARmeetup/master/Visualizations/survey/user_test.txt',
                 header = TRUE, sep = ",")

str(df)
df$n_viz <- as.factor(df$n_viz)


# plot violin -------------------------------------------------------------

png("violin_plot.png", width = 15, height = 8, units = 'in', res = 300)
ggplot(df, aes(x = n_viz, y = time_s)) + 
  geom_violin(trim=FALSE, fill = '#404040', color = '#404040', alpha = 0.8) +
  geom_boxplot(notch = T, width=0.25, fill = 'grey',color='white',
               outlier.shape = NA, alpha = 0.2) +
  geom_jitter(aes(color = as.factor(df$response)),
              shape=16, position=position_jitter(0.05)) +
  scale_color_manual(values = c('#80ccff','#ffad33'),
                     name = "Response", labels = c("Wrong", 'Right')) +
  labs(x = '', y = 'Time (s)') +
  theme_clean()  
  # stat_summary(fun.data='mean_sdl', 
  #                geom="pointrange", color="red") 
  # 
dev.off()
