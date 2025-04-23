# The following libraries allow many of the functions below, including pipelining
# and changing the shape of data frames.
library(tidyverse)
library(reshape2)

# This block of code reads in the original data, limits the residence and work
# counties to Georgia to leave just commuter numbers within Georgia.
data = read.csv("CommutingData.csv", header=TRUE) %>%
  setNames(c("ResidenceState", "ResidenceCounty", "WorkState", "WorkCounty", "Commuters")) %>%
  subset(ResidenceState == "Georgia" & WorkState == "Georgia") %>%
  select(-c("ResidenceState", "WorkState")) %>%
  mutate(Commuters = as.numeric(Commuters))

# The following data frame has the total commuters leaving from each county.
totals = data %>% group_by(ResidenceCounty) %>% summarise(total = sum(Commuters))

# The following data frame has counts of commuters going from one county (row)
# to another county (column).
counts = merge(x=data, y=totals, by="ResidenceCounty", all.x=TRUE) %>%
  select(-c("total")) %>%
  reshape(idvar="ResidenceCounty", timevar="WorkCounty", direction="wide") %>%
  replace(is.na(.), 0) %>%
  select(c("ResidenceCounty", order(colnames(.))))
colnames(counts) = gsub("Commuters.", "", colnames(counts))

# The following data frame converts the counts data frame to percentages based
# the sum across the columns.
percents = merge(x=data, y=totals, by="ResidenceCounty", all.x=TRUE) %>%
  mutate(Percentage = Commuters / total) %>%
  select(-c("Commuters", "total")) %>%
  reshape(idvar="ResidenceCounty", timevar="WorkCounty", direction="wide") %>%
  replace(is.na(.), 0) %>% 
  select(c("ResidenceCounty", order(colnames(.))))
colnames(percents) = gsub("Percentage.", "", colnames(percents))

# The following line writes the percents data frame to a csv.
write.csv(percents, file="TransitionMatrix.csv", row.names = FALSE)

# The following lines implement the Sinkhorn-Knopp algorithm to convert the counts
# data frame to a doulby stochastic transition matrix.
sinkhorn_knopp <- function(X, max_iters = 1000, tol = 1e-8) {
  rownames(X) <- X[,1]
  X <- X[,-1]
  n <- nrow(X)
  m <- ncol(X)
  
  for (i in 1:max_iters) {
    row_sums <- rowSums(X)
    X <- X / matrix(row_sums, n, m)  # Normalize rows
    
    col_sums <- colSums(X)
    X <- X / matrix(col_sums, n, m, byrow = TRUE)  # Normalize columns
    
    # Check convergence
    if (all(abs(row_sums - 1) < tol) && all(abs(col_sums - 1) < tol)) {
      break
    }
  }
  
  return(X)
}
dbstoch <- sinkhorn_knopp(counts)
dbstoch = rownames_to_column(dbstoch, var="ResidenceCounty")

# The following line writes the dbstoch data frame to a csv.
write.csv(dbstoch, file="TransitionMatrixDBS.csv", row.names=FALSE)

################################################################################
# Preprocessing the validation data that contains the COVID cases per GA county
covid_cases = read.csv("covid_confirmed_usafacts.csv", header=TRUE) %>%
  filter(State=="GA") %>%
  slice(-1) %>%
  select(-c(X2020.01.22:X2020.03.12)) %>%
  rename_with(~ str_replace_all(., "[X.]", ""))
write.csv(covid_cases, file="GeorgiaCOVIDCases.csv", row.names=FALSE)
