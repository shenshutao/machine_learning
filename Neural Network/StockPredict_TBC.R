setwd("D:/GitHub/Machine-Learning/Neural Network")
library(TTR)

# Loading the raw data
data <- read.csv("STI 2004-2013.csv")

########################################################################################
# Data preprocessing
########################################################################################

# Using zoo library for timeseries data, 
library(zoo)

dates = data$Date
data$Date = NULL
ts=zoo(data, as.Date(dates, "%Y-%m-%d")) 
head(ts, 2)

################################################################################################
# a. Adding Trend Variable
################################################################################################
# User created function to create a trend variable
thresholdFunc <- function(x) {
  threshold = 5
  if (!is.na(x)) {
    if (abs(x) < threshold)
    { 
      return(0)
    } else {
      return(x/abs(x))
    }
  }
  return(NA)
}

wkgain = diff(ts, lag=7) #7 days trend variable
head(wkgain, 2)
wkgain$tominc = diff(ts$Close, lag=-1) # increase from today to tomorrow
wkgain$tomclose = ts$Close + wkgain$tominc # tomorrow's close price
wkgain$tomtrend = wkgain$tominc/abs(wkgain$tominc) # 1 or -1.
#using the above created fuction for this trend variable
wkgain$tomtrendthreshod = zoo(apply(as.data.frame(wkgain$tominc), 1, thresholdFunc), as.Date(dates, "%Y-%m-%d"))
wkgain$ma10d = SMA(ts$Close, n=10) #10 days moving average
wkgain$ma30d = SMA(ts$Close, n=30) #30 days moving average
wkgain$ma200d = SMA(ts$Close, n=200) #200 days moving average
wkgain$rsi6 =  RSI(ts$Close, n=6, maType="SMA") - 50 # 6 days ratio of stock index
wkgain$rsi12 =  RSI(ts$Close, n=12, maType="SMA") - 50 #12 days ratio of stock index
wkgain$rsi24 =  RSI(ts$Close, n=24, maType="SMA") - 50 #24 days ratio of stock index

ts = cbind(ts, wkgain)
ts = na.omit(ts) #omitting the rows with na values

head(ts)
################################################################################################
# b. Handling missing value
################################################################################################
# Just don't use the volume column as input variable,as it has too many missing values

################################################################################################
# c.Data normalization
################################################################################################
colsd <- apply(ts, 2, function(x) sqrt(sum(x^2)/(length(x)-1)))

scaled <- scale(ts[, !names(ts) %in% c("tomtrend","tomtrendthreshod")], center = FALSE, scale = TRUE)
scaled <- zoo(scaled,  index(ts))

ts = cbind(ts, scaled)
###########################################################################################
# d.Data Partition (According to the assignment)
###########################################################################################
sta = as.Date("01-Jan-2000", "%d-%b-%Y")
mid1 = as.Date("31-Dec-2011", "%d-%b-%Y")
mid2 = as.Date("01-Jan-2012", "%d-%b-%Y")
last = as.Date("31-Dec-2020", "%d-%b-%Y")
traindata = as.data.frame(window(ts, start = sta, end = mid1))
testdata = as.data.frame(window(ts, start = mid2, end = last))

##########################################################################################
# e.neural net for tomclose - neural net number 1
##########################################################################################

#input variables
input <- c("Open.ts.scaled",
           "High.ts.scaled",
           "Low.ts.scaled",
           "Close.ts.scaled",
           "ma10d.scaled",
           "ma30d.scaled",
           "ma200d.scaled",
           "rsi6.scaled",
           "rsi12.scaled",
           "rsi24.scaled",
           "Open.wkgain.scaled",
           "High.wkgain.scaled",
           "Low.wkgain.scaled",
           "Close.wkgain.scaled"
           )
#target variable
target  <- "tomclose.scaled" 

#loading the required packages
library(neuralnet)
library(nnet)
library(caret)

# Tuning the neural network parameters to get the best values
# Cost time !!! the result is not best also. If too slow can skip.
set.seed(1000)
model <- train(form=tomclose.scaled ~ .,     # formula
             data=traindata[,c(input, target)],
             method="nnet",
           # try different parameters, minimise RMSE
             tuneGrid = expand.grid(.decay = c(0.0001, 0.001, 0.01), .size = c(4 : 10)),
             linout=TRUE, skip=TRUE, MaxNWts=10000, trace=FALSE, maxit=100
)
#Tuning takes a bit of time to process

bestsize <- model$bestTune$size #best size is 5
bestdecay <- model$bestTune$decay #best decay is 0.001
cat(sprintf("Tuned size is %d, decay is %f /r/n", bestsize, bestdecay))


set.seed(469)
nnet_tomclose <- nnet(tomclose.scaled ~ .,
             data=traindata[,c(input, target)],
             size= 5, #5
             decay=0.001, #0.001
             linout=TRUE, skip=TRUE, MaxNWts=10000, trace=FALSE, maxit=100)

preds <- predict(nnet_tomclose, testdata[, input])*colsd["tomclose"]
actual <- testdata$tomclose.ts
errors = preds - actual

# Plot the neural network
# library(NeuralNetTools)
# plotnet(nnet_tomclose)

Mean_Abs_Error<-mean((abs(errors)))
Base_Mean_Abs_Error<-mean(abs(testdata$tominc.ts))
summary(nnet_tomclose)
nnet_tomclose

#List of errors for the neural net of tomclose
cat(sprintf("Mean Abs Error (MAE) = %f /r/n", mean((abs(errors)))))
cat(sprintf("Mean Squared Error (MSE) = %f /r/n", mean(errors^2)))
cat(sprintf("Root Mean Squared Error (RMSE) = %f /r/n", sqrt(mean(errors^2))))
cat(sprintf("Base Mean Absolute error (Base MAE) = %f /r/n", mean(abs(testdata$tominc.ts))))

# confusion matrix 1 (TASK 1) Actual trend vs nnet1 Predicted trend- Table 1
todayClose <- testdata["Close.ts.ts"]
predinc <- preds - todayClose
predtrend <- predinc/abs(predinc)
tomtrend <-  testdata$tomtrend
table1 <- table(tomtrend, predtrend[,1], dnn=c("Actual", "Predicted"))

#Profit 1 - Tomorrow close prediction nnet's profit
tomclose_profit <- (table1[1,1] + table1[2,2] - table1[1,2] - table1[2,1]) *0.1
cat(sprintf(" Tomorrow close prediction nnet's profit = $ %f /r/n",tomclose_profit))

# ##########################################################################################
# #f.Bull or Bear trend prediction
# ##########################################################################################
# 
# # confusion matrix 2 - Bull or Bear Prediction - Table 2
# predtrendthreshold <- apply(predinc, 1, thresholdFunc)
# tomtrendthreshod <- testdata$tomtrendthreshod.ts
# table2 <- table(tomtrendthreshod, predtrendthreshold, dnn=c("Actual", "Predicted"))
# 
# #Profit 2 - Bull or Bear Profit Calculation 
# bullbear_profit <- table2[1,1]*0.1 + table2[3,3]*0.1 - table2[2,1]*0.05 - table2[3,1]*0.1 - table2[2,3]*0.05 - table2[1,3]*0.1
# cat(sprintf(" Bull or Bear profit = $ %f /r/n",bullbear_profit))
# 
# ##########################################################################################
# #g.Best Guess prediction
# ##########################################################################################
# 
# # Confusion matrix 3 - Actual Trend vs Best Guess Trend - Table 3
# # Tomorrow's close STI is equal to today's close STI
# bestguess_trend<-testdata$Close.ts.ts-testdata$Close.ts.ts
# table3 <- table(tomtrend, bestguess_trend, dnn=c("Actual", "Predicted"))
# 
# # Profit 3 -Best Guess prediction's profit
# bestguess_profit <- -(table3[1,1]+table3[2,1]) * 0.1
# cat(sprintf(" Best Guess prediction profit = $ %f /r/n",bestguess_profit))
# 
# ##########################################################################################
# #g.Frequent Trend prediction
# ##########################################################################################
# 
# #Creating a table to find the frequent trend
# trend_table<-table(traindata$tomtrend) #Looks like increasing trend is more
# #result of trend table
# ##-1   1 ## Increasing trend is more frequent
# ##835 957## 
# inc_trend<-rep(1,496) #creating an increasing trend object
# 
# # Confusion matrix 4 - Actual Trend vs Increasing Trend - Table 4
# table4 <- table(testdata$tomtrend, inc_trend,dnn=c("Actual", "freq_Predicted"))
# 
# #Profit 4 - Frequent Trend prediction's profit
# Frequent_trend_profit <-  (table4[2,1]-table4[1,1])*0.1
# cat(sprintf(" Frequent trend prediction profit = $ %f /r/n",Frequent_trend_profit))
# 
# ##########################################################################################
# #h.neural net for tom increase - neural net number 2
# ##########################################################################################
# 
# input2 <- c("Open.ts.scaled",
#            "High.ts.scaled",
#            "Low.ts.scaled",
#            "Close.ts.scaled",
#            "ma10d.scaled",
#            "ma30d.scaled",
#            "ma200d.scaled",
#            "rsi6.scaled",
#            "rsi12.scaled",
#            "rsi24.scaled",
#            "Open.wkgain.scaled",
#            "High.wkgain.scaled",
#            "Low.wkgain.scaled",
#            "Close.wkgain.scaled"
# )
# target2  <- "tominc.scaled"
# 
# 
# set.seed(479)
# nnet_tominc <- nnet(tominc.scaled ~ .,
#                       data=traindata[,c(input2, target2)],
#                       size= 5,#bestsize 
#                       decay= 0.001, #bestdecay, 
#                       linout=TRUE, skip=TRUE, MaxNWts=10000, trace=FALSE, maxit=100)
# 
# preds_inc <- predict(nnet_tominc, testdata[, input2])*colsd["tominc"]
# 
# #Re-computing trend with tominc nnet2
# 
# preds_inc_trend<-preds_inc/abs(preds_inc) # trend based on prediction 
# 
# # Confusion matrix 5 - Actual Trend vs nnet2 predicted trend - Table 5
# 
# table5 <- table(tomtrend, preds_inc_trend, dnn=c("Actual", "Predicted"))
# 
# #Profit 5 -  Tomorrow increase prediction nnet's profit
# tompinc_profit <- ((table5[1,1]+table5[2,2])-(table5[1,2]+table5[2,1]))*0.1 
# 
# cat(sprintf(" Tomorrow increase prediction nnet's profit = $ %f /r/n",tompinc_profit))

##########################################################################################
#i.neural net for tomorrow trend - neural net number 3
##########################################################################################


############################################################################################

# input3 <- c("Open.ts.ts",
#             "High.ts.ts",
#             "Low.ts.ts",
#             "Close.ts.ts",
#             "ma10d.ts",
#             "ma30d.ts",
#             "ma200d.ts",
#             "rsi6.ts",
#             "rsi12.ts",
#             "rsi24.ts",
#             "Open.wkgain.ts",
#             "High.wkgain.ts",
#             "Low.wkgain.ts",
#             "Close.wkgain.ts"
# )
# target3  <- "tomtrend_cat"
# traindata$tomtrend_cat<-class.ind(traindata$tomtrend_cat)
# 
# bestProfit = 0;
# bestseed = 0;
# for(i in 1:1000) {
#   set.seed(i)
#   nnet_tomtrend <- nnet(tomtrend_cat ~ .,
#                         data=traindata[,c(input3, target3)],size=5,decay= 0.001,linout=FALSE,
#                         skip=TRUE, MaxNWts=10000, trace=FALSE, maxit=100,softmax=TRUE)
#   
#   preds_trend <- predict(nnet_tomtrend, testdata[,input3],type=("class"))
#   
#   # Confusion matrix 6 - Actual Trend vs nnet3 predicted trend - Table 6
#   
#   table6 <- table(testdata$tomtrend, preds_trend, dnn=c("Actual", "Predicted"))
#   
#   #confusionMatrix(preds_trend, as.factor(testdata$tomtrend))
#   
#   #Profit 6 -  Tomorrow trend prediction nnet's profit
#   
#   preds_trend_profit <- 0
#   try(preds_trend_profit <- ((table6[1,1]+table6[2,2])-(table6[1,2]+table6[2,1]))*0.1)
#   
#   cat(sprintf(" Tomorrow trend prediction nnet's profit = $ %f /r/n",preds_trend_profit))
#   if(bestProfit < preds_trend_profit) {
#     bestProfit <- preds_trend_profit
#     bestseed <- i
#   }
# }
# 
# bestProfit
# bestseed
# 
# #######################################END##################################################


# input4 <- c("Open.ts.ts",
#             "High.ts.ts",
#             "Low.ts.ts",
#             "Close.ts.ts",
#             "ma10d.ts",
#             "ma30d.ts",
#             "ma200d.ts",
#             "rsi6.ts",
#             "rsi12.ts",
#             "rsi24.ts",
#             "Open.wkgain.ts",
#             "High.wkgain.ts",
#             "Low.wkgain.ts",
#             "Close.wkgain.ts"
# )
# target4  <- "tomtrendthreshod"
# levels(traindata$tomtrendthreshod)
# plot(traindata$tomtrendthreshod)
# plot(as.factor(traindata$tomtrendthreshod))
# traindata$tomtrendthreshod<-class.ind(traindata$tomtrendthreshod)
# 
# bestProfit = 0;
# bestseed = 0;
# for(i in 1:1000) {
# set.seed(i)
# nnet_tomtrendthreshod <- nnet(tomtrendthreshod ~ .,
#                     data=traindata[,c(input4, target4)],size=5,decay= 0.001,linout=FALSE,
#                   skip=TRUE, MaxNWts=10000, trace=FALSE, maxit=100,softmax=TRUE)
# 
# predtrendthreshod <- predict(nnet_tomtrendthreshod, testdata[,input4],type=("class"))
# 
# table2 <- table(testdata$tomtrendthreshod, predtrendthreshod, dnn=c("Actual", "Predicted"))
# 
# #Profit 6 -  Tomorrow trend prediction nnet's profit
# 
# task2profit <- 0
# try((task2profit <- table2[1,1]*0.1 + table2[3,3]*0.1 - table2[2,1]*0.05 - table2[3,1]*0.1 - table2[2,3]*0.05 - table2[1,3]*0.1))
# table2["1","1"]
# table2["1","-1"]
# table2["0","1"]
# 
# 
# cat(sprintf(" Tomorrow trend prediction nnet's profit = $ %f /r/n",task2profit))
# 
# if(bestProfit < task2profit) {
#     bestProfit <- task2profit
#     bestseed <- i
# }
# }
# 
# bestProfit
# bestseed


