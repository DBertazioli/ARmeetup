df <- read.csv('Questionario psicometrico (VIZ_1).csv')
df <- df[,-1]

str(df)
df2 = ifelse(df <= 3, 0, 1)

  