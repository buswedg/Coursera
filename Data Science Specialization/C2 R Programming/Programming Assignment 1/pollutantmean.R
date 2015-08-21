## R Programming
## Programming Assignment 1: Air Pollution
## pollutantmean.R

pollutantmean <- function(directory, pollutant, id = 1:332) {
  
  mn <- vector()
  
  for(i in id) { 
    
    csvname <- sprintf("%03d.csv", i)
    csvpath <- paste(directory, csvname, sep = "/")	
    csvdata <- read.csv(csvpath)
    
    case <- csvdata[,pollutant]
    case <- case[!is.na(case)]
    mn <- c(mn, case)
    
  }
  
  print(mean(mn), digits = 3)
  
}

## pollutantmean("specdata", "sulfate", 1:10)
## pollutantmean("specdata", "nitrate", 70:72)
## pollutantmean("specdata", "nitrate", 23)