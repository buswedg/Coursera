## R Programming
## Programming Assignment 3: Hospital Quality
## rankall.R

rankall <- function(outcome, num = "best") {
  
  ## Read outcome data
  data_outcome <- read.csv("data/outcome-of-care-measures.csv", colClasses = "character")
  
  val_diseases <- c("heart attack", "heart failure", "pneumonia")
  val_states <- sort(unique(data_outcome[, 7]))
  val_hospital <- character(0)
  
  ## Check desired outcome is valid
  if((outcome %in% val_diseases) == FALSE){stop("invalid outcome")}

  ## Return column number for desired outcome
  if(outcome == "heart attack"){column <- 11}
  else if(outcome == "heart failure"){column <- 17}
  else if(outcome == "pneumonia"){column <- 23}

  for (i in seq_along(val_states)){

    data_outcome_states <- data_outcome[data_outcome$State == val_states[i], ]

    data_outcome_states[, column] <- suppressWarnings(as.numeric(data_outcome_states[, column]))
    
    val_isna <- is.na(data_outcome_states[, column])
    
    data_outcome_states <- data_outcome_states[!val_isna, ]
    
    data_outcome_states <- data_outcome_states[order(data_outcome_states[, column], data_outcome_states$Hospital.Name), ]
    
    if(num == "best"){num <- 1}
    else if(num == "worst"){num <- nrow(data_outcome_states)}

    val_hospital[i] <- data_outcome_states[num, "Hospital.Name"]

  }

  data.frame(hospital = val_hospital, state = val_states, row.names = val_states)

}

## head(rankall("heart attack", 20), 10)
## tail(rankall("pneumonia", "worst"), 3)
## tail(rankall("heart failure"), 10)