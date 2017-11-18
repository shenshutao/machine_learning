######Support Vector Machine#######

# Change to your own workspace #
setwd("C:/Users/Shutao/Desktop/NUS/Assigments/Semi 2/Semi 2-DA 1 bikeshare")

library(Hmisc) # For Lag function
library(TTR)   # For moving average function
library(e1071) # Functions for latent class analysis

#Importing the day dataset
day <- read.csv("day.csv")

################### Data Preparation ####################
## Lagging the required vectors by 2 days
# Also Lagging registered and casual
day$registeredL2 <- Lag(day$registered, shift = 2)
day$casualL2 <- Lag(day$casual, shift = 2)

# Trend Variable - Moving Average for casual and registered (3 days moving average )
day$registered7DaysMAL2 <- SMA(day$registeredL2, n = 7)
day$casual7DaysMAL2 <- SMA(day$casualL2, n = 7)

# Change into factor
day$weekday <- as.factor(day$weekday)

# Remove the first 8 records, because of Lag & SMA
size = nrow(day)
day <- day[9:size, ]

############### Prepare training set & test set ###########
train_set_registered <-
  day[day$yr == 0, c(
    "holiday",
    "weekday",
    "workingday",
    "registeredL2",
    "registered7DaysMAL2",
    "registered"
  )]
test_set_registered <-
  day[day$yr == 1, c("holiday",
                     "weekday",
                     "workingday",
                     "registeredL2",
                     "registered7DaysMAL2")]
test_set_registered_actual <- day[day$yr == 1, c("registered")]

train_set_casual <-
  day[day$yr == 0, c("holiday",
                     "weekday",
                     "workingday",
                     "casualL2",
                     "casual7DaysMAL2",
                     "casual")]
test_set_casual <-
  day[day$yr == 1, c("holiday",
                     "weekday",
                     "workingday",
                     "casualL2",
                     "casual7DaysMAL2")]
test_set_casual_actual <- day[day$yr == 1, c("casual")]

############### Modelling SVM Train & Test ############################
# Train
model_svm_registered <-
  svm(registered ~ .,
      data = train_set_registered,
      type = "nu-regression",
      kernel = "linear")
model_svm_casual <-
  svm(casual ~ .,
      data = train_set_casual,
      type = "nu-regression",
      kernel = "linear")

# Test
predict_registered <-
  predict(model_svm_registered, test_set_registered, type = "raw")
predict_registered[predict_registered < 0] <-
  0 # Remove the negative value
predict_casual <-
  predict(model_svm_casual, test_set_casual, type = "raw")
predict_casual[predict_casual < 0] <- 0  # Remove the negative value

##### Profit calculation ###########
result <-
  cbind(
    test_set_casual_actual,
    predict_casual,
    test_set_casual_actual,
    predict_casual,
    test_set_registered_actual,
    predict_registered
  )
test_set_total_actual <- day[day$yr == 1, c("cnt")]
test_set_total_predict <- round(predict_casual + predict_registered)
result <-
  cbind(result, test_set_total_actual, test_set_total_predict)
colnames(result) <-
  c(
    "casual_actual",
    "casual_predict",
    "casual_actual",
    "predict_casual",
    "registered_actual",
    "registered_predict",
    "total_actual",
    "total_predict"
  )

total_profit = 0
for (i in 1:nrow(result))
{
  actual_no <- result[i, "total_actual"]
  predict_no <- result[i, "total_predict"]
  
  if (actual_no >= predict_no) {
    profit_per_day = predict_no * 1
  }
  else if (actual_no < predict_no) {
    profit_per_day = actual_no * 1 - (predict_no - actual_no) * 2
  }
  
  total_profit = total_profit + profit_per_day
}

# Calculate MSE
library(hydroGOF)
result <- as.data.frame(result)
resultMse <-
  mse(result$total_actual, result$total_predict, na.rm = TRUE)
resultRmse <-
  rmse(result$total_actual, result$total_predict, na.rm = TRUE)
cat("MSE is ", resultMse)
cat("RMSE is ", resultRmse)

total_profit  # Display result

write.csv(result, file = "result_svm.csv")
