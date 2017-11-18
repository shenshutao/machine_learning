setwd("D:/GitHub/Machine-Learning/Recommender System")
users <- read.csv("u_data_tabular.csv")
movies <- read.csv("u_item.csv")

# transpose the data (make columns ~ users), ignore record index
items <- as.data.frame(t(users[,2:ncol(users)]))
colnames(items) <- users[,1]

summary(items)


sims <<- cor(items[,"u1"], items[, !names(items) %in% "u1"], use="pairwise.complete.obs")
sims <<- sims[1,!is.na(sims)]

#items[,"u1"]

# for each item compute weighted average of all the other user ratings
wavrats = apply(items[,names(sims)],1,function(x) weighted.mean(x, sims+1, na.rm=TRUE))
wavrats = wavrats[!is.na(wavrats[])]

# remove items already rated by the user
notseenitems = row.names(items[is.na(items[,"u1"]),])
t = wavrats[notseenitems]  
suggest <- sort(t[!is.na(t)] , decreasing = TRUE)[1:min(10,length(t))]  # get top 5 items
suggest
abc <- names(suggest)
abc <- as.data.frame(abc)
apply(abc,1,function(x) movies[as.numeric(substr(x, 2, 1000000L)),2])




