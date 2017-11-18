setwd("D:/GitHub/Machine-Learning/Recommender System")
users <- read.csv("simplemovies.csv")

#####################################
# user-based collaborative filtering
#####################################
# transpose the data (make columns ~ users), ignore record index
items <- as.data.frame(t(users[,2:ncol(users)]))
colnames(items) <- users[,1]

cor(items, items)
cor(items[,"Toby"], items, use="pairwise.complete.obs", method = "pearson")
#cor(items[,"Toby"], items[,!names(items) %in% "Toby"], use="pairwise.complete.obs")
#wavrats = apply(items[,names(sims)],1,function(x) weighted.mean(x, sims+1, na.rm=TRUE))
#
#notseenitems = row.names(items[is.na(items[,"Toby"]),])
#t = wavrats[notseenitems]  
#sort(t[!is.na(t)] , decreasing = TRUE)[1:min(5,length(t))]  # get top 5 items
getrecommendations <- function(target) {
  
  # compute similarity between targetuser and all other users
  sims <<- cor(items[,target],items[,!names(items) %in% c(target)],use="pairwise.complete.obs")
  sims <<- sims[1,!is.na(sims)]

  # for each item compute weighted average of all the other user ratings
  wavrats = apply(items[,names(sims)],1,function(x) weighted.mean(x, sims+1, na.rm=TRUE))
  wavrats = wavrats[!is.na(wavrats[])]
  
  #sims <<- apply(itemsims, 1, function(simrow) weighted.mean(wavrats, simrow, na.rm=TRUE)) # gets a pred for each item (row)
  
  # remove items already rated by the user
  notseenitems = row.names(items[is.na(items[,target]),])
  t = wavrats[notseenitems]  
  sort(t[!is.na(t)] , decreasing = TRUE)[1:min(5,length(t))]  # get top 5 items
}

getrecommendations("Toby")

##################################################
# TESTING
##################################################
testusernames  = sample(names(items), 2) # identify 2 user randomly for testing
trainusernames = setdiff(names(items),testusernames) # take remaining users for training

#test recommendations for all users
testall <- function() {
  toterr = 0
  for (user in testusernames) {
    mae = testuser(user)
    cat("mae for ", user, "is ", mae, "\n");
    toterr = toterr + mae
  }
  cat(sprintf("AVERAGE MAE=%0.4f\n", toterr/length(testusernames)))
}

#test recommendations for one user
testuser <- function(target) {
  testitems  = row.names(items[!is.na(items[,target]),]) 
  targetdata  = items[testitems,target] 
  names(targetdata) = testitems
  traindata = items[testitems,trainusernames] 
  toterr = valid = 0
  for (item in testitems) { 
    truerating = targetdata[item]
    targetdata[item] = NA
    sims = cor(targetdata,traindata,use="pairwise.complete.obs")
    sims = sims[,!is.na(sims)] 
    prediction = weighted.mean(traindata[item,names(sims)], sims+1, na.rm=TRUE)
    if (!is.na(prediction)) {
      toterr = toterr + abs(prediction - unname(truerating))
      valid = valid + 1 
    }
    targetdata[item] = truerating
  }
  return(toterr/valid)
}

testall()

###########################
# for item-item CF
###########################
#precompute the similarity matrix
itemsims = apply(items, 1, function(item) apply(items, 1, function(x) 1/(1+sqrt(sum((x - item)^2,na.rm=TRUE))))) # euclidean distance

#get pedicted ratings for unseen movies for a given user

getrecommendations2 <- function(username) {
  myRats = items[,username]
  wavrats = apply(itemsims, 1, function(simrow) weighted.mean(myRats, simrow, na.rm=TRUE)) 
  
  # remove items already rated by the user
  notseenitems = row.names(items[is.na(items[,username]),])
  t = wavrats[notseenitems]  
  sort(t[!is.na(t)] , decreasing = TRUE)[1:min(5,length(t))]  # get top 5 items
}

getrecommendations2("Toby")
