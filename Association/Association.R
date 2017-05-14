library(arules)

data("Groceries")

inspect(Groceries)
summary(Groceries)

itemFrequencyPlot(Groceries, support = 0.05, cex.names=0.8)

fsets = eclat(Groceries, parameter = list(support = 0.05), control = list(verbose=FALSE))

summary(fsets)

singleItems = fsets[size(items(fsets)) == 1]
inspect(singleItems)

multiItems = fsets[size(items(fsets)) >1]
inspect (multiItems)


Grules = apriori(Groceries, parameter = list(support=0.01, confidence = 0.5))

inspect(sort(Grules, by="lift"))
quality(Grules)

subrules = Grules[quality(Grules)$confidence > 0.55]
inspect(subrules)

library(arulesViz)
plot(Grules)

plot(Grules, method="grouped")
plot(Grules, method="paracoord")
