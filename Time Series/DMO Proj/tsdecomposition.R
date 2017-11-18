library(forecast)
library(tseries)
require(graphics)

# Load data
setwd("~/Documents/GitHub/Machine-Learning/Time Series/DMO Proj")
data <- read.csv(file="TownGas.csv",header=TRUE,sep=",");

# split data into training & testing set
trainData <- data$DomTownGas_MKWH[1:74]
testData <- data$DomTownGas_MKWH[75:94]
predictLength = length(testData)

datats <-ts(trainData, frequency=4, start=c(1994,1))

plot( decompose(datats))

# Plot data
plot.ts(datats)

########### STL
fit <- stl(datats, s.window="periodic")
stlForecase <- forecast(fit,h=predictLength)
plot(stlForecase)

stlForecase$mean
cat("MSE of STL:")
mean((stlForecase$mean - testData)^2)

########### Holt-Winters
hw <- HoltWinters(datats)
plot(hw)
plot(fitted(hw))

hwForecast <- predict(hw, n.ahead = predictLength, prediction.interval = T, level = 0.95)
plot(hw, hwForecast)
hwForecast[,1]
cat("MSE of HoltWinters:")
mean((hwForecast[,1] - testData)^2)


########### ARIMA - seasonal-
adf.test(datats, alternative = "stationary", k = 0)
datatsdiff1<-diff(datats,differences=1)
adf.test(datatsdiff1, alternative = "stationary", k = 0)

# check acf & pacf to get the p , q values (or we can use auto arima instead.)
acf(datatsdiff1,lag.max=20)
pacf(datatsdiff1,lag.max=20)

#datasarima<-auto.arima(datatsdiff1)
datasarima<-arima(datatsdiff1,order=c(1,1,7))

arimaForecast <- forecast(datasarima,h=predictLength)
plot(arimaForecast)

lastVal <- datats[length(datats)]
meanOrigVal <- diffinv(arimaForecast$mean, differences = 1, xi = lastVal)
cat("MSE of ARIMA:")
meanOrigVal[2:length(meanOrigVal)]

mean((meanOrigVal[2:length(meanOrigVal)] - testData)^2)
ts.plot(datats, meanOrigVal, gpars = list(col=c("black", "red")))
