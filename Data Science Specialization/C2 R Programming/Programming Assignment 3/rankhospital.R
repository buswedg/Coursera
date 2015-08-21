## R Programming
## Programming Assignment 3: Hospital Quality
## rankhospital.R

rankhospital <- function(state, outcome, num = "best") {
  
  ## Read outcome data
  data_outcome <- read.csv("data/outcome-of-care-measures.csv", colClasses = "character")
  
  val_diseases <- c("heart attack", "heart failure", "pneumonia")
  val_states <- sort(unique(data_outcome[, 7]))

  ## Check desired state is valid
  if((state %in% val_states) == FALSE){stop("invalid state")}

  ## Check desired outcome is valid
  if((outcome %in% val_diseases) == FALSE){stop("invalid outcome")}
  
  ## Return column number for desired outcome
  if(outcome == "heart attack"){column <- 11}
  else if(outcome == "heart failure"){column <- 17}
  else if(outcome == "pneumonia"){column <- 23}

  data_outcome_states <- data_outcome[data_outcome$State == state, ]

  data_outcome_states[, column] <- suppressWarnings(as.numeric(data_outcome_states[, column]))

  val_isna <- is.na(data_outcome_states[, column])

  data_outcome_states <- data_outcome_states[!val_isna, ]

  data_outcome_states <- data_outcome_states[order(data_outcome_states[, column], data_outcome_states$Hospital.Name), ]

  if(num == "best"){num <- 1}
  else if(num == "worst"){num <- nrow(data_outcome_states)} 

  suppressWarnings(val_rank <- as.numeric(num))

  return(data_outcome_states[val_rank, ]$Hospital.Name)

}

## rankhospital("TX", "heart failure", 4)
## rankhospital("MD", "heart attack", "worst")
## rankhospital("MN", "heart attack", 5000)