## R Programming
## Programming Assignment 1: Air Pollution
## corr.R

corr <- function(directory, threshold = 0) {
  
  correl <- vector()
  
  csvraw <- complete(directory, 1:332)
  csvsubset <- subset(csvraw, nobs > 0 )
  
  for(i in csvsubset$id) {
    
    csvname <- sprintf("%03d.csv", i)
    csvpath <- paste(directory, csvname, sep = "/")
    csvdata <- read.csv(csvpath)
    
    case <- csvdata[complete.cases(csvdata),]
    count <- nrow(case)
    
    if( count >= threshold) {
      
      correl <- c(correl, cor(case$nitrate, case$sulfate))			
      
    }
    
  }
  
  correl
  
}

## cr <- corr("specdata", 150)
## head(cr)
## summary(cr)

## cr <- corr("specdata", 400)
## head(cr)
## summary(cr)

## cr <- corr("specdata", 5000)
## summary(cr)
## length(cr)

## cr <- corr("specdata")
## summary(cr)
## length(cr)