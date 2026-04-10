# =========================================================
# 🌞 SOLAR ENERGY PREDICTION PROJECT (FINAL COMPLETE VERSION)
# =========================================================

# =========================================================
# ⚙️ SET WORKING DIRECTORY
# =========================================================
setwd("C:/Users/purna/OneDrive/Desktop/solar_energy_prediction")

# =========================================================
# 📦 INSTALL PACKAGES (RUN ONLY FIRST TIME)
# =========================================================
# install.packages(c("dplyr","ggplot2","corrplot","randomForest","Metrics","xgboost","httr","jsonlite"))

# =========================================================
# 📚 LOAD LIBRARIES
# =========================================================
library(dplyr)
library(ggplot2)
library(corrplot)
library(randomForest)
library(Metrics)
library(xgboost)
library(httr)
library(jsonlite)

# =========================================================
# 📡 DATA COLLECTION (API - DEMO)
# =========================================================
url <- "https://api.open-meteo.com/v1/forecast?latitude=13.0827&longitude=80.2707&hourly=temperature_2m"
response <- GET(url)
data_json <- content(response, "text")
data_list <- fromJSON(data_json)

# =========================================================
# 📂 LOAD DATASET (MAIN)
# =========================================================
data <- read.csv("data/solar_data_clean.csv")

# =========================================================
# 🧹 DATA CLEANING
# =========================================================
data$time <- as.POSIXct(data$time)
data$city <- as.factor(data$city)
data <- na.omit(data)

# =========================================================
# 🧠 FEATURE ENGINEERING
# =========================================================
data$hour <- as.numeric(format(data$time, "%H"))
data$day <- as.numeric(format(data$time, "%d"))
data$month <- as.numeric(format(data$time, "%m"))
data$is_daytime <- ifelse(data$hour >= 6 & data$hour <= 18, 1, 0)

# =========================================================
# 📊 DESCRIPTIVE ANALYTICS (EDA)
# =========================================================

# Time Series
ggplot(data, aes(x = time, y = ac_power_kw)) +
  geom_line(color = "blue") +
  ggtitle("Solar Power Output Over Time")

# Smoothed Trend
ggplot(data, aes(x = time, y = ac_power_kw)) +
  geom_smooth() +
  ggtitle("Smoothed Power Trend")

# Scatter: Irradiance vs Power
ggplot(data, aes(x = irradiance_ghi, y = ac_power_kw)) +
  geom_point() +
  ggtitle("Irradiance vs Power")

# Scatter: Temperature vs Power
ggplot(data, aes(x = ambient_temp, y = ac_power_kw)) +
  geom_point(color="orange") +
  ggtitle("Temperature vs Power")

# =========================================================
# 🔍 DIAGNOSTIC ANALYTICS
# =========================================================
numeric_data <- data[sapply(data, is.numeric)]
corr_matrix <- cor(numeric_data)
corrplot(corr_matrix, method = "color")

# =========================================================
# ✂️ TRAIN-TEST SPLIT
# =========================================================
set.seed(123)
sample_size <- 0.8 * nrow(data)
train_index <- sample(seq_len(nrow(data)), size = sample_size)

train <- data[train_index, ]
test <- data[-train_index, ]

# =========================================================
# 🌲 RANDOM FOREST MODEL
# =========================================================
model_rf <- randomForest(ac_power_kw ~ ., data = train)

pred_rf <- predict(model_rf, test)

rmse_rf <- rmse(test$ac_power_kw, pred_rf)
mae_rf  <- mae(test$ac_power_kw, pred_rf)

print(paste("Random Forest RMSE:", rmse_rf))
print(paste("Random Forest MAE:", mae_rf))

# =========================================================
# 🚀 XGBOOST MODEL
# =========================================================
train_matrix <- as.matrix(train[, sapply(train, is.numeric)])
test_matrix  <- as.matrix(test[, sapply(test, is.numeric)])

y_train <- train$ac_power_kw
y_test  <- test$ac_power_kw

model_xgb <- xgboost(
  data = train_matrix,
  label = y_train,
  nrounds = 100,
  objective = "reg:squarederror",
  verbose = 0
)

pred_xgb <- predict(model_xgb, test_matrix)

rmse_xgb <- rmse(y_test, pred_xgb)
mae_xgb  <- mae(y_test, pred_xgb)

print(paste("XGBoost RMSE:", rmse_xgb))
print(paste("XGBoost MAE:", mae_xgb))

# =========================================================
# 📊 MODEL COMPARISON
# =========================================================
comparison <- data.frame(
  Model = c("Random Forest", "XGBoost"),
  RMSE  = c(rmse_rf, rmse_xgb),
  MAE   = c(mae_rf, mae_xgb)
)
print(comparison)

# =========================================================
# 📉 ACTUAL VS PREDICTED
# =========================================================
results <- data.frame(
  Actual = test$ac_power_kw,
  Predicted = pred_rf
)

ggplot(results, aes(x = Actual, y = Predicted)) +
  geom_point(color = "red") +
  ggtitle("Actual vs Predicted (RF)")

# =========================================================
# 🔥 FULL DATA PREDICTION
# =========================================================
data$Predicted_Power <- predict(model_rf, data)
data$Prediction_Error <- abs(data$ac_power_kw - data$Predicted_Power)

# =========================================================
# 📊 FEATURE IMPORTANCE
# =========================================================
importance(model_rf)
varImpPlot(model_rf)

# =========================================================
# ⚙️ PRESCRIPTIVE ANALYTICS
# =========================================================

# Best hours
best_times <- data %>%
  group_by(hour) %>%
  summarise(avg_power = mean(Predicted_Power)) %>%
  arrange(desc(avg_power))

print("Best hours for energy usage:")
print(head(best_times, 5))

# Alert system
threshold <- 0.05
low_power <- data %>%
  filter(Predicted_Power < threshold)

print("Low power alerts:")
print(head(low_power))

# =========================================================
# 💾 EXPORT FINAL OUTPUT
# =========================================================
write.csv(data, "outputs/final_full_output.csv", row.names = FALSE)

print("PROJECT COMPLETED SUCCESSFULLY")

