library(genalg)

# Find two values to best match PI and Sqrt(50)
# As GA not promise to get the best result.
# Let's see what accuarcy can GA archieve based on this configuration.
evaluate <- function(string = c()) {
  returnVal = NA
  
  if (length(string) == 2) {
    # minimal the returnVal to make best match.
    returnVal = abs(string[1] - pi) + abs(string[2] - sqrt(50))
  } else {
    stop("Expecting a chromosome of length 2!")
  }
  returnVal
}

monitor <- function(obj) {
  # plot the population
  xlim = c(obj$stringMin[1], obj$stringMax[1])
  
  ylim = c(obj$stringMin[2], obj$stringMax[2])
  
  plot(
    obj$population,
    xlim = xlim,
    ylim = ylim,
    xlab = "pi",
    ylab = "sqrt(50)"
  )
  
}

rbga.results = rbga(
  c(1, 1),
  c(5, 10),
  monitorFunc = monitor,
  evalFunc = evaluate,
  verbose = TRUE,
  mutationChance = 0.01
)

plot(rbga.results)
plot(rbga.results, type = "hist")
plot(rbga.results, type = "vars")
summary(rbga.results, echo=TRUE)
