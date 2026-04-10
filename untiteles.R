library(dplyr)

data <- read.csv("your_dataset.csv")
head(data)

getwd()

data <- read.csv("C:/Users/PURNAYOO PURNENDU/Desktop/solar_energy_prediction/data/solar_data_clean.csv")

head(data)

data <- read.csv(file.choose())


library(dplyr)

# set working directory manually from menu first

data <- read.csv("data/solar_data_clean.csv")

head(data)
str(data)


data <- read.csv(file.choose())

str(data)
summary(data)

data$time <- as.POSIXct(data$time)

library(ggplot2)

ggplot(data, aes(x = time, y = ac_power_kw)) +
  geom_line(color = "blue") +
  ggtitle("Solar Power Output Over Time")

ggplot(data, aes(x = time, y = ac_power_kw)) +
  geom_smooth() +
  ggtitle("Smoothed Solar Power Output")

set.seed(123)

sample_size <- 0.8 * nrow(data)
train_index <- sample(seq_len(nrow(data)), size = sample_size)

train <- data[train_index, ]
test <- data[-train_index, ]

install.packages("randomForest")   # run once
library(randomForest)

model_rf <- randomForest(ac_power_kw ~ ., data = train)

pred_rf <- predict(model_rf, test)

data$city <- as.factor(data$city)

install.packages("Metrics")
library(Metrics)

rmse(test$ac_power_kw, pred_rf)
mae(test$ac_power_kw, pred_rf)

