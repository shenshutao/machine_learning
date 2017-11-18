library(genalg)

# A got horse, speed 50, 40, 30
a <- c(50, 40, 30)
# B got horse, speed 55, 45, 35
b <- c(55, 45, 35)
# Question: How can A beat B ?

###############################################
# Evaluate function, when score is low, better.
evaluate <- function(string = c()) {
  if (length(string) == 3) {
    score <- 5
    
    a1 <- ceiling(string[1])
    a2 <- ceiling(string[2])
    a3 <- ceiling(string[3])
    
    # Punishment 
    if (a1 == a2 || a2 == a3 || a1 == a3) {
      return(10)
    }
    
    if (a[a1] > b[1])
      score <- score - 1
    if (a[a2] > b[2])
      score <- score - 1
    if (a[a3] > b[3])
      score <- score - 1
    
    return (score)
  } else {
    stop("Expecting a chromosome of length 3!")
  }
}

# Start GA
rbga.results = rbga(
  c(0, 0, 0),
  c(3, 3, 3),
  popSize = 10,
  iters = 1000,
  evalFunc = evaluate,
  verbose = FALSE,
  mutationChance = 0.05
)

summary(rbga.results, echo = TRUE)
plot(rbga.results)

# Final result
ceiling(rbga.results$population)
