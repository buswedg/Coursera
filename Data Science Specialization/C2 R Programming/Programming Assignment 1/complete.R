## R Programming
## Programming Assignment 1: Air Pollution
## complete.R

complete <- function(directory, id = 1:332) {
  
  ids <- vector()
  obs <- vector()
  
  for(i in id) {
    
    csvname <- sprintf("%03d.csv", i)
    csvpath <- paste(directory, csvname, sep = "/")
    csvdata <- read.csv(csvpath)
    
    case <- csvdata[complete.cases(csvdata),]
    obs <- c(obs, nrow(case))
    ids <- c(ids, i)
    
  }
  
  data.frame(id = ids, nobs = obs)
  
}

## complete("specdata", 1)
## complete("specdata", c(2, 4, 8, 10, 12))
## complete("specdata", 30:25)
## complete("specdata", 3)