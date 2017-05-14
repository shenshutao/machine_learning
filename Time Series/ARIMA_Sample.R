library(forecast)

# Skirt length per year from 1866 to 1911.
skirts <- scan("http://robjhyndman.com/tsdldata/roberts/skirts.dat",skip=5)
skirtsts<- ts(skirts,start = c(1866))
plot.ts(skirtsts)

# a.Find the difference, usually is 1 or 2.
skirtstsdiff<-diff(skirtsts,differences=1)
plot.ts(skirtstsdiff)

skirtstsdiff2<-diff(skirtsts,differences=2)
plot.ts(skirtstsdiff2) # Seems good


# b.build ARIMA(p,d,q), to get the p & q, need check the ACF & PACF first.
acf(skirtstsdiff2,lag.max=20)
acf(skirtstsdiff2,lag.max=20,plot=FALSE)

pacf(skirtstsdiff2,lag.max=20)
pacf(skirtstsdiff2,lag.max=20,plot=FALSE)

# According to the graph, use q=5, then use Armia (1,2,5)
skirtsarima<-arima(skirtsts,order=c(1,2,5))
skirtsarima

##### Or use auto arima #####
# skirtsarima2<-auto.arima(skirtsts,trace=T,start.q=5, max.q=5)
# skirtsarima2
#############################

# Forcast shirt length 5 years later.
skirtsarimaforecast<-forecast.Arima(skirtsarima,h=5,level=c(99.5))
skirtsarimaforecast

plot.forecast(skirtsarimaforecast)

# TEST check if the residuals fit normal distribution, with mean 0.
acf(skirtsarimaforecast$residuals,lag.max=20)
Box.test(skirtsarimaforecast$residuals, lag=20, type="Ljung-Box")
plot.ts(skirtsarimaforecast$residuals)
hist(skirtsarimaforecast$residuals, col="red", freq=FALSE, xlim = range(seq(-100,100)))
