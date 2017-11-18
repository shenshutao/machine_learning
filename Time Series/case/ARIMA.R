library(forecast)
library(tseries)

# Load data
setwd("~/Documents/GitHub/Machine-Learning/Time Series/case")
data <- read.csv(file="weekly.csv",header=TRUE,sep=",");
datats <-ts(data$Amount)
# Plot
plot.ts(datats)

# Check ADF
adf.test(datats, alternative = "stationary", k = 0)

# Data already stationary.
# p-value is small

# 1. Differencing (Remove Trend)
# a.Find the difference, usually is 1 or 2.
# datatsdiff<-diff(datats,differences=1)
# plot.ts(datatsdiff)
# datatsdiff2<-diff(datats,differences=2)
# plot.ts(datatsdiff2) # Seems good

# b.build ARIMA(p,d,q), to get the p & q, need check the ACF & PACF first.
acf(datats,lag.max=20)
acf(datats,lag.max=20,plot=FALSE)

pacf(datats,lag.max=20)
pacf(datats,lag.max=20,plot=FALSE)

# According to the graph, use q=5, then use Armia (1,2,5)
datasarima<-arima(window(datats,end=130),order=c(11,0,11))
datasarima
plot(forecast(datasarima,h=20))

##### Or use auto arima #####
# datasarima2<-auto.arima(datats, seasonal=FALSE,trace=T,start.q=20, max.q=20)
# datasarima2
# plot(forecast(datasarima2,h=5))
#############################

# Forcast data 5 weeks later.
datasarimaforecast <- Arima(window(datats,start=131),model=datasarima)
datasarimaforecast

accuracy(datasarima)

# TEST check if the residuals fit normal distribution, with mean 0.
acf(datasarimaforecast$residuals,lag.max=20)
Box.test(datasarimaforecast$residuals, lag=20, type="Ljung-Box")
plot.ts(datasarimaforecast$residuals)
hist(datasarimaforecast$residuals, col="red", freq=FALSE, xlim = range(seq(-100,100)))
