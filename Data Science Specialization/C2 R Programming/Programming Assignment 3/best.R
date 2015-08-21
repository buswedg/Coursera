## R Programming
## Programming Assignment 3: Hospital Quality
## best.R

best <- function(state, outcome){
  
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
  
  val_selectrow <- which.min(data_outcome_states[, column])

  return(data_outcome_states[val_selectrow, ]$Hospital.Name)

}

## best("TX", "heart attack")
## best("TX", "heart failure")
## best("MD", "heart attack")
## best("MD", "pneumonia")
## best("BB", "heart attack")
## best("NY", "hert attack")